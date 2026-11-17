"""gen_voices.py <ep>: ElevenLabs dialogue track for one episode.
1. Creates each speaking character's voice once from the Lookbook brief (Voice Design), saved to voices.json.
2. Records every line (one take per line), placed at its cut's start time from the final table.
3. Writes audio/epNN_dialogue.wav (2 s title-card offset + episode + 3 s end card), ready to lay under any cut.
Key from ELEVENLABS_API_KEY (user environment); never printed."""
import hashlib, json, os, re, sys, wave, urllib.request, urllib.error, winreg
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ.get("ELEVENLABS_API_KEY") or winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), "ELEVENLABS_API_KEY")[0]
API = "https://api.elevenlabs.io/v1"
SR, LEAD, TAIL = 24000, 2.0, 3.0  # pcm_24000: the free plan does not allow 44.1 kHz PCM
ep = int(sys.argv[1])

# Briefs and starting settings from the Lookbook's voice casting table
CAST = {
    "HUNTER": ("Male, early 30s, American Midwest, low and soft, careful and a little tired, short sentences, warm underneath, speeds up slightly when nervous", .50, .75, .05),
    "ABBY": ("Female, late 20s, Mexican-American from Chicago, bright and quick, teasing, warm, light Chicago accent, laughs easily", .40, .75, .15),
    "PRIYA": ("Female, mid-30s, American, crisp and fast, efficient, slightly out of breath", .50, .75, .10),
    "JO": ("Female, late 20s, Chicago, dry and quick, a nurse's no-nonsense directness, low register, skeptical warmth", .45, .75, .10),
    "LUPE": ("Female, 60s, Mexican, Spanish-accented English that slips into Spanish, big warm voice, bossy and affectionate, loud", .35, .75, .25),
    "GRANT": ("Male, mid-30s, American, smooth and polished, measured, quietly condescending, never raises his voice", .60, .80, .10),
    "CELESTE": ("Female, early 30s, American, East Coast money, lazy and amused, purring, every line an inside joke", .40, .75, .30),
    "INSTRUCTOR": ("Male, 30s, American, big booming improv-coach voice, theatrical, energetic, rising on every instruction", .35, .70, .35),
    "POTTERY": ("Female, 50s, American, low and unhurried, warm, a little amused, a calm pottery teacher", .55, .75, .05),
    "TEAMMATE": ("Female, late 20s, American, dry and deadpan, fond exasperation, flat delivery that lands as a joke", .50, .75, .10),
    "BANK": ("Female, 40s, American, polished call-center politeness, even and slightly scripted", .70, .75, .0),
    "STAFFER": ("Male, mid-20s, Chicago, flat and unhurried, deadpan, slight vocal fry", .60, .75, .0),
    "GUIDE": ("Male, 40s, Chicago, sun-tired and friendly kayak guide, loud enough to carry across a dock", .45, .75, .10),
    "HOST": ("Female, 20s, American, chipper and fast theater host, front-of-house friendly, slightly rushed", .40, .75, .15),
}
# Group lines are a small layered crowd built from the day-player voices
GROUPS = {"TEAM": ["TEAMMATE", "STAFFER", "HOST"], "AUDIENCE": ["HOST", "STAFFER", "GUIDE", "TEAMMATE"], "ALL": ["TEAMMATE", "STAFFER", "HOST"]}

def req(path, body=None, raw=False):
    r = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None,
                               method="POST" if body is not None else "GET",
                               headers={"xi-api-key": KEY, "Content-Type": "application/json", "User-Agent": "off-the-clock-previs/1.0"})
    with urllib.request.urlopen(r, timeout=180) as resp:
        return resp.read() if raw else json.load(resp)

def design(name, brief, sample):
    """Voice Design: preview from the brief, then save it. Tries the current and the older endpoint names."""
    for pv, save in (("/text-to-voice/design", "/text-to-voice"),
                     ("/text-to-voice/create-previews", "/text-to-voice/create-voice-from-preview")):
        try:
            p = req(pv, {"voice_description": brief, "text": sample})
            gid = p["previews"][0]["generated_voice_id"]
            return req(save, {"voice_name": f"OTC {name.title()}", "voice_description": brief, "generated_voice_id": gid})["voice_id"]
        except urllib.error.HTTPError as e:
            if e.code not in (404, 405, 422):
                raise
    raise RuntimeError("Voice Design endpoints not available on this account")

