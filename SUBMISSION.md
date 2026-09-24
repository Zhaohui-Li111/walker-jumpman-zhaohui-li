Assignment: Assignment 1 - Extend Walker Jumpman

Student: Zhaohui Li (li.zhaohui@northeastern.edu)

Project name: walker-jumpman-zhaohui-li

GitHub repository/folder URL: https://github.com/Zhaohui-Li111/walker-jumpman-zhaohui-li

Submitted commit SHA: see the Canvas note — a commit cannot contain its own SHA.
Read it with `git rev-parse HEAD` on the submitted revision.

Game-source revision shown in the film: `cc8ae01` (`build_id` `0be6756a…3bf9`, the id
recorded in the film's `coverage.json`). The submitted source differs in **6 of 30 files and
none are gameplay**: reopening the project in the Godot editor re-normalised `project.godot`
(removing two lines equal to engine defaults) and generated five `.uid` files. Every gameplay
file is byte-identical and the suite still passes. Enumerated in
`youtube/claude-liam-walker-jumpman-zhaohui-li-walkthrough/CAPTURE.md`.

Godot version and operating system: Godot 4.7.2.stable.official.ed1daf0bf, Compatibility/OpenGL
· Windows 11 Home China (10.0.26200)

Final film URL and filename:
https://drive.google.com/file/d/1zgNUQ5ItB9XI64Gouuah-qUQD21IpmS8/view?usp=drive_link ·
`claude-liam-walker-jumpman-zhaohui-li-walkthrough.mp4`

Final film SHA-256: `09bfdfc689362efe6830f05ae8c2abe6c934a8ba5e4720eef55d62cecd7882b3`
(3840×2160, 30 fps, 145.07 s, 14.7 MB. Downloaded from the link above with no credentials and
hashed — byte-identical to the master, so Drive did not re-encode.)

Summary of my changes:

Extends the walker-jumpman "First Steps" starter by Nik Bear Brown, preserved unmodified at
commit `7f412c8` so every later commit is a readable diff of my own work.

- **Character.** Replaced the starter's blue rectangle with **BEACON**, a courier automaton —
  domed head, visor with one cyan eye slot, and a cargo pack and swept fin on the trailing side
  that flip when you turn, so facing reads from the outline alone at 18 px wide. A `_draw()`
  rewrite only: `tuning.gd` diff is empty, the 18×28 collider is untouched, and `low-ceiling`
  reports `300.000274658203` before and after — bit-identical. No drawn pixel leaves the
  collider in any of six states.
- **Level.** Widened 960 → 1600 and moved the finish 916 → 1548, so the original route alone can
  no longer win; Zones 01–02 stay byte-identical and walkable. Added **Zone 03 "Pick your line"**:
  a 56 px entry jump onto a fork pad, then a choice between a **low road** (spikes, then a 64 px
  pit) and a **high line** (a step and two ledges, no hazard, ending by running off an overhang
  onto the finish pad). Four new landings require jumps; the two lines finish 0.05 s apart.
- **Presentation.** Made the starter's hard-coded drawing data-driven — backdrop, grid, hills,
  spike baseline, flag pole and zone labels now follow the level file, and the HUD progress bar
  derives its span from spawn → finish instead of the constant 852.
- **Verification.** 31 mechanics + 9 keyboard checks, 0 failures, re-run from an **anonymous
  clone of GitHub** and from the submitted zip. Baseline captured before any edit; all 25
  starter checks kept at original tolerances, 6 added, none deleted or weakened. Failing runs
  retained in `evidence/`.
- **Film.** *Walker Jumpman, Extended*, 2:25, native 4K, Brutalist `godot-waikthrough` in
  `walker` mode. Real engine capture driven by real key events, labelled SCRIPTED INPUT on every
  frame. Gate V 0 BLOCKER / 0 MAJOR, GATE T PASS.

Known limitations:

1. **Playtested by the author only** (three sessions, 2026-09-24: high line, low road, then
   deliberate deaths). **No naive player has seen it**, so whether the fork reads as a *choice*
   to a stranger is unknown.
2. **A usability finding left unfixed:** the retry feels fast, but the death card "flashes past"
   — the gist arrives, there is no time to read it properly. Recorded as a design tension
   (TEST-REPORT §4 cycle 4) rather than trading a confirmed strength for a rushed fix.
3. **The walkthrough is partial by one feature.** `pause-on-focus-loss` cannot be filmed by an
   unattended capture, so the skill's coverage check **fails on it by design** — it was not
   relabelled to force a pass. Excluding it, the same verifier returns PASS.
4. **The fork-pad take-off window is calculated (~46 px), not measured.** Cleared first try by a
   human, which is an anecdote from the person who placed the platform, not a measurement.
5. **The film's gameplay predates the playtest.** The Verdict beat was re-rendered on 2026-09-24
   so the film says this itself; no gameplay was re-captured.
6. **The starter ships with no licence.** My `LICENSE` (MIT) is scoped to my own additions and
   grants nothing over the starter. See SOURCES §2a.
7. Windows only; the starter's macOS launcher was not re-verified. No cherries, audio, settings,
   moving platforms or Web export — out of scope, as in the starter.

---

Supporting documents in the repository: `README.md` (run instructions, controls, changes),
`CHANGE-BRIEF.md` (predictions, written before implementation, revisions appended in §6),
`TEST-REPORT.md` (baseline, every run including failures, revision cycles), `FRICTIONAL.md`
(honest log), `SOURCES.md` (credits, licences §2a, style guides §2b, student-vs-AI code share
§4a), `LICENSE`, and the film reel under `youtube/`.
