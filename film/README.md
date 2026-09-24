# film/ — superseded planning notes

> **Read the reel instead:**
> [`youtube/claude-liam-walker-jumpman-zhaohui-li-walkthrough/`](../youtube/claude-liam-walker-jumpman-zhaohui-li-walkthrough/)

The three documents in this folder — `BEAT-SHEET.md`, `SCRIPT.md`,
`EVIDENCE-INDEX.md` — were written **before the Brutalist `godot-waikthrough`
skill was available on this machine**, when the film was blocked. They describe
a plan, written against the assignment's stated requirements, with an explicit
warning at the top of the beat sheet that they would have to be reconciled with
the skill's own template once it arrived.

They are kept because the assignment's Frictional record asks for what was
actually tried, and because comparing the plan with what got built is honest.
They are **not** the film's specification and should not be read as such.

## Where the real artefacts are

| Planned here | Actually built, in the reel |
|---|---|
| `BEAT-SHEET.md` | `beat_sheet.json` — 12 beats, machine-readable, with build and render provenance stamped in by the toolkit |
| `SCRIPT.md` | narration lives in `beat_sheet.json`; `RIFF.md` pairs each spoken line with the capture time range it describes |
| `EVIDENCE-INDEX.md` | `coverage.json` (the skill's contract, generated from measurements) + `CAPTURE.md` (provenance) |
| — | `SHOTLIST.md`, `FACTCHECK.md`, `PROMPTS.md`, `BUILD-LOG.md`, `_qc/REPORT.md`, `_qc/HUMAN-REVIEW.md` |

## What changed between the plan and the film

Worth recording, because most of it was forced by evidence rather than taste:

1. **The plan had 18 beats; the film has 12.** The planned beat list assumed
   narration could run as long as it liked over gameplay. It cannot — there are
   only 30.2 seconds of capture, and freezing frames to cover narration is
   exactly what the capture reference warns against.
2. **The cause-and-effect beat moved off the gameplay.** The plan put the
   headroom-bug explanation over footage. It became its own beat carried by the
   level map, because the footage does not show a bug that was fixed before the
   capture, and staging one would have been dishonest.
3. **The outro changed.** The plan said "Walker opening/summary, Verdict → Your
   Turn → regular outro" from the assignment. The skill's `OUTRO-LOCK.md` is
   stricter and newer: the card is spoken, never scored. The film follows the lock.
4. **Labels became concrete.** The plan listed label categories (`LIVE`,
   `SCRIPTED`, `HELD`). In the film every gameplay frame carries a burned-in
   `SCRIPTED INPUT · native 4K Godot capture, real engine run · NOT a human
   playtest`, and the map beat carries its own provenance label. No `HELD` frames
   were needed in the end, because clips were cut to their narration instead of
   frozen to fit it.
