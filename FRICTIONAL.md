# FRICTIONAL — honest log

**Project:** walker-jumpman-zhaohui-li · **Student:** Zhaohui Li · **Date:** 2026-09-23

How to read this file: entries are in the order they happened. Each says what was
attempted, what was expected, what actually happened, and what changed as a result.
Where a claim can be checked, the commit, receipt file or command is named.

**Attribution convention used throughout:** *Human* = Zhaohui Li. *AI* = Claude Code
(Opus 5), used as an interactive assistant in one working session. Where a decision
and its implementation had different authors, both are named.

> **Section 9 is not yet written.** It is the human playtest, and it is the one thing
> in this project that an assistant cannot produce. It is left visibly empty rather
> than filled with plausible-sounding text.

---

## 1. Orientation, before writing anything

**Attempted.** Read the starter before proposing changes: `README.md`, `BUILD-REPORT.md`,
`player.gd`, `session.gd`, `hud.gd`, `first_steps.json`, all four test scripts, `project.godot`.

**Expected.** That the character would be a sprite or scene I could swap out.

**What actually happened.** It is not. `player.gd::_draw()` builds the whole figure from
seven `draw_rect` calls in code, and the collider is created in `_ready()` rather than in a
scene file. So "replace the character" means "rewrite a drawing function without touching the
body it is drawn around" — a much tighter constraint than swapping an image, and the reason
the collider-overlay check in §4 exists at all.

Also found: several drawing coordinates in `session.gd` are literals that the level JSON does
not control (`Rect2(-400,-200,1800,900)`, `range(0,961,32)`, hills at `[100,470,770]`, spike
baseline pinned to `y=320`, three `draw_string` calls at fixed positions), and `hud.gd` computes
progress as `(x-64)/852`, where 852 is the old finish minus the spawn. The assignment warns
that moving data alone will not move the picture; this is exactly where that bites.

**Human / AI.** AI read the files and reported the constraints. Human set the scope.

---

## 2. Baseline first, because "I didn't break it" needs a before

**Attempted.** Run both test suites on the untouched starter before editing a single line.

**Result.** 25/25 and 9/9, engine `4.7.2.stable.official.ed1daf0bf`.
Receipts: `evidence/mechanics-1790192843.449.json`, `evidence/keyboard-1790192851.968.json`.
Reference numbers kept for later comparison: jump rise **56.0747 px**, `low-ceiling` minimum
feet **300.000274658203**.

**Learned.** Worth the two minutes. Those two numbers are what later let me say the character
swap changed nothing, instead of merely believing it.

**Human / AI.** Human decided to baseline first. AI ran the commands.

---

## 3. Predictions written before implementation

`CHANGE-BRIEF.md` was written before any edit and has not been rewritten since. Four failure
cases were predicted. Scoring them honestly afterwards:

| # | Prediction | Outcome |
|---|---|---|
| F1 | Route fixture breaks and dies at the old level edge | **Correct, and correct about the mechanism.** `jump_marks_used: 5`, died at x≈1046. |
| F2 | A new jump might not be reachable because the closed-form arithmetic ignores 60 Hz integration | **Wrong in the direction predicted.** Discrete stepping *overshoots* (56.07 px actual vs 53.3 px predicted), so jumps were easier, not harder. The reachability problem I did hit had nothing to do with arithmetic — see §6. |
| F3 | Character art will poke outside the 18×28 collider, worst at the cargo pack and the domed head | **Correct as a risk, avoided by the method.** Authoring everything in a mirrored "facing-right" space and rendering the collider in red caught it immediately. The head radius did have to be held at 5.2 px centred at y=−22.6 to top out at −27.8. |
| F4 | Relocated finish reachable but unreadable; flag pole hard-coded to y=320 | **Correct that it was a risk, and the fix was needed.** The pole now stands on `finish[1]+finish[3]`. But the readability problem that actually occurred was a *label* overlapping the jump arc, which I had not predicted. |

**Learned.** Three of four predictions were useful, and the one that was wrong (F2) was wrong
in a comforting direction, which is its own lesson: I budgeted with the pessimistic number and
it cost nothing. The real bug was in a category I had not imagined at all.

---

## 4. Character replacement — went smoothly, and here is how I know

