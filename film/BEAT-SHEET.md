> **SUPERSEDED planning note.** Written before the Brutalist skill was available, when the film was blocked. The film as actually built lives in `youtube/claude-liam-walker-jumpman-zhaohui-li-walkthrough/`. See [film/README.md](README.md) for what changed and why. Kept as an honest record of the plan, not as a specification.

# Beat sheet — walker-jumpman-zhaohui-li explainer

**Format:** landscape, native 4K, single film. **Workflow:** Brutalist `godot-walkthrough`
(original spelling `godot-waikthrough`) with the `walker` modifier.
**Structure required by the assignment:** Walker opening → body → Walker summary →
**Verdict → Your Turn → regular outro.**

> **Status: not rendered.** The Brutalist skill is not installed on this machine
> (see [SOURCES.md §6](../SOURCES.md)). This beat sheet and the script are written
> against the assignment's stated requirements; **both must be reconciled with the
> skill's own template once it is available** — the skill owns the exact opening
> wording, card layouts and quality gates, and this document does not guess at them.

**Game source demonstrated:** commit `adc7f4e` (to be re-confirmed at render time;
the film must name the revision actually on screen).

---

## Labelling rules applied throughout

Every beat below is tagged with what the footage actually is. These tags become on-screen
labels; nothing is presented as something it is not.

- `LIVE` — real engine viewport, real gameplay
- `SCRIPTED` — real engine viewport, but driven by an automated input route
- `FIXTURE` — real draw output, bodies frozen deliberately (the character contact sheet)
- `HELD` — a still frame held under narration
- `CODE` — source on screen
- `RECON` — reconstructed interface view (none currently planned)

No completion is faked, and no defect is hidden by editing. If the human playtest finds
something ugly, it goes in the film rather than being cut around.

---

## Beats

| # | Beat | Footage | Tag | Approx. |
|---|---|---|---|---|
| 1 | **Walker opening** — per skill template. Project name `walker-jumpman-zhaohui-li`; starter credited on screen: walker-jumpman by Nik Bear Brown. | Title cards | — | per template |
| 2 | **What this is** — an extension of a starter, not a new game. Show the starter's original figure and 960-wide level, then cut to the modified build. | `03-jump.png` (starter zone, new character) + live play | HELD / LIVE | ~15 s |
| 3 | **The character** — BEACON, a signal-courier automaton. Domed head, visor, cargo pack and fin on the trailing side. Show the contact sheet with the collider overlay and say plainly it is a fixture render. | `05-character-states.png` | FIXTURE | ~20 s |
| 4 | **Cause and effect #1 — the collider did not change.** Show `player.gd::_ready()` (18 × 28 at (0, −14)) beside `_draw()`, then the red overlay. State the consequence: because only `_draw()` changed, the `low-ceiling` check still reports `300.000274658203`, bit-identical to the pre-change baseline. Cut to that number in the two receipts. | `CODE` + receipt JSONs | CODE / HELD | ~25 s |
| 5 | **The extension** — Zone 03. Width 960 → 1600, finish 916 → 1548. Walk the original route live, cross into the new zone, stand on the fork pad. | live play | LIVE | ~25 s |
| 6 | **The decision** — low road (spikes, then a pit) versus high line (climb, then glide). Play the low road: jump the spikes, jump the pit. | live play | LIVE | ~25 s |
| 7 | **Both new landings** — replay from the fork and take the high line instead: step, ledge A, ledge B, then run off onto the finish pad. | live play | LIVE | ~25 s |
| 8 | **Failure and recovery** — a real death. Miss the pit on the low road; show the retry card, the automatic respawn, and that it says *"Missed the landing"* while the spikes say *"Watch the spikes."* | live play | LIVE | ~20 s |
| 9 | **Cause and effect #2 — the headroom bug.** The one the film exists to explain. Show the first draft's geometry (ledge stacked over the low road), the `probe_route.gd` trace with the jump stopping at 17 px, then the redesigned geometry and the regression check reporting a full 56.08 px rise. Say the number the check would report if the bug returned. | `CODE` + trace text + current build | CODE / HELD / LIVE | ~40 s |
| 10 | **Completion** — reach the relocated flag, show the results card and Enter-to-replay actually working. | live play | LIVE | ~15 s |
| 11 | **What I tested** — 31 mechanics + 9 keyboard, 0 failures; baseline captured before any edit; the failing runs kept. Name the receipts. | receipt list | HELD | ~15 s |
| 12 | **What is uncertain** — say it plainly: the fork-pad window is calculated, not measured; the two lines are within 0.05 s of each other and I do not know whether players will feel a reason to try both; nothing checks label placement. State the human-playtest status **truthfully as of render day**. | held card | HELD | ~20 s |
| 13 | **One next improvement** — a check that measures the *width* of the take-off window at each new landing, by sweeping the jump mark and recording which values still complete. Turns "is this jump fair?" from an opinion into a number. | held card | HELD | ~12 s |
| 14 | **Contributions** — human decided scope, character concept, the no-pixel-outside-the-collider rule, the fork's intent, and the call to redesign rather than weaken a check; AI wrote the drawing code, the geometry, the test harnesses, diagnosed the headroom bug, and drafted the documents. Narration is AI. Name the game revision on screen. | held card | HELD | ~15 s |
| 15 | **Walker summary** — per skill template. | | — | per template |
| 16 | **Verdict** | | — | per template |
| 17 | **Your Turn** — clone, import `godot/project.godot`, play it, and try the other line. | | — | per template |
| 18 | **Regular outro** | | — | per template |

Duration follows the explanation. Body beats total roughly **4½ minutes**; there is no runtime
to pad.

---

## Capture plan

| Need | How |
|---|---|
| Live gameplay | Screen-capture the real game window at 2560 × 1440 or better, scaled into the 4K frame. Logical resolution is 640 × 360 with `stretch/mode=canvas_items`, so integer scaling keeps the pixel art crisp — avoid non-integer scales. |
| Scripted route (if used) | `godot --path godot --script res://tests/capture_game.gd`; label `SCRIPTED`. |
| Contact sheet | `godot --path godot --script res://tests/capture_character.gd`; label `FIXTURE`. |
| Code on screen | Large type. `player.gd` `_ready()` + `_draw()` head; `route_driver.gd` `LINES`; the `low-road-jump-not-clipped-by-high-line` check. |
| Trace text | The `probe_route.gd` output quoted in [TEST-REPORT §1](../TEST-REPORT.md). |

**Readability gates before export:** smallest on-screen code legible at 1080p downscale;
HUD text legible; narration intelligible at −16 LUFS-ish speech level; watch the whole 4K export
end to end before publishing anything.

---

## Claims made in the film, and where each is evidenced

| Claim | Evidence |
|---|---|
| Collider and tuning unchanged | `git diff 7f412c8..HEAD -- godot/features/player/tuning.gd` is empty; `low-ceiling` = `300.000274658203` in both baseline and final receipts |
| Both fork lines reach the flag | `complete-real-route-low` / `-high`, 0 deaths |
| Original route still walkable | `starter-section-still-walkable` |
| Old finish no longer wins | `old-finish-no-longer-wins` |
| Two distinct failure modes | `zone3-spikes-are-live`, `zone3-pit-is-fatal` |
| The headroom bug was real and is fixed | `mechanics-1790193519.35.json` (failing) → `low-road-jump-not-clipped-by-high-line` (passing at 56.0757 px) |
| 31 + 9 checks, 0 failures | `mechanics-1790194068.827.json`, `keyboard-1790194015.969.json` |
