# Human visual review — walker-jumpman-zhaohui-li walkthrough

`_qc/REPORT.md` is **overwritten by Gate V on every compile**, so it only ever
holds the machine's current verdict. This file is the human record: what was
looked at, what was wrong, and what changed. Machine checks and eyes are kept
separate on purpose.

---

## Round 1 — before any compile (frames pulled by hand)

Two defects, both found by extracting PNGs and looking at them. Neither would
have been caught by a duration probe, and neither was reported by any test.

| # | Defect | Severity | Fix |
|---|---|---|---|
| 1 | The `SCRIPTED INPUT` label was burned over a full-bleed 6× frame and sat directly on top of the game's own HUD — "No lives. Just another try." and the retry counter were both obscured. The label was also 34 px at 4K, which is ~8 px at 1080p: illegible. | BLOCKER | Gameplay inset to an exact **5× integer scale** (3200×1800) on the game's cream page colour, giving a clean 180 px band. Label raised to 44 px. Still crisp — 5× of a 640×360 canvas is integer, so no resampling — and no crop of the play area. |
| 2 | The map beat scaled to 114% and panned, which cut off its own title and its legend — the two things that explain what the colours mean. | BLOCKER | Replaced the pan with three cuts: full map, in on the stacked ledges over the low road while the numbers land, back out. Motion now follows the narration instead of decorating it, and nothing essential leaves the frame. |

## Round 2 — Gate V, first compile

`Frames sampled: 24 · BLOCKER: 14 · MAJOR: 2`. Both causes were real. Fixed at
the source; **the gate was not relaxed and no check was disabled.**

| # | Gate finding | Cause | Fix |
|---|---|---|---|
| 3 | `edge-bleed` on B02–B07 (12 frames) — content crosses the title-safe bottom | The label's top was at y=2036 with a 46 px box, ending ~2082 against the 2052 safe line. I had positioned it from the band, not from the safe inset. | Label y is now derived from `SAFE_BOTTOM` itself (`0.95·H − size − 20`), so it cannot drift past the line again. |
| 4 | `edge-bleed` on B08 (all four edges) | The map was scaled full-bleed to 3840×2160, so its own content ran to the frame edge. | Matted at 3148×1771 inside the safe box. |
| 5 | `low-contrast` on B08, 0.16 and 0.25 against a 0.3 floor | A pale cream diagram on a pale cream surround gives the frame almost no luminance separation. | Matted on **ink** (`#25354A`) with a light label. Fixes the bleed and the contrast with one change, and reads as deliberate rather than as a letterbox. |

## Round 3 — bookend timing

Not a visual defect, but it would have become one. The first compile reported:

```
[art] B00: clip 21.0s center-cut to 16.6s (skip 2.2s head/tail)
[art] B01: clip 12.0s center-cut to 9.8s (skip 1.1s head/tail)
```

The Remotion beats had been rendered against `estimated_duration_s` before the
audio existed, so the compiler was **centre-cutting 2.2 s off the head** of a
type-on animation — the beginning of the typing, which is the whole point of the
cold open and of the hesitant-writer correction. Re-rendered with `--force` once
`actual_duration_s` was stamped, so each bookend is authored at its real length
and the compiler has nothing to cut.

---

## What a human still has to judge, and has not yet

- Whether the gameplay reads at 1080p and on a phone, not just at 4K.
- Whether Liam's narration is intelligible over the whole run, and whether the
  cuts between gameplay beats feel abrupt where adjacent windows overlap.
- Whether the film's claims land as honest rather than defensive.

These require watching the finished export end to end, which is the last step
before the film is considered done. Recorded here as outstanding until then.
