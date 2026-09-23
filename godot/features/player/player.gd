extends CharacterBody2D

const Tuning = preload("res://features/player/tuning.gd")
var tuning = Tuning.new()
var enabled: bool = false
var tick: int = 0
var last_floor_tick: int = -1000
var jump_request_tick: int = -1000
var opportunity_consumed: bool = false
var require_jump_release: bool = true
var facing: float = 1.0
var jumps: int = 0
var test_control: bool = false
var test_axis: float = 0.0
var test_jump_pressed: bool = false
var test_jump_held: bool = false
## Draws the exact collider rectangle over the art. Used to verify that no part
## of BEACON's silhouette leaves the 18x28 body. Off in normal play.
var debug_bounds: bool = false

func _ready() -> void:
	name = "Player"
	collision_layer = 2
	collision_mask = 1
	floor_snap_length = 1.0
	var shape := RectangleShape2D.new()
	shape.size = Vector2(18, 28)
	var collider := CollisionShape2D.new()
	collider.shape = shape
	collider.position = Vector2(0, -14)
	add_child(collider)

func reset_at(spawn: Vector2) -> void:
	position = spawn
	velocity = Vector2.ZERO
	last_floor_tick = -1000
	jump_request_tick = -1000
	opportunity_consumed = false
	require_jump_release = true
	test_jump_pressed = false
	jumps = 0
	queue_redraw()

func _physics_process(delta: float) -> void:
	if not enabled:
		return
	tick += 1
	var axis := test_axis if test_control else Input.get_axis("move_left", "move_right")
	var held := test_jump_held if test_control else Input.is_action_pressed("jump")
	var pressed := test_jump_pressed if test_control else Input.is_action_just_pressed("jump")
	test_jump_pressed = false
	if not held:
		require_jump_release = false
	if is_on_floor() and velocity.y >= 0.0:
		last_floor_tick = tick
		opportunity_consumed = false
	if pressed and not require_jump_release:
		jump_request_tick = tick
	var rate: float = tuning.acceleration if not is_zero_approx(axis) else tuning.deceleration
	velocity.x = move_toward(velocity.x, axis * tuning.speed, rate * delta)
	if not is_zero_approx(axis):
		facing = signf(axis)
	velocity.y = minf(velocity.y + tuning.gravity * delta, tuning.terminal_velocity)
	if not opportunity_consumed and tick - last_floor_tick <= tuning.coyote_ticks and tick - jump_request_tick <= tuning.buffer_ticks:
		velocity.y = tuning.jump_velocity
		opportunity_consumed = true
		jump_request_tick = -1000
		jumps += 1
	move_and_slide()
	position.x = maxf(position.x, 10.0)
	queue_redraw()

func _rr(x: float, y: float, w: float, h: float, dir: float) -> Rect2:
	## A rect authored in facing-right space, mirrored about x = 0 when facing left.
	return Rect2(x if dir > 0.0 else -x - w, y, w, h)

func _pp(points: Array, dir: float) -> PackedVector2Array:
	## A polygon authored in facing-right space, mirrored about x = 0.
	var out := PackedVector2Array()
	for p in points:
		out.append(Vector2(p.x * dir, p.y))
	return out

