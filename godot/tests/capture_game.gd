extends SceneTree
const Game = preload("res://game/session.gd")
const Route = preload("res://tests/route_driver.gd")
var game: Node2D
var output: String

func _initialize() -> void:
	call_deferred("run")

func step() -> void:
	await physics_frame
	await process_frame

func capture(label: String) -> void:
	await RenderingServer.frame_post_draw
	var error := root.get_texture().get_image().save_png(output + "/" + label + ".png")
	assert(error == OK)
	print("Captured rendered game viewport: " + label)

## Runs a route line until `stop` is true, capturing `label` at that moment.
## Returns false if the run ended before the condition was met.
func run_until(line: String, stop: Callable, label: String) -> bool:
	game.state = Game.State.MENU
	game.start_session()
	game.player.test_control = true
	var route = Route.new(line)
	for i in range(900):
		route.step(game.player)
		await step()
		if stop.call(game):
			await capture(label)
			return true
		if game.state != Game.State.PLAYING:
			return false
	return false

func run() -> void:
	output = ProjectSettings.globalize_path("res://../evidence/screens")
	DirAccess.make_dir_recursive_absolute(output)
	game = Game.new()
	game.test_mode = true
	root.add_child(game)
	for i in range(3): await step()
	await capture("01-menu")

	game.start_session()
	game.player.test_control = true
	game.player.test_axis = 1
	# Walk from a safe landing into the spike trigger, not an invented failure card.
	game.player.position = Vector2(275, 320)
	for i in range(90):
		await step()
		if game.state == Game.State.DYING: break
	assert(game.state == Game.State.DYING)
	await capture("02-failure")

	# Zone 01-02, unchanged starter route: the jump across the first gap.
	assert(await run_until("low",
		func(g): return g.player.position.x > 463 and g.player.position.y < 300,
		"03-jump"), "could not reach the Zone 02 gap")

	# Zone 03 additions.
	assert(await run_until("low",
		func(g): return g.player.position.x > 1040 and g.player.is_on_floor() and g.player.position.y < 300,
		"06-zone3-fork"), "could not reach the fork pad")
	assert(await run_until("high",
		func(g): return g.player.position.x > 1270 and g.player.position.y < 230,
		"07-zone3-high-line"), "could not reach the high line")
	assert(await run_until("low",
		func(g): return g.player.position.x > 1250 and g.player.position.x < 1300 and g.player.position.y < 290,
		"08-zone3-spike-jump"), "could not reach the low road spike jump")

	# A real failure in the new section: walk off the low road into the pit.
	game.state = Game.State.MENU
	game.start_session()
	game.player.test_control = true
	game.player.position = Vector2(1340, 320)
	game.player.test_axis = 1
	for i in range(120):
		await step()
		if game.player.position.y > 328:
			await capture("09-zone3-pit-failure")
			break
	for i in range(60):
		await step()
		if game.state == Game.State.DYING: break
	assert(game.state == Game.State.DYING, "the pit did not kill")

	# Completion at the relocated finish.
	var finished := await run_until("high", func(g): return g.state == Game.State.COMPLETE, "04-complete")
	assert(finished, "input route did not complete")
	print("VISUAL ROUTE: completed with %d deaths" % game.deaths)
	game.queue_free()
	await process_frame
	quit()
