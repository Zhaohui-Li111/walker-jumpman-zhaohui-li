# CAPTURE.md — how the gameplay evidence was recorded

Reel: `claude-liam-walker-jumpman-zhaohui-li-walkthrough`
Game: **walker-jumpman-zhaohui-li**, an extension of walker-jumpman by Nik Bear Brown

---

## Build identity

| | |
|---|---|
| Source root hashed | `godot/` (the shipped game), excluding the `.godot` engine cache |
| `build_id` **as filmed** | `0be6756a1c222cf89964287272c5d6659111e6f50d2bb2f01969e8d03f963bf9` |
| `build_id` **as submitted** | `a16c4f8d6d00bb1ef886e1506c1bf434c95b42f325c11dfb33fc2e2758835247` — see "Drift after the capture" below |
| Hash method | SHA-256 over `"<relpath>\0<sha256(file)>\n"` for all 25 files, paths sorted |
| Per-file manifest | [SOURCE-SNAPSHOT.json](SOURCE-SNAPSHOT.json) |
| Git revision | `cc8ae01` (working tree clean at capture time) |
| Engine | Godot `4.7.2.stable.official.ed1daf0bf`, Compatibility/OpenGL |
| Host | Windows 11 Home China 10.0.26200, Intel UHD Graphics |

## Capture method

Godot's built-in **Movie Maker** writer, driven by a deterministic input driver.

```bash
godot --path "<reel>/capture/game" \
  --resolution 3840x2160 \
  --write-movie "<reel>/capture/run-01.avi" \
  --fixed-fps 30 --disable-vsync --quit-after 1100
```

| | |
|---|---|
| Output | `capture/run-01.avi`, **3840 × 2160**, 30 fps, MJPEG in AVI |
| Verified with | `ffprobe` — dimensions read from the file, not assumed |
| Method | `scripted-input` |
| Input log | `capture/run-01-inputs.jsonl` |
| Driver summary | `capture/run-01-driver.json` |

**This is offline rendering, not evidence of real-time frame rate.** Movie Maker
renders each frame as long as it needs and writes it at a fixed 30 fps. The probe run
recorded at roughly 16% of real-time speed. Nothing in this film should be read as a
performance measurement.

**Native 4K is genuine, not upscaled.** The display on this machine is 1536 × 960;
Godot renders the movie offscreen at the requested resolution regardless. The game's
**logical** canvas is 640 × 360 with `stretch/mode=canvas_items` and `aspect=keep`,
so 3840 × 2160 is an exact **6× integer scale** of the intended pixel grid — crisp,
with no resampling. Logical resolution is disclosed separately here because
"native 4K" for pixel art means the canvas was scaled, not that the art has 4K detail.

## Isolated copy, and the one harness change

Capture ran against `capture/game/`, a copy of `godot/`. The original project, its
source, and any open instance were untouched. The copy differs in exactly two ways,
both harness, neither gameplay:

1. **`capture/walkthrough_driver.gd` added as an autoload** — drives input, logs it,
   asserts outcomes. It does not modify the game's scripts.
2. **`project.godot` window override raised** from 1280 × 720 to 3840 × 2160, and the
   config name suffixed `(capture)`. Viewport stays 640 × 360; physics, input map,
   collision layers, renderer and clear colour are unchanged.

The driver sets `game.test_mode = true` at start. That flag gates **only** the
`focus_exited → set_paused(true)` handler, so an unattended capture is not paused by
the window losing focus. It changes no movement, collision, scoring or state logic.
Consequence for coverage: pause-on-focus-loss is not filmed — see
[coverage.json](coverage.json) and [_qc/REPORT.md](_qc/REPORT.md).

## What the driver is and is not allowed to do

Per `references/capture-and-coverage.md`, the driver:

- sends **only real `InputEventKey` events** via `Input.parse_input_event`, the same
  path a physical keyboard takes — `_unhandled_input` for Enter/Esc/P/R/M, and
  `Input.get_axis` / `is_action_pressed` for movement and jump
- **observes** `position.x`, `is_on_floor()` and `state` to decide *when* to press a
  key, which the reference explicitly permits
- **never** teleports the body, assigns velocity, sets completion, disables collision,
  or touches the `test_control` path the unit tests use
- logs every key transition with the physics tick, player position, game state and
  death count
