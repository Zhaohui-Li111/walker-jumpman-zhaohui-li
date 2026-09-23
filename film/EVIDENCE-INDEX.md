# Evidence index for the explainer

Every artefact the film draws on, what it actually is, and how to regenerate it.
Nothing here is a mock-up or a desktop screenshot; all images are real engine viewport output.

## Screens — `evidence/screens/`

| File | What it shows | Kind | Regenerate with |
|---|---|---|---|
| `01-menu.png` | Start card on the modified build | SCRIPTED | `capture_game.gd` |
| `02-failure.png` | BEACON dying on the starter's spike cluster, retry card visible | SCRIPTED | `capture_game.gd` |
| `03-jump.png` | The starter's Zone 02 gap, new character | SCRIPTED | `capture_game.gd` |
| `04-complete.png` | Completion at the relocated flag (x=1548), high line arrival | SCRIPTED | `capture_game.gd` |
| `05-character-states.png` | Six BEACON poses with the exact 18×28 collider in red | **FIXTURE** — bodies frozen on purpose, not gameplay | `capture_character.gd` |
| `06-zone3-fork.png` | Standing on the fork pad; both lines visible | SCRIPTED | `capture_game.gd` |
| `07-zone3-high-line.png` | High line mid-climb, low road and spikes below, flag in frame | SCRIPTED | `capture_game.gd` |
| `08-zone3-spike-jump.png` | Low road, clearing the Zone 03 spikes | SCRIPTED | `capture_game.gd` |
| `09-zone3-pit-failure.png` | A real fall into the Zone 03 pit, falling pose | SCRIPTED | `capture_game.gd` |

```bash
godot --path godot --script res://tests/capture_game.gd
```

```bash
godot --path godot --script res://tests/capture_character.gd
```

## Receipts — `evidence/`

| File | Content | Used in the film for |
|---|---|---|
| `mechanics-1790192843.449.json` | **Baseline**, starter source, 25/25 | Beat 4: the `low-ceiling` number before the character change |
| `mechanics-1790193254.788.json` | After BEACON, 25/25 | Beat 4: the same number after |
| `mechanics-1790193396.732.json` | 25 checks, **1 failure** — predicted route break | Beat 11: the failing runs were kept |
| `mechanics-1790193519.35.json` | 29 checks, **1 failure** — the headroom bug | Beat 9 |
| `mechanics-1790193781.822.json` | 31/31 after the redesign | Beat 9 |
| `mechanics-1790194068.827.json` | 31/31 final | Beat 11 |
| `keyboard-1790192851.968.json` | Baseline keyboard 9/9 | Beat 11 |
| `keyboard-1790194015.969.json` | Final keyboard 9/9 | Beat 11 |

Starter receipts from 2026-09-10 (`*-17890*.json`) are retained unmodified and are not
presented as this project's results.

## Source shown on screen

| Beat | File | Region |
|---|---|---|
| 4 | `godot/features/player/player.gd` | `_ready()` collider construction; head of `_draw()` |
| 9 | `godot/levels/first_steps.json` | the Zone 03 solids |
| 9 | `godot/tests/test_game.gd` | `low-road-jump-not-clipped-by-high-line` |
| 9 | trace text | quoted in [TEST-REPORT.md §1](../TEST-REPORT.md), regenerate with `probe_route.gd -- low` |

```bash
godot --headless --path godot --script res://tests/probe_route.gd -- low
```

## Film file identification

To be completed at render time and mirrored into README.md and SUBMISSION.md:

- Filename: *(pending)*
- SHA-256: *(pending)*
- Storage location: course media storage *(pending)*
- Game-source commit demonstrated: `adc7f4e`
