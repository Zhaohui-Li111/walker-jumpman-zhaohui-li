#!/usr/bin/env python3
"""Author beat_sheet.json for the walker-jumpman-zhaohui-li walkthrough.

walker mode per skills/make/godot-waikthrough/SKILL.md section 3:
  B00 ClaudeComposerAsk  -> B01 hesitant-writer "what was built"
  -> B02..B07 gameplay body -> B08 Verdict -> B09 Your Turn -> B10 regular outro

Gameplay windows are capture-relative seconds into capture/run-01.avi and are
anchored on measured events from the input log, not chosen by eye.

WARNING: this script REWRITES beat_sheet.json from scratch. generate_audio_kokoro.py
and remotion_scenes.py both stamp provenance into that file (audio_file,
actual_duration_s, render_duration_s, remotion.rendered). Re-running this after
them silently drops those stamps and the compiler then refuses with
"missing required audio". If you must re-run it, re-run the audio generator
afterwards to restore the stamps.
"""
import json
import pathlib

REEL = pathlib.Path(__file__).resolve().parent.parent
SLUG = "claude-liam-walker-jumpman-zhaohui-li-walkthrough"
TITLE = "Walker Jumpman, Extended"
HANDLE = "@NikBearBrown"

# beat_id -> (clip start, clip end) in the capture. Target durations; the
# audio pass re-fits these to the measured narration without cutting an action.
# Sized to the MEASURED Kokoro durations so the action plays at real speed with
# no freeze padding: gameplay narration was cut to fit the footage, rather than
# the footage stretched or frozen to fit the narration.
# Each window is exactly its beat's measured Kokoro duration, anchored so the
# action it evidences stays inside. Adjacent windows overlap by a second or so;
# that is continuous real footage, not a repeated take, and no frame is frozen,
# slowed or retimed to make a sentence fit.
WINDOWS = {
    "B02": (0.00, 3.63),
    "B03": (2.40, 6.24),
    "B04": (4.90, 11.49),
    "B05": (10.40, 14.84),
    "B06": (13.30, 17.50),
    "B07": (17.28, 30.23),
}

GAMEPLAY = [
    ("B02", "OPEN", "Enter starts it. The level was already running behind.",
     [("0.0", "title card over the live level"),
      ("0.35", "Enter: card clears, player is at the spawn point"),
      ("0.6", "D then A — the cargo pack and head fin flip across the body")]),

    ("B03", "MECHANISM", "R is free. The spikes are not — and you are back instantly.",
     [("0.1", "R: player snaps back to spawn, retry counter unchanged"),
      ("0.45", "walks into the spikes, run stops, card reads 'Watch the spikes'"),
      ("0.8", "auto-retry drops the player back at spawn, running")]),

    ("B04", "MECHANISM", "One jump, fixed height, no double jump. Six ticks of coyote, six of buffer. Every landing is built on it.",
     [("0.05", "Space: a single jump onto the first step"),
      ("0.4", "clears the spike cluster, then the first gap"),
      ("0.75", "second step and second gap; HUD progress bar advances")]),

    ("B05", "MECHANISM", "Escape freezes body and clock. Then one jump, and the level forks.",
     [("0.1", "Escape: pause card, timer frozen"),
      ("0.4", "Enter resumes from the same pixel"),
      ("0.75", "jump across the gap onto the fork pad — both routes visible")]),

    ("B06", "MECHANISM", "Low road: spikes to clear, then a pit that names a different mistake.",
     [("0.15", "drops right onto the low road"),
      ("0.4", "jumps the second spike cluster at speed"),
      ("0.8", "runs off the end into the pit; the card names the other failure")]),

    ("B07", "MECHANISM",
     "The high line climbs instead — a step, two ledges, no hazard on the route. The last ledge overhangs the pad, so it ends by falling, not jumping. Flag, results, Enter, and it replays clean. Then P, M, back to the title card.",
     [("0.08", "step up, then ledge A, then ledge B — spikes visible below"),
      ("0.42", "runs off the last ledge and lands on the finish pad"),
      ("0.62", "reaches the relocated flag; results card shows time and retries"),
      ("0.82", "Enter replays from zero; P then M returns to the title card")]),
]


def show(events):
    return [{"at": at, "event": ev} for at, ev in events]


