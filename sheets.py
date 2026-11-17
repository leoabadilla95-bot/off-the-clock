"""sheets.py <ep>: contact sheets -> img/sheets/eNN_keys_K.jpg (8 shots each) + eNN_plates.jpg"""
import re, sys, os, json
from PIL import Image, ImageDraw, ImageFont, ImageOps
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
IMG, SH = os.path.join(D, "img"), os.path.join(D, "img", "sheets")
os.makedirs(SH, exist_ok=True)
ep = int(sys.argv[1])
F = lambda s, b=False: ImageFont.truetype("C:/Windows/Fonts/" + ("segoeuib.ttf" if b else "segoeui.ttf"), s)
TW, TH, LAB, PAD, COLS = 300, 533, 64, 12, 4

src = os.path.join(D, "packs_hand", "ep1_plain.txt" if ep == 1 else f"ep{ep}.md")
heads = re.findall(r"^(?:### )?Shot (\d+) · ([^\n]+)", open(src, encoding="utf-8").read(), re.M)

def grid(tiles, out):
    rows = (len(tiles) + COLS - 1) // COLS
    sheet = Image.new("RGB", (PAD + COLS * (TW + PAD), PAD + rows * (TH + LAB + PAD)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (path, l1, l2) in enumerate(tiles):
        x, y = PAD + i % COLS * (TW + PAD), PAD + i // COLS * (TH + LAB + PAD)
        if path:
            sheet.paste(ImageOps.fit(Image.open(path).convert("RGB"), (TW, TH), Image.LANCZOS), (x, y))
        else:
            d.rectangle([x, y, x + TW, y + TH], fill=(235, 235, 235))
            d.text((x + 20, y + TH // 2), "Reuses a plate", font=F(20), fill=(120, 120, 120))
        d.text((x + 2, y + TH + 6), l1, font=F(20, True), fill=(20, 20, 20))
        d.text((x + 2, y + TH + 34), l2[:32], font=F(17), fill=(90, 90, 90))
    sheet.save(out, quality=84)

made = []
tiles = []
for num, rest in heads:
    parts = [p.strip() for p in rest.split("·")]
    p = os.path.join(IMG, f"e{ep:02d}_key_shot_{num}.jpg")
    tiles.append((p if os.path.exists(p) else None, f"Shot {num} · {parts[0]}", f"{parts[1]} · {parts[-1]}" if len(parts) > 2 else parts[-1]))
for k in range(0, len(tiles), 8):
    out = os.path.join(SH, f"e{ep:02d}_keys_{k // 8 + 1}.jpg")
    grid(tiles[k:k + 8], out); made.append((out, f"Shots {heads[k][0]}–{heads[min(k + 7, len(heads) - 1)][0]}"))
plates = sorted(f for f in os.listdir(IMG) if f.startswith(f"e{ep:02d}_plate") and f.endswith(".jpg"))
if plates:
    out = os.path.join(SH, f"e{ep:02d}_plates.jpg")
    names = {j["id"]: j["name"] for j in json.load(open(os.path.join(IMG, "jobs.json"), encoding="utf-8"))}
    grid([(os.path.join(IMG, f), names.get(f[:-4], f), "Location plate") for f in plates], out)
    made.append((out, "Location plates"))
print(ep, [os.path.basename(m[0]) for m in made], "missing keys:", [t[1] for t in tiles if not t[0]])
