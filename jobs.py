"""Build img/jobs.json: every character sheet, location plate and keyframe to generate, per episode."""
import json, re, sys, os
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "packs_hand")

SHEET = ("Character reference sheet, {d}, front view, three-quarter view, profile, full body, "
         "plus three expressions, plain light-gray background, even studio light, photorealistic.")
desc, jobs = {}, []

def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:40]

def add(ep, kind, name, prompt, w, h):
    jobs.append(dict(id=f"e{ep:02d}_{kind}_{slug(name)}", ep=ep, kind=kind, name=name, prompt=prompt, w=w, h=h))

# Episode 1 comes from the plain-text export (tables are flattened to "cell\n | cell")
t = open(os.path.join(P, "ep1_plain.txt"), encoding="utf-8").read()
for tag, d in re.findall(r"^\[([A-Z]+)\]\n \| [^\n]*\n \| ([^\n]+)", t, re.M):
    desc[tag] = d.strip()
    add(1, "sheet", tag, SHEET.format(d=desc[tag]), 1536, 1024)
loc = t.split("Locations (empty plates, no people)")[1].split("Props and screens")[0]
for name, pr in re.findall(r"^([^\n|]+)\n \| ([^\n]{40,})", loc, re.M):
    add(1, "plate", name.strip(), pr.strip(), 1024, 1792)
for m in re.finditer(r"^Shot (\d+) · ([^\n]+)\n(?:[^\n]*\n)*?Keyframe[^:]*: ([^\n]+)", t, re.M):
    if len(m.group(3)) > 40:
        add(1, "key", f"shot {m.group(1)}", m.group(3).strip(), 1024, 1792)

for ep in range(2, 11):
    s = open(os.path.join(P, f"ep{ep}.md"), encoding="utf-8").read()
    for tag, what, d in re.findall(r"^\| \[([A-Z ]+)\] \| ([^|]+) \| ([^|]+) \|", s, re.M):
        if not what.strip().lower().startswith("same"):
            desc[tag] = d.strip()
            add(ep, "sheet", tag, SHEET.format(d=desc[tag]), 1536, 1024)
        desc.setdefault(tag, d.strip())
    loc = s.split("### Locations")[1].split("###")[0] if "### Locations" in s else ""
    for name, pr in re.findall(r"^\| ([^|]+) \| ([^|]+) \|", loc, re.M):
        if name.strip() in ("Reference", "---") or pr.strip().lower().startswith(("reuse", "same")):
            continue
        add(ep, "plate", name.strip(), pr.strip(), 1024, 1792)
    for sec in re.split(r"^### Shot ", s, flags=re.M)[1:]:
        num = sec.split(" ")[0]
        k = re.search(r"\*\*Keyframe[^*]*\*\*:? \*?([^\n]+?)\*?$", sec, re.M)
        if k and len(k.group(1)) > 40:
            add(ep, "key", f"shot {num}", k.group(1).strip(), 1024, 1792)

for j in jobs:  # paste locked descriptors in place of [TAGS]
    j["prompt"] = re.sub(r"\[([A-Z ]+)\]('s)?", lambda m: (desc.get(m.group(1), m.group(1).title()) + ("," if m.group(2) else "") if m.group(1) in desc else m.group(0)), j["prompt"])
os.makedirs(os.path.join(D, "img"), exist_ok=True)
json.dump(jobs, open(os.path.join(D, "img", "jobs.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
from collections import Counter
print(len(jobs), Counter((j["ep"], j["kind"]) for j in jobs))
left = [j["id"] for j in jobs if "[" in j["prompt"]]
print("unresolved tags:", left[:10])
