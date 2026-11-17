"""Final script tables -> tables.json + captions/epNN.srt (dialogue only; on-screen text is a graphic)."""
import json, re, sys, os, textwrap
import xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))

def load(n):
    t = json.load(open(os.path.join(D, n), encoding="utf-8"))[1]["text"]
    i = t.find("\n\nThis doc takes")
    return json.loads(t[:i] if i > 0 else t)["data"]["xml"]

eps = {}
for n in ("final.json", "final2.json"):  # final2 wins (Ep 9 is cut short in final.json)
    cur = None
    for el in ET.fromstring(load(n)):
        tx = "".join(el.itertext())
        if el.tag == "paragraph" and el.get("heading"):
            m = re.match(r"Episode (\d+): .*\((\d+)s\)", tx)
            if m:
                cur = int(m.group(1))
        if el.tag == "table" and cur:
            rows = [["".join(c.itertext()).strip() for c in r if c.tag == "cell"] for r in el if r.tag == "row"]
            if rows[0][:4] == ["#", "Scene", "Shot", "Sec"]:
                eps[cur] = rows[1:]
json.dump(eps, open(os.path.join(D, "tables.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)

LABEL = re.compile(r"([A-Z][A-Z]+(?: [A-Z][A-Z]+)*(?: \([^)]*\))?):\s")

def ts(s):
    ms = round(s * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"

def lines_of(dlg):
    """[(speaker, spoken text)] — quoted words only, stage directions dropped."""
    parts = LABEL.split(dlg)
    out = []
    for i in range(1, len(parts), 2):
        said = " ".join(re.findall(r'"([^"]*)"', parts[i + 1])).strip()
        if said:
            out.append((parts[i].split(" (")[0], said))
    return out

os.makedirs(os.path.join(D, "captions"), exist_ok=True)
for ep, rows in sorted(eps.items()):
    t, cues = 0.0, []
    for r in rows:
        sec = int(r[3])
        ls = lines_of(r[5])
        words = sum(len(s.split()) for _, s in ls) or 1
        start = t
        for spk, said in ls:
            dur = sec * len(said.split()) / words
            # one cue per ~2 lines of 38 chars
            chunks = textwrap.wrap(said, 76) or [said]
            cw = sum(len(c) for c in chunks)
            s0 = start
            for c in chunks:
                d = dur * len(c) / cw
                cues.append((s0, s0 + d - 0.05, "\n".join(textwrap.wrap(c, 38))))
                s0 += d
            start += dur
        t += sec
    srt = "\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{txt}\n" for i, (a, b, txt) in enumerate(cues, 1))
    open(os.path.join(D, "captions", f"ep{ep:02d}.srt"), "w", encoding="utf-8").write(srt)
    print(ep, len(rows), "rows", t, "s", len(cues), "cues")
