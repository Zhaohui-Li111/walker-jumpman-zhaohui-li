# CHANGE-BRIEF — walker-jumpman-zhaohui-li

**Author:** Zhaohui Li · **Date written:** 2026-09-23 · **Status:** prediction, written *before* implementation
**Starter:** [nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman) — "First Steps" slice, Godot 4.7.2 / GDScript
**Baseline captured before editing:** `test_game.gd` 25/25 PASS, `test_keyboard.gd` 9/9 PASS, engine `4.7.2.stable.official.ed1daf0bf`, Windows 11.

> This file is the **prediction record**. Original predictions below are not rewritten. Anything learned later is added in
> §6 "Revisions after the fact" with a date, so a wrong prediction stays visible next to what actually happened.

---

## 1. What the starter is (verified by reading, not assumed)

| Thing | Where it lives | Current value |
|---|---|---|
| Character drawing | `godot/features/player/player.gd` → `_draw()` | 7 `draw_rect` calls: ink box, blue box, orange belt, two legs with a `sin()` stride, one eye + pupil that flips on `facing` |
| Collider | `player.gd` `_ready()` | `RectangleShape2D` 18 × 28 at offset `(0, -14)` → occupies x ∈ [-9, 9], y ∈ [-28, 0], feet at origin |
| Movement tuning | `features/player/tuning.gd` | speed 160, accel 1280, decel 1920, jump_velocity −320, gravity 960, terminal 480, coyote 6 ticks, buffer 6 ticks |
| Level data | `godot/levels/first_steps.json` | width 960, fall_y 430, spawn (64,320), 5 solids, 1 hazard, finish `[916,264,24,56]` |
| Level drawing | `godot/game/session.gd` `_draw()` | **partly hard-coded**: background `Rect2(-400,-200,1800,900)`, grid `range(0,961,32)`, mountains at x `[100,470,770]`, spike baseline pinned to `y=320`, three `draw_string` labels at literal coordinates |
| Camera | `session.gd::_physics_process` | `clampf(player.x + 100, 320, level.width - 320)` — already data-driven off `width` |
| HUD progress bar | `godot/ui/hud.gd` | **hard-coded** `(player.x - 64) / 852` — 852 = 916 − 64, i.e. the old finish |
| Route fixture | `godot/tests/route_driver.gd` | fixed jump-marks `[138, 292, 424, 548, 712]` — authored for the 960-wide layout |

Derived from tuning (I will re-check these in engine, not trust the arithmetic):
- jump rise = 320² / (2·960) = **53.3 px** (build report measured **56.07 px** — the discrete 60 Hz step overshoots the closed form, so I budget with the *smaller* 53.3 figure)
- airtime from flat ground = 2·320/960 = **0.667 s** → max horizontal gap at full speed ≈ **106 px**

**Design rule I am setting for myself:** every new gap ≤ **80 px** and every new step-up ≤ **40 px**, so the geometry has real margin instead of living on the tolerance edge. If something is unreachable I move the platform, not the tuning.

---

## 2. Character concept — "BEACON", a signal-courier automaton

Replacing the starter's blue rectangle person. Not a recolor: a different **silhouette**.

| Feature | Starter | BEACON |
|---|---|---|
| Head | flat-topped rectangle, full body width | **domed** circular head, narrower than the shoulders |
| Face | one white square eye + pupil | a dark **visor band** across the head with a bright cyan eye-slot that slides toward the facing direction |
| Back | nothing | a **cargo pack** block on the trailing side — flips across the body when the player turns, so direction reads from the outline alone |
| Head side | nothing | a swept **fin/ear** triangle on the trailing side of the head |
| Torso | 14×20 flat blue rect | a **tapered** torso, narrow at the waist, with a chest lamp |
| Legs | two bars with a `sin()` stride | same stride idea kept, but with distinct wider **feet** blocks |
| Palette | `#287baf` blue / `#ef875f` orange | `#f0b429` amber shell / `#6b4b8a` plum pack / `#5ee7d0` cyan visor, on the existing `#25354a`-family ink |

Why this concept: the cream background and dark-navy terrain of the starter are cool/neutral, so an amber body with one saturated cyan point of light will separate from the world at 640×360 without needing an outline hack. The pack + fin give an asymmetric outline, which is the cheapest way to make facing readable when the sprite is 18 px wide.

**Constraint I am imposing:** *every drawn pixel stays inside the collider box* x ∈ [-9, 9], y ∈ [-28, 0], in all states including airborne. No cosmetic overhang, no thruster flame below the feet. Reason: the rubric asks for "no misleading visual/collision mismatch," and the honest way to get that is to make the art literally not exceed the body. Cost: the character cannot have a trailing scarf or antenna. I accept that cost.

