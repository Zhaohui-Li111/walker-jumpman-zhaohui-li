extends RefCounted
## Fixed input route through the real level. No position/velocity edits: the
## driver only holds "right" and presses jump once the body is genuinely on the
## floor past a mark, so a route that completes is evidence the geometry is
## reachable with ordinary inputs.
##
## Starter fixture (unchanged): marks [138, 292, 424, 548, 712] carry Zones 01-02.
## walker-jumpman-zhaohui-li adds Zone 03, which forks, so one mark list is no
## longer enough. The shared marks are kept verbatim and each line appends its
## own; see TEST-REPORT.md for why each new mark sits where it does.
const SHARED := [138.0, 292.0, 424.0, 548.0, 712.0]
const LINES := {
	# gap to the fork pad, spikes on the low road, pit before the finish pad
	"low": [945.0, 1240.0, 1364.0],
	# gap to the fork pad, then the climb: fork pad -> step, step -> ledge A,
	# ledge A -> ledge B. No fourth mark: ledge B overhangs the finish pad, so
	# the high line ends by running off the edge rather than by jumping.
	"high": [945.0, 1108.0, 1200.0, 1320.0],
}

var jump_marks: Array = []
var next_jump: int = 0
var line: String = "low"

func _init(which: String = "low") -> void:
	assert(LINES.has(which), "unknown route line: " + which)
	line = which
	jump_marks = SHARED.duplicate()
	jump_marks.append_array(LINES[which])

func step(player: CharacterBody2D) -> void:
	player.test_control = true
	player.test_axis = 1.0
	player.test_jump_held = false
	if next_jump < jump_marks.size() and player.position.x >= jump_marks[next_jump] and player.is_on_floor():
		player.test_jump_pressed = true
		next_jump += 1
