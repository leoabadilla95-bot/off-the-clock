"""animatic.py <ep>: timed keyframe cut, one still per cut from the final table, captions burned in -> anim/epNN.mp4"""
import json, re, sys, os, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps
import imageio_ffmpeg
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
V2 = os.environ.get("V2") == "1"  # v2: Key column picks the picture, cut lengths follow the recorded performance
IMG, OUT = os.path.join(D, "img"), os.path.join(D, "anim_v2" if V2 else "anim")
W, H = 540, 960
ep = int(sys.argv[1])
rows = json.load(open(os.path.join(D, "tables_v2.json" if V2 else "tables.json"), encoding="utf-8"))[str(ep)]
if V2:
    timing = dict((c, s) for c, s in json.load(open(os.path.join(D, "audio_v2", f"ep{ep:02d}_timing.json"))))
F = lambda s, b=False: ImageFont.truetype("C:/Windows/Fonts/" + ("segoeuib.ttf" if b else "segoeui.ttf"), s)
LABEL = re.compile(r"([A-Z][A-Z]+(?: [A-Z][A-Z]+)*)(?: \(([^)]*)\))?:\s")
TAG = re.compile(r"\[[^\]]*\]\s*")

def still(path):
    return ImageOps.fit(Image.open(path).convert("RGB"), (W, H), Image.LANCZOS)

def caption(dlg):
    parts = LABEL.split(dlg)
    said = [(parts[i].title(), TAG.sub("", " ".join(re.findall(r'"([^"]*)"', parts[i + 2]))), "V.O." in (parts[i + 1] or ""))
            for i in range(1, len(parts), 3)]
    said = [x for x in said if x[1]]
    if said:
        return said
    on = re.findall(r"\*([^*]+)\*", dlg)  # on-screen text
    return [("", on[0], False)] if on else []

def frame(img, label, cap):
    im = img.copy()
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([0, 0, W, 44], fill=(0, 0, 0, 150))
    d.text((14, 10), label, font=F(18, True), fill="white")
    lines = []
    for who, txt, thought in cap:
        for k, ln in enumerate(textwrap.wrap(txt, 34)):
            lines.append(((who + " (thinks)" if thought else who) if k == 0 else "", ln, thought))
    lines = lines[:6]
    if lines:
        y = H - 70 - 34 * len(lines)
        d.rectangle([0, y - 16, W, H], fill=(0, 0, 0, 160))
        for who, ln, thought in lines:
            x = 22
            if who:
                d.text((x, y), who.upper() + "  ", font=F(20, True), fill=(150, 200, 255) if thought else (240, 196, 64))
                x += d.textlength(who.upper() + "  ", font=F(20, True))
            d.text((x, y), ln, font=ImageFont.truetype("C:/Windows/Fonts/segoeuii.ttf", 22) if thought else F(22),
                   fill=(200, 225, 255) if thought else "white")
            y += 34
    return im

os.makedirs(os.path.join(OUT, f"ep{ep:02d}"), exist_ok=True)
plates = sorted(f for f in os.listdir(IMG) if f.startswith(f"e{ep:02d}_plate"))
last = os.path.join(IMG, plates[0]) if plates else os.path.join(IMG, "e00_title_card.jpg")
concat, missing = [], []
JOBS = {j["id"]: j["name"] for j in json.load(open(os.path.join(IMG, "jobs.json"), encoding="utf-8"))}
STOP = {"the", "a", "of", "at", "in", "on", "and", "s", "recap", "night", "late", "cont", "int", "ext"}
ALIAS = {"water": "lake", "door": "entrance", "stall": "cart"}
words = lambda s: {ALIAS.get(w, w) for w in re.findall(r"[a-z0-9]+", s.lower())} - STOP
# this episode's plates first, then earlier episodes' (e.g. the Episode 1 office plate)
PLATES = sorted((f for f in os.listdir(IMG) if re.match(r"e\d\d_plate_.*\.jpg$", f)),
                key=lambda f: (int(f[1:3]) != ep, abs(int(f[1:3]) - ep)))

def plate_for(scene):
    """Best location plate for a scene name by shared words; None if nothing matches."""
    best = max(PLATES, key=lambda f: len(words(scene) & words(JOBS.get(f[:-4], ""))), default=None)
    return os.path.join(IMG, best) if best and words(scene) & words(JOBS.get(best[:-4], "")) else None
seq = [("title", os.path.join(IMG, "e00_title_card.jpg"), 2, "", [])]
for r in rows:
    num, shot, sec = r[0], r[2], int(r[3])
    base = re.match(r"\d+", num).group(0)
    p = os.path.join(IMG, f"e{ep:02d}_key_shot_{base}.jpg")
    if V2:
        sec = timing.get(num, sec)
        key = r[6] if len(r) > 6 else ""
        m = re.match(r"e(\d+):(\d+)", key)
        if m:
            p = os.path.join(IMG, f"e{int(m.group(1)):02d}_key_shot_{m.group(2)}.jpg")
        elif key.startswith("screen:"):
            p = os.path.join(IMG, "screens", key[7:].strip())
        elif key.startswith("new"):
            p = os.path.join(IMG, f"v2_e{ep:02d}_{num}.jpg")
        elif key.startswith("plate:"):
            p = plate_for(key[6:]) or ""
    tag = ""
    if os.path.exists(p):
        last = p
    else:
        missing.append(num)
        pl = plate_for(r[1])
        if pl:
            last, tag = pl, "  ·  PLATE"
    seq.append((num, last, sec, f"EP {ep}  ·  {num}  ·  {shot}{tag}", caption(r[5])))
seq.append(("end", os.path.join(IMG, "e00_end_card.jpg"), 3, "", []))
for i, (num, p, sec, label, cap) in enumerate(seq):
    fp = os.path.join(OUT, f"ep{ep:02d}", f"{i:03d}.jpg")
    (frame(still(p), label, cap) if label else still(p)).save(fp, quality=88)
    concat.append(f"file '{fp.replace(os.sep, '/')}'\nduration {sec}")
concat.append(f"file '{fp.replace(os.sep, '/')}'")
lst = os.path.join(OUT, f"ep{ep:02d}.txt")
open(lst, "w", encoding="utf-8").write("\n".join(concat))
mp4 = os.path.join(OUT, f"off-the-clock-ep{ep:02d}-animatic{'-v2' if V2 else ''}.mp4")
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-crf", "30", "-preset", "medium", "-movflags", "+faststart", mp4], check=True)
print(ep, "cuts", len(rows), "seconds", sum(s[2] for s in seq), "MB", round(os.path.getsize(mp4) / 1e6, 2), "no keyframe for:", missing)
