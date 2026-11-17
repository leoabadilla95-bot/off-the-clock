"""gen_agnes_video.py <ep> [shot ...]: animate each shot's keyframe with Agnes video (free), 9:16 720p.
One clip per shot heading in the pack, length = the shot's total seconds (4-12). Writes video/epNN/shot_N.mp4.
Key from AGNES_API_KEY (user environment); never printed."""
import json, os, re, sys, time, base64, urllib.request, urllib.error, winreg
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(D, "img")
KEY = os.environ.get("AGNES_API_KEY") or winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), "AGNES_API_KEY")[0]
API = "https://apihub.agnes-ai.com/v1"
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "User-Agent": "off-the-clock-previs/1.0"}
ep = int(sys.argv[1])
only = set(sys.argv[2:])
OUT = os.path.join(D, "video", f"ep{ep:02d}")
os.makedirs(OUT, exist_ok=True)

def call(url, body=None, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 method="POST" if body else "GET", headers=H)
    return json.load(urllib.request.urlopen(req, timeout=timeout))

def shots():
    """(num, seconds, scene, video prompt) for every shot heading in the pack."""
    src = os.path.join(D, "packs_hand", "ep1_plain.txt" if ep == 1 else f"ep{ep}.md")
    text = open(src, encoding="utf-8").read()
    for sec in re.split(r"^(?:### )?Shot (?=\d+ · )", text, flags=re.M)[1:]:
        head = sec.split("\n", 1)[0]
        num = head.split(" ")[0]
        parts = [p.strip() for p in head.split("·")]
        secs = int(re.match(r"\d+", parts[3]).group(0)) if len(parts) > 3 and re.match(r"\d+", parts[3]) else 4
        m = re.search(r"Video[^:\n]*:\**\s*\*?([^\n]+?)\*?$", sec, re.M)
        yield num, secs, parts[-1], (m.group(1).strip() if m else "")

def first_frame(num, scene):
    p = os.path.join(IMG, f"e{ep:02d}_key_shot_{num}.jpg")
    if not os.path.exists(p):
        sys.path.insert(0, D)
        import gen_agnes  # reuse the scene -> location plate lookup
        p = os.path.join(IMG, gen_agnes.plate_for(ep, scene) or "e00_title_card.jpg")
    return "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()

def one(s):
    num, secs, scene, prompt = s
    out = os.path.join(OUT, f"shot_{num}.mp4")
    if os.path.exists(out):
        return f"skip {num}"
    body = {"model": "agnes-video-2.5-flash", "mode": "keyframe", "seconds": str(max(4, min(secs, 12))),
            "size": "720P", "aspect_ratio": "9:16", "first_frame": first_frame(num, scene),
            "prompt": prompt + " Keep every face, outfit and the set exactly as in the first frame. Vertical 9:16, cinematic, natural subtle motion."}
    try:
        for wait in range(40):  # free queue fills up: retry for up to ~20 minutes
            try:
                task = call(f"{API}/videos", body)
                break
            except urllib.error.HTTPError as e:
                if e.code not in (429, 503):
                    raise
                time.sleep(30)
        else:
            return f"fail {num}: queue stayed full"
        vid = task.get("id") or task.get("video_id") or task.get("data", {}).get("id")
        t0 = time.time()
        while time.time() - t0 < 900:
            time.sleep(15)
            g = call(f"{API}/videos/{vid}")
            st = str(g.get("status", "")).lower()
            if st in ("completed", "succeeded", "success"):
                url = g.get("video_url") or g.get("url") or (g.get("metadata") or {}).get("url") or (g.get("data") or {}).get("url")
                urllib.request.urlretrieve(url, out)
                return f"ok {num} {secs}s {os.path.getsize(out) // 1024}KB in {int(time.time() - t0)}s"
            if st == "failed":
                return f"fail {num}: {json.dumps(g.get('error'))[:200]}"
        return f"timeout {num}"
    except urllib.error.HTTPError as e:
        return f"fail {num}: {e.code} {e.read()[:300]}"
    except Exception as e:
        return f"fail {num}: {str(e)[:200]}"

if __name__ == "__main__":
    todo = [s for s in shots() if not only or s[0] in only]
    print("shots", len(todo), flush=True)
    with ThreadPoolExecutor(4) as ex:
        for r in ex.map(one, todo):
            print(r, flush=True)
