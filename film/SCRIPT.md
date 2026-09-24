> **SUPERSEDED planning note.** Written before the Brutalist skill was available, when the film was blocked. The film as actually built lives in `youtube/claude-liam-walker-jumpman-zhaohui-li-walkthrough/`. See [film/README.md](README.md) for what changed and why. Kept as an honest record of the plan, not as a specification.

# Narration script — walker-jumpman-zhaohui-li explainer

Draft for the Brutalist `godot-walkthrough` workflow, `walker` modifier.
Beats 1, 15–18 (Walker opening, Walker summary, Verdict, Your Turn, outro) are **owned by the
skill's template** and are not drafted here — the skill supplies their wording. What follows is
the body.

**Narration:** AI voice (Liam or equivalent) is permitted and is what this is written for.
The film states on screen that narration is AI-generated.

**Before recording:** re-confirm every number below against the receipts on render day, and
update beat 12 to say whatever is actually true about the human playtest at that point.

---

### 2 — What this is  *(over the starter zone, then live play)*

This is not a new game. It is an extension of **walker-jumpman**, a small platformer by
Nik Bear Brown. The starter gives you two steps, two gaps, one spike hazard, a finish flag,
and a blue rectangle person who can jump exactly once.

I kept the feel and changed two things: who you are, and where the level ends.

### 3 — The character  *(contact sheet on screen)*

This is BEACON, a signal-courier automaton.

The starter's figure is a flat-topped box. BEACON has a domed head, a visor band with a single
cyan eye slot, and a cargo pack and swept fin that ride the trailing side and flip across the
body when you turn — so at eighteen pixels wide you can tell which way it is facing from the
outline alone, before you see the eye.

What you are looking at now is a **fixture render, not gameplay**. Six poses, frozen on purpose,
side by side. The red rectangle is the actual collision box: eighteen by twenty-eight pixels,
feet at the origin.

### 4 — Cause and effect: the collider did not change  *(code, then receipts)*

Here is why that red rectangle matters.

The starter creates the collider in `_ready` and draws the figure in `_draw`. I rewrote `_draw`
completely and did not touch `_ready`, `_physics_process`, or the eight tuning values.

So this is a claim I can check rather than assert. The test suite drives the player under a low
ceiling and records how high the body actually gets. Before my change, that number was
three hundred point zero zero zero two seven four six five eight two zero three. After replacing
the entire character, it is **the same number, digit for digit**.

Different character. Identical physics. That is the whole point of drawing the collider in red:
the silhouette is not allowed to promise space the body does not have.

### 5 — The extension  *(live play)*

The level was nine hundred and sixty pixels wide and finished at nine-sixteen. It is now sixteen
hundred wide and finishes at fifteen forty-eight — so the original route, on its own, can no
longer win. Zones one and two are unchanged in the level data, and still walkable.

Here is the new gap. Fifty-six pixels across, thirty-two up. Clear it and you land on the
**fork pad**, where the level splits.

### 6 — The decision  *(live play, low road)*

From the pad you can see both lines.

The **low road** is the fast one. Drop right, run, and there is a spike cluster you have to jump
at speed — and then a sixty-four pixel pit before the finish pad. Flat targets, wide landings,
two real ways to die.

### 7 — The other line  *(live play, high line)*

Or take the **high line**. A step, then two ledges. No hazard on it at all — but three jumps onto
raised targets instead of two onto flat ones.

It pays off at the end. The last ledge overhangs the finish pad, so you do not jump down; you
run off the edge and land. You buy that free descent with an extra climb.

The two lines complete within five hundredths of a second of each other. Neither is the right
answer. The trade is hazard exposure against jump precision, and you can climb back onto the pad
if you change your mind — a fork that punishes curiosity is a bad fork.

### 8 — Failure and recovery  *(live play, real death)*

Miss the pit and you get this. No lives, no menu — about half a second and you are back at the
start.

And notice the message. The pit says **"Missed the landing."** The spikes say **"Watch the
spikes."** Two failure modes, two different sentences, so the retry card tells you which mistake
you actually made.

### 9 — Cause and effect: the bug this film exists to explain  *(first draft, trace, current build)*

The first version of this fork did not work, and the reason is worth showing.

My original design stacked the two routes: the high ledges sat directly above the low road,
so that missing a high jump would drop you into the spikes you were avoiding. It read well on
paper. The automated route for the high line passed. The low line died — on the spikes — even
though the jump input had fired correctly.

The failing check told me *that* it broke. It could not tell me *why*, so I wrote a trace that
prints the real body every tick. Here it is:

Jump fires at x twelve forty-three. Six ticks later the body has risen **seventeen pixels**.
It should be at forty-five.

BEACON was hitting its head. The body is twenty-eight pixels tall and jumps fifty-six, so a jump
needs **eighty-four pixels** of headroom. The ledge above the low road left forty-eight. My tidy
cause-and-effect design was geometrically impossible for the route it was supposed to make
interesting.

The fix was geometry, not tuning. I did not raise the jump strength and I did not shorten the
character — I moved the high line up onto an intermediate step, to two-sixteen, which leaves
ninety-two pixels of clearance against the eighty-four it needs.

And then I pinned it. This check watches the real body run the real low road and asserts the
full jump. It reports fifty-six point zero seven five seven pixels. If that ledge ever creeps
back over the route, this number drops to seventeen and the suite goes red.

I lost something for that fix: the "fall into the spikes" moment is gone. I would rather have a
level that works than a story that does not.

### 10 — Completion  *(live play)*

The relocated flag. Results card. Enter plays again.

### 11 — What I tested

Thirty-one mechanics checks and nine keyboard checks, zero failures, on Godot 4.7.2.

I ran the suite on the untouched starter **before** editing anything, so "I didn't break it" is
a comparison and not an opinion. The starter's twenty-five checks are all still there, at their
original tolerances. Six are new.

The runs that failed are still in the evidence folder. When the route fixture broke, I extended
it and documented every new jump mark — I did not widen the tick budget or drop the
zero-deaths requirement to get a green report.

### 12 — What is uncertain

Three things I do not know.

The entry jump onto the fork pad has a take-off window of roughly forty-six pixels of run-up.
That is **calculated, not measured** — it is the tightest input in the level and it is exactly
the kind of number a real player should overturn.

The two lines are within five hundredths of a second. That is balanced, but balanced and
interesting are not the same thing, and I do not yet know whether anyone will feel a reason to
try the other one.

And nothing checks label placement. One of my zone labels sat inside the jump arc in a first
render. I caught it by looking at a screenshot — every test passed.

*(Render-day insert: the current, truthful status of the human playtest.)*

### 13 — One next improvement

A check that measures the **width** of the take-off window at each new landing — sweep the jump
mark and record which values still complete. That turns "is this jump fair?" from an opinion
into a number, which is the only honest way to answer the first uncertainty I just listed.

### 14 — Contributions

The decisions were mine: the scope, the rule that tuning and the collider were off limits, the
character concept and the pack-and-fin silhouette, what the fork should ask the player to trade,
and the call to redesign the geometry rather than weaken a check when it broke.

Claude Code wrote the drawing code, the level geometry, the test harnesses, found and diagnosed
the headroom bug, and drafted the written documents from the session record. This narration is
AI-generated.

Game revision demonstrated: *(commit SHA as rendered)*.
