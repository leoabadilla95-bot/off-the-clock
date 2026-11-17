"""assemble_runway.py <ep>: final cut from Runway clips.
Each cut = its Runway clip trimmed to the recorded timing (stills with a slow push-in for app screens or any cut without
a clip), title card 2 s, end card 3 s, captions from captions_v2 burned in (thoughts italic), the v3 mix as the soundtrack.
Writes video/off-the-clock-epNN-runway.mp4."""
import json, os, re, subprocess, sys
import imageio_ffmpeg
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
ep = int(sys.argv[1])
rows = json.load(open(os.path.join(D, "tables_v2.json"), encoding="utf-8"))[str(ep)]
_tf = os.path.join(D, "audio_v2", f"ep{ep:02d}_timing.json")
if not os.path.exists(_tf):  # fresh clone: the kit carries the timing
    _tf = os.path.join(D, "runway_kit", f"ep{ep:02d}", "timing.json")
timing = dict((c, s) for c, s in json.load(open(_tf)))
CLIPS = os.path.join(D, "video", f"ep{ep:02d}_runway_v2")
TMP = os.path.join(CLIPS, "cuts"); os.makedirs(TMP, exist_ok=True)
V = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=24,format=yuv420p"

def run(a):
    subprocess.run([FF, "-y", "-v", "error"] + a, check=True)

def still(img, sec, out, push=True):
    zoom = f",zoompan=z='min(zoom+0.0006,1.06)':d={int(sec * 24)}:s=720x1280:fps=24" if push else ""
    run(["-loop", "1", "-t", f"{sec:.3f}", "-i", img, "-vf", V + zoom + ",trim=duration=" + f"{sec:.3f}", "-an",
         "-c:v", "libx264", "-crf", "18", out])

sys.argv = [sys.argv[0], str(ep)]
import runway_v2  # picture() resolves each cut's Key to its image
segs = [os.path.join(TMP, "000_title.mp4")]
still(os.path.join(D, "img", "e00_title_card.jpg"), 2.0, segs[0], push=False)
motion = stills = 0
for i, r in enumerate(rows, 1):
    sec = float(timing.get(r[0], float(r[3])))
    out = os.path.join(TMP, f"{i:03d}.mp4")
    clip = os.path.join(CLIPS, f"cut_{r[0]}.mp4")
    if os.path.exists(clip):
        run(["-i", clip, "-vf", V + ",tpad=stop_mode=clone:stop_duration=10", "-t", f"{sec:.3f}", "-an", "-c:v", "libx264", "-crf", "18", out])
        motion += 1
    else:
        key = r[6] if len(r) > 6 else ""
        img = os.path.join(D, "img", "screens", key[7:].strip()) if key.startswith("screen:") else runway_v2.picture(r)
        still(img or os.path.join(D, "img", "e00_title_card.jpg"), sec, out)
        stills += 1
    segs.append(out)
segs.append(os.path.join(TMP, "999_end.mp4"))
still(os.path.join(D, "img", "e00_end_card.jpg"), 3.0, segs[-1], push=False)
lst = os.path.join(TMP, "list.txt")
open(lst, "w").write("\n".join(f"file '{s.replace(os.sep, '/')}'" for s in segs))
joined = os.path.join(TMP, "joined.mp4")
run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])

# captions: the synced v2 file, shifted 2 s for the title card; thoughts keep their <i> tags
srt = open(os.path.join(D, "captions_v2", f"off-the-clock-ep{ep:02d}-final.srt"), encoding="utf-8").read()
open(os.path.join(TMP, "subs.srt"), "w", encoding="utf-8").write(srt)
style = "FontName=Segoe UI,FontSize=12,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H90000000,BorderStyle=1,Outline=1.5,Shadow=0,MarginV=70"
final = os.path.join(D, "video", f"off-the-clock-ep{ep:02d}-runway.mp4")
mix = os.path.join(D, "audio_v2", f"ep{ep:02d}_mix_v3.wav")
if not os.path.exists(mix):  # fresh clone: the kit's soundtrack
    mix = os.path.join(D, "runway_kit", f"ep{ep:02d}", "soundtrack.m4a")
os.chdir(TMP)
run(["-i", joined, "-i", mix, "-map", "0:v", "-map", "1:a", "-vf", f"subtitles=subs.srt:force_style='{style}'",
     "-c:v", "libx264", "-crf", "21", "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
     "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", final])
print(f"ep{ep}: {motion} Runway clips, {stills} stills, wrote {os.path.basename(final)} ({os.path.getsize(final) / 1e6:.1f} MB)")