- asserts the expected outcome of all 13 phases and **quits nonzero** if any fails.
  Exhausting `--quit-after` is not treated as success.

## A real problem this surfaced

The first 4K run **diverged from the validation run**. At `--fixed-fps 30` with 60 Hz
physics, two physics ticks share one rendered frame, and input events are flushed per
*rendered* frame — so a jump whose press and release were two ticks apart landed inside
a single frame and was **silently dropped**. The player never jumped the first step,
got stuck against it, and never reached the spikes, so the `spikes-kill` assertion
failed with `state: PLAYING`.

Fixed by holding keys for 5–6 ticks (3 rendered frames at 30 fps) and, for jumps,
confirming `player.jumps` actually incremented before consuming a mark — otherwise the
next tick retries the press. This is why the driver asserts instead of assuming: a
capture that merely ran to completion would have produced 30 seconds of footage of a
character stuck against a step.

## Route and timings

1812 physics ticks ≈ **30.2 s**, 92 logged events. Tick → seconds is `t / 60`
(physics is 60 Hz; the movie is 30 fps, so movie frame = `t / 2`).

| Tick | Time | Phase |
|---|---|---|
| 0 | 0.00 s | menu card |
| 65 | 1.08 s | Enter starts |
| 75 | 1.25 s | movement both directions (facing flip) |
| 153 | 2.55 s | R — manual retry, no death counted |
| 164 | 2.73 s | walk into the spikes |
| ~267 | ~4.45 s | death, retry card |
| ~301 | ~5.02 s | auto-recovery at spawn |
| 311 | 5.18 s | clean run, Zones 01–02 |
| 630 | 10.50 s | Esc — pause, frozen 1 s, Enter resumes |
| 703 | 11.72 s | jump into Zone 03, land on the fork pad |
| 804 | 13.40 s | low road: jump the spikes, then fall in the pit |
| ~1001 | ~16.68 s | auto-recovery |
| 1011 | 16.85 s | full run, high line to the relocated flag |
| ~1582 | ~26.37 s | completion, results card |
| 1652 | 27.53 s | Enter — replay from a clean slate |
| 1697 | 28.28 s | P pause, M back to menu |

Exact timings for the submitted capture are re-read from `run-01-inputs.jsonl`;
the table above is from the matching validation run and is indicative.

## Drift after the capture — the submitted source is not byte-identical to the filmed source

Recorded because "the film shows the submitted game" is a claim a reviewer should be able to
check, and a bare mismatch of hashes would look worse than the truth.

After the film was rendered, the project was opened in the Godot editor again (to play it for
the human playtest). The editor **rewrote `project.godot`** — dropping `window/stretch/aspect`
and `physics/common/physics_ticks_per_second`, both of which equal engine defaults — and
**generated five `.uid` files** for test scripts added during this project. `.uid` files belong
in version control in Godot 4.4+, so they are committed rather than ignored.

Exactly **6 of 30 files** differ between the filmed snapshot and the submitted source:

```
MODIFIED  project.godot
ADDED     tests/capture_character.gd.uid
ADDED     tests/capture_map.gd.uid
ADDED     tests/character_board.gd.uid
ADDED     tests/map_board.gd.uid
ADDED     tests/probe_route.gd.uid
```

**Every gameplay file is byte-identical** — `features/player/player.gd`, `features/player/tuning.gd`,
`game/session.gd`, `game/main.tscn`, `ui/hud.gd`, `levels/first_steps.json`. Verified by
comparing per-file hashes against [SOURCE-SNAPSHOT.json](SOURCE-SNAPSHOT.json), which still
records the filmed state and is deliberately **not** updated.

Behaviour is unchanged, measured rather than assumed: a `ProjectSettings` probe on the submitted
source reports `aspect=keep` and 60 Hz physics — the same values the two removed lines declared.
The full suite still reports **31/31 and 9/9** on the submitted source.

`SOURCE-SNAPSHOT.json` is left at the filmed state on purpose. It is the film's evidence; it
should describe what was filmed, not be quietly refreshed so the hashes line up.

## Audio

The game is **silent** — no audio buses, no sound files, nothing in the source. No
sound effects were invented for it. Liam's narration is the only audio, and all of it
stops before the outro card, which carries only the spoken title and handle.
