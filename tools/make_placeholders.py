"""Generate elegant placeholder product images + payment QR + OG image for KIARIT."""
import os, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(os.path.join(IMG, "products"), exist_ok=True)
os.makedirs(os.path.join(IMG, "qr"), exist_ok=True)
os.makedirs(os.path.join(IMG, "og"), exist_ok=True)


def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif%s.ttf" % ("-Bold" if bold else ""),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


# Backgrounds match the category tints used in the CSS so the cards and the
# imagery read as one system.
PRODUCTS = [
    ("KIARIT",  "RITCLEAR AZ",   "Azelaic Acid Serum",    (234, 239, 231), (99, 118, 95)),
    ("KIARIT",  "RITSHADE",      "SPF 50+ PA++++",        (253, 241, 216), (201, 162, 39)),
    ("KIARIT",  "RITGLOW",       "Oil-Free Face Wash",    (244, 230, 224), (176, 118, 96)),
    ("KIARIT",  "KIAMILD",       "Foaming Shampoo",       (240, 235, 225), (150, 130, 100)),
    ("KIARIT",  "KIARESTORA",    "Cleansing Shower Oil",  (238, 240, 242), (110, 130, 145)),
]

W = H = 900


def product_image(i, brand, name, sub, bg, accent):
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)

    # soft radial light
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W * .12, H * .05, W * .95, H * .82], fill=110)
    glow = glow.filter(ImageFilter.GaussianBlur(150))
    im = Image.composite(Image.new("RGB", (W, H), (255, 255, 255)), im, glow.point(lambda v: v // 2))
    d = ImageDraw.Draw(im)

    # champagne circle backdrop
    cx, cy, r = W // 2, int(H * .47), int(W * .30)
    circ = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(circ)
    cd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent + (30,))
    circ = circ.filter(ImageFilter.GaussianBlur(3))
    im = Image.alpha_composite(im.convert("RGBA"), circ).convert("RGB")
    d = ImageDraw.Draw(im)

    # ---- bottle silhouette ----
    bw, bh = int(W * .215), int(H * .40)
    bx0, by0 = cx - bw // 2, cy - bh // 2 + 26
    bx1, by1 = bx0 + bw, by0 + bh

    bot = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bot)
    # body
    bd.rounded_rectangle([bx0, by0, bx1, by1], radius=int(bw * .21), fill=(255, 255, 255, 244))
    # neck + cap
    nw = int(bw * .34)
    bd.rectangle([cx - nw // 2, by0 - 30, cx + nw // 2, by0 + 6], fill=(255, 255, 255, 244))
    bd.rounded_rectangle([cx - nw // 2 - 7, by0 - 74, cx + nw // 2 + 7, by0 - 26],
                         radius=7, fill=(24, 24, 26, 255))
    bd.rounded_rectangle([cx - nw // 2 - 7, by0 - 40, cx + nw // 2 + 7, by0 - 30],
                         radius=3, fill=accent + (255,))
    # glass highlight
    bd.rounded_rectangle([bx0 + 13, by0 + 16, bx0 + 34, by1 - 40], radius=10, fill=(255, 255, 255, 210))
    # tinted liquid at the bottom
    bd.rounded_rectangle([bx0 + 8, by0 + int(bh * .46), bx1 - 8, by1 - 8],
                         radius=int(bw * .17), fill=accent + (78,))
    # label band
    ly0, ly1 = by0 + int(bh * .30), by0 + int(bh * .62)
    bd.rectangle([bx0 + 4, ly0, bx1 - 4, ly1], fill=(253, 251, 247, 252))
    bd.line([bx0 + 4, ly0, bx1 - 4, ly0], fill=accent + (200,), width=2)
    bd.line([bx0 + 4, ly1, bx1 - 4, ly1], fill=accent + (200,), width=2)

    # shadow
    sh = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(sh)
    sd.ellipse([bx0 - 34, by1 - 16, bx1 + 34, by1 + 34], fill=88)
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    im.paste(Image.new("RGB", (W, H), (60, 52, 40)), (0, 0), sh)

    im = Image.alpha_composite(im.convert("RGBA"), bot).convert("RGB")
    d = ImageDraw.Draw(im)

    # label micro-text
    f_b = font(15, True)
    f_s = font(11)
    tw = d.textlength(brand, f_b)
    d.text((cx - tw / 2, ly0 + 16), brand, font=f_b, fill=(28, 28, 30))
    short = name.split()[0]
    tw = d.textlength(short, f_s)
    d.text((cx - tw / 2, ly0 + 40), short, font=f_s, fill=accent)

    # top eyebrow + bottom caption
    f_e = font(19, True)
    f_n = font(40, True)
    f_c = font(20)
    tw = d.textlength(brand, f_e)
    d.text((cx - tw / 2, int(H * .085)), brand, font=f_e, fill=(150, 120, 40))
    tw = d.textlength(name, f_n)
    d.text((cx - tw / 2, int(H * .795)), name, font=f_n, fill=(24, 24, 28))
    tw = d.textlength(sub, f_c)
    d.text((cx - tw / 2, int(H * .875)), sub, font=f_c, fill=(120, 122, 128))
    d.line([cx - 34, int(H * .775), cx + 34, int(H * .775)], fill=(201, 162, 39), width=2)

    # thin gold frame
    d.rectangle([16, 16, W - 17, H - 17], outline=(201, 162, 39), width=1)

    p = os.path.join(IMG, "products", "product-%d.jpg" % i)
    im.save(p, quality=88, optimize=True)
    print(" ->", p)


for i, (b, n, s, bg, ac) in enumerate(PRODUCTS, 1):
    product_image(i, b, n, s, bg, ac)


# ---------------- Payment QR placeholder ----------------
def fake_qr(size=560):
    import random
    rng = random.Random(2026)
    mod = 33
    q = Image.new("RGB", (mod, mod), "white")
    px = q.load()
    for y in range(mod):
        for x in range(mod):
            if rng.random() < .46:
                px[x, y] = (10, 10, 12)

    def finder(ox, oy):
        for y in range(7):
            for x in range(7):
                edge = x in (0, 6) or y in (0, 6)
                core = 2 <= x <= 4 and 2 <= y <= 4
                px[ox + x, oy + y] = (10, 10, 12) if (edge or core) else (255, 255, 255)
        for y in range(-1, 8):
            for x in range(-1, 8):
                if 0 <= ox + x < mod and 0 <= oy + y < mod and (x in (-1, 7) or y in (-1, 7)):
                    px[ox + x, oy + y] = (255, 255, 255)

    finder(0, 0); finder(mod - 7, 0); finder(0, mod - 7)
    q = q.resize((size, size), Image.NEAREST)

    pad = 46
    card = Image.new("RGB", (size + pad * 2, size + pad * 2 + 74), "white")
    card.paste(q, (pad, pad))
    d = ImageDraw.Draw(card)
    d.rectangle([10, 10, card.width - 11, card.height - 11], outline=(201, 162, 39), width=3)
    f1 = font(30, True); f2 = font(20)
    t = "KIARIT PHARMACEUTICALS"
    d.text(((card.width - d.textlength(t, f1)) / 2, size + pad + 18), t, font=f1, fill=(20, 20, 24))
    t2 = "Scan to pay  •  UPI"
    d.text(((card.width - d.textlength(t2, f2)) / 2, size + pad + 56), t2, font=f2, fill=(150, 120, 40))
    p = os.path.join(IMG, "qr", "payment-qr.png")
    card.save(p, optimize=True)
    print(" ->", p)


fake_qr()


# ---------------- OG social share image ----------------
def og():
    w, h = 1200, 630
    im = Image.new("RGB", (w, h), (8, 8, 10))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=(int(8 + 14 * t), int(8 + 11 * t), int(10 + 9 * t)))
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse([w * .52, -h * .35, w * 1.35, h * .95], fill=120)
    glow = glow.filter(ImageFilter.GaussianBlur(190))
    im.paste(Image.new("RGB", (w, h), (201, 162, 39)), (0, 0), glow)
    d = ImageDraw.Draw(im)
    d.rectangle([34, 34, w - 35, h - 35], outline=(201, 162, 39), width=2)
    f1 = font(66, True); f2 = font(27); f3 = font(21, True)
    d.text((92, 214), "KIARIT", font=f1, fill=(248, 241, 222))
    d.text((92, 292), "PHARMACEUTICALS", font=f1, fill=(201, 162, 39))
    d.text((92, 170), "S C I E N C E   M E E T S   B E A U T Y", font=f3, fill=(214, 190, 130))
    d.text((92, 396), "Dermatology  •  Skincare  •  Nutraceuticals", font=f2, fill=(200, 196, 190))
    d.line([92, 372, 260, 372], fill=(201, 162, 39), width=3)
    p = os.path.join(IMG, "og", "og-default.jpg")
    im.save(p, quality=90, optimize=True)
    print(" ->", p)


og()
print("Done.")
