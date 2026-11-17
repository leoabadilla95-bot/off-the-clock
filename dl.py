"""dl.py <job_id> <figma_image_url>: download, compress to img/<id>.jpg, mark done."""
import sys, os, json, urllib.request
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
jid, url = sys.argv[1], sys.argv[2]
raw = os.path.join(D, "raw", jid + ".png")
import subprocess; subprocess.run(["curl", "-s", "-f", "-L", "-o", raw, url], check=True)
im = Image.open(raw).convert("RGB"); im.thumbnail((1280, 1280)); im.save(os.path.join(D, jid + ".jpg"), quality=82)
json.dump({"id": jid, "url": url}, open(os.path.join(D, "done", jid + ".json"), "w"))
print("ok", jid, os.path.getsize(os.path.join(D, jid + ".jpg")))
