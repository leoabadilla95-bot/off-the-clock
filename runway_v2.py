"""runway_v2.py <ep> [cut ...]: animate each v2 cut's picture with Runway Gen-4 Turbo (5 credits = $0.05 per second).
Picture = the cut's Key (keyframe, plate or new v2 frame); motion prompt = the script's Picture column. Groupon app
screens and cards stay stills (no credits). Length = the cut's final timing, rounded up to whole seconds (2-10).
Writes video/epNN_runway_v2/cut_<id>.mp4. DRY=1 prints the plan and cost only."""
import base64, json, math, os, re, sys, time, urllib.request, urllib.error, winreg
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(D, "img")
ep = int(sys.argv[1]); only = set(sys.argv[2:])
rows = json.load(open(os.path.join(D, "tables_v2.json"), encoding="utf-8"))[str(ep)]
_tf = os.path.join(D, "audio_v2", f"ep{ep:02d}_timing.json")
if not os.path.exists(_tf):  # fresh clone: the kit carries the timing
    _tf = os.path.join(D, "runway_kit", f"ep{ep:02d}", "timing.json")
timing = dict((c, s) for c, s in json.load(open(_tf)))
OUT = os.path.join(D, "video", f"ep{ep:02d}_runway_v2"); os.makedirs(OUT, exist_ok=True)
API = "https://api.dev.runwayml.com/v1"
sys.argv = [sys.argv[0], str(ep)]
import gen_agnes  # scene -> location plate lookup

def picture(r):
    key, num = (r[6] if len(r) > 6 else ""), r[0]
    m = re.match(r"e(\d+):(\d+)", key)
    if m:
        p = os.path.join(IMG, f"e{int(m.group(1)):02d}_key_shot_{m.group(2)}.jpg")
        if os.path.exists(p):
            return p
    if key.startswith("screen:"):
        return None  # app screens stay stills
    if key.startswith("new"):
        return os.path.join(IMG, f"v2_e{ep:02d}_{num}.jpg")
    pl = gen_agnes.plate_for(ep, key[6:] if key.startswith("plate:") else r[1])
    return os.path.join(IMG, pl) if pl else None

def call(url, body=None):
    k = os.environ.get("RUNWAYML_API_SECRET") or winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), "RUNWAYML_API_SECRET")[0]
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method="POST" if body else "GET",
                                 headers={"Authorization": f"Bearer {k}", "X-Runway-Version": "2024-11-06",
                                          "Content-Type": "application/json", "User-Agent": "off-the-clock-previs/1.0"})
    return json.load(urllib.request.urlopen(req, timeout=120))

TASKS = os.path.join(OUT, "tasks.json")  # cut -> Runway task id, saved the moment a job is submitted

def _tasks():
    return json.load(open(TASKS)) if os.path.exists(TASKS) else {}

def one(j):
    """Submit (or resume) one cut and wait for it without ever abandoning it: a charged job is always collected."""
    num, p, secs, prompt = j
    out = os.path.join(OUT, f"cut_{num}.mp4")
    if os.path.exists(out):
        return f"skip {num}"
    tasks = _tasks()
    try:
        tid = tasks.get(num)
        if tid:  # resume a job submitted by an earlier run
            g = call(f"{API}/tasks/{tid}")
            if g["status"] in ("FAILED", "CANCELLED"):
                tid = None
        if not tid:
            img = "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()
            tid = call(f"{API}/image_to_video", {"model": "gen4_turbo", "promptImage": img, "promptText": prompt,
                                                 "ratio": "720:1280", "duration": secs})["id"]
            tasks[num] = tid
            json.dump(tasks, open(TASKS, "w"), indent=1)
        t0 = time.time()
        while True:  # no timeout: Runway queues jobs when the account is busy, and a queued job is still billed
            g = call(f"{API}/tasks/{tid}")
            if g["status"] == "SUCCEEDED":
                urllib.request.urlretrieve(g["output"][0], out)
                return f"ok {num} {secs}s in {int(time.time() - t0)}s"
            if g["status"] in ("FAILED", "CANCELLED"):
                return f"fail {num}: {g.get('failure') or g.get('failureCode')}"
            time.sleep(10)
    except urllib.error.HTTPError as e:
        return f"fail {num}: {e.code} {e.read()[:200]}"

if __name__ == "__main__":  # importing this module (for picture()) must never start renders
    jobs = []
    for r in rows:
        if only and r[0] not in only:
            continue
        if r[0] in os.environ.get("STILLS", "").split(","):  # budget: these stay stills with a push-in
            continue
        p = picture(r)
        if not p:
            continue
        need = math.ceil(timing.get(r[0], float(r[3])))
        secs = 5 if need <= 5 or os.environ.get("FIVE") else 10  # Gen-4 Turbo makes 5 s or 10 s clips; the edit trims or holds
        picture_text = re.sub(r"\*([^*]+)\*", r"\1", r[4])
        prompt = re.sub(r"\s+", " ", f"{picture_text.split('. On screen')[0]}. Subtle, natural motion.")[:220]  # Runway rejected long prompts
        jobs.append((r[0], p, secs, prompt))
    total = sum(j[2] for j in jobs)
    print(f"episode {ep}: {len(jobs)} cuts to animate, {total}s, about {total * 5} credits (${total * 0.05:.2f}); "
          f"stills kept: {len(rows) - len(jobs) if not only else 0}", flush=True)
    if os.environ.get("DRY"):
        sys.exit()

    for jb in jobs:  # one at a time: the account runs one job at a time, and parallel jobs only queue
        print(one(jb), flush=True)
