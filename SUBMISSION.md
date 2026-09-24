# Submission note

**Assignment:** Assignment 1 — Extend Walker Jumpman

**Student:** Zhaohui Li (li.zhaohui@northeastern.edu)

**Project name:** walker-jumpman-zhaohui-li

**GitHub repository/folder URL:** https://github.com/Zhaohui-Li111/walker-jumpman-zhaohui-li (public)

**Submitted commit SHA:** *fill in from `git rev-parse HEAD` after the final commit — a commit cannot contain its own SHA. Paste the same value into Canvas.*

**Game-source revision shown in the film:** `cc8ae01`, `build_id` `0be6756a1c222cf89964287272c5d6659111e6f50d2bb2f01969e8d03f963bf9` — the id recorded in the film's `coverage.json`. The submitted source hashes to `a16c4f8d6d00bb1ef886e1506c1bf434c95b42f325c11dfb33fc2e2758835247`: **6 of 30 files differ and none are gameplay** — the Godot editor re-normalised `project.godot` (removing two lines equal to engine defaults) when the project was reopened for the playtest, and generated five `.uid` files. Every gameplay file is byte-identical; `aspect=keep` and 60 Hz physics verified unchanged by probe; suite still 31/31 + 9/9. Enumerated in the reel's `CAPTURE.md` → "Drift after the capture".

**Godot version and operating system:** Godot `4.7.2.stable.official.ed1daf0bf`, Compatibility/OpenGL renderer · Windows 11 Home China (10.0.26200)

**Final film URL and filename:** https://drive.google.com/file/d/1zgNUQ5ItB9XI64Gouuah-qUQD21IpmS8/view?usp=drive_link · `claude-liam-walker-jumpman-zhaohui-li-walkthrough.mp4`

**Final film SHA-256:** `09bfdfc689362efe6830f05ae8c2abe6c934a8ba5e4720eef55d62cecd7882b3`
*(3840 × 2160, 30 fps, h264 + AAC 48 kHz stereo, 145.07 s, 14,690 KB.)*

**Verified after upload, not assumed:** the file was downloaded from the Drive link above with
no cookies and no credentials, and hashes **byte-for-byte identically** to the local master and
to the value recorded here. Drive did not re-encode it, and the link serves the file to an
unauthenticated visitor — so this checksum describes exactly what a reviewer receives.

---

## Summary of my changes

