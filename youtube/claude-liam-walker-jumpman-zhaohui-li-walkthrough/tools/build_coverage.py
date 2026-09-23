#!/usr/bin/env python3
"""Generate coverage.json from the *measured* capture, not from typed numbers.

Times come from capture/run-01-inputs.jsonl (physics ticks -> seconds at 60 Hz),
the capture hash is read off the file bytes, and build_id is read from
SOURCE-SNAPSHOT.json. Nothing here is a sample value.

    python tools/build_coverage.py
"""
import hashlib
import json
import pathlib
import subprocess
import sys

REEL = pathlib.Path(__file__).resolve().parent.parent
TICK_HZ = 60.0
CAPTURE = "capture/run-01.avi"
INPUT_LOG = "capture/run-01-inputs.jsonl"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def load_log():
    rows = [json.loads(line) for line in
            (REEL / INPUT_LOG).read_text(encoding="utf-8").splitlines() if line.strip()]
    phase, expect, misc = {}, {}, {}
    spaces = []
    for r in rows:
        if r["kind"] == "phase":
            phase.setdefault(r["name"], r["t"])
        elif r["kind"] == "expect":
            expect.setdefault(r["id"], r["t"])
        elif r["kind"] == "key" and r.get("key") == "Space" and r.get("pressed"):
            spaces.append(r["t"])
        elif r["kind"] in ("retry-card", "results-card", "driver-start"):
            misc.setdefault(r["kind"], r["t"])
    return rows, phase, expect, misc, spaces


