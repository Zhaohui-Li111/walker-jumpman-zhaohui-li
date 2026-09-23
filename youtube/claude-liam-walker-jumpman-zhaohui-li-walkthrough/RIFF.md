# RIFF.md — walker-jumpman-zhaohui-li

Commentary pass over `capture/run-01.avi` (native 3840x2160, 30 fps, 30.23 s,
scripted keyboard input). Every row's time range is read from `coverage.json`,
which is generated from the capture's own tick log — not chosen by eye.

**Separation of kinds, per the riff skill:**

- *Observation* — what is visible in the capture at that time range.
- *Interpretation* — why it behaves that way. Where this comes from reading the
  source rather than from the footage, it says so.
- *Not claimed* — a scripted route cannot establish fun, fairness or
  accessibility, and nothing here does.

---


## Shown features

| Feature | Capture range | Beat | Visible observation | Interpretation |
|---|---|---|---|---|
| `menu-and-start` | 0.00–1.83s (action 1.17s) | B02 | Title card is on screen with the level behind it; Enter is pressed and the card clears to a live player at the spawn point. | The menu is not a separate scene - the level is already running behind it. That is why Enter starts instantly with no load. |
| `move-left-and-right` | 1.33–2.77s (action 2.63s) | B02 | D drives the character right past x=100, then A drives it back left; the cargo pack and head fin flip across the body at the turn. | Facing is readable from the outline alone, before you can see the eye - that is what the asymmetric pack buys at eighteen pixels wide. |
| `jump-fixed-height` | 5.37–6.67s (action 6.12s) | B04 | One Space press lifts the body onto the first step and it lands; holding the key does not produce a second jump. | One fixed-height jump, no double jump, six ticks of coyote and six of buffer. Every landing in the level is authored against that one arc. |
| `manual-retry` | 2.63–3.13s (action 2.90s) | B03 | R returns the player to the spawn point mid-run; the retry counter in the HUD stays where it was. | R is a restart, not a death. Separating those two means the retry count still measures mistakes rather than impatience. |
| `hazard-spikes` | 2.90–4.97s (action 4.63s) | B03 | The player walks into the spike cluster without jumping; the run stops and the card reads 'Watch the spikes'. | The hazard trigger is three exact triangles, not one oversized box - the collision matches the shape you can see. |
| `auto-retry` | 4.63–5.53s (action 5.20s) | B03 | About half a second after the death the player is back at the spawn point and playable, with no menu and no lives counter. | A cheap retry changes what the level can ask for. It does not tell us whether a first-time player saw the danger coming. |
| `starter-zones-route` | 5.37–10.92s (action 10.72s) | B04 | A clean run over the two steps, the spike cluster and both gaps of the original course, ending past x=880. | This is the starter's route, unchanged in the level data. The extension had to leave it walkable, and it does. |
| `hud-progress-timer-retries` | 6.37–10.92s (action 10.72s) | B04 | The progress bar advances across the top, the timer counts up and the retry count reads 01 after the earlier death. | The bar is derived from spawn and the finish trigger. With the starter's hard-coded span it would have pegged at full the moment the new zone began. |
| `pause-and-resume` | 10.72–12.10s (action 11.80s) | B05 | Escape freezes the body and the timer mid-run and shows the pause card; Enter resumes from exactly the same position. | Pause stops the clock as well as the body, so a paused run cannot be used to farm a better time. |
| `zone03-fork` | 12.10–13.75s (action 13.12s) | B06 | A jump across the gap at the end of the original course lands on a raised pad; from it both the low road and the climbing ledges are visible at once. | The decision is placed where you can see both answers before committing, and the climb back up is only thirty-two pixels - the fork does not punish curiosity. |
| `zone03-low-road` | 13.78–16.05s (action 15.35s) | B07 | On the low road the player jumps the second spike cluster at speed and lands back on the flat. | The low road trades precision for exposure: wide flat landings, but a hazard and a pit between you and the flag. |
| `zone03-pit-fall` | 15.73–16.90s (action 16.48s) | B07 | The player runs off the end of the low road into the pit and falls past the kill line; the card reads 'Missed the landing', not 'Watch the spikes'. | Two failure modes, two different sentences. The retry card tells you which mistake you actually made before it sends you back. |
| `zone03-high-line` | 22.72–25.88s (action 24.38s) | B08 | The other line: a step up, then two ledges above the low road, with no hazard on the route and the spikes visible below. | An early draft stacked these ledges directly over the low road. The body is twenty-eight pixels tall and jumps fifty-six, so the jump underneath needed eighty-four pixels of headroom and had forty-eight - it clipped the ledge and died. The fix was geometry, not tuning. |
| `finish-and-results` | 25.78–27.78s (action 26.78s) | B09 | The high line runs off its last ledge onto the finish pad and reaches the relocated flag; the results card shows the time and the retry count. | The flag moved from x=916 to x=1548, so the original route on its own can no longer win. The high line ends by falling, not jumping - that is what the extra climb buys. |
| `replay` | 27.95–28.70s (action 28.12s) | B09 | Enter on the results card starts a fresh attempt with the timer and the retry count both back at zero. | Replay resets the run state rather than reloading the scene, which is why it is instant. |
| `return-to-menu` | 28.78–30.22s (action 29.45s) | B09 | P pauses the new attempt and M returns to the title card, which can be started again. | Pause and menu are separate states, so M cannot be hit by accident mid-run. |

