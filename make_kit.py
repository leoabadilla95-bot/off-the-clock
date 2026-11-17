"""make_kit.py <ep...>: a Runway kit per episode in runway_kit/epNN/: start images named by cut, plus SHOT_SHEET.md
(cut, image, short prompt, Runway length, trim length, mouth note). For making the clips by hand in the Runway web app."""
import json, math, os, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
LABEL = re.compile(r"([A-Z][A-Z]+(?: [A-Z][A-Z]+)*)(?: \(([^)]*)\))?:\s")
TITLES = {1: "Hunter from Ops", 2: "Bullseye", 3: "Masa"}

for ep in map(int, sys.argv[1:]):
    sys.argv = [sys.argv[0], str(ep)]
    import importlib, runway_v2
    importlib.reload(runway_v2)
    rows = runway_v2.rows; timing = runway_v2.timing
    out = os.path.join(D, "runway_kit", f"ep{ep:02d}"); os.makedirs(out, exist_ok=True)
    lines = [f"# Episode {ep}: {TITLES.get(ep, '')} · Runway shot sheet", "",
             "Make each clip in the Runway web app with **Gen-4 Turbo**, image to video, ratio **720:1280 (9:16)**.",
             "Upload the start image, paste the prompt, set the length, generate, and download the clip as `cut_<id>.mp4` into",
             f"`video/ep{ep:02d}_runway_v2/`. Then run `python assemble_runway.py {ep}` to cut it with the soundtrack and captions.",
             "Keep prompts short: Runway's API rejected the long versions. Rows marked *still* need no clip.",
             "For lip-sync, pair a finished clip with its `voice/cut_<id>.mp3` (on-camera speech only, starting at the clip's first",
             "frame) in Runway Lip Sync or any lip-sync tool. `soundtrack.m4a` is the finished mix the assembler lays under the cut.", "",
             "| Cut | Start image | Prompt | Runway length | Trim to | Mouth | Voice for lip-sync |", "| --- | --- | --- | --- | --- | --- | --- |"]
    total = 0
    for r in rows:
        num, key = r[0], (r[6] if len(r) > 6 else "")
        trim = timing.get(num, float(r[3]))
        parts = LABEL.split(r[5]); talk, think = [], []
        for i in range(1, len(parts), 3):
            if re.findall(r'"([^"]*)"', parts[i + 2]):
                (think if "V.O." in (parts[i + 1] or "") or "O.S." in (parts[i + 1] or "") else talk).append(parts[i].title())
        mouth = ("speaks: " + ", ".join(dict.fromkeys(talk))) if talk else ("closed (thought only)" if think else "no dialogue")
        if key.startswith("screen:"):
            lines.append(f"| {num} | *still:* `img/screens/{key[7:].strip()}` | Groupon app screen, no clip | — | {trim:g} s | — | — |")
            continue
        src = runway_v2.picture(r)
        name = f"ep{ep:02d}_cut_{num.zfill(3) if num.isdigit() else num.zfill(3)}.jpg"
        if src and os.path.exists(src):
            shutil.copy(src, os.path.join(out, name))
        picture = re.sub(r"\*([^*]+)\*", r"\1", r[4]).split(". On screen")[0]
        prompt = re.sub(r"\s+", " ", f"{picture}. Subtle, natural motion. {'Mouth moves as they talk.' if talk else 'Lips stay closed.'}")[:220]
        length = 5 if math.ceil(trim) <= 5 else 10
        total += length
        voice = f"`voice/cut_{num}.mp3`" if os.path.exists(os.path.join(out, "voice", f"cut_{num}.mp3")) else "—"
        lines.append(f"| {num} | `{name}` | {prompt.replace('|', '/')} | {length} s | {trim:g} s | {mouth} | {voice} |")
    lines += ["", f"**Total:** {total} seconds of Gen-4 Turbo, about {total * 5} credits."]
    open(os.path.join(out, "SHOT_SHEET.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"ep{ep}: {len([l for l in lines if l.startswith('| ') and 'still' not in l]) - 1} clips, {total}s, kit in runway_kit/ep{ep:02d}")