**Readable states I will implement:** facing left, facing right, standing, walking (stride), rising, falling. Rising vs falling changes the leg pose and the visor, so the player can tell apex from descent.

**What stays untouched:** `tuning.gd` (all eight values), the `RectangleShape2D(18,28)` at `(0,-14)`, `collision_layer`/`mask`, `floor_snap_length`, and the whole of `_physics_process`. The character change should be a `_draw()` change and nothing else.

---

## 3. Level extension — Zone 03, "PICK YOUR LINE"

The original 0→960 route (two steps, two gaps, one spike cluster) stays **byte-identical in the data** and stays walkable. The finish moves out of it.

Planned new geometry (target values — expect these to move during playtesting):

```
width          960  ->  1600
finish  [916,264,24,56]  ->  [1548,264,24,56]

new solids
  [1032, 288,  96, 32]   FORK PAD      new landing #1, requires a ~72 px gap jump from the old end
  [1168, 320, 248, 64]   LOW ROAD      ground level, fast
  [1176, 256,  72, 16]   HIGH LEDGE A  floating
  [1296, 256,  72, 16]   HIGH LEDGE B  floating
  [1432, 320, 168, 64]   FINISH PAD    new landing #2, carries the relocated flag

new hazard
  [1272, 304, 24, 16]    spike cluster on the LOW ROAD
```

**The decision this asks the player to make.** Standing on the FORK PAD you can see both lines at once:

- **Low road** — drop right and run. Fastest, fewest inputs, but there is a spike cluster you must jump at speed, and the drop commits you (you cannot climb back up 32 px onto the pad… you can, actually — 32 < 53 — so the choice is reversible, which I *want*, because a fork that punishes curiosity is a bad fork).
- **High road** — two floating ledges, no hazard at all, but three jumps instead of two and each one is a 48–56 px target. Miss one and you fall onto the low road; the gap between Ledge A and Ledge B sits directly above the spikes, so a mistimed high jump drops you into the hazard you were trying to avoid.

So: **fewer, sloppier inputs over a hazard** vs **more, tighter inputs with no hazard**. That is a genuine trade-off rather than a longer floor, and the failure mode of the safe route is the hazard of the risky route, which is the cause-and-effect I intend to narrate in the film.

**Presentation work this forces** (because "moving data alone does not guarantee that a hazard or label will be drawn in the correct place"):
1. Background rect `(-400,-200,1800,900)` ends at x = 1400 — it will leave a hole from 1400→1632. Must be derived from `level.width`.
2. Grid `range(0, 961, 32)` and the horizontal rules ending at x=960 must extend.
3. Mountain silhouettes are a literal `[100, 470, 770]` — need entries past 960 or the new zone looks empty.
4. Spikes are drawn with the baseline pinned at `y=320`. My new spikes happen to also sit on y=320, so this would *accidentally* still work — I am going to make it read `entry[1]+entry[3]` anyway, because an accident that looks correct is exactly the trap the assignment is describing.
5. Zone labels are three literal `draw_string` calls. I will move labels into `first_steps.json` as a `labels` array so the data file actually drives what is drawn.
6. HUD progress `(x-64)/852` will read ~100% the moment you enter Zone 03. Must derive from spawn and `finish[0]`.
7. Camera clamp is `width - 320` = 1280 → shows x 960..1600, so the flag at 1548 is on screen. **Prediction: camera needs no code change.** (Flagging this as a prediction because it is the kind of thing I expect to be wrong about.)

**Explicitly unchanged:** A/D + arrows, Space, R, Esc/P, Enter, M. Jump strength, gravity, coyote/buffer windows, the collider, the fall-death boundary `fall_y=430`, the 0.55 s auto-retry, pause/focus-loss behaviour, and the Enter-to-replay loop. If I find I *must* change one, it goes in §6 with the reason and its own test.

---

## 4. Predicted failure cases and how I will check them

Four, because two felt like under-promising.

**F1 — The route fixture breaks, and it breaks *silently in the middle*.**
`route_driver.gd` jumps at fixed x positions `[138,292,424,548,712]`. After the extension the driver runs out of marks at x=712 and then just holds right, so it will walk off the end of the old level at x=960 and die to `fall_y`. `complete-real-route` will report `state=DYING` (or time out at 900 ticks), not COMPLETE.
*Check:* run `--headless --script res://tests/test_game.gd` and read the `complete-real-route` line specifically — `ticks`, final `position`, and `jump_marks_used`. If `jump_marks_used == 5` and x is near 960, that confirms this exact cause rather than a geometry error.
*Planned response:* extend the fixture with the new marks and say in TEST-REPORT which marks are new and why. I will **not** widen the 900-tick budget or relax `deaths == 0` to get green.

