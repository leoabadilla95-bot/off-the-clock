"""screens.py: mock Groupon-style app screens for the Groupon beats, drawn as full-screen 9:16 phone inserts
(img/screens/*.jpg). Made-up businesses from the doc; deal photos are crops of our own location plates."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
D = os.path.dirname(os.path.abspath(__file__))
IMG, OUT = os.path.join(D, "img"), os.path.join(D, "img", "screens")
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
GREEN, INK, MUTED, LINE, BG = (83, 163, 24), (28, 30, 34), (110, 114, 122), (228, 230, 234), (246, 247, 249)
B = lambda s: ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", s)
R = lambda s: ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", s)
SYM = lambda s: ImageFont.truetype("C:/Windows/Fonts/seguisym.ttf", s)

def photo(name, size):
    return ImageOps.fit(Image.open(os.path.join(IMG, name)).convert("RGB"), size, Image.LANCZOS)

def rounded(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, *im.size], r, fill=255)
    out = Image.new("RGBA", im.size); out.paste(im, (0, 0), m); return out

def chrome(d, title):
    d.rectangle([0, 0, W, 120], fill="white")
    d.text((48, 38), "9:41", font=B(36), fill=INK)
    d.text((W - 230, 38), "5G", font=B(30), fill=INK)
    for k in range(4):  # signal bars and battery, drawn
        d.rectangle([W - 170 + k * 16, 70 - k * 8, W - 160 + k * 16, 72], fill=INK)
    d.rounded_rectangle([W - 96, 44, W - 48, 70], 6, outline=INK, width=3); d.rectangle([W - 92, 48, W - 62, 66], fill=INK)
    d.text((48, 140), "GROUPON", font=B(44), fill=GREEN)
    d.rounded_rectangle([48, 220, W - 48, 310], 45, fill=(238, 240, 243))
    d.ellipse([92, 247, 122, 277], outline=MUTED, width=4); d.line([118, 273, 132, 287], fill=MUTED, width=5)
    d.text((150, 242), title, font=R(38), fill=MUTED)

def price(d, x, y, now, was, big=False):
    f = B(54 if big else 40); d.text((x, y), now, font=f, fill=GREEN)
    x2 = x + d.textlength(now, font=f) + 20
    fw = R(36 if big else 30); d.text((x2, y + (14 if big else 8)), was, font=fw, fill=MUTED)
    w = d.textlength(was, font=fw); yy = y + (14 if big else 8) + (21 if big else 17)
    d.line([x2, yy, x2 + w, yy], fill=MUTED, width=3)

def card(im, d, y, img, title, place, now, was, tag=None, hi=False):
    if hi:
        d.rounded_rectangle([40, y - 12, W - 40, y + 330], 34, outline=GREEN, width=6)
    im.paste(rounded(photo(img, (300, 300)), 26), (56, y + 2), rounded(photo(img, (300, 300)), 26))
    x = 390
    if tag:
        d.rounded_rectangle([x, y + 4, x + d.textlength(tag, font=B(26)) + 32, y + 50], 23, fill=(234, 245, 225))
        d.text((x + 16, y + 9), tag, font=B(26), fill=GREEN)
    d.text((x, y + 66), title, font=B(42), fill=INK)
    d.text((x, y + 124), place, font=R(32), fill=MUTED)
    d.text((x, y + 172), "★", font=SYM(30), fill=(240, 180, 30)); d.text((x + 34, y + 172), "4.8  ·  1.2k ratings", font=R(30), fill=MUTED)
    price(d, x, y + 222, now, was)

def feed(name, query, chips, active, cards, hi_index):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    chrome(d, query)
    x = 48
    for c in chips:
        w = d.textlength(c, font=B(32)) + 56
        d.rounded_rectangle([x, 345, x + w, 415], 35, fill=GREEN if c == active else "white", outline=None if c == active else LINE, width=3)
        d.text((x + 28, 359), c, font=B(32), fill="white" if c == active else INK); x += w + 18
    d.text((48, 460), "Near you · Chicago", font=B(46), fill=INK)
    y = 560
    for k, c in enumerate(cards):
        card(im, d, y, *c, hi=(k == hi_index)); y += 380
    im.save(os.path.join(OUT, name), quality=92)

def deal(name, img, title, place, now, was, off):
    im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    im.paste(photo(img, (W, 900)), (0, 0))
    d.rounded_rectangle([48, 60, 200, 128], 34, fill=(0, 0, 0)); d.text((84, 70), "‹ Back", font=B(32), fill="white")
    d.rounded_rectangle([W - 230, 820, W - 48, 880], 30, fill=GREEN); d.text((W - 200, 828), off, font=B(34), fill="white")
    d.text((56, 940), title, font=B(64), fill=INK)
    d.text((56, 1030), place, font=R(38), fill=MUTED)
    d.text((56, 1090), "★", font=SYM(34), fill=(240, 180, 30)); d.text((96, 1090), "4.8  ·  1,240 ratings  ·  First-timers welcome", font=R(34), fill=MUTED)
    price(d, 56, 1180, now, was, big=True)
    d.text((56, 1290), "• 1 hour lane for two, coach included\n• Valid any day after 5 pm\n• Free cancellation up to 24 h", font=R(36), fill=INK, spacing=18)
    d.rounded_rectangle([48, 1700, W - 48, 1830], 65, fill=GREEN)
    t = "Buy for 2  ·  " + now; d.text(((W - d.textlength(t, font=B(48))) / 2, 1733), t, font=B(48), fill="white")
    im.save(os.path.join(OUT, name), quality=92)

def voucher(name, img, title, when, shared):
    im = Image.new("RGB", (W, H), GREEN); d = ImageDraw.Draw(im)
    d.text((W / 2 - d.textlength("You're going!", font=B(80)) / 2, 230), "You're going!", font=B(80), fill="white")
    d.rounded_rectangle([70, 400, W - 70, 1650], 48, fill="white")
    im.paste(rounded(photo(img, (W - 220, 420)), 30), (110, 450), rounded(photo(img, (W - 220, 420)), 30))
    d.text((110, 910), title, font=B(54), fill=INK)
    d.text((110, 990), when, font=R(38), fill=MUTED)
    import random; random.seed(7)  # a mock QR block
    qx, qy, cell = W / 2 - 180, 1080, 24
    for i in range(15):
        for j in range(15):
            if random.random() > .5 or (i < 4 and j < 4) or (i > 10 and j < 4) or (i < 4 and j > 10):
                d.rectangle([qx + i * cell, qy + j * cell, qx + i * cell + cell - 2, qy + j * cell + cell - 2], fill=INK)
    d.text((W / 2 - d.textlength(shared, font=B(36)) / 2, 1500), shared, font=B(36), fill=GREEN)
    im.save(os.path.join(OUT, name), quality=92)

# Episode 1: the feed, the axe deal, the voucher
feed("e01_feed.jpg", "Things to do near you", ["Activities", "Classes", "Food", "Wellness"], "Activities", [
    ("e02_plate_axe_lane.jpg", "Axe Throwing for Two", "Bullseye Axe House · West Loop", "$39", "$70", "Under $40"),
    ("e06_plate_lake_dock.jpg", "Sunset Kayak Tour", "Lakeshore Paddle Co. · Lakefront", "$45", "$80", None),
    ("e05_plate_float_pod_room.jpg", "Float + Sauna for Two", "Drift Float & Sauna · Wicker Park", "$59", "$110", None),
], 0)
deal("e01_deal.jpg", "e02_plate_axe_lane.jpg", "Axe Throwing for Two", "Bullseye Axe House · West Loop", "$39", "$70", "44% off")
voucher("e01_voucher.jpg", "e02_plate_axe_lane.jpg", "Axe Throwing for Two", "Friday · 7:00 pm · Bullseye Axe House", "Shared with Hunter (Ops)")
# Episode 3: Classes tab, the tamale class highlighted
feed("e03_classes.jpg", "Classes near you", ["Activities", "Classes", "Food", "Wellness"], "Classes", [
    ("e03_plate_masa_m_a_kitchen.jpg", "Tamale-Making Class", "Masa Mía · Pilsen · you leave with dinner", "$34", "$60", "Near you"),
    ("e09_plate_kiln_co_studio.jpg", "Pottery Wheel for Two", "Kiln & Co. · Logan Square", "$49", "$90", None),
    ("e08_plate_black_box_theater_house.jpg", "Improv Night for 6", "Second Act Improv · Old Town", "$60", "$120", None),
], 0)
print(sorted(os.listdir(OUT)))
