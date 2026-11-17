# Off the Clock

**The Billionaire CEO Is Pretending to Be the New Guy, and the Girl Who Feeds Him Lunch Has No Idea She's on His Layoff List**

A 10-episode vertical (9:16) AI micro-drama, written as a spec pitch for Groupon. Episodes 1–3 are in production.
Hunter Cole, the founder of Lumen, goes undercover on his own 4th floor while deciding a 200-job layoff that starts with
the design team. Abby Reyes, a designer on that team, adopts "the sad new guy" and takes him on cheap dates she finds on
Groupon. The audience knows her job is on his desk; she doesn't.

The full production spec (scripts, storyboards, Lookbook, audio plans, captions) lives in the shared Claude doc. This
repo holds the files and the pipeline that build the episodes from it.

## Start here

- **Watch:** `deliverables/off-the-clock-ep01-v3.mp4`, `ep02`, `ep03` (previs with full sound; turn the sound on).
- **Make Episodes 1–3:** follow [EPISODES_1-3.md](EPISODES_1-3.md). It covers making the clips on Runway by hand
  (with the shot sheets in `runway_kit/`) or through the API, then assembling them with the finished soundtrack.

## What's here

| Path | What it is |
| --- | --- |
| `deliverables/` | Episodes 1–3 as finished previs videos (v2 scripts, voices, sound design, captions burned in) and their `.srt` caption files |
| `runway_kit/` | Per-episode Runway shot sheets (`SHOT_SHEET.md`) and start images named by cut, for Episodes 1–3 |
| `EPISODES_1-3.md` | Step-by-step instructions to take Episodes 1–3 from previs to Runway motion and lip-sync |
| `scripts_v2/` | The v2 scripts for all 10 episodes, plus `SPINE_AND_BRIEF.md` (season engine, monologue and dialogue rules) |
| `audio_plan/` | Shot-by-shot sound design for Episodes 1–3 (`BRIEF.md` is the sound-designer brief) |
| `captions_v2/` | Caption files timed to the recorded performances (`*-final.srt` include the 2 s title card) |
| `packs_hand/` | v1 production packs: keyframe prompts, locations, props, wardrobe (the dialogue in them is v1) |
| `img/` | Cast sheets, location plates, keyframes (`eNN_key_shot_S.jpg`), v2 frames (`v2_eNN_<cut>.jpg`), Groupon screens (`screens/`), contact sheets (`sheets/`), title and end cards |
| `tables_v2.json` | The v2 script tables in machine form (cut, scene, shot, seconds, picture, dialogue, Key) |
| `voices.json` | ElevenLabs voice IDs for the 14 designed voices (account-specific) |
| `animatics.html` | The animatics page published as a Claude artifact |

## How a cut is described

Script tables (`scripts_v2/epNN.md`) have one row per cut. `NAME: "…"` is spoken on camera and must lip-sync;
`NAME (V.O.): "…"` is an internal thought (voiceover, no lip movement, captioned in italics). The **Key** column says
which picture the cut uses: `eNN:S` = that episode's shot S keyframe, `plate:` = an empty location, `new:` = a v2 frame,
`screen:` = a mock Groupon app screen.

## Pipeline (Episodes 1–3)

Run from this folder on Windows with Python 3.11+ (`numpy`, `Pillow`, `imageio-ffmpeg`).

```bash
python build_v2.py                 # scripts_v2/*.md -> tables_v2.json
python v2_jobs.py && python gen_agnes.py 1 3   # generate any new keyframes (Agnes AI, free)
python screens.py                  # draw the mock Groupon screens
V2=1 python gen_voices.py 1        # ElevenLabs voices with delivery tags; cuts timed to the performance; captions
V2=1 python animatic.py 1          # picture cut from the Key column
python mix_v3.py 1                 # ambience, effects, scene-by-scene music, ducking, loudness -> final animatic
python runway_v2.py 1              # optional: animate each cut with Runway Gen-4 Turbo (paid)
python assemble_runway.py 1        # optional: cut the Runway clips with the soundtrack and captions
```

### Keys

No keys are stored in this repo. The scripts read them from Windows user environment variables; the `set_*_key.ps1`
helpers prompt for a key with hidden input and save it there:
`AGNES_API_KEY` (images and video, free), `ELEVENLABS_API_KEY` (voices, music, effects),
`RUNWAYML_API_SECRET` (video), `LUMAAI_API_KEY`, `OPENAI_API_KEY` (optional).

### Costs seen so far

- Keyframes: Agnes AI, free (Figma and Canva credits were used for the first batch).
- Voices, music, effects: ElevenLabs Creator plan.
- Runway Gen-4 Turbo: 5 credits ($0.05) per second, 5 s or 10 s clips; Episode 1 is about 900 credits.
- Wan 2.2 (local, via Wan2GP) also works on an 8 GB RTX 2060 Super at about 2 minutes per clip.

## Status

- Episodes 1–3: previs complete with full sound. Lip-sync not done yet.
- Episodes 4–10: v2 scripts written; not in production.
- Music is temp (AI-generated). Per the licensing plan in the spec, the series theme should be commissioned.