**F2 — A new jump is not actually reachable, i.e. my arithmetic lies.**
The 53.3 px / 106 px figures assume instant full speed and ignore the discrete 60 Hz integration. The FORK PAD asks for +32 px of height across 72 px of gap simultaneously, which is the tightest single jump in my layout.
*Check:* the route fixture reaching the new flag with `deaths == 0` is the machine check. The human check is me playing it — an automated route that nails a frame-perfect input proves reachability, not playability.
*Planned response:* move the pad closer or lower, in that order. Not touch `jump_velocity`.

**F3 — Visual/collision mismatch on the new character, worst at the boundaries.**
18 px is narrow. My worry is the cargo pack: it sits on the trailing side and if I size it by eye it will poke past x = ±9 when facing left but not right, so the character will look like it clips terrain in one direction only. Second worry: the domed head — a circle of radius 5 centred at y = −23 reaches y = −28 exactly, and a radius of 6 would breach the collider top and let the head visually overlap a ceiling it physically stops short of.
*Check:* I will add a debug draw that outlines the exact collider rect, screenshot standing/walking/rising/falling × facing-left/right, and confirm no art crosses the outline. Then re-run the existing `low-ceiling` check, which drives the player under a ceiling at y=260 and asserts the feet never rise above 300 — if the head art breaches, the picture and that number disagree.
*Planned response:* shrink the art, not the collider.

**F4 — The relocated finish is reachable but unreadable.**
Camera clamps at `width - 320`. If I get the arithmetic wrong, or if the flag's hard-coded pole geometry (`draw_line` from y=320 up to y=250) lands over a platform whose top is not 320, the flag will float or be cut off at the screen edge while the Area2D still works. The physics would pass and the picture would be wrong — the worst failure mode for this assignment.
*Check:* rendered-viewport capture via `capture_game.gd` at the moment of completion, plus my own eyes at the fork and at the flag.
*Planned response:* derive the pole base from the finish rect's bottom rather than the literal 320.

---

## 5. What "done" means

- Character replaced, all 8 tuning values and the collider untouched, art inside the box in 6 states.
- Two new landings that require jumps, a fork with a real trade-off, flag moved so the old route alone cannot win.
- Old route still walkable; retry / pause / replay unchanged.
- `test_game.gd` and `test_keyboard.gd` green **with an honestly updated route fixture**, plus at least one new check that is specific to the extension.
- My own playtest recorded in TEST-REPORT.md, including at least one observation that made me change something.

---

## 6. Revisions after the fact

**Everything above is exactly as written on 2026-09-23 before implementation.** Nothing in
§1–§5 has been edited to make a prediction look better. This section is the correction log.

### 6.1 Scoring the four predicted failures, honestly

| # | Predicted | What happened |
|---|---|---|
| **F1** | Route fixture breaks, dies at the old level edge | **Right, including the mechanism.** `jump_marks_used: 5` (marks exhausted), died at x≈1046 crossing `fall_y`. Fixed by extending the fixture; the 900-tick budget and `deaths == 0` were not relaxed. |
| **F2** | Jumps may be *unreachable* because the closed form ignores 60 Hz integration | **Wrong, and wrong in the comforting direction.** Discrete stepping *overshoots*: measured rise **56.07 px** against the predicted 53.3. Jumps came out easier, not harder. Budgeting with the pessimistic number cost nothing. |
| **F3** | Character art will poke outside the 18×28 collider, worst at the pack and the domed head | **Right as a risk; the method killed it before it shipped.** Authoring in mirrored "facing-right" space plus a red collider overlay caught it immediately. The head radius did have to be held at 5.2 px centred at y=−22.6 to top out at −27.8. |
| **F4** | Relocated finish reachable but unreadable; flag pole hard-coded to y=320 | **Half right.** The pole fix was genuinely needed and made. But the readability failure that actually occurred was a *label* sitting inside the jump arc — a thing this brief never imagined. |

**Three of four were useful. The one that was wrong was wrong safely. And the bug that actually
cost the most time was in a category none of the four anticipated** — see 6.2.

### 6.2 The failure I did not predict: vertical stacking imposes a headroom budget

