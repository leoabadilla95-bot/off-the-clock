# Episode 2: Bullseye · Runway shot sheet

Make each clip in the Runway web app with **Gen-4 Turbo**, image to video, ratio **720:1280 (9:16)**.
Upload the start image, paste the prompt, set the length, generate, and download the clip as `cut_<id>.mp4` into
`video/ep02_runway_v2/`. Then run `python assemble_runway.py 2` to cut it with the soundtrack and captions.
Keep prompts short: Runway's API rejected the long versions. Rows marked *still* need no clip.
For lip-sync, pair a finished clip with its `voice/cut_<id>.mp3` (on-camera speech only, starting at the clip's first
frame) in Runway Lip Sync or any lip-sync tool. `soundtrack.m4a` is the finished mix the assembler lays under the cut.

| Cut | Start image | Prompt | Runway length | Trim to | Mouth | Voice for lip-sync |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `ep02_cut_001.jpg` | An axe tumbles end over end toward the target, sawdust hanging in the light. Subtle, natural motion. Lips stay closed. | 5 s | 3 s | closed (thought only) | — |
| 2 | `ep02_cut_002.jpg` | Priya mid-stride, mid-word. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3 s | speaks: Priya | `voice/cut_2.mp3` |
| 3 | `ep02_cut_003.jpg` | Priya pivots without missing a beat, a too-bright smile, waving vaguely at the elevators. Subtle, natural motion. Mouth moves as they talk. | 10 s | 8.25 s | speaks: Priya | `voice/cut_3.mp3` |
| 4a | `ep02_cut_04a.jpg` | Hunter stands up too fast; the chair rolls back behind him. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3 s | speaks: Hunter | `voice/cut_4a.mp3` |
| 4b | `ep02_cut_04b.jpg` | Abby watches him go, mug halfway to her mouth, one eyebrow climbing. Subtle, natural motion. Lips stay closed. | 5 s | 4 s | closed (thought only) | — |
| 5a | `ep02_cut_05a.jpg` | The doors open on 22. Grant is leaning in the doorway, coffee in hand, as if he's been waiting a while. Subtle, natural motion. Mouth moves as they talk. | 10 s | 6.75 s | speaks: Grant | `voice/cut_5a.mp3` |
| 5b | `ep02_cut_05b.jpg` | Priya, tablet hugged to her chest, smiling much too hard. Subtle, natural motion. Mouth moves as they talk. | 10 s | 5.25 s | speaks: Priya | `voice/cut_5b.mp3` |
| 6 | `ep02_cut_006.jpg` | Abby's monitor: the invite now reads Promotion review · POSTPONED · Office of the COO. Subtle, natural motion. Lips stay closed. | 5 s | 3.5 s | closed (thought only) | — |
| 7 | `ep02_cut_007.jpg` | Across the desks, Hunter sees her face drop. He knows exactly whose office that is. Subtle, natural motion. Lips stay closed. | 5 s | 3.5 s | closed (thought only) | — |
| 8 | `ep02_cut_008.jpg` | Match cut from a glass wall to red brick, neon and wet street. Subtle, natural motion. Lips stay closed. | 5 s | 3 s | no dialogue | — |
| 9 | `ep02_cut_009.jpg` | Abby holds up her phone, screen away from camera; the scanner beeps. Subtle, natural motion. Mouth moves as they talk. | 10 s | 5.5 s | speaks: Abby | `voice/cut_9.mp3` |
| 10 | `ep02_cut_010.jpg` | Hunter pulls a thick fold of hundreds in a silver money clip, earnest. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3 s | speaks: Hunter | `voice/cut_10.mp3` |
| 11 | `ep02_cut_011.jpg` | The staffer stares at the cash, completely still. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4 s | speaks: Staffer | `voice/cut_11.mp3` |
| 12a | `ep02_cut_12a.jpg` | The secret shot, framed a little too close: he tucks the cash away too fast. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4.25 s | speaks: Abby, Hunter | `voice/cut_12a.mp3` |
| 12b | `ep02_cut_12b.jpg` | Reverse on Abby, arms folded, amused and suspicious. Subtle, natural motion. Lips stay closed. | 10 s | 6 s | closed (thought only) | — |
| 13 | `ep02_cut_013.jpg` | The watch twist. Subtle, natural motion. Lips stay closed. | 5 s | 2 s | closed (thought only) | — |
| 14 | `ep02_cut_014.jpg` | Three throws clatter off the target. Abby is bent over, crying with laughter. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4 s | speaks: Abby | `voice/cut_14.mp3` |
| 15a | `ep02_cut_15a.jpg` | Abby steps behind him, one hand on his shoulder, fixing his elbow. Subtle, natural motion. Mouth moves as they talk. | 10 s | 5.75 s | speaks: Abby | `voice/cut_15a.mp3` |
| 15b | `ep02_cut_15b.jpg` | Hunter, listening, jaw relaxing; she's very close. Subtle, natural motion. Lips stay closed. | 10 s | 7.5 s | closed (thought only) | — |
| 16 | `ep02_cut_016.jpg` | Hunter exhales and his eyes close. Subtle, natural motion. Lips stay closed. | 5 s | 2 s | no dialogue | — |
| 17 | `ep02_cut_017.jpg` | The axe from the opening turns in the air. THUNK: bullseye. Subtle, natural motion. Lips stay closed. | 5 s | 3 s | no dialogue | — |
| 18 | `ep02_cut_018.jpg` | Hunter spins toward her, laughing, loud and real. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3 s | speaks: Hunter | `voice/cut_18.mp3` |
| 19 | `ep02_cut_019.jpg` | Abby, hands on her head, beanie pushed back. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3 s | speaks: Abby | `voice/cut_19.mp3` |
| 20a | `ep02_cut_20a.jpg` | Later. Beers in plastic cups, a basket of fries. Subtle, natural motion. Mouth moves as they talk. | 10 s | 5.5 s | speaks: Hunter, Abby | `voice/cut_20a.mp3` |
| 20b | `ep02_cut_20b.jpg` | Reverse on Hunter, cup in both hands. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4.25 s | speaks: Hunter | `voice/cut_20b.mp3` |
| 20c | `ep02_cut_20c.jpg` | Hunter, chin on hand, looking at her a beat too long. Subtle, natural motion. Lips stay closed. | 5 s | 4 s | closed (thought only) | — |
| 21 | `ep02_cut_021.jpg` | The photo Abby just took of him mid-cheer (hero prop). Subtle, natural motion. Lips stay closed. | 5 s | 4 s | closed (thought only) | — |
| 22a | `ep02_cut_22a.jpg` | Jo arrives in scrubs and a denim jacket, hugs Abby, then shakes Hunter's hand a beat too long, eyes dropping to his watch. Subtle, natural motion. Mouth moves as they talk. | 5 s | 5 s | speaks: Jo | `voice/cut_22a.mp3` |
| 22b | `ep02_cut_22b.jpg` | Hunter, still mid-handshake, tight smile. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3 s | speaks: Hunter | `voice/cut_22b.mp3` |
| 23 | `ep02_cut_023.jpg` | Jo types lumen founder, then pinch-zooms a grainy 2019 conference photo: a man on a stage, from the side. Caption: Lumen founder (rarely photographed). Subtle, natural motion. Lips stay closed. | 5 s | 3 s | no dialogue | — |
| 24 | `ep02_cut_024.jpg` | Jo looks up at Hunter, then back down at the phone. Subtle, natural motion. Lips stay closed. | 5 s | 3 s | closed (thought only) | — |
| 25 | `ep02_cut_025.jpg` | Hunter laughing at something Abby said, relaxed, oblivious. Subtle, natural motion. Lips stay closed. | 5 s | 4 s | closed (thought only) | — |
| 26 | `ep02_cut_026.jpg` | Jo leans in, phone pressed face-down to her chest, eyes urgent. Freeze. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4 s | speaks: Jo | `voice/cut_26.mp3` |

**Total:** 205 seconds of Gen-4 Turbo, about 1025 credits.
