#!/usr/bin/env python3
"""Builds The Q Journal, the men's grooming journal at theqsalonsrq.com.
Edit SITE / ARTICLES / products below, then run: python3 build.py
Outputs full HTML pages in ./dist (for Netlify).

Editorial rules: articles carry "The Q Journal" byline. No appointment, booking or
gift-card links, and no copy inviting readers to visit for a service.
Former service and area pages are retired with 302 redirects (see RETIRED), so they
can be brought back by restoring the previous build.py from git."""
import datetime, json, os, re

SITE = {
    "name": "The Q Journal",
    "tagline": "A men's grooming journal",
    "email": "info@theqsalonsrq.com",
    "site": "https://www.theqsalonsrq.com",
}
B = SITE
IMG_HERO = "mens-haircut-sarasota-silver-swept-back"
IMG_SHARE = "/assets/the-q-journal-mens-grooming-share.jpg"
TODAY = datetime.date.today().isoformat()
BYLINE = "The Q Journal"

def pic(base, alt, w, h, cls="", lazy=True, extra=""):
    """<picture> with WebP + JPEG fallback (files built by make_assets.py)."""
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source srcset="/assets/{base}.webp" type="image/webp">'
            f'<img{c} src="/assets/{base}.jpg" alt="{alt}" width="{w}" height="{h}" {load}{extra}></picture>')

def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%b ") + str(d.day) + d.strftime(", %Y")

# ---- Product illustrations (generic category art, no brand names) ----
SVG_TIN = """<svg viewBox="0 0 200 160" aria-hidden="true"><defs><linearGradient id="tA" x1="0" x2="1"><stop offset="0" stop-color="#8f7146"/><stop offset=".45" stop-color="#d9bd8a"/><stop offset="1" stop-color="#8a6b40"/></linearGradient><linearGradient id="tB" x1="0" x2="1"><stop offset="0" stop-color="#1b2735"/><stop offset=".5" stop-color="#2d3e52"/><stop offset="1" stop-color="#16202c"/></linearGradient></defs>
<ellipse cx="100" cy="138" rx="72" ry="10" fill="#000" opacity=".18"/><rect x="34" y="76" width="132" height="58" rx="10" fill="url(#tB)"/><ellipse cx="100" cy="76" rx="66" ry="14" fill="#2d3e52"/>
<rect x="30" y="52" width="140" height="28" rx="8" fill="url(#tA)"/><ellipse cx="100" cy="52" rx="70" ry="14" fill="#e7d2a6"/><ellipse cx="100" cy="52" rx="40" ry="7" fill="none" stroke="#8f7146" stroke-width="1.5"/><text x="100" y="57" text-anchor="middle" font-family="Marcellus,serif" font-size="14" fill="#5b4526">Q</text></svg>"""
SVG_DROP = """<svg viewBox="0 0 200 160" aria-hidden="true"><defs><linearGradient id="dA" x1="0" x2="1"><stop offset="0" stop-color="#5a3a1c"/><stop offset=".4" stop-color="#a8692d"/><stop offset="1" stop-color="#4a2f16"/></linearGradient></defs>
<ellipse cx="100" cy="146" rx="40" ry="7" fill="#000" opacity=".18"/><rect x="72" y="62" width="56" height="82" rx="12" fill="url(#dA)"/><rect x="78" y="90" width="44" height="34" rx="3" fill="#efe8dc"/><text x="100" y="111" text-anchor="middle" font-family="Marcellus,serif" font-size="10" fill="#14202e" letter-spacing="1">BEARD</text>
<rect x="86" y="44" width="28" height="20" rx="3" fill="#c9a96e"/><path d="M90 44 Q90 14 100 12 Q110 14 110 44Z" fill="#1b2735"/><rect x="80" y="70" width="6" height="56" rx="3" fill="#fff" opacity=".18"/></svg>"""
SVG_PUMP = """<svg viewBox="0 0 200 160" aria-hidden="true"><defs><linearGradient id="pA" x1="0" x2="1"><stop offset="0" stop-color="#cfc7ba"/><stop offset=".45" stop-color="#f6f2ea"/><stop offset="1" stop-color="#bdb3a4"/></linearGradient></defs>
<ellipse cx="100" cy="148" rx="44" ry="7" fill="#000" opacity=".18"/><rect x="66" y="56" width="68" height="90" rx="14" fill="url(#pA)"/><rect x="74" y="84" width="52" height="40" rx="3" fill="#14202e"/><text x="100" y="101" text-anchor="middle" font-family="Marcellus,serif" font-size="9" fill="#c9a96e" letter-spacing="1">DAILY</text><text x="100" y="114" text-anchor="middle" font-family="Marcellus,serif" font-size="9" fill="#efe8dc" letter-spacing="1">WASH</text>
<rect x="90" y="40" width="20" height="18" rx="2" fill="#14202e"/><rect x="96" y="22" width="8" height="20" fill="#14202e"/><rect x="96" y="20" width="40" height="8" rx="3" fill="#14202e"/></svg>"""
SVG_GIFT = """<svg viewBox="0 0 200 160" aria-hidden="true"><defs><linearGradient id="gA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22324a"/><stop offset="1" stop-color="#0f1823"/></linearGradient></defs>
<ellipse cx="100" cy="140" rx="76" ry="8" fill="#000" opacity=".18"/><g transform="rotate(-6 100 84)"><rect x="28" y="36" width="144" height="92" rx="9" fill="url(#gA)" stroke="#c9a96e"/><circle cx="56" cy="64" r="14" fill="none" stroke="#c9a96e"/><text x="56" y="70" text-anchor="middle" font-family="Marcellus,serif" font-size="16" fill="#c9a96e">Q</text><text x="44" y="112" font-family="Marcellus,serif" font-size="15" fill="#efe8dc">Gift Card</text><text x="160" y="112" text-anchor="end" font-family="DM Mono,monospace" font-size="10" fill="#c9a96e">$50+</text></g></svg>"""

SVG_BOTTLE = """<svg viewBox="0 0 200 160" aria-hidden="true"><ellipse cx="100" cy="146" rx="46" ry="7" fill="#000" opacity=".18"/><rect x="58" y="58" width="84" height="86" rx="16" fill="#3a4350"/><rect x="58" y="58" width="84" height="86" rx="16" fill="none" stroke="#c9a96e" stroke-width="2"/><path d="M70 70 L130 130" stroke="#5a6472" stroke-width="3"/><path d="M82 66 L138 122" stroke="#5a6472" stroke-width="3"/><rect x="82" y="34" width="36" height="26" rx="4" fill="#14202e"/><rect x="74" y="98" width="52" height="22" rx="2" fill="#14202e"/><text x="100" y="113" text-anchor="middle" font-family="Marcellus,serif" font-size="9" fill="#c9a96e" letter-spacing="1">PARFUM</text></svg>"""
SVG_TRIM = """<svg viewBox="0 0 200 160" aria-hidden="true"><ellipse cx="100" cy="148" rx="30" ry="6" fill="#000" opacity=".18"/><rect x="80" y="30" width="40" height="116" rx="18" fill="#1b2735"/><rect x="78" y="18" width="44" height="18" rx="3" fill="#5a6472"/><g stroke="#c9a96e" stroke-width="1.5">""" + "".join(f'<line x1="{80+i*4}" y1="12" x2="{80+i*4}" y2="20"/>' for i in range(11)) + """</g><circle cx="100" cy="74" r="6" fill="none" stroke="#c9a96e" stroke-width="2"/><circle cx="100" cy="112" r="11" fill="none" stroke="#c9a96e" stroke-width="2"/></svg>"""


# Product categories shown as cards (link into the picks page).
PRODUCTS = [
    ("Styling", "Pomades & clays", "Hold from natural to sharp, from matte clay to high-shine pomade.", SVG_TIN, "styling"),
    ("Beard Care", "Oils & kits", "Soften, tame the itch and keep it groomed day to day.", SVG_DROP, "beard-care"),
    ("Hair & Scalp", "Shampoo & conditioner", "Daily scalp care for men's hair, sulfate-free options included.", SVG_PUMP, "hair-scalp"),
]

# Footer links
NAV = [("blog.html", "Journal"), ("grooming-guide.html", "Grooming Guide"), ("mens-grooming-gift-guide.html", "Gift Guide"),
       ("shop.html", "Product Picks"), ("about.html", "About")]

# Editorial product picks, loaded from qsalon/shop/products.json.
_PJ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shop", "products.json")
AFFILIATE = json.load(open(_PJ)) if os.path.exists(_PJ) else []
AFF_NOTES = {   # short card copy, label facts only (no prices, ratings or health claims)
    1: "A matte, strong-hold clay for textured cuts and crops that need to keep their shape.",
    2: "The classic barbershop pomade: medium hold and high shine for side parts, slick-backs and executive cuts.",
    3: "A small-batch American pomade with 18.21's signature Sweet Tobacco scent, in a glass jar.",
    4: "Everything a full beard needs in one box: wash, conditioner, oil, balm and a wooden comb.",
    5: "A lightweight, non-greasy oil made with desert botanicals. Softens the beard and helps calm itch.",
    6: "A shampoo and conditioner duo with 5% minoxidil and biotin on the label, plus ginseng and ginger.",
    7: "A sulfate-free set with salicylic acid, biotin and yeast extract, built around scalp health.",
    8: "An eau de parfum with bright citrus over warm vanilla, in a sculpted gunmetal bottle.",
    9: "A waterproof body trimmer with SkinSafe blades, USB-C charging and four guards for upkeep between haircuts.",
    10: "A daily beard oil made from a blend of seven-plus natural oils, mineral-oil free, in a 2 oz dropper bottle.",
    11: "A heavy-duty balm with organic shea butter and beeswax for extra control on fuller beards.",
    12: "A professional styling gel with long-lasting hold. Alcohol-free and no flaking, even in Florida humidity.",
    13: "A light texturizing powder for volume and a matte, natural look. Build the hold a pinch at a time.",
    14: "A three-step scalp and hair kit for colored, dry or damaged hair: shampoo, conditioner and a scalp treatment.",
    15: "Keratin hair fibers that fill in fine or thin-looking areas so hair looks fuller instantly. Shade shown: Black.",
    16: "A daily facial moisturizer with broad spectrum SPF 30, ceramides, niacinamide and hyaluronic acid. Oil free.",
    17: "A sugar-free peppermint gum with natural caffeine and L-theanine on the label, for long days.",
}
AFF_CATS = [("Styling", "styling"), ("Beard Care", "beard-care"), ("Hair & Scalp", "hair-scalp"), ("Skin Care", "skin-care"), ("Fragrance", "fragrance"), ("Tools", "tools"), ("Daily Extras", "extras")]
AMZ_DISCLOSE = "As an Amazon Associate, The Q Salon earns from qualifying purchases."   # existing disclosure, keep verbatim

# Journal pages, linked from the footer of every page.
SEO_LINKS = [
    ("blog.html", "The Q Journal"), ("best-pomade-for-men.html", "Best Pomade for Men"), ("what-haircut-should-i-get.html", "What Haircut Should I Get?"),
    ("what-haircut-do-girls-like.html", "Most Attractive Haircuts for Men"), ("fade-vs-taper-which-is-better.html", "Fade vs Taper"),
    ("3-2-1-rule-mens-haircuts.html", "The 3-2-1 Haircut Rule"), ("haircuts-for-receding-hairline.html", "Haircuts for a Receding Hairline"),
    ("toupee-hair-system-guide.html", "Hair Systems & Toupees"), ("mens-grooming-gift-guide.html", "Grooming Gift Guide 2026"),
    ("pomade-vs-clay-vs-gel.html", "Pomade vs Clay vs Gel"), ("beard-oil-vs-beard-balm.html", "Beard Oil vs Beard Balm"),
    ("grooming-guide.html", "The Grooming Guide"), ("shop.html", "Product Picks"), ("about.html", "About the Journal"),
]

