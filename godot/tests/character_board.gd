extends Node2D
## Backdrop and captions for the BEACON contact sheet. Test fixture only.

func _draw() -> void:
	var font := ThemeDB.fallback_font
	var ink := Color("25354a")
	draw_rect(Rect2(0, 0, 640, 360), Color("f6f3ec"))
	draw_string(font, Vector2(16, 22), "BEACON / collider overlay = red 18x28 rect, feet at origin",
		HORIZONTAL_ALIGNMENT_LEFT, -1, 13, ink)
	var captions := {
		Vector2(110, 186): "stand R",
		Vector2(320, 186): "walk R",
		Vector2(530, 186): "walk L",
		Vector2(110, 356): "rising R",
		Vector2(320, 356): "falling R",
		Vector2(530, 356): "falling L",
	}
	for at in captions:
		var label: String = captions[at]
		var w := font.get_string_size(label, HORIZONTAL_ALIGNMENT_LEFT, -1, 12).x
		draw_string(font, Vector2(at.x - w / 2.0, at.y), label, HORIZONTAL_ALIGNMENT_LEFT, -1, 12, ink)
