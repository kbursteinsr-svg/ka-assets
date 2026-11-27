"""Editorial visuals for The Q Journal: photos, charts, diagrams, sources and related-article cards.

Photos are AI photo illustrations generated for the journal (never presented as real people or real results).
They are hosted on the Netlify project q-journal-media and served on this domain through the
/assets/editorial/* proxy rule in _redirects (see redirects() in build.py).

To add a photo: upload <name>.jpg, <name>.webp, <name>-640.jpg and <name>-640.webp to q-journal-media
under editorial/, then reference <name> here. Charts and diagrams are inline SVG built below.
"""
from html import escape as _e

MEDIA_ORIGIN = "https://q-journal-media.netlify.app"
ED = "/assets/editorial"
PHOTO_CREDIT = "Photo illustration: The Q Journal"

# ---------- photos ----------
PHOTOS = {
    "styling-products-counter": "Tins of pomade, matte clay and styling powder on a walnut barber counter with a comb",
    "pomade-hands-combed-back": "A man working pomade through thick, combed-back hair",
    "textured-crop-rooftop": "A man with a textured crop haircut laughing at an evening rooftop bar",
    "low-taper-barber-chair": "Back view of a clean low taper haircut in a barber chair",
    "choosing-a-haircut-mirror": "A man studying his reflection in a barbershop mirror while choosing a haircut",
    "high-skin-fade-profile": "Side profile of a high skin fade blending into a textured top",
    "hair-system-workbench": "A men's hair system on a mannequin head with a comb, scissors and adhesive",
    "receding-hairline-textured-crop": "A man in his forties with a short textured crop and a receding hairline",
    "beard-oil-and-balm": "A dropper bottle of beard oil and a tin of beard balm with a wooden comb",
    "grooming-gifts-wrapped": "Men's grooming gifts, beard oil, pomade, cologne and a trimmer, wrapped in navy paper",
    "grooming-shelf-morning": "A men's bathroom shelf with a shaving brush, styling clay, sunscreen and a comb",
    "beard-combing-closeup": "Close-up of a full beard being combed with a wooden comb",
    "clipper-guards-flat-lay": "Clippers with guard combs laid out on a navy leather surface",
    "humid-morning-clay": "A man styling his hair with matte clay in a bathroom mirror on a humid morning",
}

def photo(name, caption="", cls="ed", lazy=True, sizes="(max-width: 860px) 100vw, 760px"):
    alt = _e(PHOTOS[name])
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    cap = f'<figcaption>{_e(caption)} <span>{PHOTO_CREDIT}</span></figcaption>' if caption else f'<figcaption><span>{PHOTO_CREDIT}</span></figcaption>'
    return (f'<figure class="{cls}"><picture>'
            f'<source type="image/webp" srcset="{ED}/{name}-640.webp 640w, {ED}/{name}.webp 1024w" sizes="{sizes}">'
            f'<img src="{ED}/{name}.jpg" srcset="{ED}/{name}-640.jpg 640w, {ED}/{name}.jpg 1024w" sizes="{sizes}" '
            f'alt="{alt}" width="1024" height="683" {load}></picture>{cap}</figure>')

def thumb(name):
    return (f'<picture><source type="image/webp" srcset="{ED}/{name}-640.webp">'
            f'<img src="{ED}/{name}-640.jpg" alt="" width="640" height="427" loading="lazy" decoding="async"></picture>')

# ---------- charts & diagrams (inline SVG, brand palette) ----------
NAVY, BRASS, STONE, INK, MUTED = "#14202e", "#b08d57", "#f3f0ea", "#1b2735", "#6b7280"

def _chart(svg, title, note, source=None):
    src = (f' Source: <a href="{source[1]}" target="_blank" rel="noopener">{_e(source[0])}</a>.' if source else "")
    return (f'<figure class="chart"><p class="chart-t">{_e(title)}</p>{svg}'
            f'<figcaption>{_e(note)}{src}</figcaption></figure>')

PINTEREST_2026 = ("Pinterest Men's Trend Report 2026", "https://newsroom.pinterest.com/news/men-trend-report-2026/")
TREND_DATA = [("soft wolf cut men", 1154), ("beard fade men", 764), ("italian beard fade", 725),
              ("modern wolf cut men", 553), ("curly wolf cut men", 245), ("modern mullet men", 223),
              ("korean two block haircut men", 212)]