# Former salon service and area pages -> closest journal article (301 since Nov 25 2026; the journal direction is settled).
RETIRED = {
    "mens-hair-salon-sarasota": "/what-haircut-should-i-get", "barber-sarasota": "/what-haircut-should-i-get",
    "mens-haircut-sarasota": "/what-haircut-should-i-get", "executive-haircut-sarasota": "/what-haircut-do-girls-like",
    "skin-fade-sarasota": "/fade-vs-taper-which-is-better", "mens-hair-color-sarasota": "/grooming-guide",
    "mens-facial-sarasota": "/grooming-guide", "kids-haircut-sarasota": "/what-haircut-should-i-get",
    "mens-grooming-sarasota": "/grooming-guide", "mens-haircut-lido-key": "/what-haircut-should-i-get",
    "mens-haircut-lakewood-ranch": "/what-haircut-should-i-get", "mens-haircut-siesta-key": "/what-haircut-should-i-get",
    "mens-haircut-longboat-key": "/what-haircut-should-i-get",
}

def url(path):
    return B["site"] + ("/" if path == "index.html" else "/" + path.replace(".html", ""))

ORG_ID = B["site"] + "/#journal"

def org_node():
    """The publisher. Same @id on every page."""
    return {"@type": "Organization", "@id": ORG_ID, "name": B["name"], "url": B["site"] + "/",
            "description": "A men's grooming journal: practical advice on haircuts, beards, skin and styling, plus editorial product picks.",
            "logo": {"@type": "ImageObject", "url": B["site"] + "/assets/icon-512.png", "width": 512, "height": 512},
            "email": B["email"]}

def schema(path, title, desc, crumb):
    """One @graph per page: publisher + website + this page (+ breadcrumb)."""
    page_url = url(path)
    graph = [org_node(),
             {"@type": "WebSite", "@id": B["site"] + "/#website", "url": B["site"] + "/", "name": B["name"],
              "description": B["tagline"], "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"}]
    kind = {"about.html": "AboutPage", "blog.html": "CollectionPage", "index.html": "CollectionPage"}.get(path, "WebPage")
    wp = {"@type": kind, "@id": page_url + "#webpage", "url": page_url,
          "name": title, "description": desc, "isPartOf": {"@id": B["site"] + "/#website"}, "publisher": {"@id": ORG_ID},
          "inLanguage": "en-US", "dateModified": TODAY,
          "primaryImageOfPage": {"@type": "ImageObject", "url": B["site"] + IMG_SHARE, "width": 1200, "height": 630}}
    if path != "index.html":
        graph.append({"@type": "BreadcrumbList", "@id": page_url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": B["site"] + "/"},
            {"@type": "ListItem", "position": 2, "name": crumb, "item": page_url}]})
        wp["breadcrumb"] = {"@id": page_url + "#breadcrumb"}
    graph.append(wp)
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)

CSS = r"""
/* Layout: alternating stone / navy bands, Roman-capital display type, brass hairlines. Single committed light look. */
:root{--stone:#e8e3db;--stone-2:#f3f0ea;--navy:#14202e;--navy-2:#1c2a3b;--ink:#1a1f26;--muted:#6a6560;--muted-d:#a9b3bf;--brass:#b08d57;--brass-l:#d6b984;--line:#d4cdc2;--line-d:#2b3a4d;
--display:"Marcellus","Trajan Pro",Optima,Georgia,serif;--body:"Hanken Grotesk",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"DM Mono",ui-monospace,Menlo,monospace;color-scheme:light}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--stone-2);color:var(--ink);font:16px/1.65 var(--body)}
a{color:inherit}img{max-width:100%;display:block}.wrap{max-width:1160px;margin:0 auto;padding-inline:20px}
h1,h2,h3{font-family:var(--display);font-weight:400;text-wrap:balance;margin:0}
h1{font-size:clamp(2.7rem,6.4vw,5.2rem);line-height:1.02;letter-spacing:-.01em}
h2{font-size:clamp(2rem,4.2vw,3.1rem);line-height:1.08}h3{font-size:1.3rem;line-height:1.25}
p{margin:0}.muted{color:var(--muted)}
.eyebrow{display:flex;align-items:center;gap:12px;font:500 .74rem/1 var(--mono);letter-spacing:.2em;text-transform:uppercase;color:var(--brass);margin-bottom:18px}
.eyebrow::before{content:"";width:28px;height:1px;background:currentColor}
.btn{display:inline-flex;align-items:center;gap:10px;background:var(--navy);color:#fff;text-decoration:none;font-weight:600;font-size:.95rem;padding:15px 28px;border-radius:999px;letter-spacing:.02em;transition:transform .25s,background .25s,box-shadow .25s}
.btn:hover{background:var(--navy-2);transform:translateY(-2px);box-shadow:0 10px 24px -12px rgba(20,32,46,.6)}
.btn .arr{transition:transform .25s}.btn:hover .arr{transform:translateX(4px)}
.btn-brass{background:var(--brass);color:var(--navy)}.btn-brass:hover{background:var(--brass-l)}
.btn-line{background:transparent;color:var(--navy);box-shadow:inset 0 0 0 1px var(--navy)}.btn-line:hover{background:var(--navy);color:#fff}
.on-dark .btn-line{color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.5)}.on-dark .btn-line:hover{background:#fff;color:var(--navy)}
.btn-sm{padding:10px 18px;font-size:.88rem}
.btn,.brand-t{white-space:nowrap}.brand{min-width:0}
a:focus-visible,.btn:focus-visible{outline:2px solid var(--brass);outline-offset:3px}
.link{color:var(--brass);text-underline-offset:4px;font-weight:500}
/* header */
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:rgba(243,240,234,.88);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.top-in{display:flex;align-items:center;gap:22px;padding-block:12px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;margin-right:auto}
.mono{display:grid;place-items:center;width:40px;height:40px;border-radius:50%;background:var(--navy);color:var(--brass-l);font:400 1.35rem/1 var(--display)}
.brand-t{font:400 1.05rem/1.05 var(--display);letter-spacing:.06em;text-transform:uppercase}.brand-t small{display:block;font:500 .62rem var(--mono);letter-spacing:.24em;color:var(--brass);margin-top:3px}
.nav{display:flex;align-items:center;gap:4px;font-size:.92rem}
.nav-a{display:inline-flex;align-items:center;gap:6px;padding:9px 12px;border-radius:999px;border:0;background:none;font:inherit;color:var(--muted);text-decoration:none;cursor:pointer;transition:color .2s,background .2s}
.nav-a:hover,.nav-a[aria-current]{color:var(--ink)}
.nav-a:focus-visible,.burger:focus-visible,.mnav summary:focus-visible{outline:2px solid var(--brass);outline-offset:2px}
.burger{display:none;flex:0 0 auto;width:44px;height:44px;border:1px solid var(--line);border-radius:50%;background:#fff;cursor:pointer;flex-direction:column;justify-content:center;align-items:center;gap:4px;padding:0}
.burger span{display:block;width:18px;height:1.5px;background:var(--navy);transition:transform .2s,opacity .2s}
.burger[aria-expanded="true"] span:nth-child(1){transform:translateY(5.5px) rotate(45deg)}.burger[aria-expanded="true"] span:nth-child(2){opacity:0}.burger[aria-expanded="true"] span:nth-child(3){transform:translateY(-5.5px) rotate(-45deg)}
.mnav{border-top:1px solid var(--line);background:var(--stone-2);max-height:calc(100dvh - 68px);overflow-y:auto;overscroll-behavior:contain;padding-bottom:calc(20px + env(safe-area-inset-bottom,0px))}
.mnav .m-top,.mnav summary{display:flex;justify-content:space-between;align-items:center;padding:16px 2px;border-bottom:1px solid var(--line);font:400 1.25rem var(--display);color:var(--navy);text-decoration:none;cursor:pointer;list-style:none}
body.menu-open{overflow:hidden}
@media(max-width:900px){.nav{display:none}.burger{display:inline-flex}.top-in{gap:10px}}
@media(max-width:420px){.brand-t{font-size:.92rem}.brand-t small{font-size:.56rem;letter-spacing:.18em}.mono{width:36px;height:36px;font-size:1.2rem}.brand{gap:9px}}
@media(max-width:350px){.top-in{gap:8px}.brand-t small{display:none}.brand-t{font-size:.84rem;letter-spacing:.03em}.burger{width:40px;height:40px}}
@media(min-width:901px){.mnav{display:none!important}}
/* hero copy */
.lede{font-size:1.15rem;color:var(--muted);max-width:46ch;margin-top:24px}
.acts{display:flex;flex-wrap:wrap;gap:12px;margin-top:32px}
@keyframes rise{from{transform:translateY(105%)}to{transform:none}}
/* hero v2: editorial split */
.hero2{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr);min-height:min(calc(100vh - 68px),720px);border-bottom:1px solid var(--line)}
.h2-media{position:relative;margin:0;display:flex;align-items:center;justify-content:center;padding:clamp(24px,3.2vw,48px);background:var(--stone)}
.h2-frame{position:relative;width:100%;max-width:min(520px,calc((min(100vh - 68px,720px) - 2*clamp(24px,3.2vw,48px))*0.811));aspect-ratio:1179/1454;overflow:hidden;border-radius:4px;background:#c2c2c9;box-shadow:0 40px 80px -40px rgba(20,32,46,.55)}
.h2-frame img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 30%;animation:h2zoom 1.6s cubic-bezier(.2,.7,.2,1) both}
.h2-frame::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(20,32,46,.32) 0,rgba(20,32,46,0) 26%);pointer-events:none}
.h2-frame::before{content:"";position:absolute;inset:14px;border:1px solid rgba(255,255,255,.55);z-index:2;pointer-events:none}
.h2-media::before{content:"";position:absolute;width:min(46%,240px);aspect-ratio:1;right:clamp(10px,2vw,28px);top:clamp(14px,2.4vw,34px);border:1px solid var(--brass);border-radius:50%;opacity:.55}
.h2-tag{position:absolute;z-index:3;display:flex;align-items:center;gap:10px;font:500 .68rem/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--navy);background:rgba(243,240,234,.92);backdrop-filter:blur(6px);padding:9px 12px;border-radius:999px;box-shadow:0 10px 24px -14px rgba(20,32,46,.55);animation:tagin .8s cubic-bezier(.2,.7,.2,1) both}
.h2-tag i{width:7px;height:7px;border-radius:50%;background:var(--brass);box-shadow:0 0 0 4px rgba(176,141,87,.25)}
.h2-tag.t1{top:9%;right:6%;animation-delay:.55s}.h2-tag.t2{bottom:17%;left:6%;animation-delay:.75s}
.h2-issue{position:absolute;z-index:3;left:30px;bottom:30px;font:500 .64rem var(--mono);letter-spacing:.3em;text-transform:uppercase;color:#fff;opacity:.9}
.h2-copy{display:flex;align-items:center;background:var(--stone-2)}
.h2-inner{padding:clamp(40px,6vw,88px) clamp(22px,5vw,72px);max-width:620px}
.hero2 h1 .l{display:block;overflow:hidden}.hero2 h1 .l>span{display:inline-block;animation:rise .9s cubic-bezier(.2,.7,.2,1) both}
.hero2 h1 .l:nth-child(2)>span{animation-delay:.08s}.hero2 h1 .l:nth-child(3)>span{animation-delay:.16s}
.hero2 h1 em{font-style:normal;color:var(--brass)}
.h1-eyebrow{display:flex}
.hero2 .stats{margin-top:28px;padding-top:22px;gap:20px 32px;flex-wrap:nowrap}
.hero2 .stats b{font-size:1.45rem;margin-bottom:6px}.hero2 .stats span{font-size:.62rem;letter-spacing:.1em;white-space:nowrap}
.hero2 h1{font-size:clamp(2.6rem,4.9vw,4.4rem)}
.hero2 .lede{margin-top:20px}.hero2 .acts{margin-top:26px}
@media(max-width:1180px){.hero2 .stats{flex-wrap:wrap}}
@keyframes h2zoom{from{transform:scale(1.08)}to{transform:none}}
@keyframes tagin{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@media(max-width:860px){.hero2{grid-template-columns:1fr;min-height:0}.h2-frame{max-width:440px}.h2-tag{font-size:.6rem;padding:8px 10px}.h2-tag.t1{top:9%;right:5%}.h2-tag.t2{bottom:10%;left:5%}.h2-issue{display:none}.h2-media::before{display:none}}
@keyframes fade{from{opacity:.2;transform:scale(1.03)}to{opacity:1;transform:none}}
/* marquee */
.ticker{background:var(--navy);color:var(--stone);overflow:hidden;border-block:1px solid var(--line-d)}
.track{display:flex;width:max-content;animation:scroll 38s linear infinite}
.track span{font:400 1.05rem var(--display);letter-spacing:.14em;text-transform:uppercase;padding:18px 28px;white-space:nowrap;display:flex;align-items:center;gap:56px}
.track span::after{content:"✦";color:var(--brass);font-size:.8rem}
@keyframes scroll{to{transform:translateX(-50%)}}
/* sections */
.sec{padding-block:clamp(64px,9vw,112px)}
.sec-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:20px;margin-bottom:44px}
.sec-head p{max-width:46ch;color:var(--muted)}
.on-dark{background:var(--navy);color:#f1ede6}.on-dark .muted,.on-dark .sec-head p{color:var(--muted-d)}.on-dark .eyebrow{color:var(--brass-l)}
.stone{background:var(--stone)}
/* shop */
.products{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
@media(max-width:760px){.products{grid-template-columns:1fr}}
.prod{background:var(--navy-2);border:1px solid var(--line-d);border-radius:10px;overflow:hidden;display:flex;flex-direction:column;transition:transform .35s cubic-bezier(.2,.7,.2,1),border-color .35s,box-shadow .35s}
.prod:hover{transform:translateY(-6px);border-color:var(--brass);box-shadow:0 24px 50px -28px rgba(0,0,0,.8)}
.prod .art{background:radial-gradient(circle at 50% 60%,#2c3d52 0,#1c2a3b 70%);aspect-ratio:5/4;display:grid;place-items:center;padding:18px}
.prod .art.photo{background:#fff;padding:0;display:block;position:relative;aspect-ratio:5/4;overflow:hidden}.prod .art.photo picture{position:absolute;inset:0;display:block}.prod .art.photo img{position:absolute;inset:0;width:100%;height:100%;max-width:none;object-fit:contain;object-position:center;padding:18px;box-sizing:border-box;transition:transform .5s cubic-bezier(.2,.7,.2,1)}.prod:hover .art.photo img{transform:scale(1.05)}
.prod .art svg{width:100%;max-width:220px;height:auto;transition:transform .5s cubic-bezier(.2,.7,.2,1)}.prod:hover .art svg{transform:scale(1.06) rotate(-2deg)}
.prod .meta{padding:22px;display:flex;flex-direction:column;gap:8px;flex:1}
.prod .k{font:500 .68rem var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--brass-l)}
.prod p{color:var(--muted-d);font-size:.93rem;flex:1}.prod .go{margin-top:10px;font-weight:600;color:#fff;text-decoration:none;display:inline-flex;gap:8px;align-items:center}
.prod .go .arr{transition:transform .25s}.prod:hover .go .arr{transform:translateX(4px)}
.shop-note{margin-top:28px;color:var(--muted-d);font-size:.88rem}
/* about */
@media(max-width:820px){.about{grid-template-columns:1fr}}
/* inner pages */
.prose{max-width:66ch}.prose p{color:var(--muted);margin-top:16px}.prose h2{margin-top:48px;font-size:clamp(1.6rem,3vw,2.2rem)}.prose ul{color:var(--muted);padding-left:20px}.prose li{margin-top:6px}.prose strong{color:var(--ink);font-weight:600}
.split{display:grid;grid-template-columns:.9fr 1.3fr;gap:56px}.split>*{min-width:0}@media(max-width:860px){.split{grid-template-columns:1fr;gap:32px}}
.sticky{position:sticky;top:100px;align-self:start}@media(max-width:860px){.sticky{position:static}}
.side{background:#fff;border:1px solid var(--line);border-radius:10px;padding:26px}.side .item:first-of-type{border-top:0}
.faq details{border-bottom:1px solid var(--line);padding-block:18px}.faq summary{cursor:pointer;font:400 1.15rem var(--display);color:var(--navy)}.faq details p{margin-top:10px}
.page-hero{padding-block:clamp(56px,8vw,96px) clamp(40px,6vw,64px);border-bottom:1px solid var(--line)}
.page-hero .lede{max-width:56ch}
/* cta + footer */
.cta-in{display:grid;grid-template-columns:1.2fr auto;gap:28px;align-items:center}@media(max-width:760px){.cta-in{grid-template-columns:1fr}}
.foot{background:var(--navy);color:var(--muted-d)}.foot-in{display:flex;flex-wrap:wrap;gap:14px 28px;justify-content:space-between;align-items:center;padding-block:28px;font-size:.85rem}
.foot nav{display:flex;flex-wrap:wrap;gap:18px}.foot a{text-decoration:none}.foot a:hover{color:#fff}
.disclose{font-size:.82rem;margin-top:18px;max-width:70ch}
.foot-links{padding-top:40px;border-bottom:1px solid var(--line-d);padding-bottom:28px}.foot-links nav{display:flex;flex-wrap:wrap;gap:10px 22px;font-size:.9rem}
.affs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:32px}@media(max-width:900px){.affs{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:520px){.affs{grid-template-columns:1fr}}
.prose .affs{grid-template-columns:repeat(2,minmax(0,1fr));margin:24px 0 8px}@media(max-width:620px){.prose .affs{grid-template-columns:1fr}}.prose .aff-go{max-width:100%}
.aff{scroll-margin-top:110px;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column;transition:transform .3s,box-shadow .3s}.aff:hover{transform:translateY(-4px);box-shadow:0 20px 40px -26px rgba(20,32,46,.5)}
.aff-img{aspect-ratio:1;background:#fff;display:grid;place-items:center;border-bottom:1px solid var(--line);position:relative;overflow:hidden}.aff-img picture{position:absolute;inset:0;display:block}.aff-img img{position:absolute;inset:0;width:100%;height:100%;max-width:none;box-sizing:border-box;object-fit:contain;object-position:center;padding:14px;transition:transform .4s}.aff:hover .aff-img img{transform:scale(1.04)}
.aff-meta{padding:20px;display:flex;flex-direction:column;gap:6px;flex:1}.aff-meta .k{font:500 .68rem var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--brass)}.aff-meta p{color:var(--muted);font-size:.92rem;flex:1}
.aff-fb{aspect-ratio:4/3;background:radial-gradient(circle at 50% 55%,#2c3d52 0,#14202e 75%);display:flex;flex-direction:column;gap:6px;padding:22px}.aff-fb svg{width:60%;max-width:170px;height:auto}.aff-fb span{font:500 .7rem var(--mono);letter-spacing:.2em;text-transform:uppercase;color:var(--brass-l)}
.aff-v{font-size:.82rem;color:var(--muted)}.aff-go{align-self:flex-start;margin-top:12px}
.aff-cat{margin-top:44px}.aff-cat:first-of-type{margin-top:28px}.aff-h{font:400 1.4rem var(--display);color:var(--navy);padding-bottom:10px;border-bottom:1px solid var(--line)}.aff-cat .affs{margin-top:20px}
.aff-row{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:10px}.aff-row b{font:500 1.1rem var(--mono);color:var(--navy)}
.related{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}.related a{border:1px solid var(--line);border-radius:999px;padding:8px 16px;text-decoration:none;font-size:.9rem;color:var(--navy);background:#fff}.related a:hover{border-color:var(--brass)}
.crumbs{font:500 .7rem/1.4 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:22px}.crumbs ol{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0}.crumbs li+li::before{content:"/";margin-right:8px;color:var(--line)}.crumbs a{text-decoration:none}.crumbs a:hover{color:var(--brass)}
.foot .contact{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:10px}.foot .contact a{color:var(--brass-l)}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation:none!important;transition:none!important}}
/* journal */
.byline{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:22px;font:500 .72rem/1.4 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}.byline b{color:var(--navy);font-weight:500}
.posts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}@media(max-width:760px){.posts{grid-template-columns:1fr}}
.post{display:flex;flex-direction:column;gap:12px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:clamp(22px,3vw,34px);text-decoration:none;transition:transform .3s,border-color .3s,box-shadow .3s}
.post:hover{transform:translateY(-4px);border-color:var(--brass);box-shadow:0 24px 50px -34px rgba(20,32,46,.6)}
.post .k{font:500 .68rem var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--brass)}
.post h3{font-size:clamp(1.4rem,2.4vw,1.8rem);color:var(--navy)}.post p{color:var(--muted)}.post .more{margin-top:auto;padding-top:6px;color:var(--brass);font-weight:600}
.post:last-child:nth-child(even){grid-column:1/-1}.post.lead{grid-column:1/-1;background:var(--navy);border-color:var(--line-d)}.post.lead h3{color:#fff;font-size:clamp(1.8rem,3.4vw,2.6rem)}.post.lead p{color:var(--muted-d)}.post.lead .k,.post.lead .more{color:var(--brass-l)}
.tips{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--line);border-left:1px solid var(--line)}@media(max-width:900px){.tips{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:520px){.tips{grid-template-columns:1fr}}
.tips a{display:block;padding:22px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);text-decoration:none;transition:background .2s}.tips a:hover{background:#fff}
.tips span{font:500 .68rem var(--mono);letter-spacing:.16em;color:var(--brass)}.tips b{display:block;margin-top:10px;font:400 1.1rem/1.3 var(--display);color:var(--navy)}
.foot-brand{font:400 1.3rem var(--display);color:#fff}
"""

