# SHOTLIST — Walker Jumpman, Extended

Landscape 4K (3840×2160), 30 fps. Voice: Kokoro `am_onyx`, Liam in for Bear.
Structure: walker mode — ask → BLUF → gameplay body → cause-and-effect →
Verdict → Your Turn → regular outro.

Durations are the **measured** Kokoro narration lengths, which are the clock.

| Beat | Act | Source | What is on screen | Label | Dur |
|---|---|---|---|---|---|
| B00 | ASK | Remotion `ClaudeComposerAsk` | Composer types the Walker ask; send arms terracotta; three RESULT lines land | *reconstructed ask* in `runningText` | 16.60 s |
| B01 | BLUF | Remotion `BrutalistHesitantWriter` | "…is **a new game**:" types, is struck through, corrects to "**an extension of Bear's starter**" | — | 9.83 s |
| B02 | OPEN | `capture/run-01.avi` 0.00–3.63 | Title card over the live level; Enter; then D and A — pack and fin flip | SCRIPTED INPUT | 3.63 s |
| B03 | MECHANISM | 2.40–6.24 | R back to spawn, counter unchanged; walks into spikes; "Watch the spikes"; auto-retry | SCRIPTED INPUT | 3.84 s |
| B04 | MECHANISM | 4.90–11.49 | Single jumps over both steps, the spike cluster and both gaps; HUD bar advances | SCRIPTED INPUT | 6.59 s |
| B05 | MECHANISM | 10.40–14.84 | Escape freezes body and timer; Enter resumes; jump onto the fork pad | SCRIPTED INPUT | 4.44 s |
| B06 | MECHANISM | 13.30–17.50 | Low road: clears the second spike cluster, then falls in the pit — "Missed the landing" | SCRIPTED INPUT | 4.20 s |
| B07 | MECHANISM | 17.28–30.23 | High line: step, ledge A, ledge B, runs off onto the pad, flag, results, Enter replay, P→M | SCRIPTED INPUT | 12.95 s |
| B08 | FALSIFIABILITY | `evidence/screens/10-level-map.png` | Whole-level map; cut in on the stacked ledges over the low road as the numbers land; cut back out | LEVEL MAP · rendered from `first_steps.json` | 29.41 s |
| B09 | VERDICT | Remotion `ClaudeVerdictArtifact` | Four artifact lines: what ran, what is not filmed, what scripted input cannot prove, what is untested | — | 20.25 s |
| B10 | HANDOFF | Remotion `ClaudeComposerAsk` | Greeting "Your turn."; the measurement prompt types in; read aloud then discussed | — | 20.22 s |
| B11 | OUTRO | Remotion `ClaudeTitleOutro` | "Walker Jumpman, Extended." · @NikBearBrown · slug-seeded mascot · no subline | — | 3.46 s + 1.0 s tail |

**Total narration ≈ 136 s (2 min 16 s).** Duration follows the explanation; no
runtime target was filled.

## Cut discipline

- No gameplay is slowed, sped up, reversed or looped. Every clip is the capture
  at 1× and is exactly its narration's length, so the compiler has nothing to
  retime and nothing to freeze-pad.
- Adjacent gameplay windows overlap by ~1 s of continuous footage. That is not a
  replayed take and is not presented as a second independent test.
- Gameplay is inset at an exact 5× integer scale on the game's own cream page
  colour so the label band never covers the game's HUD. No crop of the play area.
- B08 is the only non-gameplay body beat, and it is a diagram generated from the
  level data — not a reconstruction of gameplay.

## Audio

Game is silent by construction (no audio buses or sound files in source), so
nothing is muted and no sound effect is invented. Liam is the only audio, and it
stops before the outro card, which carries only the spoken title and handle over
a 1 s silent tail.
