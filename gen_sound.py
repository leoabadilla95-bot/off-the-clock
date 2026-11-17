"""gen_sound.py <ep>: temp score + sound effects for one episode, mixed under the dialogue.
- Score: one Eleven Music track the length of the episode, written from the cue sheet's arc (opens, builds, turn, ending),
  faded out under the last 4 seconds so every cliffhanger lands on silence, and ducked whenever someone speaks.
- Effects: each effect in the cue sheet's list is generated once and placed at the first cut whose script mentions it.
Writes audio/epNN_mix.wav (title offset included) and anim/off-the-clock-epNN-animatic-sound.mp4.
Key from ELEVENLABS_API_KEY (user environment); never printed."""
import json, os, re, sys, subprocess, urllib.request, winreg
import imageio_ffmpeg
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ.get("ELEVENLABS_API_KEY") or winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), "ELEVENLABS_API_KEY")[0]
FF = imageio_ffmpeg.get_ffmpeg_exe()
LEAD, TAIL = 2.0, 3.0
ep = int(sys.argv[1])

# The doc's music and sound cue sheet: (opens, builds, turn, ending, effects)
CUES = {
 1: ("Low drone under the lobby", "Plucked strings start on the chair bump", "Strings drop out under \"something you've never done\"", "Strings stop dead as the elevator opens; hard cut", ["badge reader beep", "office chair thunk against a desk", "cheerful app deal ding", "phone text buzz"]),
 2: ("Recap sting", "Comic stings at check-in and on missed throws", "All sound falls away on the exhale; music swells on the bullseye", "Bar ambience fades; half a second of silence", ["barcode scanner ding", "big axe thunk into a wooden target", "camera shutter click"]),
 3: ("Recap sting", "Warm acoustic guitar in a Mexican community kitchen", "Guitar thins to a few notes by the steamer", "Error buzz, ringtone, then dead silence", ["wet masa dough squelch", "card reader error buzz", "speakerphone hiss"]),
 4: ("Recap sting", "Soft piano in a penthouse; muffled all-hands audio", "Room tone only", "A tension drone as an executive steps off the elevator", ["plastic wrapper ripping", "dry-erase marker squeak", "sticky note slap", "elevator chime"]),
 5: ("Recap sting", "Ambient spa hum", "Total silence in the float; piano returns in the sauna, then drops out", "Heartbeat sub-bass", ["metal locker clunk", "water lapping in a float pool", "phone vibrating on wood"]),
 6: ("Recap sting", "Music up at the dock; playful during a splash fight", "One single piano note", "Yacht horn and bass-heavy party music, cut dead", ["cheerful app deal ding", "kayak paddle splashes", "deep yacht horn"]),
 7: ("Recap sting", "A cold drone in an executive boardroom; office murmurs", "Music stops", "A rising tone that cuts to black", ["heartbeat sub-bass thump"]),
 8: ("Recap sting; a pen click", "Warm-up laughter and whoops in a small theater", "Room hush in a spotlight", "Bar noise fades to nothing; heartbeat sub-bass", ["cheerful app voucher ding", "leather bag thud on a wooden floor"]),
 9: ("Recap sting; a door bang", "Sparse piano over an empty desk", "Near-silence; warm guitar returns at a pottery wheel", "Silence", ["phone text buzz", "soft rain on a window", "soft wet clay splat"]),
 10: ("A soft glitch, then silence", "Applause; a warm hopeful theme starts under a montage", "The theme builds through a sunny outdoor market", "The full theme swells on a crane-up and resolves", ["fork dropping on a plate", "drawer sliding shut", "market brass band"]),
}
# Words that tie each effect to the cut where it happens in the script
HINTS = {"badge": ["badge"], "chair": ["chair"], "deal ding": ["ding"], "text buzz": ["buzz", "text"], "scanner": ["scanner", "check-in", "ding"],
         "axe": ["bullseye", "axe", "throw"], "shutter": ["photo", "camera"], "masa": ["masa"], "card reader": ["card", "reader", "decline"],
         "speakerphone": ["speaker", "bank", "fraud"], "wrapper": ["rip", "plastic", "wrapper"], "marker": ["marker", "whiteboard"],
         "sticky": ["sticky"], "elevator": ["elevator"], "locker": ["locker"], "water": ["float", "water"], "vibrating": ["missed", "phone", "buzz"],
         "paddle": ["splash", "kayak", "paddle"], "yacht": ["yacht", "horn"], "heartbeat": ["heartbeat"], "voucher": ["voucher", "ding"],
         "bag": ["bag"], "rain": ["rain", "window"], "clay": ["clay", "wheel"], "fork": ["fork"], "drawer": ["drawer"], "brass": ["band", "market"]}