def _bars(rows, mx, fmt, hi=0):
    out = ""
    for i, (k, v) in enumerate(rows):
        out += (f'<div class="bar"><span class="bk">{_e(k)}</span><span class="bt"><i style="width:{100*v/mx:.1f}%;'
                f'background:{BRASS if i < hi else NAVY}"></i></span><b>{fmt(v)}</b></div>')
    return f'<div class="bars">{out}</div>'

def trend_chart():
    mx = max(v for _, v in TREND_DATA)
    return (f'<figure class="chart"><p class="chart-t">What men are searching for: haircut and beard styles, 2026</p>'
            f'<div role="img" aria-label="Year-over-year growth in Pinterest searches for men\'s haircut and beard styles">'
            f'{_bars(TREND_DATA, mx, lambda v: f"+{v:,}%", hi=3)}</div>'
            f'<figcaption>Year-over-year growth in searches on Pinterest. Source: <a href="{PINTEREST_2026[1]}" target="_blank" rel="noopener">{_e(PINTEREST_2026[0])}</a>.</figcaption></figure>')

def hold_shine_chart():
    w, h, pad = 480, 400, 56
    pts = [("Powder", .08, .36), ("Clay", .10, .80), ("Paste", .40, .56),
           ("Oil pomade", .88, .46), ("Water pomade", .80, .68), ("Gel", .92, .92)]
    def X(v): return pad + v * (w - pad - 30)
    def Y(v): return h - pad - v * (h - pad - 30)
    g = (f'<rect x="{pad}" y="30" width="{w-pad-30}" height="{h-pad-30}" fill="{STONE}" rx="6"/>'
         f'<line x1="{pad}" y1="{h-pad}" x2="{w-30}" y2="{h-pad}" stroke="{INK}" stroke-width="1.5"/>'
         f'<line x1="{pad}" y1="30" x2="{pad}" y2="{h-pad}" stroke="{INK}" stroke-width="1.5"/>'
         f'<text x="{(w+pad)/2}" y="{h-pad+40}" text-anchor="middle" font-size="17" fill="{MUTED}">Finish: matte → high shine</text>'
         f'<text x="22" y="{(h-pad+30)/2}" text-anchor="middle" font-size="17" fill="{MUTED}" transform="rotate(-90 22 {(h-pad+30)/2})">Hold: light → strong</text>')
    for name, x, y in pts:
        anchor = "end" if x > .6 else "start"
        dx = -14 if x > .6 else 14
        g += (f'<circle cx="{X(x):.0f}" cy="{Y(y):.0f}" r="11" fill="{BRASS}" stroke="{NAVY}" stroke-width="2"/>'
              f'<text x="{X(x)+dx:.0f}" y="{Y(y)+5:.0f}" text-anchor="{anchor}" font-size="19" font-weight="600" fill="{INK}">{name}</text>')
    svg = (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Map of men\'s styling products by hold and shine" '
           f'font-family="Hanken Grotesk, Arial, sans-serif">{g}</svg>')
    return _chart(svg, "Hold vs shine: where each styling product sits",
                  "An editorial guide to typical products in each category, not a lab measurement. Individual products vary.")

def guard_chart():
    rows = [("#3 guard · top", 9.5), ("#2 guard · sides", 6), ("#1 guard · edges & neckline", 3)]
    return (f'<figure class="chart"><p class="chart-t">The 3-2-1 rule in millimetres</p>'
            f'<div role="img" aria-label="Hair length left by clipper guards three, two and one">{_bars(rows, 10, lambda v: f"≈{v:g} mm", hi=1)}</div>'
            f'<figcaption>Approximate length each clipper guard leaves. Guard sizes vary slightly by clipper brand.</figcaption></figure>')

