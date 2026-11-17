"""mix_v3.py <ep>: render the shot-by-shot audio plan (audio_plan/epNN.json) into a TV-drama mix.
Stems: dialogue + thoughts (from gen_voices V2), room ambience per location, foreground effects, cinematic accents, and
music cue by cue with a per-cut level curve. Music and ambience duck under speech and dip further under thoughts; silence
cuts drop to near-nothing. Output: audio_v2/epNN_mix_v3.wav and anim_v2/off-the-clock-epNN-v3.mp4 (animatic + mix).
All generated audio is cached under audio_v2/sfx and audio_v2/music, so re-mixing costs no credits."""
import hashlib, json, os, re, subprocess, sys, urllib.request, wave, winreg
import numpy as np
import imageio_ffmpeg
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
KEY = os.environ.get("ELEVENLABS_API_KEY") or winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), "ELEVENLABS_API_KEY")[0]
SR, LEAD, TAIL = 44100, 2.0, 3.0
ep = int(sys.argv[1])
A = os.path.join(D, "audio_v2")
for sub in ("sfx", "music"):
    os.makedirs(os.path.join(A, sub), exist_ok=True)

AMBIENCE = {  # room-tone and activity beds, generated once each as 22 s loops
    "office_day": "open-plan tech office ambience, soft keyboard typing, distant murmured conversations, air conditioning hum, occasional notification ping",
    "office_quiet_late": "nearly empty office after hours, low air conditioning hum, a distant vacuum, one keyboard far away",
    "exec_floor": "quiet executive floor, deep HVAC hum, muffled footsteps on carpet, distant elevator",
    "boardroom": "silent glass boardroom room tone, faint HVAC hum, tense stillness",
    "lobby": "large glass atrium lobby, footsteps echoing on polished concrete, badge turnstile beeps, distant chatter",
    "kitchenette": "small office kitchenette, coffee machine hiss, fridge hum, distant office chatter",
    "supply_closet": "tiny supply closet room tone, muffled office outside the door, fluorescent buzz",
    "elevator": "elevator interior hum, cables, soft mechanical whir",
    "street_night": "Chicago street at night, light traffic passing on wet pavement, distant L train, a few voices",
    "street_day": "Chicago street daytime, traffic, birds, footsteps, distant conversations",
    "axe_bar": "axe throwing bar, axes thudding into wood in other lanes, rock music muffled far away, crowd chatter and laughter",
    "bar_crowd": "busy neighborhood bar, crowd chatter, glasses clinking, muffled music",
    "home_night": "cozy apartment at night, fridge hum, faint street outside the window, soft room tone",
    "penthouse_night": "vast quiet penthouse at night, deep silence, faint city hum through glass, refrigerator",
    "community_kitchen": "busy community kitchen, pots simmering, steam, spoons on bowls, Spanish chatter and laughter, radio faint",
    "spa_lobby": "calm spa lobby, soft trickling water feature, hushed voices",
    "locker_room": "spa locker room, lockers clicking, showers far away, tiled echo",
    "float_room": "float tank room, near silence, gentle water lapping, faint low hum",
    "sauna": "cedar sauna, crackling stove, soft hiss of steam",
    "dock_lake": "lake dock, gentle waves against wood, gulls, wind, kayak hulls knocking",
    "open_water": "kayaks on calm lake water, paddle drips, light wind, distant gulls",
    "yacht_party": "party yacht approaching, bass-heavy music, crowd cheering, engine",
    "theater_lobby": "small theater lobby, chatter, ticket scanner beeps",
    "theater_house": "intimate theater audience, murmurs, rustling seats, scattered laughter",
    "pottery_studio": "pottery studio, potter's wheel whirring, wet clay, quiet",
    "outdoor_market": "busy outdoor market, vendors calling, crowd, grill sizzle, brass band far away",
    "phone_screen": "near silence, faint room tone",
}
CINEMATIC = {
    "whoosh": "subtle soft cinematic whoosh transition, short, airy, not aggressive",
    "impact": "low soft cinematic impact boom, deep, restrained, short tail",
    "riser": "soft tension riser, slowly building airy synth swell, 3 seconds",
    "bass_hit": "single subtle sub bass hit, clean, short",
    "drone_swell": "dark low cinematic drone swell, ominous, restrained",
    "heartbeat": "slow heavy heartbeat, muffled, cinematic, four beats",
}

