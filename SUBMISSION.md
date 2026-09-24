# Submission note

**Assignment:** Assignment 1 — Extend Walker Jumpman
**Student:** Zhaohui Li (li.zhaohui@northeastern.edu)
**Project name:** walker-jumpman-zhaohui-li
**GitHub repository/folder URL:** *(pending — repository not yet pushed; see §Blocked below)*
**Submitted commit SHA:** *(read from `git rev-parse HEAD` after the final commit and paste here and into Canvas — a commit cannot contain its own SHA)*
**Game-source revision shown in the film:** `cc8ae01` — verified: the `godot/` tree hashes to `build_id` `0be6756a1c222cf89964287272c5d6659111e6f50d2bb2f01969e8d03f963bf9`, which is the id recorded in the film's `coverage.json`, and `godot/` is unchanged in every commit after it
**Godot version and operating system:** Godot `4.7.2.stable.official.ed1daf0bf`, Compatibility/OpenGL · Windows 11 Home China (10.0.26200)
**Final film URL and filename:** *URL pending upload to course media storage* · `claude-liam-walker-jumpman-zhaohui-li-walkthrough.mp4`
**Final film SHA-256:** `952ac415a4cd0d2eb6d06d5fe10e76d41e6433eaef5a88ed07047ef95221ea25`
**Final film spec:** 3840 × 2160, 30 fps, h264 + AAC 48 kHz stereo, 135.57 s (2:16), 14.4 MB

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

1. **Playtested by the author only** — three sessions on 2026-09-24, recorded verbatim in
   TEST-REPORT §5 and FRICTIONAL §9: high line (fork-pad entry jump cleared first try), low
   road, then deliberate deaths on each hazard. The third session found the one genuine
   usability issue in this project: the retry feels fast, but the death card flashes past —
   the gist arrives, there is no time to read it properly. Left unchanged as a deliberate
   trade (TEST-REPORT §4 cycle 4), because lengthening the hold would cost the retry speed a
   person had just confirmed. Still untested: **first-time legibility** — the player designed
   the level, so whether the fork reads as a choice to a stranger is unknown, and the fork-pad
   take-off window remains *calculated* at ~46 px rather than measured. No naive playtester
   recruited.
2. **The explainer film is not produced** — blocked, see below.
3. The fork-pad entry jump is the tightest input in the level (≈46 px run-up window);
   that figure is calculated, not measured.
4. Nothing checks label placement; one overlap was caught only by looking at a screenshot.
5. Windows only; the starter's macOS launcher was not re-verified.
6. No cherries, audio, settings/remapping, moving platforms or Web export — out of scope, as in
   the starter.

---

## The film

Built with the course-provided Brutalist toolkit — `skills/make/godot-waikthrough` in `walker`
mode, following its own instructions and the specs it requires. 12 beats: reconstructed Walker
ask → hesitant-writer BLUF → six gameplay beats → a cause-and-effect beat on the level map →
Verdict → Your Turn → the locked spoken outro.

Gameplay is a native 3840 × 2160 Godot Movie Maker capture driven by **real `InputEventKey`
events** — no teleports, no completion-setting, no test-only shortcuts. The driver asserts all
13 phases and quits nonzero on failure; the submitted run passed with zero failed expectations
over 1812 physics ticks. Every gameplay frame carries a burned-in **SCRIPTED INPUT · not a human
playtest** label.

Gates on the submitted export: **Gate V 0 BLOCKER / 0 MAJOR** (24 frames), **GATE T PASS**, and a
`.verified.json` receipt whose SHA-256 matches the delivered file.

**The skill's coverage check fails on exactly one item, by design:** `pause-on-focus-loss` is
implemented and machine-checked but cannot be filmed by an unattended capture. It is recorded as
`implemented` with empty evidence rather than relabelled `planned` to force a pass. A diagnostic
run of the same verifier with that one feature excluded returns `PASS` — 16 implemented features,
16 evidence intervals, 5 planned. Stated on screen in the Verdict beat.

One line of the course toolkit was patched (`remotion_scenes.py`, `npx` → `shutil.which("npx")`,
a Windows-only exec bug that made every bookend beat fail). Two other toolkit bugs were hit and
deliberately not patched. All three are in the reel's `BUILD-LOG.md`.

## Still outstanding

**The human playtest.** Mine, to do; not delegable. `TEST-REPORT.md §5` and `FRICTIONAL.md §9`
are deliberately empty until it happens, and every playability claim in this submission is
machine evidence only until then.

---

## Pre-submission checklist

- [x] Runs from source on Godot 4.7.2 (`godot --path godot`), no script errors
- [x] Starter credited in README, SOURCES and in git history as an unmodified baseline commit
- [x] `CHANGE-BRIEF.md` written before implementation and not rewritten
- [x] `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md` present
- [x] Caches and credentials excluded (`.godot/`, `.claude/`, `.env`); no MP3/MP4; nothing > 25 MB
- [x] Film rendered with the Brutalist workflow; frames inspected across the whole export; filename + SHA-256 recorded above
- [x] Film verified to depict the submitted game source (`build_id` match, not just a claim)
- [ ] Human playtest recorded in TEST-REPORT §5 and FRICTIONAL §9
- [ ] Film uploaded to course media storage; URL filled in above and in README
- [ ] Repository pushed; reviewer access to source and media tested
- [ ] Fresh clone of the submitted revision re-run and re-verified
- [ ] Final commit SHA pasted into Canvas and into this file's header
