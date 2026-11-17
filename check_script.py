"""check_script.py <file.md>: runtime, cut count, and every cut whose spoken + thought words outrun its seconds (2.6 words/s)."""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
rows = [l.split("|")[1:-1] for l in open(sys.argv[1], encoding="utf-8") if re.match(r"\|\s*\d", l)]
total, issues, vo = 0, [], 0
for r in rows:
    num, sec, dlg = r[0].strip(), int(r[3]), r[5]
    words = sum(len(q.split()) for q in re.findall(r'"([^"]*)"', dlg))
    vo += len(re.findall(r"\(V\.O\.", dlg))
    total += sec
    if words / sec > 2.6:
        issues.append(f"{num}: {words} words in {sec}s ({words / sec:.1f}/s)")
    if len(r) < 7 or not r[6].strip():
        issues.append(f"{num}: missing Key column")
print(f"cuts {len(rows)}, runtime {total}s, thoughts {vo}")
print("\n".join(issues) or "pacing ok")