def eleven(path, body, out):
    if not os.path.exists(out):
        r = urllib.request.Request("https://api.elevenlabs.io/v1" + path, data=json.dumps(body).encode(), method="POST",
                                   headers={"xi-api-key": KEY, "Content-Type": "application/json", "User-Agent": "off-the-clock-previs/1.0"})
        data = urllib.request.urlopen(r, timeout=600).read()
        if len(data) < 1000:  # an error body or a cut-off download: don't cache it
            raise RuntimeError(f"short audio response ({len(data)} bytes) for {os.path.basename(out)}")
        open(out + ".part", "wb").write(data)
        os.replace(out + ".part", out)
    return out

def load(path):
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype="<f4").copy()

def sfx(desc, seconds=None, loop=False):
    h = hashlib.md5((desc + str(seconds) + str(loop)).encode()).hexdigest()[:10]
    body = {"text": desc, "prompt_influence": 0.5}
    if seconds:
        body["duration_seconds"] = seconds
    if loop:
        body["loop"] = True
    try:
        return load(eleven("/sound-generation?output_format=mp3_44100_128", body, os.path.join(A, "sfx", h + ".mp3")))
    except urllib.error.HTTPError:  # older accounts reject "loop"; retry without it
        body.pop("loop", None)
        return load(eleven("/sound-generation?output_format=mp3_44100_128", body, os.path.join(A, "sfx", h + ".mp3")))

def smooth(x, sec):
    n = max(1, int(sec * SR / 64))
    k = np.ones(n) / n
    small = np.convolve(x[::64], k, mode="same")
    return np.interp(np.arange(len(x)), np.arange(0, len(x), 64)[:len(small)], small)

rows = json.load(open(os.path.join(D, "tables_v2.json"), encoding="utf-8"))[str(ep)]
plan = json.load(open(os.path.join(D, "audio_plan", f"ep{ep:02d}.json"), encoding="utf-8"))
timing = dict((c, s) for c, s in json.load(open(os.path.join(A, f"ep{ep:02d}_timing.json"))))
lines = json.load(open(os.path.join(A, f"ep{ep:02d}_lines.json")))  # [[start, end, thought], ...] episode time
pc = {c["cut"]: c for c in plan["cuts"]}
starts, t = {}, 0.0
for r in rows:
    starts[r[0]] = t; t += timing.get(r[0], float(r[3]))
runtime = t
N = int((LEAD + runtime + TAIL) * SR)
pos = lambda sec: int((LEAD + sec) * SR)

# --- dialogue stem and its envelopes
dlg = load(os.path.join(A, f"ep{ep:02d}_dialogue.wav"))[:N]
dlg = np.pad(dlg, (0, N - len(dlg)))
speech = np.zeros(N, np.float32); thought = np.zeros(N, np.float32)
for s, e, th in lines:
    (thought if th else speech)[pos(s):pos(e)] = 1
speech_env, thought_env = smooth(speech, 0.25), smooth(thought, 0.35)

# --- ambience: per-cut level curve over each location's loop
amb = np.zeros(N, np.float32); level = np.zeros(N, np.float32)
beds = {}
for r in rows:
    c = pc.get(r[0], {}); key = c.get("ambience") or "none"
    if key == "none" or key not in AMBIENCE:
        continue
    if key not in beds:
        beds[key] = sfx(AMBIENCE[key], 22, loop=True)
    b = beds[key]; s0, n = pos(starts[r[0]]), int(timing.get(r[0], float(r[3])) * SR)
    amb[s0:s0 + n] = np.resize(b, n)[:max(0, N - s0)]
    lv = 0.06 if c.get("silence") else float(c.get("ambience_level", 0.3))
    level[s0:s0 + n] = lv
