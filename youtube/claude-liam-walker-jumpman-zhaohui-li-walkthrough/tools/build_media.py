#!/usr/bin/env python3
"""Cut media/Bxx.mp4 for every gameplay beat from the single 4K capture.

Rules this enforces, from references/capture-and-coverage.md:
  - real speed only: no setpts, no fps change, no trimming inside an action
  - each clip is exactly its beat's measured narration length, so the compiler
    has nothing to retime and nothing to freeze-pad
  - every gameplay clip carries a small persistent SCRIPTED INPUT label, because
    a scripted route is not a human playtest and must not be presented as one
  - output stays native 3840x2160 at the capture's 30 fps

Also renders the still beat (B08) from the committed level map.
"""
import json
import pathlib
import subprocess
import sys

REEL = pathlib.Path(__file__).resolve().parent.parent
PROJECT = REEL.parent.parent
CAPTURE = REEL / "capture" / "run-01.avi"
MEDIA = REEL / "media"
MP3 = REEL / "mp3"
FPS = 30
W, H = 3840, 2160
# The game's own HUD occupies the top and bottom of its 640x360 canvas, so a
# label burned over a full-bleed 6x frame collides with it. The gameplay is
# inset to an exact 5x integer scale (3200x1800) on the game's cream page
# colour, which stays crisp and leaves a 180 px band top and bottom for the
# label. No resampling of the pixel grid, no crop of the play area.
GAME_W, GAME_H = 3200, 1800
BAND = (H - GAME_H) // 2
CREAM = "0xF6F3EC"
INK = "0x25354A"
LABEL = "SCRIPTED INPUT · native 4K Godot capture, real engine run · NOT a human playtest"
FONT = "C\\:/Windows/Fonts/seguisb.ttf"
LABEL_SIZE = 44
# 5% title-safe inset: y 108..2052, x 192..3648. Gate V fails any content that
# crosses it, so the label's TOP is placed so its box ends above 2052.
SAFE_BOTTOM = int(H * 0.95)
LABEL_Y = SAFE_BOTTOM - LABEL_SIZE - 20          # 1988 -> box ends ~2032
# The map beat is matted on ink rather than cream: it keeps the diagram inside
# the title-safe box AND gives the frame the ink/background luminance
# separation Gate V measures, which a pale map on a pale surround failed.
MAP_W, MAP_H = 3148, 1771


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{' '.join(map(str, cmd))}\n{r.stderr[-1500:]}")


def audio_duration(beat_id):
    for name in (f"beat-{beat_id}.mp3", f"{beat_id}.mp3"):
        p = MP3 / name
        if p.is_file():
            out = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=nw=1:nk=1", str(p)],
                capture_output=True, text=True, check=True).stdout.strip()
            return float(out)
    sys.exit(f"no narration mp3 for {beat_id} in {MP3}")


def main():
    MEDIA.mkdir(exist_ok=True)
    sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
    report = []

    for beat in sheet["beats"]:
        bid = beat["beat_id"]
        shot = beat.get("shot", {})
        dur = audio_duration(bid)

        if shot.get("type") == "FOOTAGE":
            start = float(shot["capture_start_s"])
            end = float(shot["capture_end_s"])
            # the clip is the narration's length; the window above only anchors it
            length = round(dur, 3)
            if start + length > 30.233:
                start = max(0.0, 30.233 - length)
            out = MEDIA / f"{bid}.mp4"
            vf = (
                f"scale={GAME_W}:{GAME_H}:flags=neighbor,"
                f"pad={W}:{H}:{(W-GAME_W)//2}:{BAND}:color={CREAM},"
                f"drawtext=fontfile='{FONT}':text='{LABEL}':"
                f"x=(w-text_w)/2:y={LABEL_Y}:fontsize={LABEL_SIZE}:fontcolor=0x5A6472"
            )
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                 "-ss", f"{start:.3f}", "-i", str(CAPTURE), "-t", f"{length:.3f}",
                 "-vf", vf, "-r", str(FPS), "-an",
                 "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                 "-pix_fmt", "yuv420p", str(out)])
            report.append((bid, "FOOTAGE", f"{start:.2f}-{start+length:.2f}s", length))

        elif shot.get("type") == "STILL":
            src = PROJECT / "evidence" / "screens" / "10-level-map.png"
            if not src.is_file():
                sys.exit(f"missing still source: {src}")
            out = MEDIA / f"{bid}.mp4"
            label = shot.get("label", "")
            # The map is exactly 16:9, so 6x fills the frame with nothing cropped.
            # Motion follows the narration instead of decorating it: full map while
            # the problem is stated, in on the stacked ledges and the low road
            # while the numbers land, back out for the fix. Segments are cut, not
            # panned, because a diagram reads better on a cut than on a drift.
            segs = [
                ("full", 10.0, None),
                ("zone", 12.0, (2040, 470, 2100, 1181)),
                ("full", max(dur - 22.0, 2.0), None),
            ]
            parts = []
            padx, pady = (W - MAP_W) // 2, (H - MAP_H) // 2
            for i, (kind, seglen, box) in enumerate(segs):
                part = MEDIA / f"_{bid}_{i}.mp4"
                if box is None:
                    chain = f"scale={MAP_W}:{MAP_H}:flags=lanczos"
                else:
                    x, y, cw, ch = box
                    chain = (f"scale={W}:{H}:flags=lanczos,"
                             f"crop={cw}:{ch}:{x}:{y},"
                             f"scale={MAP_W}:{MAP_H}:flags=lanczos")
                chain += f",pad={W}:{H}:{padx}:{pady}:color={INK}"
                chain += (f",drawtext=fontfile='{FONT}':text='{label}':"
                          f"x=(w-text_w)/2:y={LABEL_Y}:fontsize={LABEL_SIZE}:fontcolor=0xD8DEE6")
                run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                     "-loop", "1", "-i", str(src), "-t", f"{seglen:.3f}",
                     "-vf", chain, "-r", str(FPS), "-an",
                     "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                     "-pix_fmt", "yuv420p", str(part)])
                parts.append(part)
            listing = MEDIA / f"_{bid}.txt"
            listing.write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
            run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                 "-f", "concat", "-safe", "0", "-i", str(listing),
                 "-c", "copy", str(out)])
            for p in parts:
                p.unlink()
            listing.unlink()
            report.append((bid, "STILL", src.name, round(dur, 3)))

    print(f"{'beat':<6}{'kind':<10}{'source range':<22}{'seconds':>8}")
    for row in report:
        print(f"{row[0]:<6}{row[1]:<10}{row[2]:<22}{row[3]:>8.3f}")
    print(f"\nwrote {len(report)} clips to {MEDIA}")


if __name__ == "__main__":
    main()