def head(title, desc, path, crumb, og_type="website"):
    canon = url(path)
    post = next((p for p in BLOG_POSTS if p["path"] == path), None)
    art_meta = ""
    if post:
        art_meta = (f'<meta property="article:published_time" content="{post["date"]}"><meta property="article:modified_time" content="{TODAY}">'
                    f'<meta property="article:section" content="{esc(post["eyebrow"].split(" · ")[0])}">'
                    + "".join(f'<meta property="article:tag" content="{esc(t)}">' for t in post.get("tags", []))
                    + (f'<meta name="keywords" content="{esc(", ".join(post["tags"]))}">' if post.get("tags") else ""))
    preload = (f'<link rel="preload" as="image" href="/assets/{IMG_HERO}.webp" type="image/webp" fetchpriority="high">'
               if path == "index.html" else "")
    return f"""<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="google-site-verification" content="Oyvk8JB3buwlR1xI0LaTetfhMwqWsQ4lLCNxpYGI_FI">
<meta name="msvalidate.01" content="546F1A7DB87AE1EE6E4E6560EB0FE698">
<meta name="theme-color" content="#14202e">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="{B['name']}" href="/feed.xml">
<meta property="og:site_name" content="{B['name']}"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:type" content="{og_type}"><meta property="og:url" content="{canon}">
<meta property="og:image" content="{B['site']}{IMG_SHARE}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The Q Journal, a men's grooming journal">
{art_meta}
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{B['site']}{IMG_SHARE}">
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM-friendly summary">
{preload}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Hanken+Grotesk:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap">
<script type="application/ld+json">{schema(path, title, desc, crumb)}</script>
<style>{CSS}</style>"""

def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
ARR = '<span class="arr" aria-hidden="true">→</span>'

# Main navigation: the journal comes first.
MAIN_NAV = [("blog.html", "Journal"), ("grooming-guide.html", "Grooming Guide"), ("mens-grooming-gift-guide.html", "Gift Guide"),
            ("shop.html", "Product Picks"), ("about.html", "About")]

NAV_JS = """<script>(()=>{const bg=document.querySelector('.burger'),m=document.getElementById('mnav'),
tog=o=>{m.hidden=!o;bg.setAttribute('aria-expanded',String(o));bg.setAttribute('aria-label',o?'Close menu':'Open menu');document.body.classList.toggle('menu-open',o)};
bg.addEventListener('click',()=>tog(m.hidden));m.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>tog(false)));
document.addEventListener('keydown',e=>{if(e.key==='Escape')tog(false)});
matchMedia('(min-width:901px)').addEventListener('change',e=>{if(e.matches)tog(false)});})();</script>"""