## Implemented but not shown

- **`pause-on-focus-loss`** — implemented in source and covered by the `focus-loss-pauses` machine check, but an unattended Movie Maker capture cannot lose window focus, so there is no footage of it. The human accepted a partial walkthrough for this one feature; recorded in `_qc/REPORT.md` and stated on screen in the Verdict beat. Not relabelled `planned` to obtain a pass.

## In the GDD, not in the game

- **`cherries`** — Proposed in the starter's GDD (twenty optional collectibles). Not built in this slice and not added by this extension.
- **`audio`** — No audio buses, sound files or music anywhere in the source. The game is silent by construction; no sound was invented for the film.
- **`settings-and-remapping`** — GDD proposes a settings screen with key remapping and persistence. No settings scene exists; the input map is built in code at startup.
- **`moving-platforms`** — Explicitly out of scope in the starter's MVP and not added here. All solids are static bodies.
- **`web-export`** — Export templates are not installed and no export was produced. This is a source-only release.

## Narration actually used

**B00** — Namaste — this is Liam, in for Bear. Zhaohui Li took walker-jumpman, Bear's one-jump Godot platformer, and extended it: a character you can actually read at eighteen pixels wide, and a final zone that makes you pick a route. Everything after this card is the real build, played through its own keyboard input.

**B01** — Not a new game — an extension. The starter's two zones are byte-identical in the level data and still walkable. What changed is who you play as, and where the level stops.

**B02** — Enter starts it. The level was already running behind.

**B03** — R is free. The spikes are not — and you are back instantly.

**B04** — One jump, fixed height, no double jump. Six ticks of coyote, six of buffer. Every landing is built on it.

**B05** — Escape freezes body and clock. Then one jump, and the level forks.

**B06** — Low road: spikes to clear, then a pit that names a different mistake.

**B07** — The high line climbs instead — a step, two ledges, no hazard on the route. The last ledge overhangs the pad, so it ends by falling, not jumping. Flag, results, Enter, and it replays clean. Then P, M, back to the title card.

**B08** — That high line started in the wrong place. The first draft stacked the ledges directly over the low road. The body is twenty-eight pixels tall and jumps fifty-six, so a jump underneath needs eighty-four pixels of headroom — and it had forty-eight. It clipped the ledge, rose seventeen pixels instead of fifty-six, and died on the spikes it was trying to clear. The fix was geometry, not jump strength. The ledges moved up, leaving ninety-two pixels. A check now measures the real apex on every run and fails if it ever reads seventeen again.

**B09** — Verdict. Sixteen implemented features shown running, two real deaths and two real recoveries, both fork routes finishing. One implemented feature is not on film: pause on focus loss, which an unattended capture cannot trigger — it is covered by a machine check instead. And this was a scripted route, not a person. It proves the geometry is reachable. It cannot tell you the level is fair.

**B10** — Your turn. Paste this: 'In my Godot platformer, measure the take-off window for every jump the level requires — sweep the jump position frame by frame and report the range that still lands.' That is the number I did not have. It turns is this jump fair into a measurement instead of an opinion. Run it on your own level and see which jump has the narrowest window — that one is where your players will quit.

**B11** — Walker Jumpman, Extended. At Nik Bear Brown.


---

## Suggested next experiment

Sweep the take-off position for each required jump with the same driver and
record, per landing, the range of positions that still land. The fork-pad entry
is the suspected narrowest window — currently a calculated ~46 px of run-up,
never measured. That single number would convert "is this jump fair?" from an
opinion into a measurement, and it is the prompt the film hands to the viewer.

## What this pass did not find

No crash, no soft-lock, no visual/collision mismatch, and no failed assertion in
the capture run (`capture/run-01-driver.json`, `failed_expectations: []`).
The defect this project actually hit — the high line clipping the low road's
jump — was found before this capture and is described in
[../../TEST-REPORT.md](../../TEST-REPORT.md) section 1. It is explained on
screen in B07 using the fixed geometry; the film does not restage the bug.

## Renders that failed

None during this pass. The first 4K capture attempt failed its own assertions
(dropped jump input at 30 fps) and was discarded and re-recorded rather than
shipped; see [CAPTURE.md](CAPTURE.md).