def gameplay_beat(bid, act, narration, events):
    start, end = WINDOWS[bid]
    return {
        "beat_id": bid,
        "act": act,
        "role_note": ("GAMEPLAY EVIDENCE — native 3840x2160 Godot Movie Maker capture, "
                      "scripted keyboard input, real engine run. Labelled SCRIPTED INPUT on screen. "
                      "Not a human playtest. Clip is capture/run-01.avi %.2f-%.2fs at real speed; "
                      "any tail beyond the action is a labelled held frame." % (start, end)),
        "narration_text": narration,
        "voice": "am_onyx",
        "engine": "kokoro",
        "estimated_duration_s": round(end - start, 2),
        "shot": {
            "type": "FOOTAGE",
            "class": "SHOW",
            "source": "capture",
            "motion": "none",
            "capture": "run-01",
            "capture_start_s": start,
            "capture_end_s": end,
            "label": "SCRIPTED INPUT · native 4K engine capture",
            "show": show(events),
        },
    }


def main():
    beats = [
        {
            "beat_id": "B00",
            "act": "ASK",
            "role_note": ("COLD OPEN LAW — ClaudeComposerAsk. walker mode B00. The prompt is an "
                          "ILLUSTRATIVE RECONSTRUCTION of the Walker ask for this game, not a historical "
                          "transcript: this project was extended from an existing starter, not generated "
                          "from a blank Walker run. No invented build receipts. Liam named in first breath."),
            "narration_text": (
                "Namaste — this is Liam, in for Bear. Zhaohui Li took walker-jumpman, Bear's one-jump "
                "Godot platformer, and extended it: a character you can actually read at eighteen pixels "
                "wide, and a final zone that makes you pick a route. Everything after this card is the "
                "real build, played through its own keyboard input."),
            "voice": "am_onyx",
            "engine": "kokoro",
            "estimated_duration_s": 21,
            "shot": {
                "type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
                "show": show([
                    ("0.02", "composer card fades in on the cream page"),
                    ("0.12", "greeting 'Namaste, Liam' appears above the composer"),
                    ("0.3", "the Walker ask types in"),
                    ("0.66", "send button arms terracotta"),
                    ("0.78", "three RESULT lines land beneath the card"),
                ]),
                "remotion": {
                    "pattern": "ClaudeComposerAsk",
                    "props": {
                        "greeting": "Namaste, Liam",
                        "topic": "WALKER · GODOT WALKTHROUGH",
                        "segment": TITLE,
                        "command": ("Please use Walker to convert my game design document about a one-jump 2D "
                                    "platformer — a courier automaton crossing gaps and spikes, ending in a zone "
                                    "that forks into a fast hazardous road and a slower clean climb — into a "
                                    "playable Godot project."),
                        "runningText": "reconstructed ask · extended from walker-jumpman…",
                        "folderLabel": HANDLE,
                        "modelLabel": "Claude",
                        "effortLabel": "High",
                        "output": [
                            "Character drawn in _draw(), collider untouched.",
                            "Zone 03 forks at a raised pad.",
                            "Finish moved 916 to 1548.",
                        ],
                    },
                },
            },
        },
        {
            "beat_id": "B01",
            "act": "BLUF",
            "role_note": ("EXECUTIVE-SUMMARY LAW — hesitant writer BLUF. Misconception corrected is the "
                          "reel's actual one: 'a new game' -> 'an extension of Bear's starter'. Whole phrase "
                          "is the trigger so the corrected sentence stands alone. lead_silence_s gives the "
                          "typing a head start; seed fixed for this slug."),
            "narration_text": (
                "Not a new game — an extension. The starter's two zones are byte-identical in the level "
                "data and still walkable. What changed is who you play as, and where the level stops."),
            "voice": "am_onyx",
            "engine": "kokoro",
            "estimated_duration_s": 12,
            "lead_silence_s": 0.8,
            "shot": {
                "type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on-correct",
                "show": show([
                    ("0.0", "cream page; typing begins during the lead silence"),
                    ("0.2", "'walker-jumpman-zhaohui-li is a new game:' types, then pauses"),
                    ("0.45", "'a new game' struck through in terracotta"),
                    ("0.6", "'an extension of Bear's starter' types in its place"),
                    ("0.85", "corrected sentence settles before the cut"),
                ]),
                "remotion": {
                    "pattern": "BrutalistHesitantWriter",
                    "props": {
                        "contextTitle": "BLUF",
                        # BrutalistHesitantWriter matches triggers PER WORD:
                        #   triggers.indexOf(core.toLowerCase())  where core is one
                        #   token stripped of punctuation.
                        # A multi-word trigger can never match, so the phrase
                        # "a new game" -> "an extension of Bear's starter" silently
                        # did nothing and the correction never landed. The
                        # misconception is carried by a single verb instead:
                        # "was built" -> "was extended", which is the reel's actual
                        # claim and leaves a sentence that stands on its own.
                        # Three lines at 88pt, not two at 84: Gate V failed the
                        # two-line version for `underfill` (46% of the safe area
                        # against a 55% floor) because the correction pass leaves
                        # less text on screen at the midpoint than straight typing
                        # does. "same collider" is not padding - it is one of the
                        # film's actual claims.
                        "text": "walker-jumpman-zhaohui-li was built:\nnew character, one more zone,\nsame jump, same collider.",
                        "triggerWords": "built",
                        "replacementWords": "extended",
                        "fontSize": 88,
                        "lineSpacing": 2.7,
                        "align": "center",
                        "seed": "8821",
                        "mistakeRate": 2,
                        "hesitateWithin": 0,
                        "hesitateBetween": 1,
                        "charMs": 8,
                        "ink": "#3D3929",
                        "accent": "#D97757",
                        "bg": "#FAF9F5",
                    },
                },
            },
        },
    ]

    for bid, act, narration, events in GAMEPLAY:
        beats.append(gameplay_beat(bid, act, narration, events))

    beats.append({
        "beat_id": "B08",
        "act": "FALSIFIABILITY",
        "role_note": ("CAUSE AND EFFECT — the one source change whose consequence is a number. Visual is "
                      "evidence/screens/10-level-map.png, rendered directly from first_steps.json by "
                      "godot/tests/map_board.gd, so the diagram cannot drift from the level the game loads. "
                      "Not gameplay: this beat explains a defect that was fixed BEFORE the capture, so the "
                      "film does not restage a bug it no longer has."),
        "narration_text": (
            "That high line started in the wrong place. The first draft stacked the ledges directly over the "
            "low road. The body is twenty-eight pixels tall and jumps fifty-six, so a jump underneath needs "
            "eighty-four pixels of headroom — and it had forty-eight. It clipped the ledge, rose seventeen "
            "pixels instead of fifty-six, and died on the spikes it was trying to clear. The fix was geometry, "
            "not jump strength. The ledges moved up, leaving ninety-two pixels. A check now measures the real "
            "apex on every run and fails if it ever reads seventeen again."),
        "voice": "am_onyx",
        "engine": "kokoro",
        "estimated_duration_s": 27,
        "shot": {
            "type": "STILL", "class": "SHOW", "source": "generated", "motion": "pan-right",
            "label": "LEVEL MAP · rendered from first_steps.json, vertical scale exaggerated",
            "show": show([
                ("0.05", "whole-level map: grey starter geometry left, amber additions right"),
                ("0.3", "the two high ledges, and the low road running beneath them"),
                ("0.6", "the headroom the jump underneath needs versus what it had"),
                ("0.85", "the corrected ledge height"),
            ]),
        },
    })

    beats.append({
        "beat_id": "B09",
        "act": "VERDICT",
        "role_note": ("VERDICT — separates observed working features from what was not shown and what "
                      "is untested. The focus-loss line is the accepted partial-coverage item; the "
                      "playtest line is the honest limit of a scripted route."),
        "narration_text": (
            "Verdict. Sixteen implemented features shown running, two real deaths and two real recoveries, "
            "both fork routes finishing. One implemented feature is not on film: pause on focus loss, which "
            "an unattended capture cannot trigger — it is covered by a machine check instead. And this was a "
            "scripted route, not a person. It proves the geometry is reachable. It cannot tell you the level "
            "is fair."),
        "voice": "am_onyx",
        "engine": "kokoro",
        "estimated_duration_s": 24,
        "shot": {
            "type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "artifact-lines",
            "show": show([
                ("0.05", "verdict artifact page opens on cream"),
                ("0.2", "line 1 lands: what ran"),
                ("0.42", "line 2 lands: what is not on film"),
                ("0.64", "line 3 lands: what a scripted route cannot prove"),
                ("0.85", "line 4 lands: the one number that would settle it"),
            ]),
            "remotion": {
                "pattern": "ClaudeVerdictArtifact",
                "props": {
                    "artifactTitle": "Verdict",
                    "artifactHeading": "walker-jumpman-zhaohui-li",
                    "brandLabel": HANDLE,
                    "artifactLines": [
                        "Shown running: 16 features, 2 deaths, 2 recoveries, both fork routes finish.",
                        "Not on film: pause on focus loss — unattended capture cannot lose focus.",
                        "Scripted input proves reachability, not fairness. No human playtest yet.",
                        "Untested: the fork-pad take-off window is calculated at ~46 px, never measured.",
                    ],
                },
            },
        },
    })

    beats.append({
        "beat_id": "B10",
        "act": "HANDOFF",
        "role_note": ("HANDOFF LAW — Your Turn. The prompt extends this episode's idea into the viewer's "
                      "own project and is read aloud verbatim, then discussed, before the invitation."),
        "narration_text": (
            "Your turn. Paste this: 'In my Godot platformer, measure the take-off window for every jump the "
            "level requires — sweep the jump position frame by frame and report the range that still lands.' "
            "That is the number I did not have. It turns is this jump fair into a measurement instead of an "
            "opinion. Run it on your own level and see which jump has the narrowest window — that one is "
            "where your players will quit."),
        "voice": "am_onyx",
        "engine": "kokoro",
        "estimated_duration_s": 26,
        "shot": {
            "type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
            "show": show([
                ("0.05", "composer opens with greeting 'Your turn.'"),
                ("0.25", "the measurement prompt types in"),
                ("0.7", "send button arms terracotta"),
                ("0.82", "three RESULT lines land beneath"),
            ]),
            "remotion": {
                "pattern": "ClaudeComposerAsk",
                "props": {
                    "greeting": "Your turn.",
                    "topic": "WALKER · YOUR LEVEL",
                    "segment": "Measure The Window",
                    "command": ("In my Godot platformer, measure the take-off window for every jump the level "
                                "requires: sweep the jump position frame by frame with a scripted input driver "
                                "and report, for each landing, the range of take-off positions that still land. "
                                "Flag the narrowest one."),
                    "runningText": "sweeping take-off positions…",
                    "folderLabel": HANDLE,
                    "modelLabel": "Claude",
                    "effortLabel": "High",
                    "output": [
                        "Per-landing take-off ranges measured.",
                        "Narrowest window flagged.",
                        "Check: is that the jump players quit on?",
                    ],
                    "animateTyping": True,
                },
            },
        },
    })

    beats.append({
        "beat_id": "B11",
        "act": "OUTRO",
        "role_note": ("OUTRO LOCK (2026-09-18) — ClaudeTitleOutro, exact title restate, @NikBearBrown "
                      "hardcoded, slug-seeded mascot, NO subline. SPOKEN, never scored: Liam re-reads the "
                      "exact title then the handle, over a 1.0 s tail hold. No jingle, no music, no game "
                      "audio. kind: outro_voice."),
        "narration_text": "Walker Jumpman, Extended. At Nik Bear Brown.",
        "voice": "am_onyx",
        "engine": "kokoro",
        "kind": "outro_voice",
        "estimated_duration_s": 7,
        "tail_hold_s": 1.0,
        "shot": {
            "type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "mascot-title",
            "show": show([
                ("0.0", "title 'Walker Jumpman, Extended.' on cream, EB Garamond"),
                ("0.3", "@NikBearBrown appears beneath"),
                ("0.5", "slug-seeded crisp-safe mascot animates under the handle"),
                ("0.85", "1 s silent tail hold"),
            ]),
            "remotion": {
                "pattern": "ClaudeTitleOutro",
                "props": {"title": TITLE, "slug": SLUG},
            },
        },
    })

    sheet = {
        "metadata": {
            "title": TITLE,
            "slug": SLUG,
            "topic": "Extending a Godot platformer: a new character and a branching final zone",
            "kind": "godot-walkthrough",
            "mode": "walker",
            "brand": "claude-liam",
            "channel": HANDLE,
            "channel_title": "Nik Bear Brown",
            "folderLabel": HANDLE,
            "persona": "Liam",
            "presenter": "Liam",
            "in_for_bear": True,
            "greeting": "Namaste, Liam",
            "audience": "practitioners and makers following the channel's Claude workflows",
            "register": "Teardown",
            "engine": "kokoro",
            "voice": "am_onyx",
            "voice_kokoro": "am_onyx",
            "palette": "claude",
            "aspect_ratio": "16:9",
            "fps": 30,
            "captions": False,
            "game": {
                "name": "walker-jumpman-zhaohui-li",
                "starter": "walker-jumpman by Nik Bear Brown — https://github.com/nikbearbrown/walker-jumpman",
                "source_revision": "cc8ae01",
                "build_id": "0be6756a1c222cf89964287272c5d6659111e6f50d2bb2f01969e8d03f963bf9",
                "godot": "4.7.2.stable.official.ed1daf0bf",
            },
            "note": ("Gameplay beats are real engine capture driven by scripted keyboard input and are "
                     "labelled as such on screen. Coverage contract in coverage.json; capture provenance "
                     "in CAPTURE.md."),
        },
        "beats": beats,
    }
    out = REEL / "beat_sheet.json"
    out.write_text(json.dumps(sheet, indent=2, ensure_ascii=False), encoding="utf-8")
    total = sum(b["estimated_duration_s"] for b in beats)
    print(f"wrote {out}")
    print(f"{len(beats)} beats, estimated {total:.0f}s ({total/60:.1f} min)")
    for b in beats:
        words = len(b["narration_text"].split())
        print(f"  {b['beat_id']:<4} {b['act']:<10} est {b['estimated_duration_s']:>5}s  {words:>3} words")


if __name__ == "__main__":
    main()