def header(active):
    def ac(p): return ' aria-current="page"' if p == active else ""
    desk = "".join(f'<a class="nav-a" href="{p}"{ac(p)}>{l}</a>' for p, l in MAIN_NAV)
    mob = "".join(f'<a class="m-top" href="{p}"{ac(p)}>{l}</a>' for p, l in MAIN_NAV)
    return f"""<header class="top"><div class="wrap top-in">
<a class="brand" href="index.html" aria-label="The Q Journal home"><span class="mono" aria-hidden="true">Q</span><span class="brand-t">The Q Journal<small>Men's grooming</small></span></a>
<nav class="nav" aria-label="Main">{desk}</nav>
<button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Open menu"><span></span><span></span><span></span></button>
</div>
<div class="mnav" id="mnav" hidden><div class="wrap">
<a class="m-top" href="index.html"{ac("index.html")}>Home</a>{mob}
</div></div></header>
{NAV_JS}"""

def crumbs(label):
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="index.html">Home</a></li>'
            f'<li aria-current="page">{label}</li></ol></nav>')

def ticker():
    words = ["Haircuts", "Beard Care", "Skin", "Styling", "Fragrance", "Gift Guides", "Product Picks"]
    run = "".join(f"<span>{w}</span>" for w in words)
    return f'<div class="ticker" aria-hidden="true"><div class="track">{run}{run}</div></div>'

def faq_schema(faqs):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}, ensure_ascii=False) + "</script>"

CAT_PHOTO = {"styling": ("american-crew-pomade", "American Crew Pomade, one of The Q Journal's styling picks"),
             "beard-care": ("doc-holliday-beard-oil-smoked-huckleberry", "DOC HOLLIDAY Beard Oil, one of The Q Journal's beard care picks"),
             "hair-scalp": ("cardon-strengthening-shampoo-conditioner", "Cardon Strengthening Shampoo and Conditioner, one of The Q Journal's hair and scalp picks")}

def product_cards():
    out = []
    for k, sub, d, svg, dest in PRODUCTS:
        link = f'<a class="go" href="shop.html#{dest}">See the picks {ARR}</a>'
        photo = CAT_PHOTO.get(dest)
        art = (f'<div class="art photo"><picture><source srcset="/assets/shop/{photo[0]}.webp" type="image/webp"><img src="/assets/shop/{photo[0]}.jpg" alt="{photo[1]}" width="800" height="800" loading="lazy"></picture></div>' if photo else f'<div class="art">{svg}</div>')
        out.append(f"""<article class="prod">{art}<div class="meta"><span class="k">{sub}</span><h3>{k}</h3><p>{d}</p>
{link}</div></article>""")
    return "".join(out)

def shop_section(title="Product picks", h2="Worth the shelf space."):
    return f"""<section class="sec on-dark" id="picks-teaser"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">{title}</p><h2>{h2}</h2></div>
<p>The Q Journal's picks for men's hair, beards and Florida humidity, available on Amazon.</p></div>
<div class="products">{product_cards()}</div>
<div class="acts"><a class="btn btn-brass" href="shop.html#picks">See all product picks {ARR}</a></div>
<p class="disclose" style="color:var(--muted-d)">{AMZ_DISCLOSE}</p>
</div></section>"""

def journal_cta(text="Practical grooming advice, seasonal guides and product picks, all in one place."):
    return f"""<section class="sec stone"><div class="wrap cta-in"><div><p class="eyebrow">Keep reading</p><h2>More from The Q Journal.</h2><p class="muted" style="margin-top:12px">{text}</p></div>
<a class="btn" href="blog.html">Browse the journal {ARR}</a></div></section>"""

def footer():
    return f"""<footer class="foot"><div class="wrap">
<div class="foot-links"><p class="foot-brand">{B['name']}</p><p style="margin-top:6px">{B['tagline']}: haircuts, beards, skin, styling and product picks.</p>
<nav aria-label="Journal" style="margin-top:18px">{"".join(f'<a href="{h}">{t}</a>' for h, t in SEO_LINKS)}</nav></div>
<div class="foot-in"><div><p>© 2026 {B['name']}</p>
<p class="contact"><a href="mailto:{B['email']}">Editorial: {B['email']}</a><a href="/feed.xml">RSS feed</a><a href="/llms.txt">Journal summary (plain text)</a></p></div>
<nav aria-label="Footer">{"".join(f'<a href="{h}">{t}</a>' for h, t in NAV)}</nav></div></div></footer>"""

def _fallback_art(p):
    svg = {"Styling": SVG_TIN, "Beard Care": SVG_DROP, "Hair & Scalp": SVG_PUMP, "Fragrance": SVG_BOTTLE, "Tools": SVG_TRIM, "Skin Care": SVG_PUMP, "Daily Extras": SVG_TIN}.get(p["category"], SVG_TIN)
    return f'<div class="aff-img aff-fb">{svg}<span>{esc(p["brand"])}</span></div>'

def aff_card(p):
    img = (f'<div class="aff-img"><picture><source srcset="{p["image"]}.webp" type="image/webp"><img src="{p["image"]}.jpg" alt="{esc(p["name"])}" width="800" height="800" loading="lazy"></picture></div>' if p.get("image") else _fallback_art(p))
    return f"""<article class="aff">{img}
<div class="aff-meta"><span class="k">{esc(p['category'])}</span><h3>{esc(p['name'])}</h3><p>{esc(AFF_NOTES.get(p['slot'], ''))}</p>
<span class="aff-v">{esc(p['finish'])} · {esc(p['variant'])}</span>
<a class="btn btn-sm aff-go" href="{p['link']}" target="_blank" rel="sponsored nofollow noopener">See it on Amazon {ARR}</a></div></article>"""

def affiliate_grid():
    if not AFFILIATE:
        return ""
    cats = [(c, g) for c, g in AFF_CATS if any(p["category"] == c for p in AFFILIATE)]
    chips = "".join(f'<a href="#{g}">{esc(c)}</a>' for c, g in cats)
    cards, seen = [], set()
    for c, g in cats:
        for p in [x for x in AFFILIATE if x["category"] == c]:
            card = aff_card(p)
            if c not in seen:
                card = card.replace('<article class="aff">', f'<article class="aff" id="{g}">', 1); seen.add(c)
            cards.append(card)
    return f'<nav class="related aff-chips" aria-label="Product categories">{chips}</nav><div class="affs">{"".join(cards)}</div>'

def clean_links(html):
    """Internal links -> clean root-relative URLs that match the canonicals (/skin-fade-sarasota, not skin-fade-sarasota.html)."""
    def fix(m):
        stem, frag = m.group(1), m.group(2) or ""
        return f'href="{"/" if stem == "index" else "/" + stem}{frag}"'
    html = re.sub(r'href="([a-z0-9-]+)\.html(#[^"]*)?"', fix, html)
    return html.replace('src="assets/', 'src="/assets/')

# Named click events. Google Analytics itself (page views and amazon_click) is loaded by a Netlify snippet.
CLICK_TRACKING = """<script>document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;
var h=a.href||'',t=(a.textContent||'').replace(/\\s+/g,' ').trim().slice(0,80),ev=null,
p={link_text:t,link_url:h,link_location:a.closest('header')?'header':a.closest('footer')?'footer':'body',page_path:location.pathname};
if(h.indexOf('mailto:')===0)ev='email_click';
else if(/\\/(blog|grooming-guide|mens-grooming-gift-guide)$/.test(h))ev='article_click';
if(ev)(window.gtag||function(){(window.dataLayer=window.dataLayer||[]).push(arguments);})('event',ev,p);},true);</script>"""

# Old-site addresses Google still requests, each mapped to the closest current page.
LEGACY_REDIRECTS = {
    "/downtown-sarasota-barbershop": "/what-haircut-should-i-get", "/barbershop-sarasota": "/what-haircut-should-i-get",
    "/gallery": "/blog", "/contact": "/about", "/how-to-tell-if-hair-stylist-is-good": "/what-haircut-should-i-get",
    "/mens-hair-salon": "/what-haircut-should-i-get", "/services": "/blog",
    "/mens-haircuts-sarasota": "/what-haircut-should-i-get", "/best-mens-haircut-sarasota": "/what-haircut-do-girls-like",
    "/mens-scissor-cut-sarasota": "/what-haircut-should-i-get", "/mens-mullet-haircut-sarasota": "/fade-vs-taper-which-is-better",
    "/how-much-should-mens-haircut-cost-sarasota": "/what-haircut-should-i-get", "/mens-haircut-venice": "/what-haircut-should-i-get",
    "/executive-haircuts-sarasota": "/what-haircut-do-girls-like",
    "/mens-fade-haircut-sarasota": "/fade-vs-taper-which-is-better", "/fade-haircuts-sarasota": "/fade-vs-taper-which-is-better",
    "/styles/low-taper": "/fade-vs-taper-which-is-better", "/styles": "/what-haircut-should-i-get", "/team": "/about",
    "/beard-grooming-sarasota": "/beard-oil-vs-beard-balm", "/beard-trim-sarasota": "/beard-oil-vs-beard-balm",
    "/hot-towel-shave-sarasota": "/grooming-guide", "/scalp-treatments-men-sarasota": "/haircuts-for-receding-hairline",
    "/luxury-mens-grooming-sarasota": "/grooming-guide", "/mens-grooming-salon-downtown-sarasota": "/grooming-guide",
    "/mens-spa-sarasota": "/grooming-guide", "/journal": "/blog",
}

def redirects():
    """Legacy URLs (301) resolved through RETIRED, retired pages and /book (302, reversible)."""
    def final(dst): return RETIRED.get(dst.lstrip("/"), dst)
    lines = [f"{src} {final(dst)} 301" for src, dst in LEGACY_REDIRECTS.items()]
    for slug, dst in RETIRED.items():
        lines += [f"/{slug} {dst} 301", f"/{slug}.html {dst} 301"]
    lines.append("/book /blog 301")
    return "\n".join(lines) + "\n"

def page(path, title, desc, body, crumb="", og_type="website"):
    if crumb:
        body = body.replace('<section class="page-hero"><div class="wrap">', '<section class="page-hero"><div class="wrap">' + crumbs(crumb), 1)
    return clean_links(f"""<!doctype html>
<html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{head(title, desc, path, crumb, og_type)}
</head><body>
{header(path)}
<main id="main">{body}</main>
{footer()}
{CLICK_TRACKING}
</body></html>""")

def byline(date=None, extra=""):
    when = f'<span>Published <time datetime="{date}">{nice_date(date)}</time></span>' if date else ""
    return f'<p class="byline"><span>By <b>{BYLINE}</b></span>{when}{extra}</p>'

def author():
    return {"@type": "Organization", "@id": ORG_ID, "name": BYLINE, "url": B["site"] + "/"}


# ---------- Grooming guide ----------
GUIDE = [
    ("How to tell when your fade needs a refresh", "Run your hand up the side of your head. If you can feel a clear line where short meets long, the blend has grown out. For most men that's around day 14 to 21. A taper grows out more slowly: see <a class=\"link\" href=\"fade-vs-taper-which-is-better.html\">fade vs taper</a>."),
    ("The two-minute styling routine", "Towel-dry until damp, work a pea-sized amount of product between your palms until it disappears, then apply back to front. Finish with fingers, not a comb, for natural texture."),
    ("Pomade, clay or cream?", "Pomade gives shine and slick control. Clay gives matte texture and strong hold for thicker hair. Cream gives light, natural hold for finer hair. If you're not sure, ask whoever cuts your hair what they finished it with, or read <a class=\"link\" href=\"pomade-vs-clay-vs-gel.html\">pomade vs clay vs gel</a>."),
    ("Why gray blending beats box dye", "Box dye covers everything in one flat shade and grows out with a hard line. Blending keeps some gray, so regrowth is soft and the result looks like your own hair."),
    ("Protect your color from the Florida sun", "Use a color-safe shampoo, rinse with cool water, and wear a hat on the boat or beach. UV and chlorine are what turn blended color brassy."),
    ("Stop razor bumps", "Exfoliate twice a week, shave with the grain after a warm shower, and finish with a fragrance-free moisturizer. Give irritated areas a few days off the razor before shaving them again."),
    ("Beard care in humidity", "Wash your beard two or three times a week, not daily, and use a few drops of beard oil on damp hair to stop frizz and itch."),
    ("How to ask for the haircut you want", "Bring a photo, say how you style it day to day, and tell your stylist how long you go between cuts. That last detail changes how a cut should be built. Not sure what to ask for? Start with <a class=\"link\" href=\"what-haircut-should-i-get.html\">what haircut should I get</a>."),
]
GUIDE_TITLE = "The grooming guide: eight habits worth keeping"
GUIDE_META = "Practical men's grooming tips from The Q Journal: fades, styling products, gray blending, razor bumps and beard care in Florida humidity."