Extends the walker-jumpman "First Steps" starter by Nik Bear Brown
(https://github.com/nikbearbrown/walker-jumpman), recorded **unmodified** in this repository's
history at commit `7f412c8` so every later commit is a readable diff of my own work.

**Character — BEACON.** Replaced the starter's blue rectangle figure with a signal-courier
automaton: domed head, visor band with a single cyan eye slot, and a cargo pack plus swept fin
that ride the trailing side and flip across the body when you turn, so facing reads from the
outline alone at 18 px wide. Readable in six states (facing L/R × standing, rising, falling),
with legs that close on the way up and brace on the way down and a chest lamp that lights only
while airborne.

This is a `_draw()` rewrite. `tuning.gd`, the 18 × 28 collider, the collision layers and
`_physics_process` are untouched — evidenced by an **empty diff** on `tuning.gd` and by the
`low-ceiling` check reporting `300.000274658203` both before and after the swap, bit-identical.
Every drawn pixel stays inside the collider in every state; the one deliberate inward exception
(a ≤2 px boot lift during a grounded walk stride, never airborne) is documented.

**Level — Zone 03, "Pick your line".** Widened 960 → 1600 and moved the finish 916 → 1548, so
the original route alone can no longer win. Zones 01–02 are byte-identical in the level data and
still walkable (`starter-section-still-walkable`). A 56 px entry jump lands on a **fork pad**
where the level splits: a **low road** (spike cluster to jump, then a 64 px pit) or a **high
line** (a step and two ledges, no hazard, ending by running off an overhang onto the finish pad).
Four new landings require jumps. The trade is hazard exposure against jump precision, the choice
is reversible, and the two lines complete within 0.05 s of each other.

**Presentation.** The starter hard-codes drawing coordinates the level data does not control, so
extending the level required making them data-driven or the new zone would have been painted
wrong: backdrop, grid extent and hills now derive from `level.width`/`level.hills`; the spike
baseline comes from the hazard rect instead of a literal `y=320`; the flag pole stands on the
finish rect; zone labels moved into the level JSON; and the HUD progress bar derives its span
from spawn → finish instead of the constant `852`.

**Verification.** 31 mechanics + 9 keyboard checks, 0 failures, verified by **anonymous clone
from GitHub** with credentials disabled — not from the local folder. A baseline was captured on
the untouched starter before any edit; all 25 starter checks remain at their original tolerances
and 6 were added. No assertion was deleted and no expected value weakened. Failing runs are
retained in `evidence/` beside the passing ones, including a predicted route-fixture break and a
real bug: a first draft of Zone 03 stacked the two routes, and the low road's jump clipped the
ledge overhead, cutting a 56 px jump to 17 px. Found with a tick-by-tick trace, fixed by
redesigning geometry rather than tuning, and pinned by a regression check.

**Film.** `Walker Jumpman, Extended` — 2:25, native 4K, built with the Brutalist
`godot-waikthrough` skill in `walker` mode. Gameplay is a real Godot Movie Maker capture driven
by real `InputEventKey` events, labelled **SCRIPTED INPUT · not a human playtest** on every
frame. Gate V 0 BLOCKER / 0 MAJOR, GATE T PASS, `.verified.json` receipt SHA matches.

**Authorship.** Of ~1,700 lines of new code I typed approximately **0%**; Claude Code wrote
approximately **100%**. Measured with `git diff --shortstat`, not estimated. The design
decisions, constraints, three refusals, playtest and acceptance are mine and are traceable to
commits. Full breakdown in [SOURCES.md §4a](SOURCES.md).

---

## Known limitations

1. **Playtested by the author only.** Three sessions on 2026-09-24: high line (fork-pad entry
   jump cleared first try), low road, then deliberate deaths on each hazard. Recorded verbatim
   in TEST-REPORT §5 and FRICTIONAL §9. **No naive player has seen the build**, so whether the
   fork reads as a *choice* to a stranger is unknown, and the player designed the level and knew
   every landing before starting.

2. **A real usability finding, deliberately not fixed.** The retry feels fast, but the death
   card *"flashes past"* — the gist arrives, there is no time to read it properly. Both death
   messages are correct and machine-checked; neither is comfortably legible at 0.55 s. Left as a
   named design tension (TEST-REPORT §4 cycle 4) rather than trading a confirmed strength for a
   rushed fix hours before submission. Two candidate fixes that do not touch the timing are
   recorded for whoever picks it up.

3. **The walkthrough is partial by one feature.** `pause-on-focus-loss` is implemented and
   machine-checked, but an unattended capture cannot lose window focus. It is recorded as
   `implemented` with **empty evidence** rather than relabelled `planned` to force a pass, so the
   skill's coverage check **fails on that one item by design**. A diagnostic run excluding it
   returns PASS: 16 implemented features, 16 evidence intervals, 5 planned.

4. **The fork-pad take-off window is calculated, not measured** — roughly 46 px of run-up. It was
   cleared first try by a human, which says it is not brutal, but that is an anecdote from the
   person who placed the platform, not a measurement. The sweep that would settle it is the
   prompt the film hands the viewer.

5. **The film's gameplay predates the playtest.** The capture is from 2026-09-23; the playtest
   was the next day. The Verdict beat was re-authored and re-rendered on 2026-09-24 so the film
   states this itself rather than carrying a sentence that had stopped being true. No gameplay
   was re-captured.

6. **The starter ships with no licence.** Extending unlicensed code is legally ambiguous. Done
   here because the assignment directs it, the original author is the instructor, and the
   starter is credited and preserved unmodified. My `LICENSE` (MIT) is scoped explicitly to my
   own additions and grants nothing over the starter. See SOURCES §2a.

7. **Windows only.** The starter reports macOS results; its macOS launcher was not re-verified.
   No cherries, audio, settings/remapping, moving platforms or Web export — out of scope, as in
   the starter.

---

## Pre-submission checklist

- [x] Runs from source on Godot 4.7.2 (`godot --path godot`), no script errors
- [x] Starter credited in README, SOURCES, `LICENSE` and in git history as an unmodified baseline commit
- [x] `CHANGE-BRIEF.md` written before implementation; §1–§5 unedited, revisions appended in §6
- [x] `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md`, `LICENSE` present
- [x] Licences identified for code, art, audio and film assets (SOURCES §2a)
- [x] Style guides stated: Godot GDScript guide, PEP 8 (SOURCES §2b)
- [x] Student-vs-AI code share estimated and measured (SOURCES §4a)
- [x] Caches and credentials excluded (`.godot/`, `.claude/`, `.env`); no MP3/MP4; nothing > 25 MB
- [x] Human playtest recorded (TEST-REPORT §5, FRICTIONAL §9)
- [x] Film rendered with the Brutalist workflow, frames inspected across the whole export
- [x] Film verified to depict the submitted game source (`build_id` compared, drift enumerated)
- [x] Repository pushed, public; reviewer access tested by **anonymous clone**, suite re-run against it
- [x] Film uploaded to Google Drive; **anonymous download verified and SHA-256 matched byte for byte**
- [ ] Canvas zip built as `Li_Zhaohui_CSYE7270_Assignment_1.zip` (excludes `.git`, `.godot`, media)
- [ ] Final commit SHA pasted into Canvas and into this file's header
