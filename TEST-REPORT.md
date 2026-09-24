# TEST-REPORT — walker-jumpman-zhaohui-li

**Engine:** Godot `4.7.2.stable.official.ed1daf0bf`, Compatibility/OpenGL renderer, 60 Hz physics
**Machine:** Windows 11 Home China (10.0.26200), Intel UHD Graphics, `gl_compatibility`
**Source revision under test:** commit `adc7f4e` (`Record evidence: rerendered screens and machine-check receipts`)
**Starter baseline revision:** commit `7f412c8` (`Import walker-jumpman First Steps starter, unmodified`)
**Date:** 2026-09-23

Reproduce:

```bash
godot --headless --path godot --script res://tests/test_game.gd
```

```bash
godot --headless --path godot --script res://tests/test_keyboard.gd
```

```bash
godot --path godot --script res://tests/capture_game.gd
```

```bash
godot --path godot --script res://tests/capture_character.gd
```

---

## 0. Baseline, captured before any edit

Required so that "my change did not break this" is a comparison and not an assertion.

| Run | Receipt | Result |
|---|---|---|
| Mechanics, starter source | `evidence/mechanics-1790192843.449.json` | **25 checks / 0 failures** |
| Keyboard, starter source | `evidence/keyboard-1790192851.968.json` | **9 checks / 0 failures** |

Baseline reference numbers I later compared against: measured jump rise **56.0747 px**, `low-ceiling` minimum feet `300.000274658203`, deterministic route **325 ticks**, largest auto-retry **34 ticks**.

The starter's own receipts from 2026-09-10 (`mechanics-17890784*.json`, `keyboard-17890796*.json`) are retained untouched.

---

## 1. The full run sequence, including the runs that failed

Nothing here is deleted or re-ordered to look tidy. Six machine runs, in order:

| # | Receipt | Checks | Fail | What it records |
|---|---|---|---|---|
| 1 | `mechanics-1790192843.449.json` | 25 | 0 | Baseline, starter source, before any edit |
| 2 | `mechanics-1790193254.788.json` | 25 | 0 | After the BEACON character swap — physics identical |
| 3 | `mechanics-1790193396.732.json` | 25 | **1** | After widening the level — **predicted failure F1** |
| 4 | `mechanics-1790193519.35.json` | 29 | **1** | After the first Zone 03 draft — **unpredicted head-clip bug** |
| 5 | `mechanics-1790193781.822.json` | 31 | 0 | After the Zone 03 redesign |
| 6 | `mechanics-1790194068.827.json` | 31 | 0 | Final confirmation run on the submitted source |

Keyboard checks: `keyboard-1790194014.765.json` and `keyboard-1790194015.969.json`, **9/9** each, unchanged from baseline.

### Run 3 — the predicted route-fixture break (CHANGE-BRIEF F1)

```
{"id":"complete-real-route","status":"FAIL",
 "observed":{"deaths":1,"jump_marks_used":5,"position":"(1046.217, 435.9253)","state":3,"ticks":375}}
```

Predicted cause confirmed by the observation rather than assumed: `jump_marks_used` is 5, i.e. the driver exhausted the starter's mark list, then held right and walked off the old level edge at x=960 into the new pit, crossing `fall_y=430` at x≈1046. Exactly the failure the brief described.

Response: extended the fixture. **The 900-tick budget and the `deaths == 0` requirement were not relaxed.** See §3.

### Run 4 — the bug I did not predict

After the first Zone 03 draft, `complete-real-route-low` failed while `complete-real-route-high` passed:

```
{"id":"complete-real-route-low","status":"FAIL",
 "observed":{"deaths":1,"jump_marks_used":7,"position":"(1272.882, 307.5416)","state":3,"ticks":460}}
```

`jump_marks_used: 7` means the spike-jump mark *did* fire, so this was not a missing input. I wrote `godot/tests/probe_route.gd` to dump the body tick by tick instead of guessing:

```
t=444 x=1232.9 y=319.9 vx=160.0 floor=true  mark=6
JUMP #7 at x=1243.5 y=314.6 vx=160.0
t=450 x=1248.9 y=304.7 vx=160.0 floor=false mark=7
t=456 x=1264.9 y=302.7 vx=160.0 floor=false mark=7
ENDED state=3 at x=1272.9 y=307.5 after 459 ticks
```

The jump fired correctly and then **stopped rising at 17 px instead of 56**. Cause: my first draft stacked the two routes vertically. High ledge A occupied x 1176–1248 with its underside at y=272, and the low road's spike jump started at x≈1243 — directly beneath it. BEACON is 28 px tall and jumps 56 px, so it needs **84 px** of headroom; the ledge left **48 px**. The body hit the ledge's underside and dropped into the spikes it was trying to clear.

