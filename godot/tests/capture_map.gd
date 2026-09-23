extends SceneTree
## Renders the whole-level map to evidence/screens/10-level-map.png.
##   godot --path godot --script res://tests/capture_map.gd

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var out := ProjectSettings.globalize_path("res://../evidence/screens")
	DirAccess.make_dir_recursive_absolute(out)
	var board := Node2D.new()
	board.set_script(preload("res://tests/map_board.gd"))
	root.add_child(board)
	for i in range(3):
		await physics_frame
		await process_frame
	await RenderingServer.frame_post_draw
	var error := root.get_texture().get_image().save_png(out + "/10-level-map.png")
	assert(error == OK)
	print("Captured whole-level map: 10-level-map.png")
	quit()