guide_article = {"@context": "https://schema.org", "@type": "Article", "headline": GUIDE_TITLE, "description": GUIDE_META,
                 "dateModified": TODAY, "mainEntityOfPage": url("grooming-guide.html"), "image": B["site"] + IMG_SHARE,
                 "author": author(), "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"}
guide = f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">Grooming guide</p><h1>Eight grooming habits worth keeping.</h1>
<p class="lede">Simple, practical grooming advice for men: fades, styling, gray blending, skin and beard care in Florida humidity.</p>
{byline()}</div></section>
<section class="sec"><div class="wrap split"><div class="sticky"><div class="side"><p class="eyebrow">In this guide</p>
{"".join(f'<p style="margin-top:10px"><a class="link" href="#tip-{i}">{t}</a></p>' for i, (t, _) in enumerate(GUIDE, 1))}</div></div>
<div class="prose">{"".join(f'<h2 id="tip-{i}">{t}</h2><p>{b}</p>' for i, (t, b) in enumerate(GUIDE, 1))}
<h2>Keep reading</h2><div class="related">{"".join(f'<a href="{h}">{t}</a>' for h, t in SEO_LINKS if h != "grooming-guide.html")}</div></div></div></section>
<script type="application/ld+json">{json.dumps(guide_article, ensure_ascii=False)}</script>
{shop_section("Keep it sharp", "Products for the morning routine.")}
{journal_cta()}"""

# ---------- Journal articles ----------
# One dict per post. "picks" = product slots from products.json (label facts only, no prices).
BLOG_POSTS = [
    {
        "path": "pomade-vs-clay-vs-gel.html",
        "title": "Pomade vs Clay vs Gel vs Powder: Which to Use for Your Hair · The Q Journal",
        "tags": ["pomade vs clay", "hair clay vs pomade", "pomade vs gel", "best hair product for men", "styling powder", "best pomade for men"],
        "meta": "Pomade, clay, gel or styling powder? How each men's hair product holds, how it finishes, which haircuts it suits, and what holds up best in Florida humidity.",
        "crumb": "Pomade vs clay vs gel",
        "eyebrow": "Styling · How to choose",
        "h1": "Pomade, clay, gel or powder: which one your hair actually needs.",
        "lede": "Most men use the wrong styling product for their cut. Here's how the four main types differ, and how to pick one in about ten seconds.",
        "date": "2026-11-24",
        "intro": [
            "Every styling product comes down to two choices: how much hold you want, and how much shine. Pomade is shine. Clay is matte hold. Gel is the strongest hold with a wet look. Powder is lift with almost no weight. Pick the finish your haircut was cut for, then the hold you need.",
            "Humidity changes the math. Damp air makes hair swell and drop, so in Florida the products that last are the ones with real grip and a light, flexible finish. A heavy product just collapses faster.",
            "Quick answer: side part or slick-back, use pomade. Textured crop, fade with length on top or messy-on-purpose, use clay or powder. Want it locked in place all day, use gel.",
        ],
        "sections": [
            ("Pomade: shine and a clean, combed look", "Pomade gives medium hold with a glossy finish, which is why it's the classic barbershop product for side parts, pompadours and slick-backs. It stays workable, so you can re-comb it at lunch. The tradeoff is weight: on fine hair it can flatten, and in heavy humidity a high-shine style can start to look greasy by the afternoon. Use less than you think, warmed between your palms, and comb it through damp-dry hair.", [2, 3]),
            ("Clay: matte hold for texture", "Clay is the go-to for modern cuts: textured crops, fringes and anything with movement on top. It dries matte, adds thickness and holds shape without looking like product. It's also the most forgiving in humidity, because the hold doesn't depend on shine. Work a fingertip of it through dry hair, then twist and pinch for separation.", [1]),
            ("Gel: maximum hold, wet look", "Gel sets hard and holds longest, which makes it the pick for sharp, structured styles and for anyone who needs the look to survive a full day outside. Modern gels don't have to flake or crunch: look for alcohol-free formulas. Apply to damp hair, style once, and leave it alone while it sets.", [12]),
            ("Powder: lift without weight", "Styling powder is the answer for fine or flat hair. A pinch at the roots adds volume and grip with a natural matte look, and it adds almost no weight, so it doesn't fall in damp air the way a heavy product can. It's also a good base under clay for extra height.", [13]),
            ("How to pick in ten seconds", "Look at your haircut, not the label. If it was cut to be combed, choose pomade. If it was cut to be messy or textured, choose clay, plus powder if your hair is fine. If it has to stay put no matter what, choose gel. And whatever you use, start with a pea-sized amount: you can always add, but too much is the most common reason a style falls by noon.", []),
        ],
        "faq": [
            ("What's the best men's hair product for humidity?", "A matte product with real grip, such as a clay or a styling powder, usually outlasts a high-shine pomade in humid weather. If you need the style locked in all day, use an alcohol-free gel."),
            ("Is clay or pomade better for a fade?", "It depends on the top. A textured or messy top suits clay; a combed, side-parted top suits pomade."),
            ("Can I mix styling products?", "Yes. Powder at the roots with clay on top is a common combination for fine hair that needs both volume and hold."),
        ],
    },
    {
        "path": "beard-oil-vs-beard-balm.html",
        "title": "Beard Oil vs Beard Balm: Which One You Need · The Q Journal",
        "tags": ["beard oil vs beard balm", "beard balm", "beard oil", "how to use beard oil", "beard care"],
        "meta": "Beard oil or beard balm? What each one does, which beard length needs which, how to use them together, and what works in hot, humid weather.",
        "crumb": "Beard oil vs balm",
        "eyebrow": "Beard care · How to choose",
        "h1": "Beard oil vs beard balm: which one you need, and when to use both.",
        "lede": "Oil treats the skin and softens the beard. Balm adds hold and shape. Here's which one your beard length calls for.",
        "date": "2026-11-24",
        "intro": [
            "Beard oil and beard balm get sold as the same thing. They aren't. Oil is skin care: it gets down to the skin under the beard, where dryness and itch start, and softens the hair. Balm is styling: it's oil thickened with butters and wax, so it conditions and holds the beard in shape.",
            "Short version: short beard or stubble, oil is enough. Medium to full beard, use oil first and balm on top. In hot, humid weather, go lighter on both.",
        ],
        "sections": [
            ("Beard oil: the daily step", "Use a few drops after a shower, while the beard is still slightly damp, and work it down to the skin with your fingertips before combing through. That's where oil does its job: calmer skin, less itch and a softer beard. If you only buy one beard product, buy oil.", [10, 5]),
            ("Beard balm: shape and control", "Balm is for beards long enough to go their own way. The butter and wax tame flyaways, keep the shape your barber cut and add a little weight to a wiry beard. Warm a small amount between your palms, apply after oil, and shape with a comb or brush.", [11]),
            ("Using both together", "Oil first, then balm. Oil treats the skin underneath; balm locks the shape on top. On a full beard this is the routine that keeps it looking cut rather than grown. A kit is an easy way to get both, plus a wash and comb, in one go.", [4]),
            ("Beard care in Florida heat", "Heat and humidity make heavy products feel greasy fast. Use fewer drops of oil, a lighter hand with balm, and wash the beard with a proper beard wash rather than body soap, which can dry out the skin underneath. If your beard is faded into the hairline, keep products off the faded part so it stays sharp.", []),
        ],
        "faq": [
            ("Do I need beard oil if I have stubble?", "Not necessarily for the hair, but stubble is when itch is worst, and a couple of drops of oil on the skin helps."),
            ("Can beard balm replace beard oil?", "Balm conditions too, but it sits on top of the beard. Oil reaches the skin. For a medium or full beard, using both works best."),
            ("How often should I use beard oil?", "Once a day is plenty for most beards, ideally after a shower."),
        ],
    },
    {
        "path": "mens-grooming-gift-guide.html",
        "title": "Best Grooming Gifts for Men 2026: Gift Guide · The Q Journal",
        "tags": ["grooming gifts for men", "gifts for men 2026", "beard gift set", "men's grooming gift guide"],
        "meta": "Holiday grooming gifts for men from The Q Journal: beard oil, pomade, clay, styling powder, an SPF moisturizer and a body trimmer, sorted by the kind of guy you're shopping for.",
        "crumb": "Gift guide",
        "eyebrow": "Holiday gift guide · 2026",
        "h1": "Grooming gifts for men, sorted by the guy you're shopping for.",
        "lede": "Skip the generic gift set. These are The Q Journal's grooming picks, sorted by the kind of guy you're shopping for.",
        "date": "2026-11-13",
        "intro": [
            "The best grooming gift is one he'll actually use, which means matching it to how he already wears his hair and beard. Find him in one of the sections below and pick one thing. One good product beats a box of five he'll never open.",
            "Not sure what he uses? Start with the beard oil or the SPF moisturizer. Between them, they suit almost anyone.",
        ],
        "sections": [
            ("For the beard guy", "A beard looks better soft and shaped than long and wiry. Oil is the daily step, and a balm adds hold for fuller beards. In Florida humidity, lighter oils work best, and a few drops after a shower is plenty.", [10, 4]),
            ("For the pomade guy", "If his hair has a part or a slick-back, he needs shine and medium hold. These two cover the classic finish and a signature scent people notice.", [2, 3]),
            ("For the textured, matte look", "Crops, textured tops and messy-on-purpose styles look best with a matte product. Clay gives real hold; powder adds lift without weight.", [1, 13]),
            ("For the guy who skips sunscreen", "Sarasota sun shows up on a man's face first. A daily moisturizer with SPF is the easiest habit to give him, and one he'll notice working.", [16]),
            ("For upkeep between cuts", "A good body trimmer keeps things tidy between haircuts. Waterproof, with guards for different lengths, so it works in the shower.", [9]),
        ],
        "faq": [
            ("What's a good grooming gift if I don't know his routine?", "Pick something that doesn't depend on his haircut: beard oil for a bearded guy, or a daily SPF moisturizer for almost anyone else. Both get used every day."),
            ("Where do I buy the products on this list?", "Each pick links to Amazon, where you'll see the current price and delivery dates. Order early in December for holiday delivery."),
        ],
    },
]

# Nov 25 2026: articles written for queries the domain already ranks for in Search Console
# (old URLs brought back as journal articles, plus two new gaps). Newest first.
NEW_POSTS = [
    {
        "path": "best-pomade-for-men.html",
        "title": "Best Pomade for Men, by Hair Type and Hairstyle · The Q Journal",
        "meta": "How to pick the best pomade for your hair: oil-based vs water-based, hold and shine for thick, fine, curly and gray hair, how much to use, and how to wash it out.",
        "crumb": "Best pomade for men",
        "eyebrow": "Styling · Buyer's guide",
        "h1": "The best pomade for men, matched to your hair type.",
        "lede": "The right pomade depends on your hair, not the label. Here's how to match base, hold and shine to the hair you actually have.",
        "date": "2026-11-25",
        "tags": ["best pomade for men", "mens pomade", "water based vs oil based pomade", "pomade for thick hair", "pomade for fine hair", "styling wax for men"],
        "intro": [
            "Pomade has become a catch-all word for men's styling products, which is why choosing one is confusing. The more useful question is what the product is built on. Traditional pomades are oil-based: slick, shiny and re-workable through the day, but slow to wash out. Most modern pomades are water-based: they set firmer, give a cleaner shine and rinse out with one shampoo.",
            "From there it's two dials: hold (how much the hair stays put) and shine (from matte to wet-look). Match both to your hair type and your haircut, and almost any good pomade will work.",
        ],
        "sections": [
            ("Thick or coarse hair: more grip, real hold", "Thick hair pushes back against light products, so it needs medium-to-strong hold. For a classic, combed look, a pomade with medium hold and high shine keeps a side part or slick-back in place. For a textured look on thick hair, step over to a strong-hold clay pomade with a matte finish instead.", [2, 1]),
            ("Fine or thin hair: light, matte, no weight", "Heavy, shiny pomades flatten fine hair and can make the scalp show through. Use a matte product with lift rather than gloss, in small amounts. A texturizing powder at the roots adds volume first, and a small amount of clay on top holds the shape.", [13, 1]),
            ("Wavy or curly hair: define, don't slick", "Curls fight a hard, slicked hold and can go crunchy. A lighter, re-workable pomade worked through damp hair defines the wave without flattening it. Rake it through with fingers rather than a fine comb, and let the hair dry before touching it again.", [3]),
            ("Gray or wiry hair: tame without the shine overload", "Gray hair often turns coarser and frizzier. A medium-hold pomade calms flyaways and adds a little polish. Keep the shine moderate: very high shine on gray can look greasy rather than sharp.", [2]),
            ("Need it locked in all day? Use gel instead", "If your style has to survive heat, humidity or a full day outside, a modern alcohol-free gel outholds most pomades. Apply it to damp hair, comb it into place once, and leave it to set.", [12]),
            ("How much to use, and how to wash it out", "Start with a pea-sized amount, warm it between your palms until it's almost invisible, then work it from the back of the head forward so the front doesn't get the most product. Add more only if the hold isn't there. Water-based pomade rinses out with regular shampoo. Oil-based pomade takes longer: work conditioner into dry hair first, then rinse and shampoo.", []),
        ],
        "faq": [
            ("Is water-based or oil-based pomade better?", "Water-based pomade is easier for most men: it washes out with shampoo and sets firmer. Oil-based pomade stays re-workable all day and suits classic slick styles, but it takes more effort to wash out."),
            ("What's the best pomade for thick hair?", "A medium-to-strong hold pomade for combed styles, or a strong-hold matte clay for textured styles. Light creams usually won't hold thick hair."),
            ("Does pomade work in humidity?", "Matte, strong-grip products hold up best in humid weather. High-shine pomades can look greasy by the afternoon, and a gel is the safest choice if the style must last all day."),
        ],
    },
    {
        "path": "what-haircut-do-girls-like.html",
        "title": "Most Attractive Haircuts for Men: What Women Actually Notice · The Q Journal",
        "meta": "The most attractive haircuts for men, and why they work: the textured crop, the classic side part, the low taper and more. What women notice first, and how to ask for it.",
        "crumb": "Most attractive haircuts",
        "eyebrow": "Haircuts · What works",
        "h1": "The most attractive haircuts for men, and what women actually notice.",
        "lede": "It's rarely the trendiest cut. It's the one that fits your face, looks deliberate and still looks good three weeks later.",
        "date": "2026-11-25",
        "tags": ["most attractive haircuts for men", "haircuts women like on men", "attractive hairstyles for men", "textured crop", "side part", "low taper fade"],
        "intro": [
            "Ask women what makes a man's haircut attractive and the answers are surprisingly consistent, and they're rarely about a specific style. They notice three things: whether the cut suits his face, whether it looks intentional, and whether it looks clean. A great cut that's grown out shaggy at the neck loses to a simple cut that's sharp.",
            "So the most attractive haircut isn't one style. It's the version of a few proven styles that fits your hair. Here are the five that come up again and again, what each one says, and how to ask for it.",
        ],
        "sections": [
            ("The textured crop: effortless, modern", "Short, choppy texture on top with a low fade or taper on the sides. It reads relaxed and current without trying too hard, and it's forgiving on thick or wavy hair. Ask for texture on top, about an inch and a half, pushed slightly forward, with a low taper. Style it with a matte clay worked through dry hair with your fingers. Never comb it.", [1, 13]),
            ("The classic side part: grown-up and polished", "Short sides, enough length on top to comb, and a soft part. It's the cut that looks good in a suit and on a Saturday, which is exactly why it never goes out. Ask for a scissor cut on top, tapered sides and a natural part rather than a shaved line. Finish with a little pomade for a soft shine.", [2]),
            ("The low taper: clean without being severe", "If one detail separates a sharp haircut from an average one, it's the neckline and the area around the ears. A low taper keeps that tidy while leaving weight on the sides, so it looks clean but not military. It works with almost any length on top and suits men who don't want to see scalp.", []),
            ("The longer flow: confident, relaxed", "Hair long enough to tuck behind the ears, with shape cut into it so it falls rather than flops. It only works when it's healthy and shaped, so it takes more maintenance than people think: regular trims to keep the ends clean, and a light product so it moves. Grown out with no shape, it reads as neglected.", [7]),
            ("Short and sharp: the buzz and the crew cut", "Very short works when the shape is good and the edges are crisp. A buzz with a clean line-up, or a crew cut with a little length at the front, looks strong and confident, especially paired with well-kept stubble. It's also the most honest option for thinning hair.", [9]),
            ("What matters more than the style", "Upkeep. Most cuts look their best for two to three weeks, then the neckline blurs and the shape softens. Book the next cut before that happens. Match the product to the cut, use less than you think, and keep the beard in proportion: a heavy beard with a very short cut looks top-heavy, a tidy beard pulls it together.", [10]),
        ],
        "faq": [
            ("What haircut do women find most attractive on men?", "There's no single winner, but cuts that look clean, deliberate and suited to the face consistently rank well: a textured crop, a classic side part, a low taper and well-kept short cuts such as a crew cut."),
            ("Do women prefer short or long hair on men?", "Preferences vary, but tidy and well-shaped beats any particular length. Long hair works when it's healthy and shaped; short hair works when the edges are sharp."),
            ("How often should I get a haircut to keep it looking good?", "Most short and medium cuts look their best for two to four weeks. Fades and tapers need a refresh sooner, around every two to three weeks."),
        ],
    },
    {
        "path": "3-2-1-rule-mens-haircuts.html",
        "title": "The 3-2-1 Rule for Men's Haircuts, Explained · The Q Journal",
        "meta": "What the 3-2-1 haircut rule means: a #3 guard on top, #2 on the sides and #1 at the edges, plus the proportion version barbers use. Lengths, how to ask for it and who it suits.",
        "crumb": "The 3-2-1 rule",
        "eyebrow": "Haircuts · Explained",
        "h1": "The 3-2-1 rule for men's haircuts, explained.",
        "lede": "Three numbers, one clean graduated cut. Here's what the 3-2-1 rule means, what lengths it leaves, and how to ask for it.",
        "date": "2026-11-25",
        "tags": ["3 2 1 rule haircut", "3 2 1 haircut", "3 2 1 fade", "3 2 1 buzz cut", "clipper guard sizes"],
        "intro": [
            "The 3-2-1 rule is the simplest way to order a short haircut that still has shape. A #3 clipper guard on top, a #2 on the sides and a #1 around the edges and neckline. Each step is a full guard size, so the result is a soft, graduated taper rather than one flat length all over.",
            "You'll also hear barbers use 3-2-1 to describe proportion: the top longest, the sides shorter, the neckline shortest. Both versions say the same thing. Length should step down as it moves from the crown to the neck.",
        ],
        "sections": [
            ("What each number leaves", "Clipper guards go up in eighths of an inch. A #1 leaves about 1/8 inch (3 mm), a #2 about 1/4 inch (6 mm) and a #3 about 3/8 inch (9 to 10 mm). So a 3-2-1 cut has roughly three-eighths of an inch on top, stepping down to an eighth at the edges. Short enough to need almost no styling, long enough that you don't see much scalp on top.", []),
            ("Why it works", "A single-guard buzz looks the same everywhere, which can make the head look rounder and the neckline blunt. Stepping the length down at the sides and edges slims the silhouette and gives the cut a finished look. It also grows out more evenly: by week three it still looks like a haircut, not a fuzzy outline.", []),
            ("How to ask for it", "Say: \"A 3-2-1. Number 3 on top, 2 on the sides, 1 around the edges and neckline, blended.\" Add whether you want the neckline tapered (natural, softer) or squared off (sharper), and whether you want a line-up at the front. If you want more contrast, ask for a 4-2-1 or a 3-1-0.5.", []),
            ("Doing it at home", "The 3-2-1 is the easiest structured cut to do yourself. Cut the top with the #3 first, then the sides with the #2, stopping around the temple line, then use the #1 for the bottom inch and around the ears. Flick the clipper outward where the guards meet to soften the line. A quality trimmer handles the edges and neckline between cuts.", [9]),
            ("Who it suits", "Men who want low-maintenance, anyone in heat and humidity, and men with thinning hair on top, since short, even length makes thinning less noticeable than longer hair. It's less flattering on very round faces unless you keep a little more length on top: a 4-2-1 helps.", [16]),
        ],
        "faq": [
            ("What is the 3-2-1 rule for haircuts?", "A #3 clipper guard on top, a #2 on the sides and a #1 at the edges and neckline, which creates a short, graduated taper. Barbers also use it to describe proportion: longest on top, shorter on the sides, shortest at the neckline."),
            ("How long does a 3-2-1 haircut leave the hair?", "About 3/8 inch on top, 1/4 inch on the sides and 1/8 inch at the edges."),
            ("How often does a 3-2-1 need cutting?", "Every two to four weeks. Because it's so short, it loses its shape quickly once the sides grow past the top."),
        ],
    },
    {
        "path": "what-haircut-should-i-get.html",
        "title": "What Haircut Should I Get? A Men's Face Shape Guide · The Q Journal",
        "meta": "Not sure what haircut to get? Match it to your face shape (oval, round, square, long, heart) and your hair type, then use our checklist for asking your barber.",
        "crumb": "What haircut should I get",
        "eyebrow": "Haircuts · How to choose",
        "h1": "What haircut should I get? Start with your face shape.",
        "lede": "The right cut balances your face. Find your shape, check your hair type, then take this checklist to the chair.",
        "date": "2026-11-25",
        "tags": ["what haircut should I get", "men's haircut by face shape", "haircut for oval face men", "haircut for round face men", "haircut for square face men"],
        "intro": [
            "The goal of any haircut is balance. A cut adds height where your face needs length and keeps the sides tight where it needs width taken away. So the fastest way to choose is to find your face shape, then pick from the cuts that suit it.",
            "To check your shape, pull your hair back and look straight into a mirror. Compare the width of your forehead, cheekbones and jaw, and the length of your face from hairline to chin.",
        ],
        "sections": [
            ("Oval: almost anything works", "Slightly longer than wide, with a jaw a little narrower than the forehead. This is the most versatile shape: textured crops, side parts, quiffs and short buzzes all work. The only thing to avoid is heavy fringe that hides the forehead and makes the face look round.", [1]),
            ("Round: add height, keep the sides tight", "Width and length are similar and the jaw is soft. You want the opposite of round: height on top and short sides. A quiff, a pompadour or a textured top with a mid or high fade all work. Avoid blunt fringes and cuts that add width at the ears.", [13, 12]),
            ("Square: show off the jaw", "A strong, angular jawline and a broad forehead. Classic cuts suit you best: a side part, a crew cut, a short textured crop. Keep the sides clean and the top moderate so you don't make the face look boxy. A low taper keeps it sharp without hard lines.", [2]),
            ("Long or rectangular: don't add more height", "The face is clearly longer than it is wide. Skip tall quiffs and very short sides, which stretch it further. Keep some length on the sides, try a side part or a fringe swept to one side, and keep the top moderate.", []),
            ("Heart or diamond: balance a narrow chin", "A wider forehead or cheekbones with a narrower chin. Medium length with texture works, as does a side-swept fringe. A beard is a strong move here: it adds width at the jaw and evens out the shape.", [10]),
            ("Your hair type narrows it down", "Thick hair suits short sides and textured tops, because it gets bulky fast. Fine hair looks fuller cut shorter with texture, styled with powder rather than heavy pomade. Curly hair needs length left on top and a cut built around the curl, usually with a scissor cut rather than clippers. Thinning hair looks best kept short and even.", [7]),
            ("The checklist to take to the chair", "Bring two photos of the cut on someone with hair like yours. Say how you style it on a normal day and how long you go between cuts, because a cut built for weekly trims grows out differently from one built for six weeks. Tell them where you part your hair, and whether you want the neckline tapered or squared.", []),
        ],
        "faq": [
            ("How do I know my face shape?", "Pull your hair back and compare the width of your forehead, cheekbones and jaw with the length of your face. Similar width and length is round; longer than wide is oval or long; a strong, wide jaw is square."),
            ("What's the best haircut for a round face?", "Cuts with height on top and short sides, such as a quiff or a textured top with a mid fade, make a round face look longer."),
            ("What haircut suits every face shape?", "A short textured crop with a low taper is the safest all-rounder, because the length can be adjusted on top to add or reduce height."),
        ],
    },
    {
        "path": "fade-vs-taper-which-is-better.html",
        "title": "Fade vs Taper: The Difference and Which One to Ask For · The Q Journal",
        "meta": "Fade vs taper haircut: what's the difference, low vs mid vs high, skin fades and the low taper fade, how each grows out, and exactly what to say to your barber.",
        "crumb": "Fade vs taper",
        "eyebrow": "Haircuts · The difference",
        "h1": "Fade vs taper: the difference, and which one to ask for.",
        "lede": "Both get shorter toward the neck. A taper does it softly, a fade takes it down to the skin. Here's how to choose.",
        "date": "2026-11-25",
        "tags": ["fade vs taper", "low taper fade", "taper fade", "skin fade", "low fade", "mid fade", "high fade"],
        "intro": [
            "A taper and a fade both shorten the hair gradually as it moves down the sides and back. The difference is how far they go. A taper leaves some hair at the bottom and keeps the change subtle, usually only at the sideburns and neckline. A fade blends all the way down to very short or bare skin, with a more dramatic contrast.",
            "Quick answer: want clean but conservative, ask for a taper. Want sharp and modern, ask for a fade. Not sure, ask for a low taper fade, the in-between that's become one of the most requested cuts.",
        ],
        "sections": [
            ("The taper: subtle and grown-up", "A taper keeps most of the length on the sides and only shortens the edges: the neckline and around the ears. It looks tidy in a boardroom and grows out gracefully, so it can go four weeks between cuts. It suits longer styles, side parts and anyone who doesn't want visible scalp.", [2]),
            ("The fade: sharp contrast", "A fade takes the sides down to very short or skin, blending upward into the longer top. The higher it starts, the bolder it looks. It's crisp and modern but shows growth fast, so most fades need a touch-up every two to three weeks to stay sharp.", [1]),
            ("Low, mid and high", "Height is where the shortest part stops. A low fade stays just above the ear and neckline and is the most versatile. A mid fade starts around the temple and suits most textured tops. A high fade climbs toward the crown for maximum contrast, and works best with short or very structured tops.", []),
            ("Skin, bald and drop fades", "A skin or bald fade goes down to bare skin at the bottom. A drop fade curves down behind the ear toward the nape, following the head's shape. A burst fade fans out around the ear and leaves length at the back, which is the cut often paired with a modern mullet.", []),
            ("The low taper fade", "It's exactly what it sounds like: a fade kept low and tight to the edges like a taper. You get the clean, sharp outline of a fade around the ears and neckline, with the weight of a taper on the sides. Ask for it with a textured crop or a longer top.", [13]),
            ("What to say in the chair", "Name the type and height, then the shortest length: \"Low taper, finish at a 1 at the neckline,\" or \"Mid skin fade, blend into a 3, scissor on top.\" Say whether you want a natural or squared neckline, and how long you usually go between cuts, so it's built to grow out well.", [9]),
        ],
        "faq": [
            ("What's the difference between a fade and a taper?", "A taper shortens the hair subtly at the neckline and sideburns and leaves some length. A fade blends down to very short or bare skin, with more contrast."),
            ("Which lasts longer, a fade or a taper?", "A taper. It grows out more gradually and can usually go about four weeks, while a fade looks best refreshed every two to three weeks."),
            ("Is a low taper fade a fade or a taper?", "It's a hybrid: a fade's clean edges kept low and tight around the ears and neckline, with the sides left fuller like a taper."),
        ],
    },
    {
        "path": "toupee-hair-system-guide.html",
        "title": "Toupees & Hair Systems for Men: How They Work (2026 Guide) · The Q Journal",
        "meta": "A straight guide to men's hair systems and toupees: base types (lace, skin, mono), how they're attached, upkeep, how long they last, and the alternatives to consider first.",
        "crumb": "Hair systems guide",
        "eyebrow": "Hair loss · Explained",
        "h1": "Toupees and hair systems for men: how they actually work.",
        "lede": "The modern toupee is called a hair system, and a good one is undetectable. Here's how they're made, worn and maintained.",
        "date": "2026-11-25",
        "tags": ["toupee for men", "men's hair system", "hair replacement for men", "non-surgical hair replacement", "lace hair system"],
        "intro": [
            "The word toupee still brings to mind a hairpiece that sits on top of the head and fools no one. Modern hair systems are different. They're made from real or high-grade synthetic hair knotted into a thin base that bonds to the scalp, then cut and blended into your own hair by a stylist. Done well, they're invisible, even up close.",
            "They're a non-surgical option for men with advanced thinning or a bald area. They don't regrow anything, and they need regular upkeep, so it helps to know what you're signing up for.",
        ],
        "sections": [
            ("The three main base types", "The base is the thin layer the hair is attached to, and it decides how natural the system looks and how long it lasts. Lace bases are breathable and give the most natural hairline, but they're delicate. Skin, or poly, bases look like scalp and are easiest to clean and attach, but are warmer to wear. Mono bases are a sturdier mesh in between. Many systems combine them: lace at the front for the hairline, poly at the back for durability.", []),
            ("How they're attached", "Most are worn with tape or a liquid adhesive, applied to a cleanly shaved area of the scalp. Tape is easier to remove and reapply; adhesive holds longer. Clip-in systems exist for partial thinning and can be taken off daily. Attachment is usually redone every two to four weeks, when the system is removed, cleaned and the scalp is shaved again.", []),
            ("How long a system lasts", "It depends on the base and how it's treated. Ultra-thin, most natural-looking bases may last a few months; sturdier bases can last much longer. Sun, salt water, chlorine and heat all shorten the life of the hair, which matters in Florida. Most wearers keep a second system so one can be serviced while the other is worn.", [7]),
            ("Getting one that looks real", "The hairline, density and color matter most. Ask for slightly lower density than you think you want: real hair isn't uniformly thick, and an overly full system is what gives it away. Have it cut in by someone experienced with hair systems so it blends with the hair at your sides and back, and keep your own hair cut on the same schedule.", []),
            ("Alternatives to consider first", "If you're thinning rather than bald, there are simpler options. A shorter cut, such as a 3-2-1 or a buzz with a clean line-up, makes thinning far less noticeable. Hair-building fibers fill in thin areas instantly and wash out. For treatment, talk to a dermatologist, who can explain the options and whether they suit you.", [15, 6]),
        ],
        "faq": [
            ("Do hair systems look real?", "A well-made system with a lace front, realistic density and a proper cut-in is very hard to spot. Overly thick density and a poor color match are what make them noticeable."),
            ("Can you swim with a hair system?", "Yes, with the right adhesive, but salt water and chlorine wear the hair faster. Rinse it with fresh water afterward."),
            ("How often does a hair system need maintenance?", "Most are removed, cleaned and reattached every two to four weeks, and replaced every few months to a year depending on the base."),
        ],
    },
    {
        "path": "haircuts-for-receding-hairline.html",
        "title": "Best Haircuts for a Receding Hairline (and What to Avoid) · The Q Journal",
        "meta": "The best men's haircuts for a receding hairline: the buzz cut, crew cut, textured crop and short fade, plus the styles that make thinning more obvious and the products that help.",
        "crumb": "Receding hairline haircuts",
        "eyebrow": "Haircuts · Thinning hair",
        "h1": "The best haircuts for a receding hairline, and what to avoid.",
        "lede": "Fighting a receding hairline with length usually makes it more obvious. Going shorter and adding texture works better.",
        "date": "2026-11-25",
        "tags": ["haircuts for receding hairline", "receding hairline haircut", "buzz cut receding hairline", "fade for balding men", "thinning hair men"],
        "intro": [
            "When the hairline starts moving back, the instinct is to grow the top longer and cover it. That almost always backfires. Long hair separates and shows the scalp underneath, and a swept-over front draws the eye to exactly what you're hiding.",
            "The cuts that work do the opposite. They reduce the contrast between the thinner areas and the rest of the head, so the hairline reads as a style choice rather than something to notice.",
        ],
        "sections": [
            ("The buzz cut", "The most confident option. When everything is the same short length, the hairline stops standing out. Pair it with a sharp line-up and some stubble and it reads deliberate. A 3-2-1 gives a buzz more shape than one guard all over.", [9]),
            ("The crew cut", "A little more length at the front than the back, short tapered sides. It keeps a hint of styling without enough length to separate. Push the front slightly up and forward with a matte product.", [1]),
            ("The textured crop with a short fringe", "A short, choppy fringe brought forward covers a receding temple naturally, and texture hides thinning better than smooth, flat hair. Keep the fringe short and messy, not a blunt line.", [13]),
            ("A short fade on the sides", "Tight sides make the top look fuller by contrast. A low or mid fade with a short textured top is one of the most flattering cuts for thinning hair.", []),
            ("What to avoid", "Comb-overs, long slicked-back styles, which open up the temples, and heavy, shiny pomades that clump hair together and show scalp. Avoid letting it grow long between cuts: thinning hair looks thinnest when it's overdue.", []),
            ("Products that help", "Matte products and styling powder add grip and fullness without weight. Hair-building fibers fill in thin spots for the day. A gentle, strengthening shampoo keeps the scalp clean. If you want to treat the thinning itself, talk to a dermatologist about the options.", [15, 7, 6]),
        ],
        "faq": [
            ("Should I shave my head if I have a receding hairline?", "Not necessarily. A short buzz or crew cut often looks better than a full shave, but a clean shave suits men with a well-shaped head and a confident style."),
            ("Do fades work for balding men?", "Yes. A low or mid fade with a short textured top makes the top look fuller by contrast and draws attention away from the temples."),
            ("Does long hair hide a receding hairline?", "Usually not. Longer hair separates and shows the scalp, and swept-over styles draw attention to the hairline."),
        ],
    },
]
BLOG_POSTS = NEW_POSTS + BLOG_POSTS

# Cards for the homepage and journal index, newest first.
ARTICLES = [{"path": p["path"], "kicker": p["eyebrow"].split(" · ")[0], "title": p["h1"], "lede": p["lede"], "date": p["date"]} for p in BLOG_POSTS] + [
    {"path": "grooming-guide.html", "kicker": "Grooming guide", "title": "Eight grooming habits worth keeping.",
     "lede": "Fades, styling products, gray blending, razor bumps and beard care in Florida humidity.", "date": None},
]

def post_cards(items, lead=True):
    out = []
    for i, a in enumerate(items):
        meta = f' · {nice_date(a["date"])}' if a["date"] else ""
        cls = "post lead" if lead and i == 0 else "post"
        out.append(f'<a class="{cls}" href="{a["path"]}"><span class="k">{esc(a["kicker"])}{meta}</span><h3>{esc(a["title"])}</h3>'
                   f'<p>{esc(a["lede"])}</p><span class="more">Read the article {ARR}</span></a>')
    return f'<div class="posts">{"".join(out)}</div>'

def blog_cards(slots):
    by_slot = {p["slot"]: p for p in AFFILIATE}
    return '<div class="affs">' + "".join(aff_card(by_slot[s]) for s in slots if s in by_slot) + "</div>"

def blog_post(p):
    secs = "".join(f'<h2 id="s-{i}">{esc(h)}</h2><p>{esc(t)}</p>{blog_cards(slots)}' for i, (h, t, slots) in enumerate(p["sections"], 1))
    faq_html = "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in p["faq"])
    toc = "".join(f'<p style="margin-top:10px"><a class="link" href="#s-{i}">{esc(h)}</a></p>' for i, (h, _, _) in enumerate(p["sections"], 1))
    words = len(" ".join(p["intro"] + [t for _, t, _ in p["sections"]]).split())
    article = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["h1"], "description": p["meta"],
               "keywords": ", ".join(p.get("tags", [])), "wordCount": words, "articleSection": p["eyebrow"].split(" · ")[0],
               "datePublished": p["date"], "dateModified": TODAY, "mainEntityOfPage": url(p["path"]),
               "image": B["site"] + IMG_SHARE, "author": author(),
               "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"}
    related = "".join(f'<a href="{h}">{t}</a>' for h, t in SEO_LINKS if h != p["path"])
    return f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">{esc(p['eyebrow'])}</p><h1>{esc(p['h1'])}</h1>
<p class="lede">{esc(p['lede'])}</p>
{byline(p['date'])}</div></section>
<section class="sec"><div class="wrap split"><div class="sticky"><div class="side"><p class="eyebrow">In this guide</p>{toc}</div></div>
<div class="prose">{"".join(f"<p>{esc(x)}</p>" for x in p['intro'])}
<p class="disclose muted">{AMZ_DISCLOSE} Links open Amazon, where current prices and availability are shown.</p>
{secs}
<h2>Questions</h2><div class="faq">{faq_html}</div>
<h2>Keep reading</h2><div class="related">{related}</div>
</div></div></section>
{faq_schema(p['faq'])}
<script type="application/ld+json">{json.dumps(article, ensure_ascii=False)}</script>
{journal_cta()}"""

