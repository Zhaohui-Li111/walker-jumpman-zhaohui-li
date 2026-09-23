extends Node
## Deterministic walkthrough input driver for walker-jumpman-zhaohui-li.
##
## Contract (skills/make/godot-waikthrough/references/capture-and-coverage.md):
##   - runs the REAL main scene (this is an autoload beside game/main.tscn)
##   - drives only real InputEventKey events through Input.parse_input_event,
##     so the same code path a keyboard uses is exercised: _unhandled_input for
##     menu/pause/retry, and Input.get_axis / is_action_pressed for move/jump
##   - never teleports the body, sets completion, disables collision, or calls a
##     test-only shortcut. It may *observe* position/state to time an input,
##     which the reference explicitly permits.
##   - logs every action against the game's physics tick
##   - asserts the expected outcome of each phase and quits nonzero on failure
##
## The single harness change is documented in CAPTURE.md: game.test_mode is set
## true so the window's focus_exited handler does not auto-pause an unattended
## capture. That flag gates nothing except the focus-loss pause.

const OUT_DIR := "res://../"  # reel/capture/
var game: Node2D
var events: Array = []
var problems: PackedStringArray = []
var t: int = 0  # physics ticks since the driver started

func _ready() -> void:
	call_deferred("boot")

func boot() -> void:
	await get_tree().process_frame
	game = get_tree().current_scene
	if game == null:
		push_error("no current scene")
		get_tree().quit(2)
		return
	game.test_mode = true
	note("driver-start", {"engine": Engine.get_version_info().string, "level_width": game.level.width})
	await run()

# ── primitives ──────────────────────────────────────────────────────────────

func note(kind: String, data: Dictionary) -> void:
	var row := {"t": t, "kind": kind}
	if is_instance_valid(game) and is_instance_valid(game.player):
		row["x"] = snappedf(game.player.position.x, 0.01)
		row["y"] = snappedf(game.player.position.y, 0.01)
		row["state"] = game.state
		row["deaths"] = game.deaths
	for k in data:
		row[k] = data[k]
	events.append(row)

func tick(n: int = 1) -> void:
	for i in range(n):
		await get_tree().physics_frame
		t += 1

func key(code: Key, pressed: bool, label: String) -> void:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = pressed
	Input.parse_input_event(ev)
	note("key", {"key": label, "pressed": pressed})

## Holds are deliberately several physics ticks long. Input events are flushed
## once per *rendered* frame, and Movie Maker runs at 30 fps against 60 Hz
## physics, so a press and release two ticks apart can land inside one frame and
## be dropped entirely. Six ticks is three rendered frames at 30 fps.
func tap(code: Key, label: String) -> void:
	await key(code, true, label)
	await tick(6)
	await key(code, false, label)
	await tick(4)

func expect(id: String, ok: bool, observed: Dictionary) -> void:
	note("expect", {"id": id, "ok": ok, "observed": observed})
	if not ok:
		problems.append(id)
		push_error("walkthrough expectation failed: " + id + " " + str(observed))

## Holds a direction and jumps once the body is genuinely on the floor past each
## mark, until `stop` returns true or the budget runs out.
func advance(dir_key: Key, dir_label: String, marks: Array, stop: Callable, budget: int) -> bool:
	await key(dir_key, true, dir_label)
	var idx := 0
	var reached := false
	for i in range(budget):
		if idx < marks.size() and game.player.position.x >= float(marks[idx]) and game.player.is_on_floor():
			# Confirm the engine actually took the jump before consuming the mark;
			# if the press fell between rendered frames, the next tick retries it.
			var jumps_before: int = game.player.jumps
			await key(KEY_SPACE, true, "Space")
			await tick(5)
			await key(KEY_SPACE, false, "Space")
			await tick(2)
			if game.player.jumps > jumps_before:
				idx += 1
			continue
		await tick(1)
		if stop.call():
			reached = true
			break
	await key(dir_key, false, dir_label)
	return reached

func playing() -> bool:
	return game.state == game.State.PLAYING

func wait_state(target: int, budget: int) -> bool:
	for i in range(budget):
		await tick(1)
		if game.state == target:
			return true
	return false

# ── the walkthrough ─────────────────────────────────────────────────────────

