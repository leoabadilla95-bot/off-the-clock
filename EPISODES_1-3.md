# Episodes 1–3: production instructions

Episodes 1–3 are the episodes in production. Each one is a finished previs video today; the steps below take it to
full motion on Runway, with or without lip-sync.

| Ep | Title | Final runtime | Cuts | Groupon beat | Cliffhanger | Previs | Runway kit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Hunter from Ops | 2:12 | 35 | Feed → $39 axe-throwing deal → "Buy for 2" → voucher | Priya: "There you are! Mr. Co—" · Abby (thinks): "Mister… what?" | `deliverables/off-the-clock-ep01-v3.mp4` | `runway_kit/ep01/` |
| 2 | Bullseye | 2:16 | 33 | None on screen (the prepaid voucher is the joke) | Jo: "Abby. Come here. Like, right now." | `deliverables/off-the-clock-ep02-v3.mp4` | `runway_kit/ep02/` |
| 3 | Masa | 2:11 | 31 | Classes tab → $34 tamale class; Lupe: "Half my students find me on Groupon now." | The bank on speaker for "Mr. Cole" · Abby: "…Who's Mr. Cole?" | `deliverables/off-the-clock-ep03-v3.mp4` | `runway_kit/ep03/` |

Scripts: `scripts_v2/ep01.md`–`ep03.md`. Sound design: `audio_plan/ep01.json`–`ep03.json`. Captions:
`deliverables/off-the-clock-epNN-final.srt` (timed to the final videos, thoughts in italics).

## What's in each kit (`runway_kit/epNN/`)

Everything needed to make, lip-sync and finish the episode from a fresh clone, with no other accounts or regeneration:

| File | Use |
| --- | --- |
| `SHOT_SHEET.md` | One row per clip: start image, paste-ready prompt, Runway length, trim length, mouth note, voice file |
| `epNN_cut_XXX.jpg` | The start image for each clip, named by cut |
| `voice/cut_<id>.mp3` | On-camera speech for that cut only (thoughts and off-screen lines muted), starting at the clip's first frame, for lip-sync |
| `soundtrack.m4a` | The finished mix: voices, music and effects, with the 2 s title-card lead |
| `timing.json` | Each cut's final length in seconds (the assembler trims clips to these) |
| `lines.json` | Every recorded line's start and end in episode time, and whether it's a thought |

## What's already done for each episode

1. **Script (v2):** boardroom cold open, Grant's hunt, Abby's promotion stakes, 9–12 internal thoughts per episode.
2. **Pictures:** a keyframe for every cut (cast sheets and location plates as references), new v2 frames where the
   script changed, and mock Groupon screens for the app beats.
3. **Voices:** 14 ElevenLabs voices designed from the Lookbook briefs; every line recorded with a delivery cue from the
   audio plan. Thoughts are dry and close; spoken lines have a touch of room. The picture is cut to the performance.
4. **Sound:** room ambience per location, effects on visible action, cinematic accents on real beats only, music cue by
   cue (5–7 per episode), ducking under speech and deeper under thoughts, near-silence on cliffhangers, loudness at about
   -16 LUFS.

## Option A: make the clips by hand in the Runway web app

Use this to spend Runway subscription credits (the web app's credits don't work through the API).

1. Open `runway_kit/epNN/SHOT_SHEET.md`. Each row is one clip.
2. In Runway, choose **Gen-4 Turbo**, image to video, ratio **720:1280**.
3. Upload the row's start image (`runway_kit/epNN/epNN_cut_XXX.jpg`), paste the prompt, set the length (5 s or 10 s).
4. Generate. If a face drifts or a hand warps, generate again; budget about 1.5 takes per clip.
5. Download each clip as `cut_<id>.mp4` (the id in the sheet's Cut column, e.g. `cut_9a.mp4`) into
   `video/epNN_runway_v2/`.
6. Rows marked *still* (the Groupon screens) need no clip; the assembler uses the screen image with a slow push-in.
7. Run `python assemble_runway.py N`. It trims every clip to its exact cut length, adds the title and end cards, burns in
   the captions and lays the finished soundtrack under it: `video/off-the-clock-epNN-runway.mp4`.

Credits: about 900 (Episode 1), 1,025 (Episode 2) and 900 (Episode 3) on Gen-4 Turbo, before retakes.

## Option B: let the script call the Runway API

Needs API credit on the developer account (dev.runwayml.com → Billing), separate from any Runway subscription.

```bash
DRY=1 python runway_v2.py 1    # shows clip count and credit cost; spends nothing
python runway_v2.py 1          # renders every missing clip, 3 at a time; re-run to retry failures
python assemble_runway.py 1
```

Known behavior: Gen-4 Turbo only accepts 5 s or 10 s clips, and the API has rejected long prompts with "An unexpected
error occurred", so the script sends short prompts. Failed requests cost nothing. The account runs a few jobs at a time,
so a full episode takes a while.

## Lip-sync (not done yet)

Only on-camera speech needs it; the shot sheets mark each clip **speaks: NAME** or **closed (thought only)** and name
its voice file. After a speaking clip exists:

1. Open it in a lip-sync tool (Runway Lip Sync, sync.so, or free on a local GPU with MuseTalk or LatentSync).
2. Use `runway_kit/epNN/voice/cut_<id>.mp3` as the audio. It already starts at the clip's first frame, so no offset.
3. Save the result over `video/epNN_runway_v2/cut_<id>.mp4` and re-run `python assemble_runway.py N`. The final mix
   (`soundtrack.m4a`) carries the same dialogue at the same moments, so picture and sound stay in sync.

Episode 1 has 16 speaking clips, Episode 2 has 18 and Episode 3 has 19.

## Requirements to assemble

Python 3.11+ with `pip install imageio-ffmpeg` (it brings its own ffmpeg). On a fresh clone the assembler reads the
kit's `timing.json` and `soundtrack.m4a` automatically. No API keys are needed to assemble.

## Rebuild from scratch

```bash
python build_v2.py
python screens.py
V2=1 python gen_voices.py 1 && V2=1 python animatic.py 1 && python mix_v3.py 1
```

`gen_voices.py` and `mix_v3.py` cache every generated take, effect and music cue, so re-running costs no ElevenLabs
credits unless a line, delivery cue or cue prompt changed.
