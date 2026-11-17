"""gen_runway.py <ep> [shot ...]: animate each shot's keyframe with Runway Gen-4 Turbo (paid: 5 credits = $0.05/s).
One clip per shot heading in the pack, length = the shot's total seconds (2-10). Writes video/epNN_runway/shot_N.mp4.
Key from RUNWAYML_API_SECRET (user environment); never printed. Env DRY=1 prints the plan and cost only."""
import json, os, sys, time, base64, urllib.request, urllib.error, winreg
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]] + sys.argv[1:]
ep = int(sys.argv[1])
only = set(sys.argv[2:])
sys.argv = [sys.argv[0], str(ep)]
import gen_agnes_video as gav  # reuse the pack shot list and keyframe lookup (does no work at import with ep set)

API = "https://api.dev.runwayml.com/v1"
OUT = os.path.join(D, "video", f"ep{ep:02d}_runway")
os.makedirs(OUT, exist_ok=True)

def key():
    return os.environ.get("RUNWAYML_API_SECRET") or winreg.QueryValueEx(
        winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), "RUNWAYML_API_SECRET")[0]

def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method="POST" if body else "GET",
                                 headers={"Authorization": f"Bearer {key()}", "X-Runway-Version": "2024-11-06",
                                          "Content-Type": "application/json", "User-Agent": "off-the-clock-previs/1.0"})
    return json.load(urllib.request.urlopen(req, timeout=120))

def one(s):
    num, secs, scene, prompt = s
    secs = max(2, min(secs, 10))
    out = os.path.join(OUT, f"shot_{num}.mp4")
    if os.path.exists(out):
        return f"skip {num}"
    body = {"model": "gen4_turbo", "promptImage": gav.first_frame(num, scene), "ratio": "720:1280", "duration": secs,
            "promptText": (prompt + " Keep every face, outfit and the set exactly as in the image. Natural, subtle motion.")[:1000]}
    try:
        task = call(f"{API}/image_to_video", body)
        t0 = time.time()
        while time.time() - t0 < 900:
            time.sleep(8)
            g = call(f"{API}/tasks/{task['id']}")
            if g["status"] == "SUCCEEDED":
                urllib.request.urlretrieve(g["output"][0], out)
                return f"ok {num} {secs}s in {int(time.time() - t0)}s"
            if g["status"] in ("FAILED", "CANCELLED"):
                return f"fail {num}: {g.get('failure') or g.get('failureCode')}"
        return f"timeout {num}"
    except urllib.error.HTTPError as e:
        return f"fail {num}: {e.code} {e.read()[:300]}"
    except Exception as e:
        return f"fail {num}: {str(e)[:200]}"

todo = [s for s in gav.shots() if not only or s[0] in only]
total = sum(max(2, min(s[1], 10)) for s in todo)
print(f"shots {len(todo)}, {total}s of video, about {total * 5} credits (${total * 0.05:.2f})", flush=True)
if os.environ.get("DRY"):
    sys.exit()
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(one, todo):
        print(r, flush=True)
