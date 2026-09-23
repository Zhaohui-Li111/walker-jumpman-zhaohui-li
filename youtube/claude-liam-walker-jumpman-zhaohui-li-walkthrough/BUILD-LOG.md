# BUILD-LOG — walker-jumpman-zhaohui-li walkthrough

Every deviation, workaround and failure in producing this reel. Nothing here is
tidied away; a reviewer should be able to tell exactly what was patched and why.

Host: Windows 11 Home China 10.0.26200 · Python 3.12.9 · Node v22.17.1 ·
Godot 4.7.2.stable · ffmpeg 9.0.2 (Gyan) · Kokoro `am_onyx`, local, free.

---

## 1. Toolkit environment: what had to be installed

The Brutalist checkout (`D:\courses\7270\brutalist.art-main`) arrived with none of
its runtime dependencies present. Installed, in order:

| Dependency | How | Note |
|---|---|---|
| ffmpeg / ffprobe | `winget install Gyan.FFmpeg` (9.0.2) | winget added it to PATH but only for new shells; every command in this build prepends the package `bin/` explicitly rather than editing the user's PATH. |
| numpy, Pillow, mutagen, manim, manimpango, faster-whisper, kokoro-onnx | `pip install` by name | **Not** `-r requirements.txt` — see §2. |
| Kokoro model files | downloaded from the `model-files-v1.0` release named in the skill | `kokoro-v1.0.onnx` (325 MB) + `voices-v1.0.bin` (28 MB). SKILL.md says "model files ship with this toolkit"; **they are not in this checkout** — that line is wrong for this distribution. |
| Remotion node deps | `npm install` in `runtime/remotion` | |

## 2. Three toolkit bugs hit on Windows, and what was done about each

### 2.1 `./setup` never prints its readiness table — NOT patched

The ElevenLabs guard at `setup:102-114` greps the whole repository for
`"engine"…"elevenlabs"` and exits 1 before any dependency check runs. It matches
the toolkit's **own example beat sheets** (`youtube/brutalist/claude-liam-brutalist-command-setup/`
and five others), so on a clean checkout the doctor always aborts.

**Not patched.** Each dependency was verified directly with the same checks
`setup` would have run. Their repo is left alone for something that only affects
its self-diagnostic.

### 2.2 `pip install -r requirements.txt` fails on a Chinese-locale Windows — NOT patched

`requirements.txt` is UTF-8 and contains box-drawing characters (`──`). pip reads
it with `locale.getpreferredencoding()`, which is `cp936`/GBK here:

```
UnicodeDecodeError: 'gbk' codec can't decode byte 0x94 in position 14
```

**Not patched.** Installed the same pinned versions by name instead. The same
root cause hit `generate_audio_kokoro.py` (`Path.read_text()` with no encoding on
a UTF-8 beat sheet); that one is solved for the whole toolkit by exporting
**`PYTHONUTF8=1`**, which every command in this build does. No toolkit edit needed.

### 2.3 Remotion never renders on Windows — PATCHED, one line

`runtime/scripts/remotion_scenes.py:90` invoked `["npx", "remotion", …]` through
`subprocess.run`. On Windows npx is `npx.CMD`; `CreateProcess` only appends `.exe`
to a bare name and does not consult PATHEXT, so all five bookend beats failed with
`[WinError 2] The system cannot find the file specified` — reported in the build
output as a render failure with no hint of the cause.

**Patched**, minimally and upstreamably:

```python
npx = shutil.which("npx") or "npx"
cmd = [npx, "remotion", "render", ENTRY, pattern, str(candidate), …]
```

`shutil.which` consults PATHEXT and returns the full `npx.CMD` path, which
`subprocess` launches fine (verified directly before patching). On macOS/Linux
`which("npx")` returns the same binary the bare name would have resolved to, so
there is no behaviour change off Windows. The patch carries a dated comment naming
this project. **This is the only change made to the course-provided toolkit.**

## 3. Capture: one run discarded, not shipped

The first native-4K capture attempt **failed its own assertions** and was deleted
rather than used. At `--fixed-fps 30` against 60 Hz physics, two physics ticks
share one rendered frame and input events flush per *rendered* frame, so a jump
whose press and release were two ticks apart landed inside a single frame and was
dropped. The player never cleared the first step, got stuck against it, and the
`spikes-kill` assertion reported `state: PLAYING`.

Fixed in the driver (longer holds; confirm `player.jumps` incremented before
consuming a jump mark, otherwise retry next tick). Re-validated at capture frame
rate, then re-recorded. Full detail in [CAPTURE.md](CAPTURE.md).

This is exactly the failure mode the skill warns about: a capture that merely ran
to completion would have produced 30 seconds of footage of a character stuck
against a step, and `--quit-after` alone would have called it a success.

## 4. Beat sheet: narration cut to fit the footage

First audio pass measured **55.5 s** of gameplay narration against **30.2 s** of
capture. Rather than freeze-pad 25 s of held frames, two things changed:

1. Gameplay riffs were **cut** to roughly one third their original length. The
   riff skill asks for concise reactions over continuous chatter, so this improved
   them.
2. The long cause-and-effect explanation (the headroom bug) was moved **off the
   gameplay footage** onto its own beat, B08, carried by the level map that
   `godot/tests/map_board.gd` renders directly from `first_steps.json`.

Each gameplay clip is now cut to exactly its beat's measured narration length, so
nothing is retimed, slowed or frozen. Adjacent windows overlap by about a second;
that is continuous real footage, not a repeated take.

## 5. Visual QC caught two layout defects before render

Found by extracting frames and actually looking at them, not by probing durations:

1. **Label collided with the game's HUD.** A full-bleed 6× frame plus a bottom
   label bar covered the game's own "No lives. Just another try." / retry counter.
   Also the label was 34 px at 4K — illegible at 1080p. Fixed by insetting the
   gameplay to an exact **5× integer scale** (3200×1800) on the game's cream page
   colour, giving a 180 px band for a 46 px label. Still crisp; no crop of the
   play area; no resampling of the pixel grid.
2. **The map beat cropped its own title and legend.** The first version scaled to
   114% and panned, cutting off the heading and the legend. Replaced with a
   three-segment cut — full map, in on the stacked ledges and the low road while
   the numbers land, back out for the fix — so the motion follows the narration
   instead of decorating it, and nothing essential leaves the frame.

## 6. Coverage: one accepted partial

`pause-on-focus-loss` is implemented and covered by the `focus-loss-pauses`
machine check, but an unattended Movie Maker capture cannot lose window focus, so
there is no footage of it. Recorded as `implemented` with **empty evidence** — not
relabelled `planned` to make the checker pass. The human was asked and explicitly
accepted a partial walkthrough for this one feature. It is stated on screen in the
Verdict beat and in [_qc/REPORT.md](_qc/REPORT.md).

## 7. Outro follows the lock, not the example

The toolkit's own `claude-liam-brutalist-skill-godot-waikthrough` reel (built
2026-09-11) uses `audio_policy: "silence"` with a jingle under the outro card.
`OUTRO-LOCK.md` was locked **2026-09-18**, after that reel, and now requires the
card be **spoken**: Liam re-reads the exact title, then "At Nik Bear Brown", over a
1 s tail hold, with no jingle or music. This reel follows the lock
(`kind: "outro_voice"`), not the stale exemplar.