func _draw() -> void:
	# BEACON, a signal-courier automaton. Original vector drawing; it replaces the
	# starter's blue rectangle figure. Domed head, visor with a single cyan eye
	# slot, a cargo pack and a swept fin that both ride the trailing side, so the
	# facing direction reads from the outline alone at 18 px wide.
	#
	# Invariant: every drawn pixel stays inside the collider, x in [-9, 9] and
	# y in [-28, 0]. The one deliberate exception direction is *inward*: the
	# walk stride lifts a boot up to 2 px off y = 0, and only while grounded,
	# where a gap between art and collider floor cannot mislead a hazard read.
	# Airborne poses always keep both boots on y = 0. See CHANGE-BRIEF.md 2.
	var ink := Color("1f2b3d")
	var shell := Color("f0b429")
	var shell_lit := Color("ffd76a")
	var pack := Color("6b4b8a")
	var glow := Color("5ee7d0")

	var dir: float = 1.0 if facing >= 0.0 else -1.0
	var grounded := is_on_floor()
	var rising := not grounded and velocity.y < 0.0
	var stride: float = sin(float(tick) * 0.7) * 2.0 if grounded and absf(velocity.x) > 8.0 else 0.0
	var lift_back := maxf(stride, 0.0)
	var lift_front := maxf(-stride, 0.0)
	var back_x := -5.0
	var front_x := 1.0
	var arm_y := -17.0
	if not grounded:
		# Legs close together on the way up, braced apart on the way down.
		back_x = -4.0 if rising else -6.0
		front_x = 0.0 if rising else 2.0
		arm_y = -19.5 if rising else -15.5
		lift_back = 0.0
		lift_front = 0.0

	# Legs and boots.
	draw_rect(_rr(back_x, -8.0, 4.0, 8.0 - lift_back, dir), ink)
	draw_rect(_rr(front_x, -8.0, 4.0, 8.0 - lift_front, dir), ink)
	draw_rect(_rr(back_x - 1.0, -2.0 - lift_back, 5.0, 2.0, dir), pack)
	draw_rect(_rr(front_x, -2.0 - lift_front, 5.0, 2.0, dir), pack)

	# Cargo pack on the trailing side: the main silhouette cue for facing.
	draw_rect(_rr(-9.0, -21.0, 5.0, 12.0, dir), ink)
	draw_rect(_rr(-8.0, -20.0, 3.0, 10.0, dir), pack)
	draw_rect(_rr(-8.0, -16.0, 3.0, 1.5, dir), shell_lit)

	# Tapered torso: wide at the shoulders, narrow at the waist.
	draw_colored_polygon(_pp([Vector2(-7, -20), Vector2(7, -20), Vector2(5, -6), Vector2(-5, -6)], dir), ink)
	draw_colored_polygon(_pp([Vector2(-5.5, -18.6), Vector2(5.5, -18.6), Vector2(3.8, -7.4), Vector2(-3.8, -7.4)], dir), shell)
	draw_rect(_rr(-5.0, -16.5, 10.0, 2.0, dir), ink)

	# Leading arm.
	draw_rect(_rr(4.0, arm_y, 3.0, 7.0, dir), ink)
	draw_rect(_rr(4.6, arm_y + 0.8, 1.8, 5.6, dir), shell)

	# Chest lamp. Cyan only while airborne, so the jump state reads at a glance.
	var lamp := Vector2(0.4 * dir, -12.0)
	draw_circle(lamp, 2.4, ink)
	draw_circle(lamp, 1.4, glow if not grounded else shell_lit)

	# Domed head, offset a little toward the facing direction.
	var head := Vector2(0.6 * dir, -22.6)
	draw_circle(head, 5.2, ink)
	draw_circle(head, 4.0, shell)

	# Swept fin behind the head.
	draw_colored_polygon(_pp([Vector2(-3.0, -26.0), Vector2(-8.6, -23.2), Vector2(-3.0, -19.5)], dir), ink)
	draw_colored_polygon(_pp([Vector2(-3.6, -25.0), Vector2(-7.4, -23.1), Vector2(-3.6, -21.0)], dir), pack)

	# Visor band, with the bright eye slot pushed toward the facing direction.
	draw_rect(_rr(-4.0, -24.6, 9.2, 3.6, dir), ink)
	var eye_y := -24.0
	var eye_h := 2.4
	if not grounded:
		eye_y = -24.2 if rising else -23.4
		eye_h = 2.8 if rising else 1.4
	draw_rect(_rr(1.2, eye_y, 3.2, eye_h, dir), glow)
	draw_rect(_rr(-3.0, -23.9, 1.6, 1.6, dir), shell_lit)

	if debug_bounds:
		draw_rect(Rect2(-9, -28, 18, 28), Color(0.85, 0.1, 0.1), false, 1.0)
