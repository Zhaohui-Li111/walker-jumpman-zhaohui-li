# FACTCHECK — every claim the narration makes, and where it is checked

Each row is a factual claim spoken in the film. "Checked against" names the file,
command or measurement that settles it. Claims that are judgements rather than
facts are marked as such and are not asserted as measurements.

| Beat | Claim | Checked against | Verdict |
|---|---|---|---|
| B00 | The project extends walker-jumpman by Nik Bear Brown | `git log` — commit `7f412c8` is the unmodified starter import; README and SOURCES credit it | TRUE |
| B00 | The character is readable "at eighteen pixels wide" | collider is `RectangleShape2D(18, 28)` in `player.gd::_ready()`; `evidence/screens/05-character-states.png` overlays it | TRUE |
| B00 (card) | "Character drawn in `_draw()`, collider untouched" | `git diff 7f412c8..HEAD -- godot/features/player/tuning.gd` is **empty**; collider construction unchanged in the diff | TRUE |
| B00 (card) | "Finish moved 916 to 1548" | `first_steps.json` finish `[916,264,24,56]` → `[1548,264,24,56]` | TRUE |
| B00 | The Walker prompt shown | **Reconstruction, labelled.** This project was extended from an existing starter, not generated from a blank Walker run. `role_note` on B00 and this row say so; no build receipts are shown. | RECONSTRUCTION |
| B01 | "The starter's two zones are byte-identical in the level data" | first five `solids` entries and the first `hazards` entry are unchanged in `first_steps.json`; `git diff` of that file shows additions only | TRUE |
| B01 | "and still walkable" | `starter-section-still-walkable` check — reaches x=918.2 with 0 deaths | TRUE |
| B02 | "The level was already running behind" | `session.gd::_ready()` builds the level and starts in `State.MENU`; `_draw()` renders it under the HUD overlay | TRUE |
| B03 | "R is free. The spikes are not" | `r-retry` check (deaths unchanged) vs `actual-spike-collision` (deaths 1) | TRUE |
| B03 | "you are back instantly" | `retry_remaining = 0.55`; `twenty-retries` measured largest gap **34 ticks ≈ 0.57 s** | TRUE |
| B04 | "One jump, fixed height, no double jump" | `fixed-jump-and-no-double`, `held-jump-no-bounce` | TRUE |
| B04 | "Six ticks of coyote, six of buffer" | `tuning.gd` `coyote_ticks = 6`, `buffer_ticks = 6`; boundary checks `coyote-5/6/7`, `buffer-5/6/7` | TRUE |
| B05 | "Escape freezes body and clock" | `pause-freezes` — position and `elapsed` both unchanged across 10 steps | TRUE |
| B06 | "a pit that names a different mistake" | `zone3-pit-is-fatal` reason "Missed the landing" vs `zone3-spikes-are-live` reason "Watch the spikes" | TRUE |
| B07 | "The last ledge overhangs the pad, so it ends by falling, not jumping" | ledge B spans x 1392–1488, finish pad starts x 1448; `route_driver.gd` high line has **no fourth jump mark** and still completes | TRUE |
| B07 | "it replays clean" | `replay-idempotent` — deaths 0, jumps 0 after Enter | TRUE |
| B08 | "twenty-eight pixels tall and jumps fifty-six" | collider height 28; measured rise **56.0747 px** (`fixed-jump-and-no-double`) | TRUE |
| B08 | "needs eighty-four pixels of headroom" | 28 + 56.07 = 84.07 — arithmetic on the two measured values above | TRUE (derived) |
| B08 | "it had forty-eight" | first-draft ledge A top y=256, thickness 16 → underside y=272; low road top y=320; 320 − 272 = 48 | TRUE |
| B08 | "rose seventeen pixels instead of fifty-six" | `probe_route.gd` trace: jump at y=314.6, minimum y=302.7 → 17.3 px. Quoted in TEST-REPORT §1 | TRUE |
| B08 | "The ledges moved up, leaving ninety-two" | current ledge top y=216, underside 232 — wait: 216+16=232, 320−232=**88**. See correction below. | **CORRECTED** |
| B08 | "A check now measures the real apex on every run" | `low-road-jump-not-clipped-by-high-line`, observed `rise_px: 56.0757` | TRUE |
| B09 | "Sixteen implemented features shown running" | `coverage.json` — 16 implemented with evidence | TRUE |
| B09 | "two real deaths and two real recoveries" | input log: `spikes-kill` then `auto-retry-recovers`; `pit-kills` then `auto-retry-after-pit` | TRUE |
| B09 | "both fork routes finishing" | `complete-real-route-low` and `complete-real-route-high`, 0 deaths each | TRUE |
| B09 | "the fork-pad take-off window is calculated at ~46 px, never measured" | stated as *calculated* in CHANGE-BRIEF and TEST-REPORT §6.2; explicitly not claimed as measured | TRUE (and marked untested) |
| B09 | "It cannot tell you the level is fair" | judgement, and the correct one per the riff skill — a scripted route establishes reachability only | JUDGEMENT |

---

## Correction applied before render

**B08, "leaving ninety-two pixels."** The ledges are at y=216 with thickness 12
(`[1264, 216, 80, 12]`), so the underside is y=228 and the clearance over the low
road at y=320 is **92 px** — the original line is right, but only because the
ledge thickness is 12, not the 16 used by the first draft. The row above walked
through it with the wrong thickness. Verified against `first_steps.json`:

```
[1264, 216, 80, 12]   ledge A   underside 228   320 - 228 = 92
[1392, 216, 96, 12]   ledge B   underside 228   320 - 228 = 92
```

Requirement is 84.07 px, so the margin is **7.9 px**. Narration stands at
"ninety-two"; TEST-REPORT §1 says "92 px … with 8 px to spare", consistent.

## Claims deliberately NOT made

- No claim about frame rate or performance. The capture is offline-rendered by
  Movie Maker at roughly 8% of real-time speed; CAPTURE.md says so.
- No claim that the level is fun, fair, well-paced or accessible.
- No claim of a human playtest. There has not been one.
- No claim of a "complete walkthrough" — one implemented feature is unfilmed.
- No invented Walker build receipts; B00's prompt is labelled a reconstruction.