vfile = os.path.join(D, "voices.json")
voices = json.load(open(vfile)) if os.path.exists(vfile) else {}
LABEL = re.compile(r"([A-Z][A-Z]+(?: [A-Z][A-Z]+)*)(?: \(([^)]*)\))?:\s")
V2 = os.environ.get("V2") == "1"  # v2 scripts: internal monologue, eleven_v3 delivery, separate output folder
AUD = os.path.join(D, "audio_v2" if V2 else "audio")
rows = json.load(open(os.path.join(D, "tables_v2.json" if V2 else "tables.json"), encoding="utf-8"))[str(ep)]
PLAN = {}
pf = os.path.join(D, "audio_plan", f"ep{ep:02d}.json")
if V2 and os.path.exists(pf):  # delivery tags from the sound designer's plan, in line order per cut
    PLAN = {c["cut"]: [l.get("tag", "") for l in c.get("lines", [])] for c in json.load(open(pf, encoding="utf-8"))["cuts"]}
lines, t = [], 0
for r in rows:
    k_in_cut = 0
    parts = LABEL.split(r[5])
    for i in range(1, len(parts), 3):
        who, said = parts[i], " ".join(re.findall(r'"([^"]*)"', parts[i + 2])).strip()
        thought = "V.O." in (parts[i + 1] or "")
        if who == "INSTRUCTOR" and ep == 9:
            who = "POTTERY"
        if said and (who in CAST or who in GROUPS):
            tags = PLAN.get(r[0], [])
            tag = tags[k_in_cut] if k_in_cut < len(tags) else ""
            k_in_cut += 1
            if tag and not said.startswith("["):
                said = tag.strip() + " " + said
            lines.append((r[0], t, who, said, thought))
    t += int(r[3])
runtime = t
need = sorted({v for _, _, w, *_ in lines for v in GROUPS.get(w, [w])})
print(f"episode {ep}: {len(lines)} lines, voices {need}, {sum(len(l[3]) for l in lines)} characters", flush=True)

for who in need:
    if who not in voices:
        sample = next((l[3] for l in lines if l[2] == who), "Hey, thanks for coming in tonight. Grab a seat anywhere you like, we start in five.")
        sample = (sample + " ") * max(1, 110 // len(sample) + 1)  # Voice Design wants 100+ characters of sample text
        voices[who] = design(who, CAST[who][0], sample[:300])
        json.dump(voices, open(vfile, "w"), indent=1)
        print("created voice", who, flush=True)

os.makedirs(os.path.join(AUD, f"ep{ep:02d}"), exist_ok=True)
track = np.zeros(int((LEAD + runtime + TAIL) * SR), dtype=np.float32)
import subprocess, imageio_ffmpeg
def tighten(a, tempo=1.08, floor=0.02):
    """v3 takes: trim the silence at both ends, then speed up ~8% without changing pitch."""
    loud = np.where(np.abs(a) > floor)[0]
    if len(loud):
        a = a[max(0, loud[0] - int(0.04 * SR)): loud[-1] + int(0.08 * SR)]
    raw = (a * 32767).astype("<i2").tobytes()
    out = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
                          "-filter:a", f"atempo={tempo}", "-f", "s16le", "-"], input=raw, capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype="<i2").astype(np.float32) / 32768