blog_index = f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">The Q Journal</p><h1>Notes on men's grooming.</h1>
<p class="lede">Grooming advice, product picks and seasonal guides for men, written for Florida sun and humidity.</p>
{byline()}</div></section>
<section class="sec"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">All articles</p><h2>Latest from the journal.</h2></div><p>New guides are added through the year.</p></div>
{post_cards(ARTICLES)}
</div></section>
{shop_section()}"""

# ---------- Home ----------
home = f"""
<section class="hero2">
<figure class="h2-media"><div class="h2-frame">
{pic(IMG_HERO, "Man with a swept-back men's haircut, natural silver kept, and a sculpted salt-and-pepper beard", 900, 1110, lazy=False)}
<span class="h2-tag t1"><i></i>01 · Swept-back cut, natural silver kept</span>
<span class="h2-tag t2"><i></i>02 · Beard sculpted &amp; lined</span>
<span class="h2-issue">The Q Journal · Issue 2026</span>
</div></figure>
<div class="h2-copy"><div class="h2-inner">
<h1><span class="eyebrow h1-eyebrow">The Q Journal · Men's grooming</span><span class="l"><span>Grooming,</span></span><span class="l"><span>written down</span></span><span class="l"><span><em>properly.</em></span></span></h1>
<p class="lede">Practical advice on haircuts, beards, skin and styling, plus product picks that earn their place on the shelf.</p>
<div class="acts"><a class="btn" href="{ARTICLES[0]['path']}">Read the latest guide {ARR}</a><a class="btn btn-line" href="blog.html">Browse the journal</a></div>
</div></div>
</section>
{ticker()}
<section class="sec" id="latest"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">Latest articles</p><h2>From the journal.</h2></div>
<p>Seasonal guides and practical grooming advice for men.</p></div>
{post_cards(ARTICLES)}
<div class="acts"><a class="btn" href="blog.html">All articles {ARR}</a></div>
</div></section>
<section class="sec stone" id="guide"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">The grooming guide</p><h2>Eight habits, two minutes each.</h2></div>
<p>The short version of everything in the guide. Tap any one to read it.</p></div>
<div class="tips">{"".join(f'<a href="grooming-guide.html#tip-{i}"><span>{i:02d}</span><b>{t}</b></a>' for i, (t, _) in enumerate(GUIDE, 1))}</div>
</div></section>
{shop_section()}
<section class="sec"><div class="wrap split"><div><p class="eyebrow">About the journal</p><h2>Useful, not precious.</h2></div>
<div class="prose"><p>The Q Journal covers the parts of men's grooming that actually make a difference day to day: how a cut grows out, which product suits which hair, and what Florida sun and humidity do to hair, beards and skin.</p>
<p><a class="link" href="about.html">More about The Q Journal</a></p></div></div></section>
"""

# ---------- Product picks ----------
shop = f"""
<section class="page-hero"><div class="wrap"><p class="eyebrow">Product picks</p><h1>Grooming products worth the shelf space.</h1>
<p class="lede">Styling, beard, hair-care, skin, fragrance and grooming tools picked by The Q Journal.</p>
<div class="acts"><a class="btn" href="#picks">See the picks {ARR}</a><a class="btn btn-line" href="mens-grooming-gift-guide.html">Read the gift guide</a></div></div></section>
{shop_section("Shop by need", "Start with what you need.")}
<section class="sec" id="picks"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">The Q Journal picks</p><h2>What to use day to day</h2></div>
<p>Pomades, beard care, scalp care, skin care, fragrance and a trimmer for upkeep between haircuts.</p></div>
<p class="disclose muted">{AMZ_DISCLOSE} Links open Amazon, where current prices and availability are shown.</p>
{affiliate_grid()}
</div></section>
{journal_cta("Not sure which product suits you? The grooming guide and gift guide explain what each one does.")}
"""

# ---------- About ----------
about = f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">About</p><h1>About The Q Journal.</h1>
<p class="lede">The Q Journal is a men's grooming journal: practical advice on haircuts, beards, skin and styling, and product picks for keeping it all in shape.</p>
<div class="acts"><a class="btn" href="blog.html">Read the journal {ARR}</a><a class="btn btn-line" href="shop.html">See the product picks</a></div></div></section>
<section class="sec"><div class="wrap split"><div><p class="eyebrow">What we cover</p><h2>The grooming details that matter.</h2></div>
<div class="prose"><p><strong>Hair.</strong> How cuts grow out, when a fade needs a refresh, how to ask for the haircut you want, and how to keep gray looking natural.</p>
<p><strong>Beards and skin.</strong> Beard care that works in humidity, how to stop razor bumps, and the sun protection most men skip.</p>
<p><strong>Products.</strong> Pomades, clays, oils, balms, scalp care and tools, explained by what they do rather than how they're marketed.</p>
<p><strong>Seasonal guides.</strong> Gift guides and seasonal routines, starting with the <a class="link" href="mens-grooming-gift-guide.html">2026 grooming gift guide</a>.</p>
</div></div></section>
<section class="sec stone"><div class="wrap split"><div><p class="eyebrow">How we work</p><h2>Editorial standards.</h2></div>
<div class="prose"><p><strong>One byline.</strong> Every article is published under a single editorial byline: {BYLINE}.</p>
<p><strong>Label facts only.</strong> Product descriptions stick to what's on the label and how a product is used. We don't publish prices, star ratings or health claims, because those change and vary from person to person.</p>
<p><strong>Affiliate links, disclosed.</strong> {AMZ_DISCLOSE} Product links are marked and open Amazon, where current prices and availability are shown.</p>
<p><strong>Corrections and suggestions.</strong> Spotted something out of date, or want a topic covered? Write to <a class="link" href="mailto:{B['email']}">{B['email']}</a>.</p>
</div></div></section>
{journal_cta()}"""

