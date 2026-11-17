# Episode 1: Hunter from Ops · Runway shot sheet

Make each clip in the Runway web app with **Gen-4 Turbo**, image to video, ratio **720:1280 (9:16)**.
Upload the start image, paste the prompt, set the length, generate, and download the clip as `cut_<id>.mp4` into
`video/ep01_runway_v2/`. Then run `python assemble_runway.py 1` to cut it with the soundtrack and captions.
Keep prompts short: Runway's API rejected the long versions. Rows marked *still* need no clip.
For lip-sync, pair a finished clip with its `voice/cut_<id>.mp3` (on-camera speech only, starting at the clip's first
frame) in Runway Lip Sync or any lip-sync tool. `soundtrack.m4a` is the finished mix the assembler lays under the cut.

| Cut | Start image | Prompt | Runway length | Trim to | Mouth | Voice for lip-sync |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `ep01_cut_001.jpg` | Grant slides a tablet down black lacquer toward the head of the table. Subtle, natural motion. Mouth moves as they talk. | 5 s | 5 s | speaks: Grant | `voice/cut_1.mp3` |
| 2 | `ep01_cut_002.jpg` | Hunter at the head of the table, thumb twisting his watch. Subtle, natural motion. Lips stay closed. | 5 s | 4.25 s | closed (thought only) | — |
| 3 | `ep01_cut_003.jpg` | The tablet: RESTRUCTURE · WAVE 1 · 4TH FLOOR, PRODUCT DESIGN. Subtle, natural motion. Lips stay closed. | 5 s | 3.75 s | closed (thought only) | — |
| 4 | `ep01_cut_004.jpg` | Hunter looks up. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3 s | speaks: Hunter, Grant | `voice/cut_4.mp3` |
| 5 | `ep01_cut_005.jpg` | The watch twist. Subtle, natural motion. Lips stay closed. | 5 s | 3.5 s | closed (thought only) | — |
| 6 | `ep01_cut_006.jpg` | Hunter small in the glass atrium, walking past the blurry founder photo. Subtle, natural motion. Lips stay closed. | 10 s | 5.25 s | closed (thought only) | — |
| 7 | `ep01_cut_007.jpg` | Badge reader: HUNTER C · OPS (TEMP), beeps green. Subtle, natural motion. Lips stay closed. | 5 s | 2 s | no dialogue | — |
| 8 | `ep01_cut_008.jpg` | Hunter at a borrowed desk with a protein bar. A chair rolls into frame and bumps his. Subtle, natural motion. Lips stay closed. | 5 s | 2 s | no dialogue | — |
| 9a | `ep01_cut_09a.jpg` | Abby with her mustard mug, squinting at the bar. Subtle, natural motion. Mouth moves as they talk. | 10 s | 5.5 s | speaks: Abby | `voice/cut_9a.mp3` |
| 9b | `ep01_cut_09b.jpg` | Hunter, caught mid-chew. Subtle, natural motion. Lips stay closed. | 5 s | 2.75 s | closed (thought only) | — |
| 10a | `ep01_cut_10a.jpg` | Over Abby's shoulder. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4.25 s | speaks: Hunter | `voice/cut_10a.mp3` |
| 10b | `ep01_cut_10b.jpg` | Reverse on Abby, deadpan. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4.25 s | speaks: Abby | `voice/cut_10b.mp3` |
| 10c | `ep01_cut_10c.jpg` | Abby's eyes drop to his wrist, then back up with a smile. Subtle, natural motion. Lips stay closed. | 5 s | 4.75 s | closed (thought only) | — |
| 11 | `ep01_cut_011.jpg` | Abby slides half her torta across the desk. Subtle, natural motion. Mouth moves as they talk. | 5 s | 5 s | speaks: Abby | `voice/cut_11.mp3` |
| 12 | `ep01_cut_012.jpg` | Abby's monitor: a calendar invite, Promotion review · Fri 9:00. Subtle, natural motion. Lips stay closed. | 5 s | 4.5 s | closed (thought only) | — |
| 13a | `ep01_cut_13a.jpg` | They eat standing at the counter. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3.25 s | speaks: Abby | `voice/cut_13a.mp3` |
| 13b | `ep01_cut_13b.jpg` | Reverse on Hunter. Subtle, natural motion. Mouth moves as they talk. | 5 s | 5 s | speaks: Hunter, Abby | `voice/cut_13b.mp3` |
| 13c | `ep01_cut_13c.jpg` | Reverse on Abby. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4 s | speaks: Abby | `voice/cut_13c.mp3` |
| 13d | `ep01_cut_13d.jpg` | Hold on Abby, grinning. Subtle, natural motion. Mouth moves as they talk. | 5 s | 2.5 s | speaks: Abby | `voice/cut_13d.mp3` |
| 14a | `ep01_cut_14a.jpg` | A slow push-in. Subtle, natural motion. Lips stay closed. | 5 s | 5 s | closed (thought only) | — |
| 14b | `ep01_cut_14b.jpg` | Hold on Hunter. A long pause. Subtle, natural motion. Lips stay closed. | 5 s | 4 s | closed (thought only) | — |
| 14c | `ep01_cut_14c.jpg` | Hold. Subtle, natural motion. Mouth moves as they talk. | 10 s | 5.75 s | speaks: Hunter | `voice/cut_14c.mp3` |
| 15 | *still:* `img/screens/e01_feed.jpg` | Groupon app screen, no clip | — | 4.25 s | — | — |
| 16 | *still:* `img/screens/e01_deal.jpg` | Groupon app screen, no clip | — | 2 s | — | — |
| 17a | `ep01_cut_17a.jpg` | Abby turns the phone to him. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4 s | speaks: Abby | `voice/cut_17a.mp3` |
| 17b | `ep01_cut_17b.jpg` | Reverse on Hunter, cornered. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4 s | speaks: Hunter | `voice/cut_17b.mp3` |
| 17c | `ep01_cut_17c.jpg` | Hold on Hunter. Subtle, natural motion. Lips stay closed. | 5 s | 4 s | closed (thought only) | — |
| 17d | `ep01_cut_17d.jpg` | Reverse on Abby. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3 s | speaks: Abby | `voice/cut_17d.mp3` |
| 17e | `ep01_cut_17e.jpg` | Hunter, a beat, then a helpless half-smile. Subtle, natural motion. Mouth moves as they talk. | 5 s | 2 s | speaks: Hunter | `voice/cut_17e.mp3` |
| 18 | *still:* `img/screens/e01_voucher.jpg` | Groupon app screen, no clip | — | 2 s | — | — |
| 19 | `ep01_cut_019.jpg` | Hunter alone at the desk with the shared voucher. He reads it twice and smiles. Golden light through the blinds. Subtle, natural motion. Lips stay closed. | 10 s | 6 s | closed (thought only) | — |
| 20 | `ep01_cut_020.jpg` | In his open bag, the corner of the tablet: WAVE 1 · 4TH FLOOR. Subtle, natural motion. Lips stay closed. | 5 s | 2 s | closed (thought only) | — |
| 21 | `ep01_cut_021.jpg` | Elevator doors open; Priya rushes out with a tablet, scanning the floor. Subtle, natural motion. Lips stay closed. | 5 s | 3 s | no dialogue | — |
| 22 | `ep01_cut_022.jpg` | Priya spots him, relieved, and calls across the floor. Subtle, natural motion. Mouth moves as they talk. | 5 s | 2 s | speaks: Priya | `voice/cut_22.mp3` |
| 23 | `ep01_cut_023.jpg` | Hunter's eyes go wide. Rack focus to Abby turning around. Freeze. Subtle, natural motion. Lips stay closed. | 5 s | 4 s | closed (thought only) | — |

**Total:** 180 seconds of Gen-4 Turbo, about 900 credits.