def fade_heights():
    w, h = 520, 330
    head = ("M120 300 C120 250 105 225 102 190 C98 140 120 70 200 60 C280 52 325 105 325 160 "
            "C325 185 318 200 322 215 C326 230 340 240 332 252 C325 260 315 258 312 272 C310 290 290 300 270 300 Z")
    g = f'<path d="{head}" fill="{STONE}" stroke="{NAVY}" stroke-width="3"/>'
    g += f'<ellipse cx="170" cy="200" rx="16" ry="26" fill="none" stroke="{NAVY}" stroke-width="2.5"/>'
    for y, lab, col in [(235, "Low", NAVY), (180, "Mid", BRASS), (130, "High", NAVY)]:
        g += (f'<line x1="80" y1="{y}" x2="350" y2="{y}" stroke="{col}" stroke-width="4" stroke-dasharray="10 7"/>'
              f'<text x="362" y="{y+8}" font-size="24" font-weight="600" fill="{INK}">{lab}</text>')
    svg = (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Where low, mid and high fades start on the head" '
           f'font-family="Hanken Grotesk, Arial, sans-serif">{g}</svg>')
    return _chart(svg, "Low, mid and high fades: where the shortest part stops",
                  "Low sits just above the ear and neckline, mid starts around the temple, high climbs toward the crown. Side view, face to the right.")

def face_shapes():
    shapes = [
        ("Oval", '<ellipse cx="50" cy="58" rx="30" ry="42"/>', "Almost any cut works"),
        ("Round", '<circle cx="50" cy="58" r="38"/>', "Height on top, tight sides"),
        ("Square", '<rect x="16" y="20" width="68" height="76" rx="10"/>', "Show off the jaw"),
        ("Long", '<rect x="24" y="10" width="52" height="94" rx="22"/>', "Keep height down"),
        ("Heart", '<path d="M14 24 Q50 8 86 24 Q84 70 50 102 Q16 70 14 24Z"/>', "Balance a narrow chin"),
        ("Diamond", '<path d="M50 10 L84 50 L50 104 L16 50Z"/>', "Soften the cheekbones"),
    ]
    cells = "".join(
        f'<div class="fs"><svg viewBox="0 0 100 112" aria-hidden="true" fill="{STONE}" stroke="{NAVY}" stroke-width="3">{s}</svg>'
        f'<b>{n}</b><span>{_e(t)}</span></div>' for n, s, t in shapes)
    return (f'<figure class="chart"><p class="chart-t">Face shape cheat sheet</p><div class="fsgrid">{cells}</div>'
            f'<figcaption>A starting point, not a rule. Hair type and how you style it matter just as much.</figcaption></figure>')

def oil_vs_balm_table():
    rows = [("What it is", "Skin care for the beard", "Styling and conditioning"),
            ("Made from", "Carrier and essential oils", "Oils thickened with butters and wax"),
            ("Main job", "Softens hair, calms the skin underneath", "Holds shape, tames flyaways"),
            ("Best for", "Stubble to full beards", "Medium to full beards"),
            ("When", "Daily, after a shower", "After oil, when you need shape"),
            ("In Florida heat", "A few drops is plenty", "Use a light hand")]
    body = "".join(f"<tr><th>{_e(a)}</th><td>{_e(b)}</td><td>{_e(c)}</td></tr>" for a, b, c in rows)
    return (f'<figure class="chart"><p class="chart-t">Beard oil vs beard balm at a glance</p>'
            f'<div class="tbl"><table><thead><tr><th></th><th>Beard oil</th><th>Beard balm</th></tr></thead><tbody>{body}</tbody></table></div></figure>')

# ---------- per-article plan ----------
# hero: photo name; inline: {after_section_number: [html, ...]} (0 = after the intro);
# sources: outbound references; related: internal articles for the cards and the "read next" callout.
AAD_MPHL = ("American Academy of Dermatology: Male pattern hair loss", "https://www.aad.org/public/diseases/hair-loss/treatment/male-pattern-hair-loss-treatment")
AAD_HAIRLOSS = ("American Academy of Dermatology: How to treat hair loss", "https://www.aad.org/public/diseases/hair-loss/treatment")
HARVARD_HL = ("Harvard Health: Treating hair loss in men, what works?", "https://www.health.harvard.edu/mens-health/treating-hair-loss-in-men-what-works")
AAD_RAZOR = ("American Academy of Dermatology: Razor bump remedies", "https://www.aad.org/public/everyday-care/skin-care-basics/hair/razor-bump-remedies")
AAD_RAZOR_PREV = ("American Academy of Dermatology: 6 razor bump prevention tips", "https://www.aad.org/public/everyday-care/skin-care-basics/hair/razor-bump-prevention")
AAD_SHAVE = ("American Academy of Dermatology: How to shave", "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave")