PAGES = [  # (path, <title>, meta description, body, breadcrumb label, og:type)
    ("index.html", "The Q Journal: Men's Haircuts, Beard Care & Grooming Product Picks", "Men's grooming, explained: which haircut suits your face, fade vs taper, pomade vs clay, beard care and the products worth buying. Practical guides from The Q Journal.", home, "", "website"),
    ("blog.html", "Men's Grooming Articles & Haircut Guides · The Q Journal", "Every guide from The Q Journal: men's haircuts by face shape, fades and tapers, hair products, beard care, thinning hair and seasonal gift guides.", blog_index, "Journal", "website"),
    ("grooming-guide.html", "Men's Grooming Tips: 8 Habits Worth Keeping · The Q Journal", GUIDE_META, guide, "Grooming guide", "article"),
    ("shop.html", "Best Men's Grooming Products: Pomade, Beard Oil & More · The Q Journal", "The Q Journal's picks for the best men's grooming products: pomade, clay, styling powder, beard oil and balm, scalp care, SPF moisturizer, fragrance and trimmers.", shop, "Product picks", "website"),
    ("about.html", "About The Q Journal · A Men's Grooming Journal", "About The Q Journal: what the men's grooming journal covers, how product picks are chosen and how affiliate links are disclosed.", about, "About", "website"),
] + [(p["path"], p["title"], p["meta"], blog_post(p), p["crumb"], "article") for p in BLOG_POSTS]

