extends Node2D
## Whole-level map: starter geometry versus what this project added, drawn from
## the same first_steps.json the game loads. Communication aid for
## walker-jumpman-zhaohui-li; not part of the game.
##
## Anything at x < STARTER_EDGE is the starter's and is byte-identical in the
## level data; anything beyond it is new. The vertical scale is exaggerated
## relative to the horizontal so the ledges are legible - the map is a schematic,
## not a screenshot, and says so on its face.
const STARTER_EDGE := 960.0
const OLD_FINISH_X := 916.0

const SX := 0.385
const SY := 0.75
const OX := 12.0
const OY := -52.5

var level: Dictionary

func _ready() -> void:
	level = JSON.parse_string(FileAccess.get_file_as_string("res://levels/first_steps.json"))

func at(x: float, y: float) -> Vector2:
	return Vector2(OX + x * SX, OY + y * SY)

func box(entry: Array) -> Rect2:
	return Rect2(at(entry[0], entry[1]), Vector2(entry[2] * SX, entry[3] * SY))

func label(text: String, world_x: float, world_y: float, size: int, color: Color) -> void:
	var font := ThemeDB.fallback_font
	var w := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, size).x
	var p := at(world_x, world_y)
	draw_string(font, Vector2(p.x - w / 2.0, p.y), text, HORIZONTAL_ALIGNMENT_LEFT, -1, size, color)

func _draw() -> void:
	var font := ThemeDB.fallback_font
	var ink := Color("25354a")
	var old := Color("6f8196")
	var old_text := Color("4a5a6b")
	var new_fill := Color("f0b429")
	var new_edge := Color("b3821a")
	var new_text := Color("8a6510")
	var hazard := Color("d24e42")
	var green := Color("287c68")

	draw_rect(Rect2(0, 0, 640, 360), Color("f6f3ec"))
	draw_string(font, Vector2(12, 22), "walker-jumpman-zhaohui-li  /  whole level, x = 0 to %d" % int(level.width),
		HORIZONTAL_ALIGNMENT_LEFT, -1, 15, ink)
	draw_string(font, Vector2(12, 38), "schematic: horizontal 0.385x, vertical 0.75x, so heights are exaggerated",
		HORIZONTAL_ALIGNMENT_LEFT, -1, 10, old_text)

	# Zone banding, so "where does the starter end" is unmissable.
	var top := at(0, 140).y
	var bottom := at(0, 400).y
	draw_rect(Rect2(Vector2(OX, top), Vector2(STARTER_EDGE * SX, bottom - top)), Color(0.43, 0.51, 0.59, 0.10))
	draw_rect(Rect2(at(STARTER_EDGE, 140), Vector2((float(level.width) - STARTER_EDGE) * SX, bottom - top)), Color(0.94, 0.71, 0.16, 0.16))
	draw_line(at(STARTER_EDGE, 140), at(STARTER_EDGE, 400), ink, 1.0)

	draw_string(font, Vector2(at(330, 0).x, 62), "ORIGINAL  x 0-960   level data byte-identical",
		HORIZONTAL_ALIGNMENT_LEFT, -1, 11, old_text)
	draw_string(font, Vector2(at(985, 0).x, 62), "NEW  /  ZONE 03  PICK YOUR LINE",
		HORIZONTAL_ALIGNMENT_LEFT, -1, 11, new_text)

	for entry in level.solids:
		var r := box(entry)
		if float(entry[0]) >= STARTER_EDGE:
			draw_rect(r, new_fill)
			draw_rect(r, new_edge, false, 1.0)
		else:
			draw_rect(r, old)

	for entry in level.hazards:
		var r := box(entry)
		draw_rect(Rect2(r.position, Vector2(maxf(r.size.x, 4), r.size.y)), hazard)

	# Old finish, struck through, next to the relocated one.
	draw_line(at(OLD_FINISH_X, 320), at(OLD_FINISH_X, 252), old, 2.0)
	draw_line(at(OLD_FINISH_X - 14, 306), at(OLD_FINISH_X + 16, 276), hazard, 2.0)
	label("old finish", OLD_FINISH_X - 26, 242, 10, old_text)

	var fx: float = level.finish[0]
	draw_line(at(fx, 320), at(fx, 250), ink, 2.0)
	draw_colored_polygon(PackedVector2Array([at(fx + 4, 250), at(fx + 40, 262), at(fx + 4, 276)]), green)
	label("FINISH", fx - 30, 242, 11, green)

	draw_circle(at(level.spawn[0], level.spawn[1] - 14), 3.5, green)
	label("spawn", level.spawn[0], 288, 10, ink)

	# Callouts for the added pieces, placed clear of each other.
	label("fork pad", 1072, 276, 10, ink)
	label("step", 1196, 236, 10, ink)
	label("ledge A", 1304, 204, 10, ink)
	label("ledge B", 1440, 204, 10, ink)
	label("low road", 1240, 348, 10, ink)
	label("spikes", 1284, 396, 10, hazard)
	label("pit", 1416, 348, 10, hazard)

	# Legend.
	var ly := 328.0
	draw_rect(Rect2(12, ly, 14, 10), old)
	draw_string(font, Vector2(32, ly + 9), "starter geometry, unchanged", HORIZONTAL_ALIGNMENT_LEFT, -1, 11, ink)
	draw_rect(Rect2(212, ly, 14, 10), new_fill)
	draw_string(font, Vector2(232, ly + 9), "added by me", HORIZONTAL_ALIGNMENT_LEFT, -1, 11, ink)
	draw_rect(Rect2(326, ly, 14, 10), hazard)
	draw_string(font, Vector2(346, ly + 9), "hazard", HORIZONTAL_ALIGNMENT_LEFT, -1, 11, ink)
	draw_string(font, Vector2(404, ly + 9), "the new zone is appended, not inserted",
		HORIZONTAL_ALIGNMENT_LEFT, -1, 11, new_text)