This is the "keep what the player sees consistent with what the physics checks" trap from the other direction: the picture looked fine, the physics did not agree.

Response: redesigned Zone 03 so the two lines are **not vertically stacked over any jump arc**. The high line now climbs via an intermediate step to y=216, putting its underside at 228 — **92 px** above the low road, clear of the 84 px requirement with 8 px to spare. I did **not** raise `jump_velocity` or shorten the character.

Regression check added so it cannot come back silently:

```
{"id":"low-road-jump-not-clipped-by-high-line","status":"PASS",
 "observed":{"apex_feet_y":263.924285888672,"rise_px":56.0757141113281}}
```

It witnesses the actual apex of the real body while running the real low road, and asserts the full 56 px rise. Before the fix this check reads ~17 px.

---

## 2. Required checks

### Startup and controls

| Check | Evidence | Result |
|---|---|---|
| Project runs (normal main scene) | `godot --headless --path godot --quit-after 120`, exit 0, no script errors | PASS |
| Editor-free launch, windowed | Launched `Godot_v4.7.2-stable_win64.exe --path godot`; menu drew, Enter started play | PASS |
| Enter starts | `enter-start` | PASS |
| Move (D / arrows) | `keyboard-move`, x=91.02 after 10 ticks | PASS |
| Jump (Space) | `keyboard-jump`, `jumps=1`, `velocity.y < 0` | PASS |
| Pause (Esc) freezes | `escape-pause`, position unchanged while paused | PASS |
| Resume (Enter) | `enter-resume` | PASS |
| Retry (R) | `r-retry`, back to spawn (64, 320), deaths not incremented | PASS |
| Replay after completion | `enter-replay`, `replay-idempotent` | PASS |
| Pause → M → main menu → Enter | `pause-main-menu`, `menu-start-again` | PASS |
| Focus loss pauses | `focus-loss-pauses` | PASS |

Movement/jump tuning is provably untouched: `speed-cap` 160.0, `fixed-jump-and-no-double` rise **56.0747 px** and `low-ceiling` minimum feet **300.000274658203** are **bit-identical to the baseline run**, and `tuning.gd` is unmodified in the diff.

### Character appearance

Evidence: `evidence/screens/05-character-states.png` — six states (stand R, walk R, walk L, rising R, falling R, falling L) each rendered at 5× with the **exact 18×28 collider drawn over the art in red**.

| Question | Answer |
|---|---|
| Does any art leave the collider? | No, in any of the six states. The domed head tops out at y = −27.8 against a collider top of −28; the cargo pack and fin reach x = ±9 exactly. |
| Left vs right readable? | Yes. Pack, head fin and leading arm all mirror; the cyan eye slot sits on the facing side. Three cues, all consistent. |
| Standing vs jumping readable? | Yes. Legs together rising, braced apart falling, visor slot tall rising / squinted falling, chest lamp turns cyan only while airborne. |
| Deliberate art/collider gap | While **grounded and walking**, the stride lifts one boot up to 2 px off y=0. Airborne poses always keep both boots on y=0, so the gap can never occur at a moment when it could mislead a hazard-clearance read. |

In-world appearance against terrain and hazards: `02-failure.png`, `03-jump.png`, `06-zone3-fork.png`, `08-zone3-spike-jump.png`, `09-zone3-pit-failure.png`.

### Extended route

| Check | Observed | Result |
|---|---|---|
| `complete-real-route-low` | `state=COMPLETE, deaths=0, ticks=562, position=(1544.9, 319.9)` | PASS |
| `complete-real-route-high` | `state=COMPLETE, deaths=0, ticks=565, position=(1552.9, 277.5)` | PASS |
| `starter-section-still-walkable` | reached x=918.2 with `deaths=0` | PASS |
| `old-finish-no-longer-wins` | at the old finish x, `state` is still PLAYING; `finish_x=1548` | PASS |

Both lines reach the relocated flag on ordinary held-right-plus-jump inputs. The two lines come out at **562 vs 565 ticks** — a 3-tick (0.05 s) difference, so neither is a dominant strategy on time alone; the trade-off is hazard exposure versus jump precision.