# IndexNow key (Bing, Yandex, Seznam...). Public by design: the key file is served at /<key>.txt.
INDEXNOW_KEY = "7f3c9a1e5b2d4c8e9a6f0b1d2e3c4a5b"

AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot",
           "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "Bingbot", "DuckAssistBot", "meta-externalagent", "Amazonbot"]

def llms_txt():
    pages = "\n".join(f"- [{label or 'Home'}]({url(p)}): {d}" for p, _, d, _, label, _ in PAGES)
    arts = "\n".join(f"- [{a['title']}]({url(a['path'])})" + (f" (published {a['date']})" if a["date"] else "") for a in ARTICLES)
    return f"""# {B['name']}

> {B['tagline']} at {B['site']}/: practical advice on haircuts, beards, skin and styling, seasonal guides, and editorial product picks. Articles are published under the "{BYLINE}" byline.

## Key facts
- Name: {B['name']}
- Type: men's grooming journal (editorial site)
- Byline: {BYLINE}
- Website: {B['site']}/
- Journal index: {B['site']}/blog
- RSS: {B['site']}/feed.xml
- Editorial contact: {B['email']}
- Product picks: {len(AFFILIATE)} grooming products linked to Amazon. Disclosure: "{AMZ_DISCLOSE}"

## Articles
{arts}

## Pages
{pages}
"""

def feed_xml():
    items = "".join(
        f"<item><title>{esc(a['title'])}</title><link>{url(a['path'])}</link><guid>{url(a['path'])}</guid>"
        f"<description>{esc(a['lede'])}</description>"
        + (f"<pubDate>{datetime.date.fromisoformat(a['date']).strftime('%a, %d %b %Y')} 12:00:00 +0000</pubDate>" if a["date"] else "")
        + "</item>" for a in ARTICLES)
    return (f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{B["name"]}</title>'
            f'<link>{B["site"]}/</link><description>{B["tagline"]}</description><language>en-us</language>{items}</channel></rss>')

if __name__ == "__main__":
    os.makedirs("dist", exist_ok=True)
    for path, title, desc, body, crumb, og_type in PAGES:
        open(f"dist/{path}", "w").write(page(path, title, desc, body, crumb, og_type))
    for slug in RETIRED:   # retired pages must not exist as files, or Netlify serves them instead of the redirect
        if os.path.exists(f"dist/{slug}.html"):
            os.remove(f"dist/{slug}.html")
    urls = "".join(f"<url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod></url>" for p, *_ in PAGES)
    open("dist/sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open("dist/feed.xml", "w").write(feed_xml())
    bots = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in AI_BOTS)
    open("dist/robots.txt", "w").write(f"# Search engines and AI assistants are welcome to read and cite this site.\n{bots}User-agent: *\nAllow: /\n\nSitemap: {B['site']}/sitemap.xml\n")
    open("dist/llms.txt", "w").write(llms_txt())
    open(f"dist/{INDEXNOW_KEY}.txt", "w").write(INDEXNOW_KEY)
    open("dist/_redirects", "w").write(redirects())
    open("dist/_headers", "w").write(
        "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n"
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
        "/llms.txt\n  Content-Type: text/plain; charset=utf-8\n"
        "/feed.xml\n  Content-Type: application/rss+xml; charset=utf-8\n")
    print("built", len(PAGES), "pages")