**Attempted.** Replace the blue rectangle figure with BEACON, a courier automaton, changing
`_draw()` only.

**Expected.** Fiddly. 18×28 px is very little room, and the assignment wants left/right/standing/
jumping all to read.

**What actually happened.** It went in largely first try, which I am recording plainly rather
than inventing struggle. Two things made it easy:

1. Authoring every shape in a "facing right" coordinate space and mirroring through two small
   helpers (`_rr`, `_pp`), so left-facing is not a separate hand-tuned set of magic numbers.
2. Writing `tests/capture_character.gd` **before** trusting the result: it settles a real body
   on a real floor (so `is_on_floor()` is genuinely true), freezes it, and renders six states
   at 5× with the exact collider drawn over the top in red.

**Two things did go wrong, both caught by that harness rather than by reading the code:**

- The pose fixture asserted `is_on_floor()` and failed. Cause: `player.gd::_physics_process`
  clamps `position.x = maxf(position.x, 10.0)`, and I had staged the fixture at x = −600, so
  every body was teleported to x=10 and slid off its fixture floor. Fixed by staging at x=200.
  A real constraint in the starter that I would not have found by reading.
- The two boots met at x=0 and read as one slab. Narrowed each from 6 px to 5 px.

**Verification.** `mechanics-1790193254.788.json`: 25/25, and `low-ceiling` reports
`300.000274658203` — **bit-identical to the baseline**. `tuning.gd` is untouched in the diff.

**Human / AI.** Human chose the concept (courier automaton; amber/plum/cyan; pack-and-fin for
facing) and the hard rule that no drawn pixel may leave the collider. AI wrote the drawing code
and the pose harness. Human accepted the result after looking at the contact sheet.

---

## 5. Level extension, first draft — and the predicted break

**Attempted.** Widen 960 → 1600, move the finish 916 → 1548, add Zone 03 as a fork.

**Result.** Exactly the predicted F1 failure (`mechanics-1790193396.732.json`, 25 checks / 1 failure).

**What I chose not to do.** The fast way to green was to raise the 900-tick budget or drop the
`deaths == 0` requirement. Both would have produced a passing report about nothing. Extended the
fixture instead, and documented every new mark and the jump it triggers in TEST-REPORT §3.

**Human / AI.** Human refused the shortcut and set the rule "revise geometry, never tuning."
AI implemented the fixture split.

---

## 6. The bug I did not predict, and how it was actually found

**Attempted.** First Zone 03 draft: a low road at y=320 with a spike cluster, and two floating
ledges at y=256 directly above it. The idea was that falling off the high line would drop you
into the hazard you were avoiding — a tidy cause-and-effect for the film.

**Expected.** Both lines complete.

**What actually happened.** `complete-real-route-high` passed; `complete-real-route-low` failed,
dying on the spikes at x≈1273 with `jump_marks_used: 7` — so the jump input *had* fired.

**What I did about it.** I could not explain it from the observation, and I did not want to
guess, so I wrote `godot/tests/probe_route.gd` to print the real body tick by tick. The trace:

```
JUMP #7 at x=1243.5 y=314.6 vx=160.0
t=450 x=1248.9 y=304.7 floor=false
t=456 x=1264.9 y=302.7 floor=false      <- still only 17 px up, should be ~45
ENDED state=3 at x=1272.9 y=307.5
```

The jump rose **17 px instead of 56**. BEACON was hitting its head on the underside of the ledge
above. The arithmetic: the body is 28 px tall and jumps 56 px, so a jump needs **84 px** of
headroom; high ledge A's underside sat 48 px above the low road. My "tidy cause-and-effect"
design was geometrically impossible for the route it was supposed to make interesting.

**Learned.** Two things, and the second is the one I will actually remember.

1. In a side-scroller, *vertical* route separation silently imposes a headroom budget on the
   lower route. Two-dimensional level data does not warn you about this; only running it does.
2. The failing check told me *that* it failed and roughly where. It could not tell me *why*,
   and the difference between those two mattered enough to justify writing a throwaway
   diagnostic. Guessing would have had me adjusting jump marks — plausible, and wrong.

