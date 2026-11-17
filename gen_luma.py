"""gen_luma.py [epFrom] [epTo]: generate unfinished jobs with the Luma API (Photon), 4 at a time.
Key comes from the LUMAAI_API_KEY user environment variable; never printed."""
import json, os, sys, time, subprocess, urllib.request, winreg
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
KEY = os.environ.get("LUMAAI_API_KEY") or winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), "LUMAAI_API_KEY")[0]
API = "https://agents.lumalabs.ai/v1/generations"
lo, hi = (int(a) for a in (sys.argv[1:3] or (1, 10)))

def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method="POST" if body else "GET",
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "off-the-clock-previs/1.0"})
    return json.load(urllib.request.urlopen(req, timeout=60))

def one(j):
    try:
        g = call(API, {"prompt": j["prompt"], "aspect_ratio": "16:9" if j["w"] > j["h"] else "9:16"})
        for _ in range(90):
            g = call(f"{API}/{g['id']}")
            if g["state"] == "completed":
                out = subprocess.run([sys.executable, os.path.join(D, "dl.py"), j["id"], g["output"][0]["url"]], capture_output=True, text=True)
                return out.stdout.strip() or out.stderr.strip()[-200:]
            if g["state"] == "failed":
                return f"fail {j['id']}: {g.get('failure_reason')}"
            time.sleep(4)
        return f"timeout {j['id']}"
    except Exception as e:
        return f"fail {j['id']}: {str(e)[:120]} {getattr(e, 'read', lambda: b'')()[:300]}"

jobs = [j for j in json.load(open(os.path.join(D, "img", "jobs.json"), encoding="utf-8"))
        if lo <= j["ep"] <= hi and not os.path.exists(os.path.join(D, "img", "done", j["id"] + ".json"))]
jobs = jobs[:int(os.environ.get("LIMIT", 10**9))]
print("todo", len(jobs), flush=True)
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(one, jobs):
        print(r, flush=True)