def main():
    cap_path = REEL / CAPTURE
    if not cap_path.is_file():
        sys.exit(f"missing capture: {cap_path}")
    duration = probe_duration(cap_path)
    snapshot = json.loads((REEL / "SOURCE-SNAPSHOT.json").read_text(encoding="utf-8"))
    build_id = snapshot["build_id"]
    rows, phase, expect, misc, spaces = load_log()
    last_tick = rows[-1]["t"]

    def s(tick):
        return round(min(tick / TICK_HZ, duration - 0.01), 3)

    def first_space_after(tick):
        for t in spaces:
            if t >= tick:
                return t
        return tick

    def ev(cap, beat, start, action, end, observation, riff):
        a, b, c = s(start), s(action), s(end)
        # the contract requires strictly increasing, inside the capture
        assert 0 <= a < b < c <= duration + 0.001, (beat, a, b, c, duration)
        return {"capture": cap, "beat_id": beat, "start_s": a, "action_s": b, "end_s": c,
                "observation": observation, "riff": riff}

    C = "run-01"
    features = [
        {"id": "menu-and-start", "status": "implemented", "evidence": [ev(
            C, "B02", phase["menu"], expect["enter-starts"], expect["enter-starts"] + 40,
            "Title card is on screen with the level behind it; Enter is pressed and the card clears to a live player at the spawn point.",
            "The menu is not a separate scene - the level is already running behind it. That is why Enter starts instantly with no load.")]},

        {"id": "move-left-and-right", "status": "implemented", "evidence": [ev(
            C, "B02", phase["movement"], expect["moves-both-ways"], expect["moves-both-ways"] + 8,
            "D drives the character right past x=100, then A drives it back left; the cargo pack and head fin flip across the body at the turn.",
            "Facing is readable from the outline alone, before you can see the eye - that is what the asymmetric pack buys at eighteen pixels wide.")]},

        {"id": "jump-fixed-height", "status": "implemented", "evidence": [ev(
            C, "B04", phase["zones-01-02"], first_space_after(phase["zones-01-02"]) + 12,
            first_space_after(phase["zones-01-02"]) + 45,
            "One Space press lifts the body onto the first step and it lands; holding the key does not produce a second jump.",
            "One fixed-height jump, no double jump, six ticks of coyote and six of buffer. Every landing in the level is authored against that one arc.")]},

        {"id": "manual-retry", "status": "implemented", "evidence": [ev(
            C, "B03", phase["manual-retry"], expect["r-retries-without-death"],
            expect["r-retries-without-death"] + 14,
            "R returns the player to the spawn point mid-run; the retry counter in the HUD stays where it was.",
            "R is a restart, not a death. Separating those two means the retry count still measures mistakes rather than impatience.")]},

        {"id": "hazard-spikes", "status": "implemented", "evidence": [ev(
            C, "B03", phase["failure-spikes"], expect["spikes-kill"], expect["spikes-kill"] + 20,
            "The player walks into the spike cluster without jumping; the run stops and the card reads 'Watch the spikes'.",
            "The hazard trigger is three exact triangles, not one oversized box - the collision matches the shape you can see.")]},

        {"id": "auto-retry", "status": "implemented", "evidence": [ev(
            C, "B03", misc.get("retry-card", expect["spikes-kill"]), expect["auto-retry-recovers"],
            expect["auto-retry-recovers"] + 20,
            "About half a second after the death the player is back at the spawn point and playable, with no menu and no lives counter.",
            "A cheap retry changes what the level can ask for. It does not tell us whether a first-time player saw the danger coming.")]},

        {"id": "starter-zones-route", "status": "implemented", "evidence": [ev(
            C, "B04", phase["zones-01-02"], expect["starter-zones-cleared"],
            expect["starter-zones-cleared"] + 12,
            "A clean run over the two steps, the spike cluster and both gaps of the original course, ending past x=880.",
            "This is the starter's route, unchanged in the level data. The extension had to leave it walkable, and it does.")]},

        {"id": "hud-progress-timer-retries", "status": "implemented", "evidence": [ev(
            C, "B04", phase["zones-01-02"] + 60, expect["starter-zones-cleared"],
            expect["starter-zones-cleared"] + 12,
            "The progress bar advances across the top, the timer counts up and the retry count reads 01 after the earlier death.",
            "The bar is derived from spawn and the finish trigger. With the starter's hard-coded span it would have pegged at full the moment the new zone began.")]},

        {"id": "pause-and-resume", "status": "implemented", "evidence": [ev(
            C, "B05", phase["pause"], expect["escape-pauses"], expect["enter-resumes"] + 8,
            "Escape freezes the body and the timer mid-run and shows the pause card; Enter resumes from exactly the same position.",
            "Pause stops the clock as well as the body, so a paused run cannot be used to farm a better time.")]},

        {"id": "zone03-fork", "status": "implemented", "evidence": [ev(
            C, "B06", phase["zone-03-fork"], expect["fork-pad-reached"],
            expect["fork-pad-reached"] + 38,
            "A jump across the gap at the end of the original course lands on a raised pad; from it both the low road and the climbing ledges are visible at once.",
            "The decision is placed where you can see both answers before committing, and the climb back up is only thirty-two pixels - the fork does not punish curiosity.")]},

        {"id": "zone03-low-road", "status": "implemented", "evidence": [ev(
            C, "B07", phase["low-road-and-pit"], first_space_after(phase["low-road-and-pit"]) + 18,
            first_space_after(phase["low-road-and-pit"]) + 60,
            "On the low road the player jumps the second spike cluster at speed and lands back on the flat.",
            "The low road trades precision for exposure: wide flat landings, but a hazard and a pit between you and the flag.")]},

        {"id": "zone03-pit-fall", "status": "implemented", "evidence": [ev(
            C, "B07", expect["pit-kills"] - 45, expect["pit-kills"], expect["pit-kills"] + 25,
            "The player runs off the end of the low road into the pit and falls past the kill line; the card reads 'Missed the landing', not 'Watch the spikes'.",
            "Two failure modes, two different sentences. The retry card tells you which mistake you actually made before it sends you back.")]},

        {"id": "zone03-high-line", "status": "implemented", "evidence": [ev(
            C, "B08", phase["high-line-to-finish"] + 330, phase["high-line-to-finish"] + 430,
            phase["high-line-to-finish"] + 520,
            "The other line: a step up, then two ledges above the low road, with no hazard on the route and the spikes visible below.",
            "An early draft stacked these ledges directly over the low road. The body is twenty-eight pixels tall and jumps fifty-six, so the jump underneath needed eighty-four pixels of headroom and had forty-eight - it clipped the ledge and died. The fix was geometry, not tuning.")]},

        {"id": "finish-and-results", "status": "implemented", "evidence": [ev(
            C, "B09", expect["high-line-completes"] - 60, expect["high-line-completes"],
            expect["high-line-completes"] + 60,
            "The high line runs off its last ledge onto the finish pad and reaches the relocated flag; the results card shows the time and the retry count.",
            "The flag moved from x=916 to x=1548, so the original route on its own can no longer win. The high line ends by falling, not jumping - that is what the extra climb buys.")]},

        {"id": "replay", "status": "implemented", "evidence": [ev(
            C, "B09", phase["replay"], expect["enter-replays"], expect["enter-replays"] + 35,
            "Enter on the results card starts a fresh attempt with the timer and the retry count both back at zero.",
            "Replay resets the run state rather than reloading the scene, which is why it is instant.")]},

        {"id": "return-to-menu", "status": "implemented", "evidence": [ev(
            C, "B09", phase["menu-return"], expect["m-returns-to-menu"],
            expect["m-returns-to-menu"] + 100,  # clamped to the capture end by s()
            "P pauses the new attempt and M returns to the title card, which can be started again.",
            "Pause and menu are separate states, so M cannot be hit by accident mid-run.")]},

        # Implemented, deliberately NOT filmed. See _qc/REPORT.md - the human
        # explicitly accepted a partial walkthrough for this one feature.
        {"id": "pause-on-focus-loss", "status": "implemented", "evidence": []},

        {"id": "cherries", "status": "planned", "reason":
            "Proposed in the starter's GDD (twenty optional collectibles). Not built in this slice and not added by this extension.", "evidence": []},
        {"id": "audio", "status": "planned", "reason":
            "No audio buses, sound files or music anywhere in the source. The game is silent by construction; no sound was invented for the film.", "evidence": []},
        {"id": "settings-and-remapping", "status": "planned", "reason":
            "GDD proposes a settings screen with key remapping and persistence. No settings scene exists; the input map is built in code at startup.", "evidence": []},
        {"id": "moving-platforms", "status": "planned", "reason":
            "Explicitly out of scope in the starter's MVP and not added here. All solids are static bodies.", "evidence": []},
        {"id": "web-export", "status": "planned", "reason":
            "Export templates are not installed and no export was produced. This is a source-only release.", "evidence": []},
    ]

    coverage = {
        "schema_version": 1,
        "game": {"name": "walker-jumpman-zhaohui-li", "build_id": build_id},
        "captures": {
            C: {
                "path": CAPTURE,
                "sha256": sha256(cap_path),
                "build_id": build_id,
                "method": "scripted-input",
                "input_log": INPUT_LOG,
            }
        },
        "features": features,
    }
    out = REEL / "coverage.json"
    out.write_text(json.dumps(coverage, indent=2), encoding="utf-8")
    shown = sum(1 for f in features if f["status"] == "implemented" and f["evidence"])
    unshown = [f["id"] for f in features if f["status"] == "implemented" and not f["evidence"]]
    print(f"wrote {out}")
    print(f"capture duration {duration:.3f}s, last logged tick {last_tick} ({last_tick/TICK_HZ:.2f}s)")
    print(f"implemented+shown {shown}, implemented+unshown {unshown}, "
          f"planned {sum(1 for f in features if f['status']=='planned')}")


if __name__ == "__main__":
    main()
