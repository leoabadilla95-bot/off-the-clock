"""v2_jobs.py: add every `new:` keyframe from tables_v2.json to img/jobs.json (id v2_eNN_<cut>), descriptors pasted in."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
jobs = json.load(open(os.path.join(D, "img", "jobs.json"), encoding="utf-8"))
have = {j["id"] for j in jobs}
# locked descriptors from the existing jobs' sheet prompts
desc = {}
for j in jobs:
    if j["kind"] == "sheet":
        m = re.match(r"Character reference sheet, (.+?), front view", j["prompt"])
        if m:
            desc[j["name"].upper()] = m.group(1)
NAMES = {"Hunter": "HUNTER", "Abby": "ABBY", "Priya": "PRIYA", "Grant": "GRANT", "Jo": "JO", "Lupe": "LUPE", "Celeste": "CELESTE"}
added = 0
for ep, rows in json.load(open(os.path.join(D, "tables_v2.json"), encoding="utf-8")).items():
    for r in rows:
        key = r[6] if len(r) > 6 else ""
        if not key.startswith("new"):
            continue
        jid = f"v2_e{int(ep):02d}_{r[0]}"
        if jid in have:
            continue
        prompt = key.split(":", 1)[1].strip()
        for n, tag in NAMES.items():  # first mention of a character gets the full locked descriptor
            if re.search(rf"\b{n}\b", prompt) and tag in desc:
                prompt = re.sub(rf"\b{n}\b", f"{n} ({desc[tag]})", prompt, count=1)
        prompt += ", vertical 9:16, cinematic, photorealistic, natural light"
        jobs.append({"id": jid, "ep": int(ep), "kind": "key", "name": f"v2 cut {r[0]}", "scene": r[1], "prompt": prompt, "w": 1024, "h": 1792})
        added += 1
json.dump(jobs, open(os.path.join(D, "img", "jobs.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("added", added, "v2 keyframe jobs")
