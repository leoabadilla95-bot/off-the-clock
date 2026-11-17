"""build_v2.py: scripts_v2/epNN.md tables -> tables_v2.json ({"1": [[#, scene, shot, sec, picture, dialogue, key], ...]})
(captions come from gen_voices.py in V2 mode)."""
import json, os, re, sys, glob, textwrap
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
LABEL = re.compile(r"([A-Z][A-Z]+(?: [A-Z][A-Z]+)*)(?: \(([^)]*)\))?:\s")
TAG = re.compile(r"\[[^\]]*\]\s*")

tables = {}
for f in sorted(glob.glob(os.path.join(D, "scripts_v2", "ep*.md"))):
    ep = str(int(re.search(r"ep(\d+)", f).group(1)))
    rows = [[c.strip() for c in l.split("|")[1:-1]] for l in open(f, encoding="utf-8") if re.match(r"\|\s*\d", l)]
    tables[ep] = [r[:7] + [""] * (7 - len(r)) for r in rows]
json.dump(tables, open(os.path.join(D, "tables_v2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)

def ts(s):
    ms = round(s * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"

# Captions are written by gen_voices.py (V2=1) from the recorded line timings, so they stay in sync.
for ep, rows in tables.items():
    print(f"ep{ep}: {len(rows)} cuts, {sum(int(r[3]) for r in rows)}s scripted")
