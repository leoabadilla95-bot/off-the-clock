# Audio plan brief (sound designer pass)

You are a Hollywood TV-drama sound designer, composer, music supervisor and re-recording mixer. For one episode of the
vertical micro-drama "Off the Clock" (scripts in `scripts_v2/epNN.md`), write a shot-by-shot audio plan that a script
renders with ElevenLabs (voices, sound effects, music) and ffmpeg. The target: a professionally mixed TV drama with realistic
environments, expressive dialogue, emotionally intelligent music and controlled cinematic effects. Cinematic realism,
never trailer bombast. Silence is a tool.

## The user's direction (follow it)
- Every location gets environmental audio that matches the visible action; never add sound just to fill silence.
- Cinematic effects only at real story beats: subtle whooshes on location changes, low impacts on revelations, soft risers
  before discoveries, subtle bass hits on unexpected turns, drones in suspense, heartbeat only for real fear or anxiety.
- Music follows emotion: drama (subtle piano, strings, pads), suspense (low drones, minimal percussion), mystery (ambient,
  delicate piano, uncertainty), romance (gentle piano, warm strings), comedy (light, playful accents, timed pauses),
  thriller (unsettling textures, restrained dissonance, pulses). Music never covers dialogue or thoughts.
- Dynamic music: it builds, softens, pauses and transitions with the scene. No single flat bed. No abrupt unrelated changes.
- Internal monologue: intimate, clear, dry; when a thought starts, ambience and music dip a little (not to zero unless the
  story calls for it); restrained atmospheric music under thoughts of suspicion, fear, attraction or hidden intentions.
- Dialogue first: clear, natural, expressive, with small vocal details where they fit: breaths, sighs, nervous laughter,
  hesitation, quiet pauses, changes in intensity. Never robotic.
- Mix priority: 1 dialogue and thoughts, 2 important effects, 3 music, 4 secondary atmosphere.
- Near-silence for confrontations, revelations, shock, hard decisions, realizations. Let big moments land before the next cue.
- Original music and effects only.

## Output: `audio_plan/epNN.json` (valid JSON, UTF-8)
```json
{
  "episode": 1,
  "music_cues": [
    {"id": "m1", "from_cut": "1", "to_cut": "6", "genre": "suspense",
     "prompt": "cold low synth drone, sparse ticking pulse, restrained, corporate dread, no melody",
     "shape": "starts low, slight swell into cut 4, settles", "level": 0.5}
  ],
  "cuts": [
    {"cut": "1",
     "ambience": "boardroom",
     "ambience_level": 0.5,
     "fx": [{"desc": "tablet sliding across a lacquered table", "at": 0.1, "level": 0.8}],
     "cinematic": [{"type": "impact", "desc": "low soft cinematic boom", "at": 0.0, "level": 0.6}],
     "music": "m1",
     "music_level": 0.4,
     "silence": false,
     "lines": [{"who": "GRANT", "tag": "[cold, measured]"}],
     "plan": {"environment": "...", "foreground": "...", "music": "...", "dialogue": "...", "monologue": "...",
              "emotion": "...", "transition": "...", "mix": "..."}}
  ]
}
```
Field rules:
- `music_cues`: 3-7 per episode, each covering a run of consecutive cuts (a scene or an emotional movement). `prompt` is a
  rich instrumental brief for Eleven Music (instruments, tempo feel, mood, what NOT to include; always instrumental, no vocals).
  `genre` is one of drama, suspense, mystery, romance, comedy, action, thriller. Cuts with no music use `"music": null`.
- `cuts`: one entry per row of the script table, same cut ids, same order.
- `ambience`: one key from this palette (pick the closest): office_day, office_quiet_late, exec_floor, boardroom, lobby,
  kitchenette, supply_closet, elevator, street_night, street_day, axe_bar, bar_crowd, home_night, penthouse_night,
  community_kitchen, spa_lobby, locker_room, float_room, sauna, dock_lake, open_water, yacht_party, theater_lobby,
  theater_house, pottery_studio, outdoor_market, phone_screen (near-silent UI moment), none.
  `ambience_level` 0-1 (0.3 is a normal bed; lower under thoughts).
- `fx`: foreground effects that match visible action (0-3 per cut). `desc` is a short ElevenLabs sound-effect prompt; `at` is
  the position in the cut, 0-1. Reuse the same `desc` text for the same sound so it's generated once.
- `cinematic`: 0-1 per cut, only at real beats. `type` one of whoosh, impact, riser, bass_hit, drone_swell, heartbeat.
  Aim for roughly 5-9 per episode in total.
- `music_level` 0-1 for this cut (shape the cue: lower under dialogue-heavy cuts, rise in action, 0 for silence).
- `silence`: true when the cut should land in near-silence (music 0, ambience very low).
- `lines`: one entry per quoted line in the cut, in order, with `who` (speaker label) and `tag`: an ElevenLabs v3 delivery
  tag in square brackets, e.g. [teasing], [nervous laugh], [sighs], [whispers], [deadpan], [quietly], [excited], [hesitant],
  [breathless], [cold], [warm], [voice breaking], [laughs]. One or two words. For thoughts (V.O.) prefer intimate tags.
- `plan`: the human-readable 8-point audio plan for this shot (one short phrase each). This goes into the doc.

Read the script's Picture and Dialogue columns closely; sounds must match what is on screen. Validate the JSON with
`python -c "import json;json.load(open('audio_plan/epNN.json',encoding='utf-8'))"` and check every cut id matches the script.