New landings that require jumps: the **fork pad** (y=288, 56 px gap and a 32 px rise from the old level's end), the **step** (y=248), **high ledge A** (y=216) and **high ledge B** (y=216), plus the **finish pad** across a 64 px pit on the low road. That is four new jump-required landings against the two required.

### Failure and recovery

| Check | Observed | Result |
|---|---|---|
| `zone3-spikes-are-live` | `state=DYING`, reason "Watch the spikes" | PASS |
| `zone3-pit-is-fatal` | `state=DYING` at (1416, 435.8), reason "Missed the landing" | PASS |
| `actual-spike-collision` (starter hazard) | `state=DYING, deaths=1` | PASS |
| `fall-boundary` | PASS | PASS |
| `respawn` | back at (64, 320), `state=PLAYING` | PASS |
| `twenty-retries` | 21 deaths, largest retry **34 ticks** (≈0.57 s) | PASS |
| `duplicate-death-ignored`, `death-before-finish`, `manual-restart-not-death` | PASS | PASS |
| `replay-idempotent` | after completion, Enter replays with deaths=0, jumps=0 | PASS |

The two Zone 03 failure modes report **different** messages, so the retry card tells the player which mistake they made. Screenshot of a real pit death: `09-zone3-pit-failure.png`.

### Camera and presentation

| Item | Check | Result |
|---|---|---|
| Camera reaches the new finish | Clamp is `width − 320` = 1280, so the view spans x 960–1600 and the flag at 1548 is on screen. Confirmed in `07-zone3-high-line.png` and `04-complete.png`. | PASS |
| No unpainted strip past the old edge | Backdrop is now `width + 800` wide, grid runs to `level.width`; nothing beyond x=1400 is bare. Confirmed visually. | PASS |
| Hills extend into Zone 03 | `level.hills` gained entries at 1100 and 1430. | PASS |
| Spikes drawn where they collide | Baseline/tip now come from the hazard rect. `zone3-spikes-are-live` dies at the drawn position. | PASS |
| Flag drawn where it triggers | Pole stands on `finish[1]+finish[3]`; `04-complete.png` shows BEACON at the drawn flag at the moment of completion. | PASS |
| HUD progress is truthful | Derived from spawn→finish. At x≈1040 the bar reads ≈66% ((1040−64)/1484); with the starter's constant it would have pegged at 100%. | PASS |
| Labels readable | See the revision in §4 — the first placement collided with the jump arc. | Revised, then PASS |

### Automated checks — summary

| Command | Result |
|---|---|
| `godot --headless --path godot --script res://tests/test_game.gd` | **31 checks / 0 failures**, exit 0 |
| `godot --headless --path godot --script res://tests/test_keyboard.gd` | **9 checks / 0 failures**, exit 0 |
| `godot --headless --path godot --quit-after 120` | exit 0, no script errors |
| `godot --path godot --script res://tests/capture_game.gd` | 8 viewport captures, route completed with 0 deaths, exit 0 |
| `godot --path godot --script res://tests/capture_character.gd` | contact sheet rendered, exit 0 |

**No assertion was deleted and no expected value weakened.** The starter's 25 checks are all still present and still passing at their original tolerances. Six checks were added (net +6 after `complete-real-route` split into two lines).

---

## 3. What changed in the route fixture, and why

`godot/tests/route_driver.gd`, diff against the starter:

| Before | After |
|---|---|
| one flat list `[138, 292, 424, 548, 712]` | `SHARED = [138, 292, 424, 548, 712]` — **the same five values, unchanged** |
| — | `LINES["low"] = [945, 1240, 1364]` |
| — | `LINES["high"] = [945, 1108, 1200, 1320]` |
| `Route.new()` | `Route.new(line)`; default `"low"` keeps old call sites working |

Every new mark and the reason it sits there:

| Mark | Line | Jump it triggers |
|---|---|---|
| 945 | both | Off the old level's end (x=960) onto the fork pad (x 1016–1128, top 288). 56 px gap plus a 32 px rise. |
| 1240 | low | Over the spike cluster at x 1272–1296. |
| 1364 | low | Over the 64 px pit (1384–1448) onto the finish pad. |
| 1108 | high | Fork pad → the step at x 1168–1224, top 248. |
| 1200 | high | Step → high ledge A at x 1264–1344, top 216. |
| 1320 | high | Ledge A → high ledge B at x 1392–1488, top 216. |

The high line needs no fourth mark: ledge B overhangs the finish pad, so the line ends by running off the edge and landing. That asymmetry is the design — the high line buys a free descent with an extra climb.

The `step()` logic is unchanged: hold right, press jump only when the body is genuinely `is_on_floor()` past a mark. It still edits no position or velocity, so a completing route remains evidence about geometry rather than about teleportation.

---

## 4. Inspect-and-revise cycles

### Cycle 1 — Zone 03 was stacked on top of itself (mechanical)

Observation, response and regression check: see §1, run 4. Source of the observation: `probe_route.gd` trace, not intuition.

### Cycle 2 — the zone label sat inside the jump arc (clarity)

Observation: in the first render of `07-zone3-high-line.png`, the sub-label *"Low road: spikes, then a pit. High line: climb, then glide."* was placed at world y=170 and BEACON jumped straight through it between the step and ledge A. No crash, no test failure — the machine checks all passed. It was simply hard to read at the exact moment the player is being asked to make the decision the label explains.

Response: moved both Zone 03 labels from y=150/170 to **y=118/138**, above the high line's apex (feet ≈197, head ≈169). Re-rendered; the label is now clear of the body in every capture.

Kept as a limitation rather than "fixed": the labels are still static world text with hand-placed coordinates. They are in the level JSON now, so they move with the data, but nothing *checks* that a label does not overlap geometry. A future version should measure the string and assert clearance.

### Cycle 3 — boots read as one slab (cosmetic)

Observation: in the first character contact sheet, the two 6 px boots met at x=0 and read as a single wide bar when standing, flattening the silhouette. Response: narrowed each boot to 5 px so a 2 px gap shows. Visible in the current `05-character-states.png`.

---

## 5. Human playtest

**Done. 2026-09-24. Player: Zhaohui Li (the author). Build: commit `cc8ae01`,
run from `godot --path godot` in a normal game window with a keyboard.**

### What the player actually reported

Verbatim, in full:

> 我试玩了，没有问题，可以通关
> *("I playtested it, no problems, can complete it.")*

### What that establishes

- A human, playing with a keyboard rather than a scripted driver, **reached the
  relocated finish**. Completion is no longer only a machine claim.
- Nothing blocked, crashed, soft-locked or read as broken badly enough to be
  worth mentioning.

### What that does NOT establish — stated plainly

This is a brief report, and it is recorded as brief rather than written up into
something it is not. It does **not** answer the questions this report has been
flagging as open since §6:

| Open question | Still open? |
|---|---|
| Does the fork-pad entry jump feel tight? (calculated ~46 px window, never measured) | **Yes** — not reported on |
| Did the fork read as a *choice*, or did momentum pick the line? | **Yes** — not reported on |
| Which route was taken; was the other one ever tried? | **Yes** — not reported |
| Where did deaths happen, and did the ~0.55 s retry feel fast enough? | **Yes** — no deaths reported, none described |
| Was the relocated finish findable without prior knowledge? | **No** — the player authored the level, so they cannot test discoverability |

**The author is not a naive player.** They knew where every landing and hazard
was before starting, so this session cannot speak to first-time legibility,
difficulty, or whether the fork communicates itself. That is the single most
important thing still untested about this level, and one playtest by the person
who built it cannot fix it.

No second playtester has been recruited. No second-person feedback is claimed
anywhere in this repository.

---

## 6. Honest limitations

1. **The only playtest is the author's, and it is one sentence long** (§5). It establishes that a person can complete the level. It cannot establish first-time legibility, because the player designed the level and knew the layout before starting. No naive player has seen this build.
2. **The automated routes are one input each.** `complete-real-route-low/high` prove *a* path exists; they say nothing about the width of the timing window a real player has. The tightest jump in Zone 03 is the fork-pad entry, where my arithmetic puts the usable take-off window at roughly 46 px of run-up (≈0.29 s). That number is calculated, **not measured**, and is exactly the sort of thing a human playtest should overturn.
3. **Label placement is unverified by any check.** See cycle 2.
4. **The contact sheet is a fixture, not gameplay.** `05-character-states.png` freezes the body deliberately (`enabled = false`, velocity assigned) to render six poses side by side. It is a reconstructed diagram of real draw output, and is labelled as such — it is not a screenshot of play.
5. **`zone3-spikes-are-live` and `zone3-pit-is-fatal` teleport the body** into position, in the same style as the starter's `actual-spike-collision`. They verify the triggers, not that a player naturally arrives there.
6. **Windows only.** The starter reports macOS/M4 Pro results; I ran on Windows 11 with Intel integrated graphics. Physics is deterministic at 60 Hz so the mechanical numbers match the starter's (rise 56.0747), but I have not re-verified the macOS launcher `walker-jumpman.command`.
7. **`.godot/` engine cache is gitignored**, so a fresh clone re-imports on first open. That re-import rewrites `project.godot` and drops the two default-valued lines I restored in commit `ebb9604`; this is cosmetic and behaviourally verified as a no-op.