PLAN = {
    "best-pomade-for-men.html": dict(hero="pomade-hands-combed-back",
        inline={1: ["CHART:hold_shine"], 3: ["PHOTO:humid-morning-clay|Matte products with real grip outlast high shine on humid days."]},
        related=["pomade-vs-clay-vs-gel.html", "haircuts-for-receding-hairline.html", "what-haircut-should-i-get.html"]),
    "pomade-vs-clay-vs-gel.html": dict(hero="styling-products-counter",
        inline={0: ["CHART:hold_shine"], 2: ["PHOTO:humid-morning-clay|Clay and powder hold up best when the air is wet."]},
        related=["best-pomade-for-men.html", "fade-vs-taper-which-is-better.html", "3-2-1-rule-mens-haircuts.html"]),
    "what-haircut-do-girls-like.html": dict(hero="textured-crop-rooftop",
        inline={2: ["CHART:trend"]}, sources=[PINTEREST_2026],
        related=["what-haircut-should-i-get.html", "fade-vs-taper-which-is-better.html", "best-pomade-for-men.html"]),
    "3-2-1-rule-mens-haircuts.html": dict(hero="clipper-guards-flat-lay",
        inline={1: ["CHART:guards"], 3: ["PHOTO:low-taper-barber-chair|Length steps down from the top to the neckline."]},
        related=["fade-vs-taper-which-is-better.html", "haircuts-for-receding-hairline.html", "what-haircut-should-i-get.html"]),
    "what-haircut-should-i-get.html": dict(hero="choosing-a-haircut-mirror",
        inline={0: ["CHART:faces"], 6: ["CHART:trend"]}, sources=[PINTEREST_2026],
        related=["what-haircut-do-girls-like.html", "fade-vs-taper-which-is-better.html", "3-2-1-rule-mens-haircuts.html"]),
    "fade-vs-taper-which-is-better.html": dict(hero="high-skin-fade-profile",
        inline={1: ["PHOTO:low-taper-barber-chair|A low taper: short at the edges, length kept everywhere else."], 3: ["CHART:fades"], 4: ["CHART:trend"]},
        sources=[PINTEREST_2026],
        related=["3-2-1-rule-mens-haircuts.html", "what-haircut-should-i-get.html", "pomade-vs-clay-vs-gel.html"]),
    "toupee-hair-system-guide.html": dict(hero="hair-system-workbench", sources=[AAD_HAIRLOSS, AAD_MPHL],
        related=["haircuts-for-receding-hairline.html", "best-pomade-for-men.html", "what-haircut-should-i-get.html"]),
    "haircuts-for-receding-hairline.html": dict(hero="receding-hairline-textured-crop",
        inline={2: ["PHOTO:clipper-guards-flat-lay|Short sides make a thinning front look intentional."]},
        sources=[AAD_MPHL, HARVARD_HL],
        related=["toupee-hair-system-guide.html", "3-2-1-rule-mens-haircuts.html", "pomade-vs-clay-vs-gel.html"]),
    "beard-oil-vs-beard-balm.html": dict(hero="beard-oil-and-balm",
        inline={2: ["CHART:oil_balm"], 3: ["PHOTO:beard-combing-closeup|Oil first, then balm, then a comb to set the shape."]},
        sources=[AAD_RAZOR],
        related=["mens-grooming-gift-guide.html", "grooming-guide.html", "fade-vs-taper-which-is-better.html"]),
    "mens-grooming-gift-guide.html": dict(hero="grooming-gifts-wrapped",
        inline={2: ["PHOTO:styling-products-counter|Pomade for shine, clay for texture, powder for lift."]},
        related=["beard-oil-vs-beard-balm.html", "best-pomade-for-men.html", "pomade-vs-clay-vs-gel.html"]),
    "grooming-guide.html": dict(hero="grooming-shelf-morning", sources=[AAD_RAZOR_PREV, AAD_SHAVE],
        related=["beard-oil-vs-beard-balm.html", "pomade-vs-clay-vs-gel.html", "fade-vs-taper-which-is-better.html"]),
}
DEFAULT_HERO = "grooming-shelf-morning"

CHARTS = {"hold_shine": hold_shine_chart, "trend": trend_chart, "guards": guard_chart,
          "fades": fade_heights, "faces": face_shapes, "oil_balm": oil_vs_balm_table}