func run() -> void:
	# S1 — title card / menu.
	note("phase", {"name": "menu"})
	await tick(60)
	expect("menu-visible", game.state == game.State.MENU, {"state": game.state})

	# S2 — Enter starts.
	await tap(KEY_ENTER, "Enter")
	expect("enter-starts", playing(), {"state": game.state})
	await tick(10)

	# S3 — movement both directions, so BEACON's facing flip is on screen.
	note("phase", {"name": "movement"})
	await key(KEY_D, true, "D")
	await tick(34)
	await key(KEY_D, false, "D")
	await tick(8)
	var x_after_right: float = game.player.position.x
	await key(KEY_A, true, "A")
	await tick(26)
	await key(KEY_A, false, "A")
	await tick(10)
	expect("moves-both-ways", x_after_right > 100.0 and game.player.position.x < x_after_right,
		{"x_right": x_after_right, "x_back": game.player.position.x})

	# S4 — manual retry (R) returns to spawn without counting a death.
	note("phase", {"name": "manual-retry"})
	var deaths_before: int = game.deaths
	await tap(KEY_R, "R")
	await tick(6)
	expect("r-retries-without-death",
		game.deaths == deaths_before and game.player.position.distance_to(Vector2(64, 320)) < 1.0,
		{"deaths": game.deaths, "position": str(game.player.position)})

	# S5 — a genuine failure: walk into the starter's spikes without jumping.
	note("phase", {"name": "failure-spikes"})
	await advance(KEY_D, "D", [138.0], func(): return game.state == game.State.DYING, 260)
	expect("spikes-kill", game.state == game.State.DYING and game.death_reason == "Watch the spikes",
		{"state": game.state, "reason": game.death_reason})
	note("retry-card", {})
	var recovered := await wait_state(game.State.PLAYING, 80)
	expect("auto-retry-recovers", recovered and game.player.position.distance_to(Vector2(64, 320)) < 1.0,
		{"state": game.state, "position": str(game.player.position), "deaths": game.deaths})
	await tick(10)

	# S6 — clean run through the starter's Zones 01-02.
	note("phase", {"name": "zones-01-02"})
	var got_far := await advance(KEY_D, "D", [138.0, 292.0, 424.0, 548.0, 712.0],
		func(): return game.player.position.x >= 880.0, 520)
	expect("starter-zones-cleared", got_far and game.deaths == 1,
		{"x": game.player.position.x, "deaths": game.deaths})

	# S7 — pause freezes, Enter resumes.
	note("phase", {"name": "pause"})
	await tap(KEY_ESCAPE, "Escape")
	var frozen_at: Vector2 = game.player.position
	var frozen_time: float = game.elapsed
	await tick(55)
	expect("escape-pauses", game.state == game.State.PAUSED and game.player.position == frozen_at
		and is_equal_approx(game.elapsed, frozen_time),
		{"state": game.state, "position": str(game.player.position)})
	await tap(KEY_ENTER, "Enter")
	expect("enter-resumes", playing(), {"state": game.state})
	await tick(8)

	# S8 — cross into Zone 03 and stand on the fork pad.
	note("phase", {"name": "zone-03-fork"})
	var on_pad := await advance(KEY_D, "D", [945.0],
		func(): return game.player.position.x >= 1040.0 and game.player.is_on_floor(), 200)
	expect("fork-pad-reached", on_pad and game.player.position.y < 300.0,
		{"position": str(game.player.position)})
	await tick(40)

	# S9 — the low road, then a genuine fall into the pit.
	note("phase", {"name": "low-road-and-pit"})
	await advance(KEY_D, "D", [1240.0], func(): return game.state == game.State.DYING, 260)
	expect("pit-kills", game.state == game.State.DYING and game.death_reason == "Missed the landing",
		{"state": game.state, "reason": game.death_reason})
	var recovered2 := await wait_state(game.State.PLAYING, 80)
	expect("auto-retry-after-pit", recovered2, {"state": game.state, "deaths": game.deaths})
	await tick(10)

	# S10 — the high line, all the way to the relocated finish.
	note("phase", {"name": "high-line-to-finish"})
	var done := await advance(KEY_D, "D",
		[138.0, 292.0, 424.0, 548.0, 712.0, 945.0, 1108.0, 1200.0, 1320.0],
		func(): return game.state == game.State.COMPLETE, 780)
	expect("high-line-completes", done and game.state == game.State.COMPLETE and game.deaths == 2,
		{"state": game.state, "deaths": game.deaths, "time_s": game.last_finish_time})
	note("results-card", {"time_s": game.last_finish_time, "deaths": game.deaths})
	await tick(70)

	# S11 — Enter replays from a clean slate.
	note("phase", {"name": "replay"})
	await tap(KEY_ENTER, "Enter")
	expect("enter-replays", playing() and game.player.jumps == 0 and game.deaths == 0,
		{"state": game.state, "jumps": game.player.jumps, "deaths": game.deaths})
	await tick(40)

	# S12 — pause, then M back to the menu.
	note("phase", {"name": "menu-return"})
	await tap(KEY_P, "P")
	expect("p-pauses", game.state == game.State.PAUSED, {"state": game.state})
	await tick(20)
	await tap(KEY_M, "M")
	expect("m-returns-to-menu", game.state == game.State.MENU, {"state": game.state})
	await tick(45)

	finish()

func finish() -> void:
	var dir := ProjectSettings.globalize_path(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(dir)
	var f := FileAccess.open(dir + "/run-01-inputs.jsonl", FileAccess.WRITE)
	for row in events:
		f.store_line(JSON.stringify(row))
	f.close()
	var summary := {
		"ticks": t,
		"engine": Engine.get_version_info().string,
		"failed_expectations": problems,
	}
	var s := FileAccess.open(dir + "/run-01-driver.json", FileAccess.WRITE)
	s.store_string(JSON.stringify(summary, "  "))
	s.close()
	if problems.is_empty():
		print("WALKTHROUGH OK: %d ticks, %d logged events" % [t, events.size()])
		get_tree().quit(0)
	else:
		printerr("WALKTHROUGH FAILED: " + ", ".join(problems))
		get_tree().quit(1)
