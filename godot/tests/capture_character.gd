extends SceneTree
## Renders BEACON in six states with the exact collider rectangle overlaid, so the
## "does any art leave the 18x28 body?" question is answered by a picture instead
## of by reading the drawing code. Added for walker-jumpman-zhaohui-li; not part
## of the starter. Run WITHOUT --headless:
##   godot --path godot --script res://tests/capture_character.gd
const Player = preload("res://features/player/player.gd")

var board: Node2D
var output: String

func _initialize() -> void:
	call_deferred("run")

func step() -> void:
	await physics_frame
	await process_frame

func floor_under(p: Vector2) -> void:
	var body := StaticBody2D.new()
	body.position = p + Vector2(0, 8)
	body.collision_layer = 1
	body.collision_mask = 2
	var shape := RectangleShape2D.new()
	shape.size = Vector2(80, 16)
	var collision := CollisionShape2D.new()
	collision.shape = shape
	body.add_child(collision)
	board.add_child(body)

## Settles a player on real ground (so is_on_floor() is genuinely true), then
## freezes it and moves it to a display slot at 5x for the contact sheet.
func pose(slot: Vector2, grounded: bool, face: float, vx: float, vy: float, phase: int) -> void:
	var p: CharacterBody2D = Player.new()
	board.add_child(p)
	# Off-screen staging point. Must keep x > 10: player.gd clamps position.x
	# to a minimum of 10, which would slide the body off a negative-x fixture floor.
	p.position = Vector2(200, 600)
	if grounded:
		floor_under(p.position)
		# Drive through the test-control path: this fixture has no InputMap.
		p.test_control = true
		p.enabled = true
		p.velocity = Vector2(0, 60)
		for i in range(6):
			await step()
		assert(p.is_on_floor(), "pose fixture did not actually reach the floor")
	p.enabled = false
	p.velocity = Vector2(vx, vy)
	p.facing = face
	p.tick = phase
	p.debug_bounds = true
	p.scale = Vector2(5, 5)
	p.position = slot
	p.queue_redraw()

func run() -> void:
	output = ProjectSettings.globalize_path("res://../evidence/screens")
	DirAccess.make_dir_recursive_absolute(output)
	board = Node2D.new()
	board.set_script(preload("res://tests/character_board.gd"))
	root.add_child(board)
	await step()
	# sin(tick * 0.7) peaks near tick 2 and troughs near tick 7: two stride phases.
	await pose(Vector2(110, 170), true, 1.0, 0.0, 0.0, 0)      # stand, right
	await pose(Vector2(320, 170), true, 1.0, 160.0, 0.0, 2)    # walk, right
	await pose(Vector2(530, 170), true, -1.0, -160.0, 0.0, 7)  # walk, left
	await pose(Vector2(110, 340), false, 1.0, 160.0, -220.0, 0)  # rising, right
	await pose(Vector2(320, 340), false, 1.0, 160.0, 180.0, 0)   # falling, right
	await pose(Vector2(530, 340), false, -1.0, -160.0, 180.0, 0) # falling, left
	for i in range(3):
		await step()
	await RenderingServer.frame_post_draw
	var error := root.get_texture().get_image().save_png(output + "/05-character-states.png")
	assert(error == OK)
	print("Captured BEACON contact sheet with collider overlay: 05-character-states.png")
	quit()