def render_inline(token):
    kind, _, val = token.partition(":")
    if kind == "CHART":
        return CHARTS[val]()
    name, _, cap = val.partition("|")
    return photo(name, cap)

def hero_name(path):
    return PLAN.get(path, {}).get("hero", DEFAULT_HERO)

def hero_banner(path):
    return f'<div class="wrap hero-ph">{photo(hero_name(path), cls="ed ed-hero", lazy=False, sizes="(max-width: 1200px) 100vw, 1160px")}</div>'

def sources_block(path):
    src = PLAN.get(path, {}).get("sources", [])
    if not src:
        return ""
    items = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{_e(t)}</a></li>' for t, u in src)
    return f'<h2>Sources and further reading</h2><ul class="srcs">{items}</ul>'

CSS = r"""
.hero-ph{margin-top:-8px}.ed{margin:28px 0}.ed img{width:100%;height:auto;border-radius:14px;display:block;box-shadow:0 24px 48px -28px rgba(20,32,46,.55)}
.ed-hero{margin:0 0 8px}.ed-hero img{aspect-ratio:3/2;object-fit:cover;max-height:620px}
.ed figcaption,.chart figcaption{font-size:.82rem;color:var(--muted);margin-top:10px;line-height:1.5}.ed figcaption span{display:block;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;opacity:.75}
.chart{margin:36px 0;padding:22px 22px 16px;background:#fff;border:1px solid var(--line);border-radius:14px}
.chart svg{width:100%;height:auto;display:block;margin-top:10px}.chart-t{font:400 1.15rem var(--display);color:var(--navy);margin:0}
.chart figcaption a{color:var(--brass)}
.fsgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:14px}@media(max-width:560px){.fsgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
.fs{display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;padding:10px;border-radius:10px;background:var(--stone,#f3f0ea)}.fs svg{width:64px;height:72px;margin:0}.fs b{color:var(--navy);font-weight:600}.fs span{font-size:.82rem;color:var(--muted)}
.tbl{overflow-x:auto;margin-top:14px}.tbl table{width:100%;border-collapse:collapse;font-size:.92rem}.tbl th,.tbl td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl thead th{color:var(--navy);font-weight:600;border-bottom:2px solid var(--brass)}.tbl tbody th{color:var(--ink);font-weight:600;white-space:nowrap}.tbl td{color:var(--muted)}
.readnext{display:flex;gap:16px;align-items:center;margin:32px 0;padding:14px;border:1px solid var(--line);border-left:4px solid var(--brass);border-radius:12px;text-decoration:none;background:#fff}
.readnext picture{flex:0 0 120px}.readnext img{width:120px;height:80px;object-fit:cover;border-radius:8px;display:block}.readnext small{display:block;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--brass)}.readnext b{color:var(--navy);font-weight:600;line-height:1.35}
.rcards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:20px}@media(max-width:760px){.rcards{grid-template-columns:1fr}}
.rcard{text-decoration:none;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;display:flex;flex-direction:column}.rcard img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block}
.rcard span{padding:12px 14px 16px;color:var(--navy);font-weight:600;line-height:1.35}.rcard:hover{border-color:var(--brass)}
.srcs{color:var(--muted);padding-left:20px}.srcs a{color:var(--navy)}
.post .pthumb{margin:-22px -22px 16px;display:block;overflow:hidden;border-radius:14px 14px 0 0}.post .pthumb img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;transition:transform .5s}.post:hover .pthumb img{transform:scale(1.03)}
.trendsec .chart{max-width:780px;margin-inline:auto}
.bars{display:grid;gap:10px;margin-top:16px}.bar{display:grid;grid-template-columns:minmax(0,13em) 1fr auto;gap:12px;align-items:center;font-size:.92rem;color:var(--ink)}
.bar .bt{height:22px;background:var(--stone,#f3f0ea);border-radius:5px;overflow:hidden}.bar i{display:block;height:100%;border-radius:5px}.bar b{font-weight:600;min-width:4.5em;text-align:right}
@media(max-width:560px){.bar{grid-template-columns:1fr auto;row-gap:4px}.bar .bk{grid-column:1/-1}.bar .bt{grid-column:1}}
"""
