# Episode 3: Masa · Runway shot sheet

Make each clip in the Runway web app with **Gen-4 Turbo**, image to video, ratio **720:1280 (9:16)**.
Upload the start image, paste the prompt, set the length, generate, and download the clip as `cut_<id>.mp4` into
`video/ep03_runway_v2/`. Then run `python assemble_runway.py 3` to cut it with the soundtrack and captions.
Keep prompts short: Runway's API rejected the long versions. Rows marked *still* need no clip.
For lip-sync, pair a finished clip with its `voice/cut_<id>.mp3` (on-camera speech only, starting at the clip's first
frame) in Runway Lip Sync or any lip-sync tool. `soundtrack.m4a` is the finished mix the assembler lays under the cut.

| Cut | Start image | Prompt | Runway length | Trim to | Mouth | Voice for lip-sync |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `ep03_cut_001.jpg` | Lupe points her wooden spoon dead at the lens. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3 s | speaks: Lupe | `voice/cut_1.mp3` |
| 2 | `ep03_cut_002.jpg` | Jo, low, phone pressed to her chest. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3 s | speaks: Jo | `voice/cut_2.mp3` |
| 3a | `ep03_cut_03a.jpg` | Abby leans over Jo's shoulder, chin on her hand, unimpressed. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4.5 s | speaks: Abby | `voice/cut_3a.mp3` |
| 3b | `ep03_cut_03b.jpg` | Jo, squinting, not letting it go. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4.5 s | speaks: Jo | `voice/cut_3b.mp3` |
| 4 | `ep03_cut_004.jpg` | Hunter at the counter, paying for fries in cash, overhears. His hand drifts up to his ear. The watch. Subtle, natural motion. Lips stay closed. | 5 s | 3 s | closed (thought only) | — |
| 5 | `ep03_cut_005.jpg` | Abby laughs, steals a fry, then glances at Hunter's back a second too long. Subtle, natural motion. Mouth moves as they talk. | 10 s | 5.75 s | speaks: Abby | `voice/cut_5.mp3` |
| 6 | `ep03_cut_006.jpg` | Match cut, glass to brick. Abby on the couch under string lights; the fridge behind her is papered with vouchers, the Bullseye one pinned on top. Subtle, natural motion. Lips stay closed. | 5 s | 3 s | no dialogue | — |
| 7 | *still:* `img/screens/e03_classes.jpg` | Groupon app screen, no clip | — | 3.5 s | — | — |
| 8 | `ep03_cut_008.jpg` | Hunter alone at the island. A takeout bag. A cookware set still sealed in plastic. He types, then winces at her reply. Subtle, natural motion. Lips stay closed. | 5 s | 3 s | closed (thought only) | — |
| 9a | `ep03_cut_09a.jpg` | Doña Lupe grabs Abby's face in both floury hands. Hunter hangs back, hands in pockets. Subtle, natural motion. Mouth moves as they talk. | 5 s | 5 s | speaks: Lupe | `voice/cut_9a.mp3` |
| 9b | `ep03_cut_09b.jpg` | Hunter, startled to be noticed, a small surprised laugh. Subtle, natural motion. Lips stay closed. | 5 s | 4 s | closed (thought only) | — |
| 10 | `ep03_cut_010.jpg` | Hunter's hands. The husk tears and masa squeezes out everywhere. Subtle, natural motion. Lips stay closed. | 5 s | 2 s | no dialogue | — |
| 11a | `ep03_cut_11a.jpg` | Lupe grabs his wrist and turns his hand palm up, like evidence. Subtle, natural motion. Mouth moves as they talk. | 5 s | 5 s | speaks: Lupe | `voice/cut_11a.mp3` |
| 11b | `ep03_cut_11b.jpg` | Hunter, masa on his fingers, listening, then looking up, already scraping it off. Subtle, natural motion. Mouth moves as they talk. | 10 s | 7 s | speaks: Hunter | `voice/cut_11b.mp3` |
| 12 | `ep03_cut_012.jpg` | Hunter freezes. "It all falls apart" lands somewhere. Subtle, natural motion. Lips stay closed. | 5 s | 3.5 s | closed (thought only) | — |
| 13a | `ep03_cut_13a.jpg` | Abby bumps his shoulder with hers, grinning. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4 s | speaks: Abby | `voice/cut_13a.mp3` |
| 13b | `ep03_cut_13b.jpg` | Lupe, hands on hips, her eyes moving from his hands to his face as he watches Abby. Subtle, natural motion. Lips stay closed. | 5 s | 5 s | closed (thought only) | — |
| 14 | `ep03_cut_014.jpg` | Abby's hands over his, guiding a fold, then a tie. A lopsided tamale (hero prop). Flour on his navy quarter-zip. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3 s | speaks: Abby | `voice/cut_14.mp3` |
| 15a | `ep03_cut_15a.jpg` | Shoulder to shoulder on stools by the steamer, steam rolling between them and the lens. Subtle, natural motion. Mouth moves as they talk. | 10 s | 7 s | speaks: Abby, Hunter | `voice/cut_15a.mp3` |
| 15b | `ep03_cut_15b.jpg` | Abby, soft, laughing at the memory. Subtle, natural motion. Mouth moves as they talk. | 10 s | 7 s | speaks: Abby | `voice/cut_15b.mp3` |
| 16 | `ep03_cut_016.jpg` | Hunter looks down at his floury hands. Subtle, natural motion. Mouth moves as they talk. | 10 s | 7 s | speaks: Hunter | `voice/cut_16.mp3` |
| 17 | `ep03_cut_017.jpg` | His messenger bag on the next stool, flour-dusted. The corner of the tablet peeks out: WAVE 1 · 4TH FLOOR. Subtle, natural motion. Lips stay closed. | 5 s | 5 s | closed (thought only) | — |
| 18a | `ep03_cut_18a.jpg` | Abby holds up his steamed tamale like a trophy. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4 s | speaks: Abby | `voice/cut_18a.mp3` |
| 18b | `ep03_cut_18b.jpg` | Hunter, laughing at it. Subtle, natural motion. Mouth moves as they talk. | 5 s | 3.75 s | speaks: Hunter | `voice/cut_18b.mp3` |
| 18c | `ep03_cut_18c.jpg` | Back on Abby, the smile catching in her throat. Subtle, natural motion. Lips stay closed. | 5 s | 3 s | closed (thought only) | — |
| 19 | `ep03_cut_019.jpg` | Hunter stands up a little too loud, one masa hand raised; the class turns. Subtle, natural motion. Mouth moves as they talk. | 10 s | 5.75 s | speaks: Hunter, Lupe | `voice/cut_19.mp3` |
| 20 | `ep03_cut_020.jpg` | A black card taps the reader. DECLINED. Subtle, natural motion. Lips stay closed. | 5 s | 2 s | no dialogue | — |
| 21 | `ep03_cut_021.jpg` | His phone rings. Masa on both hands, he elbows it and it goes on speaker. Subtle, natural motion. Lips stay closed. | 5 s | 3 s | closed (thought only) | — |
| 22a | `ep03_cut_22a.jpg` | The phone face up on the counter, masa smeared on the glass. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4 s | speaks: Bank | `voice/cut_22a.mp3` |
| 22b | `ep03_cut_22b.jpg` | The whole room frozen mid-motion, every head turned to the phone. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4 s | speaks: Bank | `voice/cut_22b.mp3` |
| 23 | `ep03_cut_023.jpg` | Abby, flour on her cheek, smile gone, eyes narrowing. Freeze. Subtle, natural motion. Mouth moves as they talk. | 5 s | 4 s | speaks: Abby | `voice/cut_23.mp3` |

**Total:** 180 seconds of Gen-4 Turbo, about 900 credits.