def eleven(path, body, out):
    if not os.path.exists(out):
        r = urllib.request.Request("https://api.elevenlabs.io/v1" + path, data=json.dumps(body).encode(), method="POST",
                                   headers={"xi-api-key": KEY, "Content-Type": "application/json", "User-Agent": "off-the-clock-previs/1.0"})
        open(out, "wb").write(urllib.request.urlopen(r, timeout=600).read())
    return out

V2 = os.environ.get("V2") == "1"
rows = json.load(open(os.path.join(D, "tables_v2.json" if V2 else "tables.json"), encoding="utf-8"))[str(ep)]
if V2:  # cut lengths follow the recorded performance
    tm = dict((c, s) for c, s in json.load(open(os.path.join(D, "audio_v2", f"ep{ep:02d}_timing.json"))))
    for r in rows:
        r[3] = tm.get(r[0], r[3])
starts, t = [], 0
for r in rows:
    starts.append(t); t += float(r[3])
runtime = t
opens, builds, turn, ending, fx = CUES[ep]
A = os.path.join(D, "audio_v2" if V2 else "audio", f"ep{ep:02d}")
os.makedirs(A, exist_ok=True)

# 1. Score, written as a timeline so the arc lands roughly where the episode's beats do
prompt = (f"Instrumental underscore for a {runtime}-second vertical romantic micro-drama episode set in Chicago. "
          f"Warm, intimate, modern indie film score; restrained, never busy, leaves room for dialogue. "
          f"0:00 {opens}. Around 0:{int(runtime * .25):02d} {builds}. Around {int(runtime * .65) // 60}:{int(runtime * .65) % 60:02d} {turn}. "
          f"Final 10 seconds: {ending}. No vocals, no lyrics.")
music = eleven("/music?output_format=mp3_44100_128",
               {"prompt": prompt, "music_length_ms": int((LEAD + runtime) * 1000), "force_instrumental": True},
               os.path.join(A, "score.mp3"))
print("score ready", flush=True)

# 2. Effects placed at their cut
placed = []
for k, name in enumerate(fx):
    key = next((h for h in HINTS if h in name), None)
    words = HINTS.get(key, name.split()[-1:])
    # sound column first (it names effects outright), then the picture notes
    hit = next((i for col in (5, 4) for i, r in enumerate(rows) if any(re.search(r"\b" + re.escape(w.lower()) + r"\b", r[col].lower()) for w in words)), None)
    if hit is None:
        print(f"  skip effect (no matching cut): {name}"); continue
    f = eleven("/sound-generation?output_format=mp3_44100_128",
               {"text": name, "duration_seconds": 2.5 if "band" not in name and "rain" not in name else 6, "prompt_influence": 0.6},
               os.path.join(A, f"fx_{k}.mp3"))
    placed.append((f, LEAD + starts[hit] + 0.2))
    print(f"  {name} -> cut {rows[hit][0]} at {starts[hit]}s", flush=True)

# 3. Mix: score ducked under dialogue and faded before the cliffhanger, effects on top
dlg = os.path.join(D, "audio_v2" if V2 else "audio", f"ep{ep:02d}_dialogue.wav")
total = LEAD + runtime + TAIL
fade_at = LEAD + runtime - 4
inputs = ["-i", dlg, "-i", music] + sum((["-i", f] for f, _ in placed), [])
graph = [f"[1:a]volume=0.32,afade=t=out:st={fade_at:.1f}:d=3,apad,atrim=0:{total:.2f}[m]",
         "[0:a]aresample=44100,asplit=2[d][sc]",
         "[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck]"]
mixin = ["[d]", "[duck]"]
for j, (_, at) in enumerate(placed):
    graph.append(f"[{j + 2}:a]volume=0.7,adelay={int(at * 1000)}:all=1[f{j}]")
    mixin.append(f"[f{j}]")
graph.append("".join(mixin) + f"amix=inputs={len(mixin)}:duration=first:normalize=0,alimiter=limit=0.89[out]")
mix = os.path.join(D, "audio_v2" if V2 else "audio", f"ep{ep:02d}_mix.wav")
subprocess.run([FF, "-y", "-v", "error"] + inputs + ["-filter_complex", ";".join(graph), "-map", "[out]", "-ar", "44100", "-ac", "2", mix], check=True)
vid = os.path.join(D, "anim_v2" if V2 else "anim", f"off-the-clock-ep{ep:02d}-animatic{'-v2' if V2 else ''}.mp4")
out = os.path.join(D, "anim_v2" if V2 else "anim", f"off-the-clock-ep{ep:02d}-animatic{'-v2' if V2 else ''}-sound.mp4")
subprocess.run([FF, "-y", "-v", "error", "-i", vid, "-i", mix, "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", out], check=True)
print("wrote", os.path.basename(out))
