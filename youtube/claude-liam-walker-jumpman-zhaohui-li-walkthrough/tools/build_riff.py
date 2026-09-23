#!/usr/bin/env python3
"""Write RIFF.md from coverage.json + beat_sheet.json, so every time range in
the report is the measured one. Observations describe what is visible in the
capture; interpretations are marked with their source."""
import json
import pathlib

REEL = pathlib.Path(__file__).resolve().parent.parent

HEAD = """# RIFF.md — walker-jumpman-zhaohui-li

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

"""

TAIL = """
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
"""


def main():
    cov = json.loads((REEL / "coverage.json").read_text(encoding="utf-8"))
    sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
    narration = {b["beat_id"]: b["narration_text"] for b in sheet["beats"]}

    rows = []
    for feature in cov["features"]:
        if feature["status"] != "implemented":
            continue
        if not feature["evidence"]:
            rows.append((feature["id"], None))
            continue
        for ev in feature["evidence"]:
            rows.append((feature["id"], ev))

    lines = [HEAD]
    lines.append("## Shown features\n")
    lines.append("| Feature | Capture range | Beat | Visible observation | Interpretation |")
    lines.append("|---|---|---|---|---|")
    for fid, ev in rows:
        if ev is None:
            continue
        rng = f"{ev['start_s']:.2f}–{ev['end_s']:.2f}s (action {ev['action_s']:.2f}s)"
        obs = ev["observation"].replace("|", "\\|")
        rif = ev["riff"].replace("|", "\\|")
        lines.append(f"| `{fid}` | {rng} | {ev['beat_id']} | {obs} | {rif} |")

    lines.append("\n## Implemented but not shown\n")
    for feature in cov["features"]:
        if feature["status"] == "implemented" and not feature["evidence"]:
            lines.append(
                f"- **`{feature['id']}`** — implemented in source and covered by the "
                f"`focus-loss-pauses` machine check, but an unattended Movie Maker capture "
                f"cannot lose window focus, so there is no footage of it. The human accepted a "
                f"partial walkthrough for this one feature; recorded in `_qc/REPORT.md` and "
                f"stated on screen in the Verdict beat. Not relabelled `planned` to obtain a pass.")

    lines.append("\n## In the GDD, not in the game\n")
    for feature in cov["features"]:
        if feature["status"] == "planned":
            lines.append(f"- **`{feature['id']}`** — {feature['reason']}")

    lines.append("\n## Narration actually used\n")
    for bid in sorted(narration):
        lines.append(f"**{bid}** — {narration[bid]}\n")

    lines.append(TAIL)
    out = REEL / "RIFF.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out} ({len(rows)} evidence rows)")


if __name__ == "__main__":
    main()
