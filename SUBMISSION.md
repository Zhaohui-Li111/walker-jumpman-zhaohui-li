# Submission note

**Assignment:** Assignment 1 — Extend Walker Jumpman
**Student:** Zhaohui Li (li.zhaohui@northeastern.edu)
**Project name:** walker-jumpman-zhaohui-li
**GitHub repository/folder URL:** *(pending — repository not yet pushed; see §Blocked below)*
**Submitted commit SHA:** *(read from `git rev-parse HEAD` after the final commit and paste here and into Canvas — a commit cannot contain its own SHA)*
**Game-source revision shown in the film:** `adc7f4e` — *Record evidence: rerendered screens and machine-check receipts*
**Godot version and operating system:** Godot `4.7.2.stable.official.ed1daf0bf`, Compatibility/OpenGL · Windows 11 Home China (10.0.26200)
**Final film URL and filename:** *(pending — see §Blocked)*
**Final film SHA-256:** *(pending)*

---

## Summary of my changes

Extended the walker-jumpman "First Steps" starter by Nik Bear Brown
(https://github.com/nikbearbrown/walker-jumpman), recorded in this repository's history at
commit `7f412c8` **unmodified**, so every later commit is a readable diff of my own work.

**Character.** Replaced the starter's blue rectangle figure with **BEACON**, a signal-courier
automaton: domed head, visor band with a single cyan eye slot, and a cargo pack plus swept fin
on the trailing side that flip across the body when you turn, so facing reads from the outline
alone at 18 px wide. Readable in six states (facing L/R × standing, rising, falling), with legs
that close on the way up and brace on the way down, a squinting visor while falling, and a chest
lamp that lights cyan only while airborne.

This is a `_draw()` rewrite. `tuning.gd`, the 18 × 28 collider, the collision layers and
`_physics_process` are untouched — evidenced by the `low-ceiling` check reporting
`300.000274658203` both before and after the swap, bit-identical. Every drawn pixel stays inside
the collider in every state; the one deliberate inward exception (a 2 px boot lift during a
grounded walk stride, never airborne) is documented and cannot occur at a moment that could
mislead a hazard read.

**Level.** Widened 960 → 1600 and moved the finish 916 → 1548, so the original route alone can
no longer win. Zones 01–02 are byte-identical in the level data and still walkable. Added
**Zone 03 "Pick your line"**: a 56 px entry jump onto a fork pad, then a genuine choice between
a **low road** (spike cluster to jump, then a 64 px pit) and a **high line** (a step and two
ledges, no hazard, three jumps, ending by running off an overhang onto the finish pad). Four new
landings require jumps. The trade is hazard exposure against jump precision, it is reversible,
and the two lines complete within 0.05 s of each other.

**Presentation.** The starter hard-codes drawing coordinates the level data does not control, so
extending the level required making them data-driven or the new zone would have been painted
wrong: backdrop, grid extent and hills now derive from `level.width`/`level.hills`; the spike
baseline comes from the hazard rect instead of a literal `y=320`; the flag pole stands on the
finish rect; zone labels moved into the level JSON; and the HUD progress bar derives its span
from spawn → finish instead of the constant `852`.

**Verification.** 31 mechanics checks and 9 keyboard checks, 0 failures, on Godot 4.7.2.
A baseline was captured on the untouched starter before any edit. All 25 starter checks remain
at their original tolerances; 6 were added. No assertion was deleted and no expected value
weakened. Runs that failed are retained in `evidence/` alongside the ones that passed, including
the predicted route-fixture break and a real bug found while building: a first draft of Zone 03
stacked the two routes, and the low road's jump clipped the ledge overhead, cutting a 56 px jump
to 17 px. Diagnosed with a tick-by-tick trace, fixed by redesigning geometry (not tuning), and
pinned by a regression check.

---

## Known limitations

1. **No human playtest recorded.** Every playability claim is machine evidence only.
   TEST-REPORT §5 and FRICTIONAL §9 are deliberately empty rather than filled with invented
   feedback. An automated input route proves reachability, not playability.
2. **The explainer film is not produced** — blocked, see below.
3. The fork-pad entry jump is the tightest input in the level (≈46 px run-up window);
   that figure is calculated, not measured.
4. Nothing checks label placement; one overlap was caught only by looking at a screenshot.
5. Windows only; the starter's macOS launcher was not re-verified.
6. No cherries, audio, settings/remapping, moving platforms or Web export — out of scope, as in
   the starter.

---

## Blocked

Two required deliverables are not complete, and are reported as incomplete rather than
substituted:

**The Brutalist explainer film.** The course-provided `godot-walkthrough` skill (original
spelling `godot-waikthrough`) is **not installed on this machine**. Verified by searching
`~/.claude/` (no `skills/` directory), `~/.claude/plugins/`, and the course tree for
`brutalist`, `walkthrough` and `waikthrough` — no match. The assignment says to request the
course-provided version rather than proceed. No substitute workflow was used, because producing
a video another way and calling it a Brutalist explainer would misrepresent the workflow.
`film/BEAT-SHEET.md`, `film/SCRIPT.md` and `film/EVIDENCE-INDEX.md` are written and the render
is the only remaining step.

**The human playtest.** Mine, to do; not delegable.

---

## Pre-submission checklist

- [x] Runs from source on Godot 4.7.2 (`godot --path godot`), no script errors
- [x] Starter credited in README, SOURCES and in git history as an unmodified baseline commit
- [x] `CHANGE-BRIEF.md` written before implementation and not rewritten
- [x] `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md` present
- [x] Caches and credentials excluded (`.godot/`, `.claude/`, `.env`); no MP3/MP4; nothing > 25 MB
- [ ] Human playtest recorded in TEST-REPORT §5 and FRICTIONAL §9
- [ ] Film rendered with the Brutalist workflow, watched end to end, filename + SHA-256 recorded
- [ ] Repository pushed; reviewer access to source and media tested
- [ ] Fresh clone of the submitted revision re-run and re-verified
- [ ] Final commit SHA pasted into Canvas and into this file's header