**Response.** Redesigned so no ledge overhangs a jump arc: the high line now climbs via an
intermediate step to y=216, leaving **92 px** of clearance over the low road against the 84 px
requirement. Added `low-road-jump-not-clipped-by-high-line`, which witnesses the real apex of
the real body and asserts the full 56 px rise, so this exact mistake cannot return quietly.

**What I gave up.** The original "miss the high line, land in the spikes" moment is gone; the
gap between the ledges now drops you onto safe road. I preferred a reachable level to a
narratable one. The fork still has distinct consequences — spikes and a pit on the low road, a
long fall into the pit off the end of the high line.

**Human / AI.** AI proposed the stacked first draft. AI also found and diagnosed the bug. Human
made the call to redesign the geometry rather than lower the ledge count or weaken the check,
and accepted losing the narrative beat.

---

## 7. Something I found that was not mine, and checked before touching

`git diff` against the starter showed `godot/project.godot` modified, which surprised me because
I had not opened it. Opening the project in the Godot editor (which had happened before this
session — `.godot/` was already present) rewrites the file and had removed two lines:
`window/stretch/aspect="keep"` and `physics/common/physics_ticks_per_second=60`.

**Expected.** That this was a real regression: stretch aspect affects letterboxing, and physics
tick rate would invalidate every timing number in this report.

**What I did.** Did not assume either way. Ran a `ProjectSettings` probe in the real engine:

```
aspect=keep   stretch_mode=canvas_items   phys_ticks=60   engine_phys_ticks=60
```

Both removed lines were engine defaults, so Godot had simply normalised the file and runtime
behaviour is unchanged. Restored the explicit lines anyway (commit `ebb9604`) so a reviewer
diffing against the starter sees no unexplained engine-config change — and noted in TEST-REPORT
§6 that a fresh clone's first editor open will drop them again.

**Learned.** "Modified file I didn't touch" is worth ninety seconds of actual measurement.
Had `physics_ticks_per_second` genuinely changed, every tick count in this report would have
been wrong.

---

## 8. Version history was reconstructed deliberately

I had already made edits before initialising git. Rather than commit one undifferentiated blob,
I extracted the original `walker-jumpman-main.zip` and committed the **pristine starter first**
(`7f412c8`), then replayed my work on top of it in four topical commits. Every line of my own
work is therefore a readable diff against the starter, which is the whole point of the credit
requirement.

Recorded plainly because it is a rewrite: the commit *timestamps* are all from one session and
do not reflect the order in which I originally typed things. The commit *contents* and the
evidence receipts do, and the receipts are timestamped independently
(19:47 → 19:54 → 19:56 → 19:58 → 20:03 → 20:07).

---

## 9. Human playtest — done, and thinner than I wanted

**2026-09-24.** Played the build at `cc8ae01` with a keyboard, in a normal game window.

**What I reported, in full:** *"我试玩了，没有问题，可以通关"* and, when asked which route and
whether the fork-pad jump gave me trouble, *"我一次就过，走的上面的路"* — cleared it on the
first try, took the high line.

**What I learned:**

1. The level is completable by a person, not just by the driver. That was the one thing a
   scripted route genuinely could not tell me.
2. **The fork-pad entry jump went first try.** This is the input I have been most worried about
   since writing the brief — the one with a *calculated* ~46 px take-off window that I never
   measured. Clearing it cold, without retries, says the window is not brutal.

**Why I am not calling #2 settled.** One success, by the person who placed the platform and knew
exactly where to jump from, is evidence that the jump is *possible under ideal knowledge*. It is
not a measurement of the window, and it is not a test of whether a stranger finds the take-off
point. The number stays "calculated, never measured" in the report, because that is what it is.

**What this session exposed that I had not thought about.** I took the high line — which meant
**nobody had played the low road.** The spikes, the 64 px pit and the "Missed the landing"
recovery were covered by machine checks and appeared in the film, but half of the fork I
designed as a genuine choice had never been experienced by a human being. I only noticed
because I was asked which route I took. If I had written "no problems, completed it" and
stopped, that gap would have gone straight into the submission unrecorded.

**Gap closed the same day.** I went back and played the low road: *"低路我也玩了，没啥问题"* —
played it too, no real problems. Both halves of the fork have now been played by a person. The
second spike cluster is jumpable at speed and the 64 px pit is crossable by hand, not just by
the driver.