amb *= smooth(level, 0.3) * 0.45 * (1 - 0.35 * speech_env) * (1 - 0.45 * thought_env)

# --- foreground and cinematic effects
fx = np.zeros(N, np.float32); cine = np.zeros(N, np.float32)
for r in rows:
    c = pc.get(r[0], {}); s, dur = starts[r[0]], timing.get(r[0], float(r[3]))
    for f in c.get("fx", []):
        a = sfx(f["desc"]); i0 = pos(s + float(f.get("at", 0)) * dur)
        seg = a[:max(0, N - i0)] * 0.55 * float(f.get("level", 0.8)); fx[i0:i0 + len(seg)] += seg
    for f in c.get("cinematic", []):
        a = sfx(CINEMATIC.get(f["type"], f.get("desc", "")) if f["type"] in CINEMATIC else f.get("desc", "soft whoosh"))
        i0 = pos(s + float(f.get("at", 0)) * dur)
        if f["type"] == "riser":  # a riser ends on its beat
            i0 = max(0, i0 - len(a))
        seg = a[:max(0, N - i0)] * 0.5 * float(f.get("level", 0.6)); cine[i0:i0 + len(seg)] += seg

# --- music, cue by cue, shaped by the per-cut level curve; crossfaded; ducked
music = np.zeros(N, np.float32); mlevel = np.zeros(N, np.float32)
order = [r[0] for r in rows]
for cue in plan.get("music_cues", []):
    try:
        i, j = order.index(cue["from_cut"]), order.index(cue["to_cut"])
    except ValueError:
        continue
    s = starts[order[i]]; e = starts[order[j]] + timing.get(order[j], float(rows[j][3]))
    length = max(10.0, e - s + 1.5)
    h = hashlib.md5((cue["prompt"] + str(round(length))).encode()).hexdigest()[:10]
    f = eleven("/music?output_format=mp3_44100_128", {"prompt": cue["prompt"] + " Instrumental only, no vocals.",
               "music_length_ms": int(length * 1000), "force_instrumental": True}, os.path.join(A, "music", h + ".mp3"))
    m = load(f)
    i0, n = pos(s), int((e - s) * SR) + int(1.0 * SR)  # 1 s overlap into the next cue for a crossfade
    seg = m[:n]
    fade = int(0.8 * SR)
    seg[:fade] *= np.linspace(0, 1, min(fade, len(seg)))[:len(seg[:fade])]
    seg[-fade:] *= np.linspace(1, 0, len(seg[-fade:]))
    music[i0:i0 + len(seg)] += seg[:max(0, N - i0)] * float(cue.get("level", 0.5))
for r in rows:
    c = pc.get(r[0], {}); s0, n = pos(starts[r[0]]), int(timing.get(r[0], float(r[3])) * SR)
    mlevel[s0:s0 + n] = 0 if c.get("silence") or not c.get("music") else float(c.get("music_level", 0.4))
music *= smooth(mlevel, 0.6) * (1 - 0.6 * speech_env) * (1 - 0.5 * thought_env)

# --- mix: dialogue first; gentle bus compression by soft clip; loudness to about -16 LUFS-ish by RMS of speech
dn = dlg / (np.sqrt(np.mean(dlg[speech > 0] ** 2)) + 1e-9) * 0.12 if speech.any() else dlg
mix = dn + fx + cine * 0.8 + amb + music * 0.55
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix = mix / (np.abs(mix).max() + 1e-9) * 0.9
out = os.path.join(A, f"ep{ep:02d}_mix_v3.wav")
pcm = (np.stack([mix, mix], 1) * 32767).astype("<i2")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
vid = os.path.join(D, "anim_v2", f"off-the-clock-ep{ep:02d}-animatic-v2.mp4")
final = os.path.join(D, "anim_v2", f"off-the-clock-ep{ep:02d}-v3.mp4")
subprocess.run([FF, "-y", "-v", "error", "-i", vid, "-i", out, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-shortest", final], check=True)
print(f"ep{ep}: {runtime:.0f}s, beds {sorted(beds)}, cues {len(plan.get('music_cues', []))}, wrote {os.path.basename(final)}")
