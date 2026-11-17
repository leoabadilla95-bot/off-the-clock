# Brief: hand-written production packs (shared by all helper agents)

Doc: Claude Doc "Groupon: Off the Clock", project id 7fca9098-aa58-47fa-8818-d80c8dedab97.
Container for every doc call: {"kind":"project","id":"7fca9098-aa58-47fa-8818-d80c8dedab97"}.
Doc tools: mcp__1a59c906-04da-521d-bda7-7f71b9f9e01c__read and mcp__1a59c906-04da-521d-bda7-7f71b9f9e01c__update
(load with ToolSearch "select:mcp__1a59c906-04da-521d-bda7-7f71b9f9e01c__read,mcp__1a59c906-04da-521d-bda7-7f71b9f9e01c__update" if needed).

## Goal
Replace the auto-generated production pack for your episode(s) with a HAND-WRITTEN pack in exactly the style of the
Episode 1 pack. The auto pack reads like a template ("Medium close-up: X. Location, light. Vertical 9:16...").
Yours must read like a director's shot prompts: specific framing, lens, expression, wardrobe, props, light, background
action, and a specific performance/motion note per cut.

## Inputs
1. STYLE REFERENCE: the Episode 1 pack tab. Read it with
   read(ref={"object":"node","id":"ea7e3c50-ad1a"}, engine="prose", container=C, payload={"kind":"view"})
   (if the result is saved to a file because it is large, read that file). Match its structure, tone and level of detail.
2. SOURCE OF TRUTH for your episode: packs/epN.md in this folder
   (C:/Users/kybel/AppData/Local/Temp/claude/ddd1136be54bb0d9/04aeff73-fb3e-41bd-a472-6a4105c5a286/scratchpad/packs/epN.md).
   It has every cut with its number, start time, length, location, picture note, tool, and the exact dialogue,
   plus new-cast descriptors, wardrobe/continuity and the screens list.
   NEVER change cut numbers, start times, lengths, or dialogue words. Only rewrite the prompts and notes around them.

## Locked descriptors (paste these where a prompt uses the token; the pack may say "[HUNTER]" and define it in Step 1)
- [HUNTER]: A man in his early 30s, tall and lean with slightly hunched shoulders, short dark hair in a neat side part, clean-shaven, tired but kind eyes, plain steel wristwatch on his left wrist, navy quarter-zip over a white tee, no logos, understated, natural skin texture
- [ABBY]: A Mexican-American woman in her late 20s, long dark wavy hair half-up in a tortoiseshell claw clip, large gold hoop earrings, warm expressive face with an easy grin, mustard-yellow knit beanie, thrifted oversized cardigan in warm tones, natural skin texture
- [PRIYA]: A South Asian woman in her mid-30s, sleek low bun, fitted black blazer over a white blouse, holding a tablet, sharp and efficient, natural skin texture
- New characters: use the descriptors in Step 1 of the episode's auto pack (Jo, Lupe, Grant, Celeste, etc.).
Wardrobe changes by episode are in each auto pack's continuity note (e.g. olive overshirt from Episode 5, rust sweater in Episode 10) — adjust the Hunter descriptor's clothing words accordingly and say so in Step 1.

## Required structure (Markdown)
# Episode N production pack: "Title"
One-paragraph intro (runtime, cut count, how to work: references -> keyframes -> animate -> voices -> assemble; tokens mean the locked descriptors).
## Step 1: Lock the references
  ### Characters  (table: Reference | What to generate | Locked descriptor — include only characters in this episode; returning ones may say "same sheet as Episode 1/2/..." and give wardrobe changes)
  ### Locations (empty plates, no people)  (table: Reference | Prompt — hand-written, specific)
  ### Props and screens  (bullets: hero props, phone plates, inserts to build)
## Step 2: Shot by shot
  Short intro paragraph (same as Episode 1's).
  One "### Shot N · m:ss · SHOT TYPE · Ns · Place" section per shot NUMBER, in order (start time and total length of the shot;
  for split shots add the cut breakdown in the heading, e.g. "· 13s (8a 3s two-shot, 8b 4s Hunter, 8c 4s Abby, 8d 2s Abby)").
  Bullets inside each section, like Episode 1:
  - **Keyframe:** *italic, specific image prompt* (for split shots give one keyframe per cut: **Keyframe 8a:**, **Keyframe 8b:** …)
  - **Video (Tool):** *italic motion/performance prompt* (tools: Veo 3.1 for dialogue faces, Kling for body motion/handheld/crowds, Runway for push-ins, whips, cranes, high/low angles; screens are composites)
  - **Line(s):** exact dialogue from the source, speaker in caps, per cut if split
  - **Audio:** music/sound for that moment (when relevant)
  - **Post:** on-screen text, composites, freezes (when relevant)
## Step 3: Voices
  Short paragraph; table of any NEW voices for this episode (Voice | Voice Design description); returning voices: "use the saved voice IDs".
  ### Every line, in order  (table: # | Cut | Who | Line | Delivery — delivery notes hand-written)
## Step 4: Screens and inserts
  Table: Screen | Used in | What's on it (specific copy, prices, layout). Groupon screens follow Episode 1's mock style
  (bright green accent, white cards, generic wordmark, made-up businesses, regular price struck through). Include texts, notifications, documents.
## Step 5: Assembly and checks
  Numbered steps like Episode 1 (lay picture with the full cut-length list in order, composite, lip-sync, grade, music and sound cues, text and captions, export),
  then "### Final checks" as a - [ ] checklist specific to the episode (wardrobe, watch, props, legibility, runtime, ending).

## Writing rules
- Plain, specific, cinematic English. No filler. Every prompt names the framing, subject, action, light and background.
- Keep the color script: office = cool steel-blue fluorescent; outings = warm (Edison bulbs, golden hour, tungsten); penthouse = cold, empty.
- Hero props and motifs must appear where the script has them (the watch twist, the sticky note, the fridge, the rust sweater, etc.).
- Do not invent new dialogue or new shots.

## Writing it into the doc
1. Save your finished Markdown to packs_hand/epN.md in the scratchpad folder.
2. Read the existing tab body outline: read(ref={"object":"node","id":"<BODY ID>"}, engine="prose", container=C, payload={"projection":"outline"}).
   Collect the full ids of ALL top-level blocks (ids print short after the first, e.g. '.45' means '<session>.45' — expand them) and the rev.
3. One update call on that body with two ops, in this order:
   {"op":"insert","target":{"kind":"root"},"side":"end","source":{"as":"markdown","from":{"kind":"inline","content":"<YOUR MARKDOWN>"}}}
   {"op":"delete","target":{"kind":"blocks","ids":[<all old top-level ids>]},"ifRev":<rev from step 2>}
   If refused, read the refusal and fix only the request shape; never use force.
4. Re-read the outline and confirm the first heading is your "# Episode N production pack" and no old auto-pack blocks remain.

Body node ids: Ep2 3218af12-59f7 · Ep3 009e7352-5a74 · Ep4 327edba3-d4a0 · Ep5 4588c1a5-d31c · Ep6 7b35a071-2b2d · Ep7 0e9ddb3c-0be0 · Ep8 6d511adb-88cb · Ep9 491188c3-6e75 · Ep10 d9b8434b-bf50

## Report back (short)
Per episode: written to doc yes/no, number of shot sections, any refusals verbatim, anything you could not do.
