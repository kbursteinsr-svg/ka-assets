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
    ("blog.html", "The Q Journal"), ("mens-grooming-gift-guide.html", "Grooming Gift Guide 2026"),
    ("grooming-guide.html", "The Grooming Guide"), ("shop.html", "Product Picks"), ("about.html", "About the Journal"),
]

# Former salon service and area pages -> closest journal page (302 so the change stays reversible).
RETIRED = {
    "mens-hair-salon-sarasota": "/blog", "barber-sarasota": "/blog", "mens-haircut-sarasota": "/blog",
    "executive-haircut-sarasota": "/blog", "skin-fade-sarasota": "/grooming-guide", "mens-hair-color-sarasota": "/grooming-guide",
    "mens-facial-sarasota": "/grooming-guide", "kids-haircut-sarasota": "/blog", "mens-grooming-sarasota": "/grooming-guide",
    "mens-haircut-lido-key": "/blog", "mens-haircut-lakewood-ranch": "/blog", "mens-haircut-siesta-key": "/blog",
    "mens-haircut-longboat-key": "/blog",
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
    "/downtown-sarasota-barbershop": "/mens-haircut-sarasota", "/barbershop-sarasota": "/barber-sarasota",
    "/gallery": "/about", "/contact": "/about", "/how-to-tell-if-hair-stylist-is-good": "/about",
    "/mens-hair-salon": "/mens-hair-salon-sarasota", "/services": "/",
    "/mens-haircuts-sarasota": "/mens-haircut-sarasota", "/best-mens-haircut-sarasota": "/mens-haircut-sarasota",
    "/mens-scissor-cut-sarasota": "/mens-haircut-sarasota", "/mens-mullet-haircut-sarasota": "/mens-haircut-sarasota",
    "/how-much-should-mens-haircut-cost-sarasota": "/mens-haircut-sarasota", "/mens-haircut-venice": "/mens-haircut-sarasota",
    "/executive-haircuts-sarasota": "/executive-haircut-sarasota",
    "/mens-fade-haircut-sarasota": "/skin-fade-sarasota", "/fade-haircuts-sarasota": "/skin-fade-sarasota",
    "/fade-vs-taper-which-is-better": "/skin-fade-sarasota", "/styles/low-taper": "/skin-fade-sarasota",
    "/beard-grooming-sarasota": "/mens-grooming-sarasota", "/beard-trim-sarasota": "/mens-grooming-sarasota",
    "/hot-towel-shave-sarasota": "/mens-grooming-sarasota", "/scalp-treatments-men-sarasota": "/mens-grooming-sarasota",
    "/luxury-mens-grooming-sarasota": "/mens-grooming-sarasota", "/mens-grooming-salon-downtown-sarasota": "/mens-grooming-sarasota",
    "/mens-spa-sarasota": "/mens-facial-sarasota",
    "/journal": "/blog","/what-haircut-should-i-get": "/grooming-guide",
    "/what-haircut-do-girls-like": "/grooming-guide", "/3-2-1-rule-mens-haircuts": "/grooming-guide",
}

def redirects():
    """Legacy URLs (301) resolved through RETIRED, retired pages and /book (302, reversible)."""
    def final(dst): return RETIRED.get(dst.lstrip("/"), dst)
    lines = [f"{src} {final(dst)} {302 if dst.lstrip('/') in RETIRED else 301}" for src, dst in LEGACY_REDIRECTS.items()]
    for slug, dst in RETIRED.items():
        lines += [f"/{slug} {dst} 302", f"/{slug}.html {dst} 302"]
    lines.append("/book /blog 302")
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
    ("How to tell when your fade needs a refresh", "Run your hand up the side of your head. If you can feel a clear line where short meets long, the blend has grown out. For most men that's around day 14 to 21."),
    ("The two-minute styling routine", "Towel-dry until damp, work a pea-sized amount of product between your palms until it disappears, then apply back to front. Finish with fingers, not a comb, for natural texture."),
    ("Pomade, clay or cream?", "Pomade gives shine and slick control. Clay gives matte texture and strong hold for thicker hair. Cream gives light, natural hold for finer hair. If you're not sure, ask whoever cuts your hair what they finished it with."),
    ("Why gray blending beats box dye", "Box dye covers everything in one flat shade and grows out with a hard line. Blending keeps some gray, so regrowth is soft and the result looks like your own hair."),
    ("Protect your color from the Florida sun", "Use a color-safe shampoo, rinse with cool water, and wear a hat on the boat or beach. UV and chlorine are what turn blended color brassy."),
    ("Stop razor bumps", "Exfoliate twice a week, shave with the grain after a warm shower, and finish with a fragrance-free moisturizer. Give irritated areas a few days off the razor before shaving them again."),
    ("Beard care in humidity", "Wash your beard two or three times a week, not daily, and use a few drops of beard oil on damp hair to stop frizz and itch."),
    ("How to ask for the haircut you want", "Bring a photo, say how you style it day to day, and tell your stylist how long you go between cuts. That last detail changes how a cut should be built."),
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
        "path": "mens-grooming-gift-guide.html",
        "title": "Grooming Gifts for Men: The 2026 Gift Guide · The Q Journal",
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
    article = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["meta"],
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
    ("index.html", "The Q Journal · Men's Grooming Journal: Haircuts, Beards, Skin & Product Picks", "The Q Journal is a men's grooming journal with practical advice on haircuts, beards, skin and styling, seasonal gift guides and editorial product picks.", home, "", "website"),
    ("blog.html", "The Q Journal · All Men's Grooming Articles", "Every article from The Q Journal: men's grooming advice, seasonal guides and product picks for haircuts, beards, skin and styling.", blog_index, "Journal", "website"),
    ("grooming-guide.html", "Men's Grooming Guide: Eight Habits Worth Keeping · The Q Journal", GUIDE_META, guide, "Grooming guide", "article"),
    ("shop.html", "Product Picks · Men's Grooming Products · The Q Journal", "The Q Journal's men's grooming product picks: pomade, clay, beard oil, scalp care, SPF moisturizer, fragrance and trimmers, with affiliate links disclosed.", shop, "Product picks", "website"),
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