**Still untested, and I want it on the record rather than buried:** across both sessions I
**died zero times**. So no human has ever seen the retry loop. The ~0.55 s recovery I keep
describing as "cheap", and the two distinct death messages I make a design point of in the film
("Watch the spikes" vs "Missed the landing"), are still entirely machine evidence. I have
verified they are *correct*; I have never verified they *feel* right, which is the only thing a
playtest was supposed to add.

There is a mild irony here worth naming: I designed a level around failure and retry, then
tested it twice without failing once.

**The deeper problem with this playtest:** I built the level. I knew where every landing, hazard
and pit was before I pressed Enter. I cannot test whether the fork reads as a choice, because I
already knew it was one. Completing a level you designed proves the geometry works; it proves
nothing about legibility.

**What I would do next, in order:**

1. **Die on purpose, once on each hazard.** Two minutes, and it is the last thing in the level
   I have verified only by machine. Walk into the spikes, walk off into the pit, and find out
   whether half a second actually feels like "just another try" or like being yanked backwards.
2. Hand it to one person who has never seen it, say nothing, and watch where they die and which
   line they take. That is the only way to learn whether the fork reads as a choice — I played
   both routes deliberately, one after the other, which is not the same as choosing one.
3. Run the take-off-window sweep — the prompt the film hands the viewer — so the fork-pad jump
   becomes a number instead of a first-try anecdote.

**Human / AI.** Entirely human: the AI did not play the game and does not claim to have. It
recorded this session in my words and wrote down what the session does not cover, rather than
expanding one sentence into a report I did not give it.

---

## 10. Unresolved questions

1. **Is the fork-pad entry jump fair?** My arithmetic puts the usable take-off window at roughly
   46 px of run-up (≈0.29 s). That is calculated, not measured, and is the tightest single input
   in the level. A person may find it fussy.
2. **Does the fork read as a choice in motion?** Standing still on the pad, both lines are
   visible. Running at 160 px/s into a new zone, the player may simply take whichever line their
   momentum points at and never notice they chose.
3. **Is the high line actually worth taking?** 562 vs 565 ticks means the two lines are within
   0.05 s of each other. That is balanced, but "balanced" and "interesting" are not the same, and
   I do not yet know whether players will feel a reason to try the other one.
4. **Nothing checks label placement.** Cycle 2 in TEST-REPORT §4 was caught by looking at a
   screenshot. A level edit could re-introduce that overlap and every test would still pass.

---

## 11. Contributions, explicitly

**Human (Zhaohui Li)**
- Scope and the constraint that tuning, collider and controls were off-limits.
- Character concept: a courier automaton; the pack-and-fin silhouette as the facing cue; the
  amber / plum / cyan palette against the starter's cool world.
- The rule that no drawn pixel may leave the collider, which drove the whole verification method.
- Zone 03's design intent: a reversible fork trading hazard exposure against jump precision.
- The decision, at §6, to redesign geometry rather than weaken a check or a tuning value — and
  to accept losing the "fall into the spikes" narrative beat as the cost.
- Refusing the tick-budget shortcut at §5.
- Ownership of the playtest (§9) and of every judgment about whether this is any good.

**AI (Claude Code, Opus 5)**
- Read the starter and reported the hard-coded coordinates and the in-code collider.
- Wrote `_draw()` for BEACON, the mirroring helpers, and `capture_character.gd` / `character_board.gd`.
- Wrote the Zone 03 geometry, made `session.gd` and `hud.gd` data-driven, split the route fixture.
- Wrote `probe_route.gd` and diagnosed the head-clip bug from its trace.
- Ran every command and produced every receipt in `evidence/`.
- Drafted this file and TEST-REPORT.md from the actual session record.

**Accepted from the AI:** the mirroring-helper approach, the data-driven drawing refactor, the
headroom regression check, and the diagnosis in §6.

**Rejected / overridden:** the stacked first draft of Zone 03 (redesigned); the temptation to
widen the route tick budget (refused); leaving the normalised `project.godot` alone (restored
instead, after measuring).

**Modified:** the character silhouette was tightened after looking at the contact sheet (boots);
the Zone 03 labels were moved after looking at a render; the fork-pad gap was reduced from 72 px
to 56 px after working out that the original take-off window was about 31 px wide.

**Not AI-authored:** §9, when it is written.
