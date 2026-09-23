extends SceneTree
## Diagnostic trace for one route line. Prints a tick-by-tick sample of the real
## body so a failing route can be explained instead of guessed at. Added for
## walker-jumpman-zhaohui-li while tuning Zone 03.
##   godot --headless --path godot --script res://tests/probe_route.gd -- low
const Game = preload("res://game/session.gd")
const Route = preload("res://tests/route_driver.gd")

func _initialize() -> void:
	call_deferred("run")

func steps(n: int) -> void:
	for i in range(n):
		await physics_frame
		await process_frame

func run() -> void:
	var args := OS.get_cmdline_user_args()
	var line: String = args[0] if args.size() > 0 else "low"
	var game: Node2D = Game.new()
	game.test_mode = true
	root.add_child(game)
	game.start_session()
	game.player.test_control = true
	await steps(3)
	var route = Route.new(line)
	var last_jumps := 0
	for tick in range(900):
		route.step(game.player)
		await steps(1)
		if game.player.jumps != last_jumps:
			last_jumps = game.player.jumps
			print("JUMP #%d at x=%.1f y=%.1f vx=%.1f" % [last_jumps, game.player.position.x, game.player.position.y, game.player.velocity.x])
		if game.player.position.x > 1100 and tick % 6 == 0:
			print("t=%d x=%.1f y=%.1f vx=%.1f floor=%s mark=%d state=%d" % [tick, game.player.position.x, game.player.position.y, game.player.velocity.x, game.player.is_on_floor(), route.next_jump, game.state])
		if game.state != Game.State.PLAYING:
			print("ENDED state=%d at x=%.1f y=%.1f after %d ticks" % [game.state, game.player.position.x, game.player.position.y, tick])
			break
	quit()
