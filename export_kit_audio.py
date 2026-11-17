"""export_kit_audio.py <ep...>: put everything a fresh clone needs to finish an episode into runway_kit/epNN/:
- soundtrack.m4a: the final mix (voices, music, effects), title-card offset included, loudness-normalized
- timing.json / lines.json: each cut's final length and each recorded line's start, end and thought flag
- voice/cut_<id>.mp3: for every cut where someone speaks ON CAMERA, that cut's spoken dialogue only (thoughts and
  off-screen lines muted), starting at the cut's first frame, for lip-sync tools."""
import json, os, re, shutil, subprocess, sys, wave
import numpy as np
import imageio_ffmpeg
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
LEAD = 2.0
LABEL = re.compile(r"([A-Z][A-Z]+(?: [A-Z][A-Z]+)*)(?: \(([^)]*)\))?:\s")

for ep in map(int, sys.argv[1:]):
    A, K = os.path.join(D, "audio_v2"), os.path.join(D, "runway_kit", f"ep{ep:02d}")
    os.makedirs(os.path.join(K, "voice"), exist_ok=True)
    shutil.copy(os.path.join(A, f"ep{ep:02d}_timing.json"), os.path.join(K, "timing.json"))
    shutil.copy(os.path.join(A, f"ep{ep:02d}_lines.json"), os.path.join(K, "lines.json"))
    subprocess.run([FF, "-y", "-v", "error", "-i", os.path.join(A, f"ep{ep:02d}_mix_v3.wav"), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-c:a", "aac", "-b:a", "160k", os.path.join(K, "soundtrack.m4a")], check=True)

    rows = json.load(open(os.path.join(D, "tables_v2.json"), encoding="utf-8"))[str(ep)]
    timing = dict((c, s) for c, s in json.load(open(os.path.join(A, f"ep{ep:02d}_timing.json"))))
    placed = json.load(open(os.path.join(A, f"ep{ep:02d}_lines.json")))
    # the same line order gen_voices.py recorded: every labelled quote, cut by cut
    order = []
    for r in rows:
        parts = LABEL.split(r[5])
        for i in range(1, len(parts), 3):
            if " ".join(re.findall(r'"([^"]*)"', parts[i + 2])).strip():
                tag = parts[i + 1] or ""
                order.append((r[0], "V.O." in tag or "O.S." in tag))
    if len(order) != len(placed):
        sys.exit(f"ep{ep}: {len(order)} script lines vs {len(placed)} recorded; re-run gen_voices.py first")
    with wave.open(os.path.join(A, f"ep{ep:02d}_dialogue.wav")) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32)
    keep = np.zeros(len(x), np.float32)  # on-camera speech only
    for (cut, hidden), (s, e, _) in zip(order, placed):
        if not hidden:
            keep[int((LEAD + s) * sr):int((LEAD + e) * sr)] = 1
    spoken = x * keep
    starts, t = {}, 0.0
    for r in rows:
        starts[r[0]] = t; t += float(timing.get(r[0], r[3]))
    made = 0
    for r in rows:
        cut = r[0]
        if not any(c == cut and not h for c, h in order):
            continue
        a, b = int((LEAD + starts[cut]) * sr), int((LEAD + starts[cut] + float(timing.get(cut, r[3]))) * sr)
        seg = spoken[a:b].astype("<i2")
        if not seg.any():
            continue
        out = os.path.join(K, "voice", f"cut_{cut}.mp3")
        subprocess.run([FF, "-y", "-v", "error", "-f", "s16le", "-ar", str(sr), "-ac", "1", "-i", "-", "-c:a", "libmp3lame",
                        "-b:a", "128k", out], input=seg.tobytes(), check=True)
        made += 1
    print(f"ep{ep}: soundtrack.m4a, timing.json, lines.json, {made} voice files")