clips = []  # (cut, audio, who, said, thought)
for k, (cut, start, who, said, thought) in enumerate(lines):
    takes = []
    for m, v in enumerate(GROUPS.get(who, [who])):
        _, stab, sim, style = CAST[v]
        pcm = os.path.join(AUD, f"ep{ep:02d}", f"{k:02d}_{cut}_{v.lower()}{'_vo' if thought else ''}{'_' + hashlib.md5(said.encode()).hexdigest()[:6] if V2 else ''}.pcm")
        if not os.path.exists(pcm):
            if V2:  # eleven_v3 takes [delivery] tags; thoughts are softer and closer
                text = said if said.startswith("[") or not thought else "[quietly] " + said
                body = {"text": text.replace("…", "..."), "model_id": "eleven_v3",
                        "voice_settings": {"stability": 0.5, "similarity_boost": sim}}
            else:
                body = {"text": said.replace("…", "..."), "model_id": "eleven_multilingual_v2",
                        "voice_settings": {"stability": stab, "similarity_boost": sim, "style": style, "use_speaker_boost": True}}
            open(pcm, "wb").write(req(f"/text-to-speech/{voices[v]}?output_format=pcm_24000", body, raw=True))
        a = np.frombuffer(open(pcm, "rb").read(), dtype="<i2").astype(np.float32) / 32768
        if V2:
            a = tighten(a)
        takes.append(np.concatenate([np.zeros(int(0.07 * m * SR), np.float32), a]))  # stagger crowd voices slightly
    n = max(len(a) for a in takes)
    audio = sum(np.pad(a, (0, n - len(a))) for a in takes) / (1 if len(takes) == 1 else len(takes) ** 0.5)
    if V2 and not thought:  # spoken lines sit in the room: two faint early reflections; thoughts stay dry and close
        room = np.zeros(len(audio) + int(0.05 * SR), np.float32)
        room[:len(audio)] += audio
        for d, g in ((0.023, 0.14), (0.041, 0.09)):
            j = int(d * SR); room[j:j + len(audio)] += g * audio
        audio = room
    elif V2:
        audio = audio * 0.9
    clips.append((cut, audio, who, said, thought))

# Layout. v1: picture timing is fixed and lines follow it. v2: the picture is cut to the performance,
# so a cut grows to hold its lines (never shrinks), and later cuts slide to follow.
placed, timing, cursor, prev_end = [], [], 0.0, 0.0
for r in rows:
    cut, sec = r[0], int(r[3])
    start = cursor if V2 else sum(int(x[3]) for x in rows[:rows.index(r)])
    end_needed = start + sec
    for c in [c for c in clips if c[0] == cut]:
        at = max(start + 0.15, prev_end)
        placed.append((at, c))
        prev_end = at + len(c[1]) / SR + 0.12
        end_needed = max(end_needed, prev_end + 0.2)
    final = max(float(sec) if sec <= 2 else 0, float(np.ceil((end_needed - start) * 4) / 4)) if V2 else sec
    timing.append([cut, final])
    cursor = start + final
runtime = cursor if V2 else runtime
track = np.zeros(int((LEAD + runtime + TAIL) * SR), dtype=np.float32)
for at, (cut, audio, who, said, thought) in placed:
    i0 = int((LEAD + at) * SR)
    track[i0:i0 + len(audio)] += audio[:max(0, len(track) - i0)]
if V2:
    json.dump(timing, open(os.path.join(AUD, f"ep{ep:02d}_timing.json"), "w"))
    json.dump([[at, at + len(c[1]) / SR, bool(c[4])] for at, c in placed], open(os.path.join(AUD, f"ep{ep:02d}_lines.json"), "w"))
    import textwrap
    def ts(x):
        ms = round(x * 1000); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    cues = []  # captions follow the recorded lines exactly (episode time, no title offset); thoughts in italics
    for at, (cut, audio, who, said, thought) in placed:
        txt = "\n".join(textwrap.wrap(re.sub(r"\[[^\]]*\]\s*", "", said), 38))
        cues.append(f"{ts(at)} --> {ts(at + len(audio) / SR)}\n" + (f"<i>{txt}</i>" if thought else txt))
    os.makedirs(os.path.join(D, "captions_v2"), exist_ok=True)
    open(os.path.join(D, "captions_v2", f"ep{ep:02d}.srt"), "w", encoding="utf-8").write(
        "\n".join(f"{i}\n{c}\n" for i, c in enumerate(cues, 1)))
    grown = [f"{c} {int(next(r[3] for r in rows if r[0] == c))}->{int(s)}" for c, s in timing if s > int(next(r[3] for r in rows if r[0] == c))]
    print(f"runtime {sum(int(r[3]) for r in rows)}s scripted -> {runtime:.0f}s cut to the performance; grown cuts: {', '.join(grown) or 'none'}")

peak = float(np.abs(track).max() or 1)
track = (track / peak * 0.89 * 32767).astype("<i2")  # normalize to about -1 dBFS
out = os.path.join(AUD, f"ep{ep:02d}_dialogue.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(track.tobytes())
print("wrote", out, f"{len(track) / SR:.0f}s")