The brief's §3 laid the two fork routes **on top of each other** — a low road at y=320 with two
floating ledges at y=256 directly above it — and treated "miss the high line, fall into the
spikes" as a feature.

That layout is geometrically impossible for the route underneath. BEACON is 28 px tall and
jumps 56 px, so a jump needs **84 px** of headroom; the planned ledge underside sat **48 px**
above the low road. The low road's spike jump clipped the ledge, rose **17 px instead of 56**,
and died on the hazard it was clearing.

Found by writing `probe_route.gd` and reading a tick-by-tick trace, not by inspection. Full
account in [TEST-REPORT §1](TEST-REPORT.md).

**What this brief should have contained and did not:** a headroom rule alongside the gap and
step-up rules in §1 — *no platform may overhang a place where the route below must jump, unless
its underside clears body height + jump height.*

### 6.3 Geometry actually shipped, against the plan in §3

| Piece | Planned in §3 | Shipped | Why it moved |
|---|---|---|---|
| Fork pad | `[1032, 288, 96, 32]`, 72 px gap | `[1016, 288, 112, 32]`, **56 px gap** | The 72 px version left a take-off window of only ~31 px of run-up. Widened the pad and shortened the gap to open it to ~46 px. |
| Low road | `[1168, 320, 248, 64]` | `[1152, 320, 232, 64]` | Moved left so the drop off the fork pad lands on it reliably rather than marginally. |
| — | *(not planned)* | **step `[1168, 248, 56, 12]`** | Added. The high line could not reach y=216 in one jump from y=288, and y=216 is where it has to be to clear the low road's headroom. |
| High ledge A | `[1176, 256, 72, 16]` | `[1264, 216, 80, 12]` | Raised 40 px and moved right — the 6.2 fix. Clearance over the low road went 48 px → **92 px** against the 84 px requirement. |
| High ledge B | `[1296, 256, 72, 16]` | `[1392, 216, 96, 12]` | Same, and lengthened so it overhangs the finish pad. |
| Finish pad | `[1432, 320, 168, 64]` | `[1448, 320, 152, 64]` | Shifted to keep the pit a clean 64 px. |
| Spikes | `[1272, 304, 24, 16]` | unchanged | The one piece of Zone 03 that shipped exactly as planned. |

**What the redesign cost:** the "miss the high line and land in the spikes" moment is gone. The
gap between the ledges now drops you onto safe road. I preferred a reachable level to a
narratable one, and the film says so rather than pretending the current design was the intent.

### 6.4 Predictions in §3 that held

- **Camera needed no code change.** The brief flagged this as "the kind of thing I expect to be
  wrong about." It was right: the clamp is `width − 320` = 1280, which puts the flag at 1548
  on screen with no edit.
- All six presentation items in §3 were genuinely required. The spike baseline was the
  interesting one — the new cluster also sits at y=320, so the starter's hard-coded literal
  would have *looked* correct while being wrong by luck. Made data-driven anyway.
- Labels moved once more than planned, from y=150/170 to **y=118/138**, after a render showed
  them inside the high line's jump arc.

### 6.5 The constraint in §2 held exactly

`tuning.gd` diff against the starter is **empty**. The collider is untouched. `low-ceiling`
reports `300.000274658203` before and after the character swap — bit-identical. No drawn pixel
leaves the 18×28 box in any of the six states.

The one deliberate inward exception named in §2 — a ≤2 px boot lift during a grounded walk
stride — is the only gap between art and collider, and it cannot occur airborne.

### 6.6 Added after the brief, outside its scope

The brief was written before the Brutalist skill was available, so it says nothing about the
film. What the film work added to the *game* repository: `tests/probe_route.gd` (the diagnostic
that found 6.2), `tests/map_board.gd` + `capture_map.gd` (the whole-level map), and
`tests/capture_character.gd` + `character_board.gd` (the collider contact sheet).

### 6.7 What the playtest changed, 2026-09-24

The brief's §4 predicted mechanical failures. The human playtest found a **usability** one it
had no category for: the retry is fast enough that the death card *"flashes past"* — the gist
arrives, there is no time to read it. Both messages are correct and machine-checked; neither is
comfortably legible at 0.55 s. Recorded as a named design tension in
[TEST-REPORT §4 cycle 4](TEST-REPORT.md) and deliberately **not** fixed.

The fork-pad entry jump — the §4 F2 descendant, and the tightest input in the level — was
cleared **first try**. That is evidence the ~46 px window is not brutal. It is still not a
measurement, and the brief's figure remains *calculated, never measured*.
