"""ep1_assemble.py: cut the Wan shot clips into the 80-second Episode 1 edit.
Each shot is stretched (down to half speed) or held on its last frame to fill its exact slot in the
final table, then title card (2 s) + shots + end card (3 s), captions burned in. Silent."""
import json, os, re, subprocess, shutil
import imageio_ffmpeg
D = os.path.dirname(os.path.abspath(__file__))
WAN = r"C:\Users\kybel\wangp\ep01_720"
TMP = os.path.join(WAN, "assemble")
os.makedirs(TMP, exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 704, 1280, 24
clips = json.load(open(os.path.join(WAN, "clips.json")))
rows = json.load(open(os.path.join(D, "tables.json"), encoding="utf-8"))["1"]

order, need = [], {}
for r in rows:
    b = re.match(r"\d+", r[0]).group(0)
    if b not in need:
        order.append(b)
    need[b] = need.get(b, 0) + int(r[3])

def run(*a):
    subprocess.run([FF, "-y", "-v", "error", *a], check=True)

def card(img, sec, out):
    run("-loop", "1", "-i", img, "-t", str(sec), "-vf",
        f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p",
        "-c:v", "libx264", "-crf", "20", out)

parts = [os.path.join(TMP, "000_title.mp4")]
card(os.path.join(D, "img", "e00_title_card.jpg"), 2, parts[0])
for b in order:
    c = clips[b]
    have = c["frames"] / FPS
    speed = max(0.5, min(1.0, have / need[b]))  # never slower than half speed
    out = os.path.join(TMP, f"shot_{int(b):02d}.mp4")
    run("-i", c["file"], "-vf",
        f"setpts=PTS/{speed:.4f},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
        f"fps={FPS},tpad=stop_mode=clone:stop_duration={need[b]},format=yuv420p",
        "-t", str(need[b]), "-an", "-c:v", "libx264", "-crf", "20", out)
    parts.append(out)
parts.append(os.path.join(TMP, "999_end.mp4"))
card(os.path.join(D, "img", "e00_end_card.jpg"), 3, parts[-1])

lst = os.path.join(TMP, "list.txt")
open(lst, "w").write("".join(f"file '{p.replace(os.sep, '/')}'\n" for p in parts))
joined = os.path.join(TMP, "joined.mp4")
run("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined)

# captions: the episode SRT shifted 2 s for the title card
def shift(m):
    h, mi, s, ms = map(int, m.groups())
    t = (h * 3600 + mi * 60 + s) * 1000 + ms + 2000
    return f"{t // 3600000:02d}:{t // 60000 % 60:02d}:{t // 1000 % 60:02d},{t % 1000:03d}"
srt = re.sub(r"(\d\d):(\d\d):(\d\d),(\d\d\d)", shift, open(os.path.join(D, "captions", "ep01.srt"), encoding="utf-8").read())
open(os.path.join(TMP, "subs.srt"), "w", encoding="utf-8").write(srt)
final = os.path.join(D, "off-the-clock-ep01-720p.mp4")
style = "FontName=Segoe UI,FontSize=13,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=70,Alignment=2"
cwd = os.getcwd(); os.chdir(TMP)  # relative path keeps the filter free of drive-letter colons
subprocess.run([FF, "-y", "-v", "error", "-i", joined, "-vf", f"subtitles=subs.srt:force_style='{style}'",
                "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", final], check=True)
os.chdir(cwd)
print("wrote", final, round(os.path.getsize(final) / 1e6, 1), "MB",
      "shots slowed:", [b for b in order if clips[b]["frames"] / FPS < need[b]])
