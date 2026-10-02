#!/usr/bin/env python3
"""Builds optimized image assets for theqsalonsrq.com from the two source photos.
Run once after replacing a source photo: python3 make_assets.py [fontdir]
Outputs into dist/assets/ (descriptive SEO filenames, WebP + JPEG, OG share image, favicons)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

A = "dist/assets"
FONTS = sys.argv[1] if len(sys.argv) > 1 else "fonts"
NAVY, BRASS, BRASS_L, STONE = (20, 32, 46), (176, 141, 87), (214, 185, 132), (243, 240, 234)

def save_pair(im, base, width, q=78):
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im = im.convert("RGB")
    im.save(f"{A}/{base}.jpg", "JPEG", quality=q, optimize=True, progressive=True)
    im.save(f"{A}/{base}.webp", "WEBP", quality=q - 4, method=6)
    return im.size

hero = Image.open(f"{A}/hero-gent.jpg")
susy = Image.open(f"{A}/susy.jpg")
print("hero", save_pair(hero, "mens-haircut-sarasota-silver-swept-back", 900))
print("susy", save_pair(susy, "susy-master-barber-sarasota", 800))
save_pair(susy, "susy-master-barber-sarasota-thumb", 120, q=80)

# ---- 1200x630 share image: photo left, navy panel right ----
W, H = 1200, 630
og = Image.new("RGB", (W, H), NAVY)
ph = hero.convert("RGB")
pw = 470
scale = max(pw / ph.width, H / ph.height)
ph = ph.resize((round(ph.width * scale), round(ph.height * scale)), Image.LANCZOS)
top = round((ph.height - H) * 0.3)
og.paste(ph.crop(((ph.width - pw) // 2, top, (ph.width - pw) // 2 + pw, top + H)), (0, 0))
d = ImageDraw.Draw(og)
d.rectangle([pw, 0, pw + 3, H], fill=BRASS)
disp = ImageFont.truetype(f"{FONTS}/Marcellus-Regular.ttf", 64)
mono = ImageFont.truetype(f"{FONTS}/DMMono-Medium.ttf", 22)
body = ImageFont.truetype(f"{FONTS}/HankenGrotesk[wght].ttf", 28)
x = pw + 70
d.text((x, 120), "MEN'S GROOMING · SARASOTA", font=mono, fill=BRASS_L)
d.text((x, 175), "The Q Salon", font=disp, fill=STONE)
d.text((x, 250), "for Men", font=disp, fill=BRASS_L)
d.line([x, 352, x + 90, 352], fill=BRASS, width=2)
d.text((x, 380), "Haircuts · Skin fades · Gray blending", font=body, fill=STONE)
d.text((x, 422), "Every cut by master stylist Susy", font=body, fill=(169, 179, 191))
d.text((x, 520), "1415 1ST ST · DOWNTOWN SARASOTA", font=mono, fill=BRASS_L)
og.save(f"{A}/the-q-salon-for-men-sarasota-share.jpg", "JPEG", quality=86, optimize=True)

# ---- favicons: brass Q on navy circle ----
def mark(size):
    s = size * 4
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.ellipse([0, 0, s - 1, s - 1], fill=NAVY)
    f = ImageFont.truetype(f"{FONTS}/Marcellus-Regular.ttf", int(s * 0.62))
    bb = dd.textbbox((0, 0), "Q", font=f)
    dd.text(((s - (bb[2] - bb[0])) / 2 - bb[0], (s - (bb[3] - bb[1])) / 2 - bb[1]), "Q", font=f, fill=BRASS_L)
    return im.resize((size, size), Image.LANCZOS)

touch = Image.new("RGB", (180, 180), NAVY)
touch.paste(mark(180), (0, 0), mark(180))
touch.save(f"{A}/apple-touch-icon.png")
mark(512).save(f"{A}/icon-512.png")
mark(48).save("dist/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
for f in sorted(os.listdir(A)):
    print(f, os.path.getsize(f"{A}/{f}"))
