"""assemble.py <ep>: cut video/epNN/shot_N.mp4 clips to the final timing -> video/off-the-clock-epNN-motion.mp4
Split cuts (5a, 5b...) take consecutive slices of their shot's clip. A shot with no clip falls back to the
animatic still. Title card 2 s up front, end card 3 s at the close, captions burned in from captions/epNN.srt."""
import json, os, re, sys, subprocess
import imageio_ffmpeg
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
ep = int(sys.argv[1])
rows = json.load(open(os.path.join(D, "tables.json"), encoding="utf-8"))[str(ep)]
VID, TMP = os.path.join(D, "video", f"ep{ep:02d}"), os.path.join(D, "video", f"ep{ep:02d}", "cuts")
os.makedirs(TMP, exist_ok=True)
SCALE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=24,format=yuv420p"

def run(args):
    subprocess.run([FF, "-y", "-v", "error"] + args, check=True)

def still(img, sec, out):
    run(["-loop", "1", "-t", str(sec), "-i", img, "-vf", SCALE, "-an", "-c:v", "libx264", "-crf", "20", out])

segs, offset, used = [], {}, []
segs.append(os.path.join(TMP, "000_title.mp4"))
still(os.path.join(D, "img", "e00_title_card.jpg"), 2, segs[-1])
for i, r in enumerate(rows, 1):
    num, sec = r[0], int(r[3])
    base = re.match(r"\d+", num).group(0)
    clip = os.path.join(VID, f"shot_{base}.mp4")
    out = os.path.join(TMP, f"{i:03d}_{num}.mp4")
    if os.path.exists(clip):
        start = offset.get(base, 0.0)
        run(["-ss", f"{start:.2f}", "-i", clip, "-t", str(sec), "-vf", SCALE + ",tpad=stop_mode=clone:stop_duration=12",
             "-t", str(sec), "-an", "-c:v", "libx264", "-crf", "20", out])
        offset[base] = start + sec
        used.append(num)
    else:  # no motion clip: hold the clean keyframe (or the scene's plate) for this cut
        img = os.path.join(D, "img", f"e{ep:02d}_key_shot_{base}.jpg")
        if not os.path.exists(img):
            sys.path.insert(0, D)
            import gen_agnes
            img = os.path.join(D, "img", gen_agnes.plate_for(ep, r[1]) or "e00_title_card.jpg")
        still(img, sec, out)
    segs.append(out)
segs.append(os.path.join(TMP, "999_end.mp4"))
still(os.path.join(D, "img", "e00_end_card.jpg"), 3, segs[-1])

lst = os.path.join(TMP, "list.txt")
open(lst, "w", encoding="utf-8").write("\n".join(f"file '{s.replace(os.sep, '/')}'" for s in segs))
joined = os.path.join(TMP, "joined.mp4")
run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])

# captions shifted by the 2 s title card; burned in with a phone-friendly style
srt_src = open(os.path.join(D, "captions", f"ep{ep:02d}.srt"), encoding="utf-8").read()
def shift(m):
    h, mi, s, ms = map(int, m.groups()); t = h * 3600000 + mi * 60000 + s * 1000 + ms + 2000
    return f"{t // 3600000:02d}:{t // 60000 % 60:02d}:{t // 1000 % 60:02d},{t % 1000:03d}"
srt = os.path.join(TMP, "subs.srt")
open(srt, "w", encoding="utf-8").write(re.sub(r"(\d\d):(\d\d):(\d\d),(\d\d\d)", shift, srt_src))
final = os.path.join(D, "video", f"off-the-clock-ep{ep:02d}-motion.mp4")
style = "FontName=Segoe UI,FontSize=13,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=1.6,Shadow=0,MarginV=60"
os.chdir(TMP)  # subtitles filter path: keep it relative to dodge Windows drive-letter escaping
run(["-i", joined, "-vf", f"subtitles=subs.srt:force_style='{style}'", "-c:v", "libx264", "-crf", "23",
     "-preset", "medium", "-movflags", "+faststart", final])
print(ep, "cuts", len(rows), "with motion:", len(used), "stills:", len(rows) - len(used), "MB", round(os.path.getsize(final) / 1e6, 1))
