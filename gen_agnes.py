"""gen_agnes.py [epFrom] [epTo]: generate unfinished jobs with Agnes AI's free image model.
Shots that name Hunter or Abby send their locked reference sheet so faces stay consistent.
Key comes from the AGNES_API_KEY user environment variable; never printed. Env LIMIT caps the job count."""
import json, os, sys, time, base64, subprocess, urllib.request, urllib.error, winreg
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(D, "img")
KEY = os.environ.get("AGNES_API_KEY") or winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), "AGNES_API_KEY")[0]
URL = "https://apihub.agnes-ai.com/v1/images/generations"
MODEL = "agnes-image-2.5-flash"
# A phrase from each lead's locked descriptor -> that lead's reference sheet
REFS = {"Mexican-American woman in her late 20s": "e01_sheet_abby.jpg",
        "tall and lean with slightly hunched shoulders": "e01_sheet_hunter.jpg"}
import re
STOP = {"the", "a", "of", "at", "in", "on", "and", "s", "recap", "night", "late", "cont", "int", "ext"}
ALIAS = {"water": "lake", "door": "entrance", "stall": "cart"}
words = lambda t: {ALIAS.get(w, w) for w in re.findall(r"[a-z0-9]+", t.lower())} - STOP
NAMES = {j["id"]: j["name"] for j in json.load(open(os.path.join(IMG, "jobs.json"), encoding="utf-8"))}

def location(ep, shot):
    """Scene name from the pack's shot heading ('### Shot 3 · 0:08 · MS · 7s · 4th floor')."""
    src = os.path.join(D, "packs_hand", "ep1_plain.txt" if ep == 1 else f"ep{ep}.md")
    m = re.search(rf"^(?:### )?Shot {shot} · ([^\n]+)", open(src, encoding="utf-8").read(), re.M)
    return m.group(1).split("·")[-1].strip() if m else ""

def plate_for(ep, scene):
    plates = sorted((f for f in os.listdir(IMG) if re.match(r"e\d\d_plate_.*\.jpg$", f)),
                    key=lambda f: (int(f[1:3]) != ep, abs(int(f[1:3]) - ep)))
    best = max(plates, key=lambda f: len(words(scene) & words(NAMES.get(f[:-4], ""))), default=None)
    return best if best and words(scene) & words(NAMES.get(best[:-4], "")) else None


def data_uri(name):
    return "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(IMG, name), "rb").read()).decode()

def one(j):
    body = {"model": MODEL, "prompt": j["prompt"], "n": 1, "size": "1280x720" if j["w"] > j["h"] else "720x1280"}
    names = {"e01_sheet_abby.jpg": "Abby", "e01_sheet_hunter.jpg": "Hunter"}
    refs = [data_uri(f) for k, f in REFS.items()
            if j["kind"] == "key" and (k in j["prompt"] or re.search(rf"{names[f]}", j["prompt"]))]
    if refs:
        plate = plate_for(j["ep"], j.get("scene") or location(j["ep"], j["name"].split()[-1]))
        if plate:
            refs.insert(0, data_uri(plate))
            body["prompt"] += (" Reference 1 is the location: set the shot in that exact place, keeping its walls, light and props."
                               " The other references are character sheets: take only each person's face, hair and clothing from them, never their gray backdrop.")
        else:
            body["prompt"] += (" The references are character sheets: take only each person's face, hair and clothing, never their gray backdrop;"
                               " build the full location described above.")
        body["extra_body"] = {"response_format": "url", "image": refs}
    for attempt in range(4):
        req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST", headers={
            "Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "User-Agent": "off-the-clock-previs/1.0"})
        try:
            d = json.load(urllib.request.urlopen(req, timeout=180))["data"][0]
            if d.get("url"):
                src = d["url"]
            else:  # base64 answer: write the raw file, then let dl.py treat it as a file:// URL
                raw = os.path.join(IMG, "raw", j["id"] + ".png")
                open(raw, "wb").write(base64.b64decode(d["b64_json"]))
                src = "file:///" + raw.replace(os.sep, "/")
            out = subprocess.run([sys.executable, os.path.join(D, "dl.py"), j["id"], src], capture_output=True, text=True)
            return (out.stdout.strip() or out.stderr.strip()[-200:]) + (" (ref)" if refs else "")
        except urllib.error.HTTPError as e:
            msg = e.read()[:300]
            if e.code == 429:  # free tier: 16 requests/min
                time.sleep(15); continue
            return f"fail {j['id']}: {e.code} {msg}"
        except Exception as e:
            return f"fail {j['id']}: {str(e)[:200]}"
    return f"fail {j['id']}: still rate limited"

if __name__ == "__main__":
    lo, hi = (int(a) for a in (sys.argv[1:3] or (1, 10)))
    jobs = [j for j in json.load(open(os.path.join(IMG, "jobs.json"), encoding="utf-8"))
            if lo <= j["ep"] <= hi and not os.path.exists(os.path.join(IMG, "done", j["id"] + ".json"))]
    jobs = jobs[:int(os.environ.get("LIMIT", 10**9))]
    print("todo", len(jobs), flush=True)
    with ThreadPoolExecutor(3) as ex:
        for r in ex.map(one, jobs):
            print(r, flush=True)
