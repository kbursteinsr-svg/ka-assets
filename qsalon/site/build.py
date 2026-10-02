#!/usr/bin/env python3
"""Builds The Q Salon for Men static site.
Edit BUSINESS / SERVICES / PRODUCTS below, then run: python3 build.py
Outputs full HTML pages in ./dist (for Netlify) and ./preview (artifact preview)."""
import json, os, re

BUSINESS = {
    "name": "The Q Salon for Men",
    "street": "1415 1st St", "city": "Sarasota", "state": "FL", "zip": "34236",
    "phone": "(941) 340-2389", "phone_e164": "+19413402389",
    "site": "https://www.theqsalonsrq.com",
    "book": "https://getsqr.co/susy-r-6",
    # Swap for the Squire retail/shop link once it's set up:
    "shop": "https://getsqr.co/susy-r-6",
    "hours": "Mon–Fri · 9 AM – 2 PM",
    "maps": "https://www.google.com/maps/search/?api=1&query=1415+1st+St+Sarasota+FL+34236",
}
B = BUSINESS
ADDR = f"{B['street']}, {B['city']}, {B['state']} {B['zip']}"

SERVICES = [
    ("Classic Haircut", "45 min", 60, "Scissor and clipper cut, styled to finish."),
    ("Executive Haircut", "1 hr", 80, "Our signature cut with extra time and detail work."),
    ("Skin Fade", "1 hr", 80, "Seamless fade down to the skin, sharp lines and blend."),
    ("Natural Look Color & Style", "1 hr 15 min", 130, "Gray blending that looks like you, not like dye."),
    ("Gentleman's Facial", "45 min", 75, "Cleanse, exfoliate and hydrate. Leave refreshed."),
    ("Kid's Haircut (under 12)", "30 min", 30, "Clean, comfortable cuts for young gentlemen."),
]

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

# Shop categories. Add real products (name, price, link, photo) as they're stocked.
PRODUCTS = [
    ("Styling", "Pomades, clays & creams", "Hold from natural to sharp. The same products Susy finishes with in the chair.", SVG_TIN, "shop"),
    ("Beard Care", "Oils & balms", "Soften, tame the itch and keep it groomed between visits.", SVG_DROP, "shop"),
    ("Hair & Scalp", "Shampoo & conditioner", "Daily care for men's hair, including color-safe formulas after gray blending.", SVG_PUMP, "shop"),
    ("Gift Cards", "From $50", "Good for any service or product. The gift he'll actually use.", SVG_GIFT, "book"),
]

NAV = [("index.html", "Home"), ("index.html#services", "Services"), ("shop.html", "Shop"),
       ("mens-haircut-sarasota.html", "Haircuts"), ("skin-fade-sarasota.html", "Fades"), ("mens-hair-color-sarasota.html", "Gray Blending")]

# Affiliate products ("Susy's Picks"). Add one dict per product:
# {"name": "...", "brand": "...", "price": "$24", "img": "https://... or assets/...", "url": "https://affiliate-link", "note": "Why Susy likes it"}
AFFILIATE = []

# Every SEO page, linked from the footer of every page (internal linking for Google).
SEO_LINKS = [
    ("barber-sarasota.html", "Barber in Sarasota"), ("mens-haircut-sarasota.html", "Men's Haircut Sarasota"),
    ("executive-haircut-sarasota.html", "Executive Haircut"), ("skin-fade-sarasota.html", "Skin Fade Sarasota"),
    ("mens-hair-color-sarasota.html", "Men's Gray Blending"), ("mens-facial-sarasota.html", "Men's Facial Sarasota"),
    ("kids-haircut-sarasota.html", "Kids' Haircuts Sarasota"), ("mens-grooming-sarasota.html", "Men's Grooming Sarasota"),
    ("mens-haircut-lakewood-ranch.html", "Lakewood Ranch"), ("mens-haircut-siesta-key.html", "Siesta Key"),
    ("mens-haircut-longboat-key.html", "Longboat Key"), ("grooming-guide.html", "Grooming Guide"),
]

def schema():
    return json.dumps({
        "@context": "https://schema.org", "@type": "HairSalon", "name": B["name"], "image": B["site"] + "/assets/susy.jpg",
        "url": B["site"], "telephone": B["phone_e164"], "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": B["street"], "addressLocality": B["city"],
                    "addressRegion": B["state"], "postalCode": B["zip"], "addressCountry": "US"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "14:00"}],
        "makesOffer": [{"@type": "Offer", "price": str(p), "priceCurrency": "USD",
                        "itemOffered": {"@type": "Service", "name": n}} for n, _, p, _ in SERVICES],
    }, indent=1)

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
a:focus-visible,.btn:focus-visible{outline:2px solid var(--brass);outline-offset:3px}
.link{color:var(--brass);text-underline-offset:4px;font-weight:500}
/* header */
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:rgba(243,240,234,.88);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.top-in{display:flex;align-items:center;gap:22px;padding-block:12px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;margin-right:auto}
.mono{display:grid;place-items:center;width:40px;height:40px;border-radius:50%;background:var(--navy);color:var(--brass-l);font:400 1.35rem/1 var(--display)}
.brand-t{font:400 1.05rem/1.05 var(--display);letter-spacing:.06em;text-transform:uppercase}.brand-t small{display:block;font:500 .62rem var(--mono);letter-spacing:.24em;color:var(--brass);margin-top:3px}
.nav{display:flex;gap:20px;font-size:.92rem}.nav a{text-decoration:none;color:var(--muted);transition:color .2s}.nav a:hover,.nav a[aria-current]{color:var(--ink)}
@media(max-width:900px){.nav{display:none}}
/* hero */
.hero{padding-block:clamp(40px,7vw,84px) clamp(48px,7vw,88px);overflow:hidden}
.hero-in{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(32px,6vw,80px);align-items:center}
.hero-in>*{min-width:0}
.hero h1 .l{display:block;overflow:hidden}.hero h1 .l>span{display:inline-block;animation:rise .9s cubic-bezier(.2,.7,.2,1) both}
.hero h1 .l:nth-child(2)>span{animation-delay:.08s}.hero h1 .l:nth-child(3)>span{animation-delay:.16s}
.hero h1 em{font-style:normal;color:var(--brass)}
.lede{font-size:1.15rem;color:var(--muted);max-width:46ch;margin-top:24px}
.acts{display:flex;flex-wrap:wrap;gap:12px;margin-top:32px}
.stats{display:flex;flex-wrap:wrap;gap:28px 40px;margin-top:40px;padding-top:28px;border-top:1px solid var(--line)}
.stats b{display:block;font:400 1.7rem/1 var(--display);color:var(--navy)}.stats span{font:500 .7rem var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.portrait{position:relative;max-width:460px;justify-self:end;width:100%}
.portrait::before{content:"";position:absolute;inset:18px -18px -18px 18px;border:1px solid var(--brass);border-radius:220px 220px 6px 6px}
.portrait .frame{position:relative;border-radius:220px 220px 6px 6px;overflow:hidden;aspect-ratio:4/5;background:var(--stone);animation:fade 1.1s ease both .1s}
.portrait img{width:100%;height:100%;object-fit:cover;object-position:50% 18%;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}
.portrait:hover img{transform:scale(1.04)}
.badge{position:absolute;left:-24px;bottom:36px;background:var(--navy);color:#fff;padding:16px 20px;border-radius:6px;box-shadow:0 18px 40px -18px rgba(20,32,46,.7);animation:rise 1s cubic-bezier(.2,.7,.2,1) both .35s}
.badge b{display:block;font:400 1.15rem var(--display)}.badge span{font:500 .66rem var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--brass-l)}
@media(max-width:860px){.hero-in{grid-template-columns:1fr}.portrait{justify-self:center;max-width:380px}.badge{left:0}}
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
.h2-by{display:inline-flex;align-items:center;gap:12px;margin-top:28px;text-decoration:none;padding:6px 18px 6px 6px;border:1px solid var(--line);border-radius:999px;background:#fff;transition:border-color .25s,transform .25s}
.h2-by:hover{border-color:var(--brass);transform:translateY(-2px)}
.h2-by img{width:44px;height:44px;border-radius:50%;object-fit:cover;object-position:50% 20%}
.h2-by b{display:block;font:400 1rem/1.1 var(--display);color:var(--navy)}.h2-by small{font:500 .64rem var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.hero2 .stats{margin-top:28px;padding-top:22px;gap:20px 32px;flex-wrap:nowrap}
.hero2 .stats b{font-size:1.45rem;margin-bottom:6px}.hero2 .stats span{font-size:.62rem;letter-spacing:.1em;white-space:nowrap}
.hero2 h1{font-size:clamp(2.6rem,4.9vw,4.4rem)}
.hero2 .lede{margin-top:20px}.hero2 .acts{margin-top:26px}
@media(max-width:520px){.hero2 .stats{flex-wrap:wrap}}
@keyframes h2zoom{from{transform:scale(1.08)}to{transform:none}}
@keyframes tagin{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@media(max-width:860px){.hero2{grid-template-columns:1fr;min-height:0}.h2-frame{max-width:440px}.h2-tag{font-size:.6rem;padding:8px 10px}.h2-tag.t1{top:9%;right:5%}.h2-tag.t2{bottom:10%;left:5%}.h2-issue{display:none}.h2-media::before{display:none}}
@keyframes rise{from{transform:translateY(105%)}to{transform:none}}
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
/* menu */
.menu{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 56px}@media(max-width:760px){.menu{grid-template-columns:1fr}}
.item{display:grid;grid-template-columns:1fr auto;gap:4px 16px;padding-block:22px;border-top:1px solid var(--line)}
.item h3{display:flex;align-items:baseline;gap:12px;min-width:0}.item h3::after{content:"";flex:1;border-bottom:1px dotted var(--line);transform:translateY(-5px)}
.item .price{font:500 1.2rem var(--mono);color:var(--navy);font-variant-numeric:tabular-nums}
.item p{grid-column:1/-1;color:var(--muted);font-size:.95rem}.item .dur{font:500 .72rem var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--brass)}
.menu-foot{display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;align-items:center;margin-top:36px;padding-top:28px;border-top:1px solid var(--line)}
/* shop */
.products{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
@media(max-width:980px){.products{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:520px){.products{grid-template-columns:1fr}}
.prod{background:var(--navy-2);border:1px solid var(--line-d);border-radius:10px;overflow:hidden;display:flex;flex-direction:column;transition:transform .35s cubic-bezier(.2,.7,.2,1),border-color .35s,box-shadow .35s}
.prod:hover{transform:translateY(-6px);border-color:var(--brass);box-shadow:0 24px 50px -28px rgba(0,0,0,.8)}
.prod .art{background:radial-gradient(circle at 50% 60%,#2c3d52 0,#1c2a3b 70%);aspect-ratio:5/4;display:grid;place-items:center;padding:18px}
.prod .art svg{width:100%;max-width:220px;height:auto;transition:transform .5s cubic-bezier(.2,.7,.2,1)}.prod:hover .art svg{transform:scale(1.06) rotate(-2deg)}
.prod .meta{padding:22px;display:flex;flex-direction:column;gap:8px;flex:1}
.prod .k{font:500 .68rem var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--brass-l)}
.prod p{color:var(--muted-d);font-size:.93rem;flex:1}.prod .go{margin-top:10px;font-weight:600;color:#fff;text-decoration:none;display:inline-flex;gap:8px;align-items:center}
.prod .go .arr{transition:transform .25s}.prod:hover .go .arr{transform:translateX(4px)}
.shop-note{margin-top:28px;color:var(--muted-d);font-size:.88rem}
/* about */
.about{display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(32px,6vw,80px);align-items:center}.about>*{min-width:0}
@media(max-width:820px){.about{grid-template-columns:1fr}}
.about .ph{border-radius:6px;overflow:hidden;aspect-ratio:1;max-width:440px}.about .ph img{width:100%;height:100%;object-fit:cover;object-position:50% 20%}
.quote{font:400 clamp(1.5rem,3vw,2.1rem)/1.3 var(--display);color:var(--navy);margin-top:6px}
.about .body p{color:var(--muted);margin-top:16px;max-width:60ch}.about .sig{margin-top:24px;font:500 .74rem var(--mono);letter-spacing:.2em;text-transform:uppercase;color:var(--brass)}
.pillars{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:32px}@media(max-width:560px){.pillars{grid-template-columns:1fr}}
.pillars div{border-top:1px solid var(--brass);padding-top:14px}.pillars b{font:400 1.1rem var(--display);display:block;color:var(--navy)}.pillars span{font-size:.88rem;color:var(--muted)}
/* review band */
.review{text-align:center}.review .stars{color:var(--brass);letter-spacing:.3em;font-size:1.2rem}.review h2{margin-top:14px}.review p{color:var(--muted-d);margin-top:14px}
/* inner pages */
.prose{max-width:66ch}.prose p{color:var(--muted);margin-top:16px}.prose h2{margin-top:48px;font-size:clamp(1.6rem,3vw,2.2rem)}.prose ul{color:var(--muted);padding-left:20px}.prose li{margin-top:6px}.prose strong{color:var(--ink);font-weight:600}
.split{display:grid;grid-template-columns:.9fr 1.3fr;gap:56px}.split>*{min-width:0}@media(max-width:860px){.split{grid-template-columns:1fr;gap:32px}}
.sticky{position:sticky;top:100px;align-self:start}@media(max-width:860px){.sticky{position:static}}
.side{background:#fff;border:1px solid var(--line);border-radius:10px;padding:26px}.side .item:first-of-type{border-top:0}
.faq details{border-bottom:1px solid var(--line);padding-block:18px}.faq summary{cursor:pointer;font:400 1.15rem var(--display);color:var(--navy)}.faq details p{margin-top:10px}
.page-hero{padding-block:clamp(56px,8vw,96px) clamp(40px,6vw,64px);border-bottom:1px solid var(--line)}
.page-hero .lede{max-width:56ch}
/* cta + visit */
.cta-in{display:grid;grid-template-columns:1.2fr auto;gap:28px;align-items:center}@media(max-width:760px){.cta-in{grid-template-columns:1fr}}
.visit-in{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:36px}@media(max-width:820px){.visit-in{grid-template-columns:1fr}}
.visit h3{font-size:1.5rem;color:var(--navy);margin-bottom:8px}.visit p+p{margin-top:6px}.visit .tel{font:400 1.5rem var(--display);color:var(--navy);text-decoration:none}
.foot{background:var(--navy);color:var(--muted-d)}.foot-in{display:flex;flex-wrap:wrap;gap:14px 28px;justify-content:space-between;align-items:center;padding-block:28px;font-size:.85rem}
.foot nav{display:flex;flex-wrap:wrap;gap:18px}.foot a{text-decoration:none}.foot a:hover{color:#fff}
.disclose{font-size:.82rem;margin-top:18px;max-width:70ch}
.foot-links{padding-top:40px;border-bottom:1px solid var(--line-d);padding-bottom:28px}.foot-links nav{display:flex;flex-wrap:wrap;gap:10px 22px;font-size:.9rem}
.affs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:32px}@media(max-width:900px){.affs{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:520px){.affs{grid-template-columns:1fr}}
.aff{background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column;transition:transform .3s,box-shadow .3s}.aff:hover{transform:translateY(-4px);box-shadow:0 20px 40px -26px rgba(20,32,46,.5)}
.aff-img{aspect-ratio:1;background:var(--stone);display:grid;place-items:center}.aff-img img{width:100%;height:100%;object-fit:contain;padding:18px}
.aff-meta{padding:20px;display:flex;flex-direction:column;gap:6px;flex:1}.aff-meta .k{font:500 .68rem var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--brass)}.aff-meta p{color:var(--muted);font-size:.92rem;flex:1}
.aff-row{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:10px}.aff-row b{font:500 1.1rem var(--mono);color:var(--navy)}
.related{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}.related a{border:1px solid var(--line);border-radius:999px;padding:8px 16px;text-decoration:none;font-size:.9rem;color:var(--navy);background:#fff}.related a:hover{border-color:var(--brass)}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation:none!important;transition:none!important}}
"""

def head(title, desc, path):
    canon = B["site"] + ("/" if path == "index.html" else "/" + path.replace(".html", ""))
    return f"""<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:image" content="{B['site']}/assets/susy.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Hanken+Grotesk:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap">
<script type="application/ld+json">{schema()}</script>
<style>{CSS}</style>"""

ARR = '<span class="arr" aria-hidden="true">→</span>'

def header(active):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == active else ""}>{t}</a>' for h, t in NAV)
    return f"""<header class="top"><div class="wrap top-in">
<a class="brand" href="index.html" aria-label="The Q Salon for Men home"><span class="mono">Q</span><span class="brand-t">The Q Salon<small>For Men · Sarasota</small></span></a>
<nav class="nav" aria-label="Main">{links}</nav>
<a class="btn btn-sm" href="{B['book']}" target="_blank" rel="noopener">Book now</a>
</div></header>"""

def ticker():
    words = ["Classic Cuts", "Skin Fades", "Executive Cuts", "Gray Blending", "Gentleman's Facials", "Grooming Products", "Gift Cards"]
    run = "".join(f"<span>{w}</span>" for w in words)
    return f'<div class="ticker" aria-hidden="true"><div class="track">{run}{run}</div></div>'

def menu(items=SERVICES):
    return "".join(f"""<div class="item"><h3>{n}</h3><span class="price">${p}</span><p><span class="dur">{t}</span> · {d}</p></div>""" for n, t, p, d in items)

def product_cards():
    out = []
    for k, sub, d, svg, dest in PRODUCTS:
        href = B["book"] if dest == "book" else B["shop"]
        label = "Buy a gift card" if dest == "book" else f"Shop {k.lower()}"
        out.append(f"""<article class="prod"><div class="art">{svg}</div><div class="meta"><span class="k">{sub}</span><h3>{k}</h3><p>{d}</p>
<a class="go" href="{href}" target="_blank" rel="noopener">{label} {ARR}</a></div></article>""")
    return "".join(out)

def shop_section(title="The Q Shop", h2="Take the finish home."):
    return f"""<section class="sec on-dark" id="shop"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">{title}</p><h2>{h2}</h2></div>
<p>The products Susy uses in the chair, picked for men's hair and Florida humidity. Order online or pick up at your next visit.</p></div>
<div class="products">{product_cards()}</div>
<div class="acts"><a class="btn btn-brass" href="{B['shop']}" target="_blank" rel="noopener">Shop all products {ARR}</a><a class="btn btn-line" href="shop.html">Visit the shop</a></div>
</div></section>"""

def cta(text="Pick your service and any open time in under a minute."):
    return f"""<section class="sec stone"><div class="wrap cta-in"><div><p class="eyebrow">Appointments</p><h2>Your chair is waiting.</h2><p class="muted" style="margin-top:12px">{text}</p></div>
<a class="btn" href="{B['book']}" target="_blank" rel="noopener">Book with Susy {ARR}</a></div></section>"""

def visit():
    return f"""<section class="sec visit"><div class="wrap visit-in">
<div><p class="eyebrow">Visit</p><h3>Downtown Sarasota</h3><p>{ADDR}</p><p><a class="link" href="{B['maps']}" target="_blank" rel="noopener">Get directions</a></p></div>
<div><p class="eyebrow">Hours</p><h3>{B['hours']}</h3><p class="muted">By appointment. Closed Saturday &amp; Sunday.</p></div>
<div><p class="eyebrow">Call or text</p><a class="tel" href="tel:{B['phone_e164']}">{B['phone']}</a><p class="muted">Our front desk will text you the booking link.</p></div>
</div></section>
<footer class="foot"><div class="wrap">
<div class="foot-links"><p class="eyebrow" style="color:var(--brass-l)">Services &amp; areas</p><nav aria-label="Services and areas">{"".join(f'<a href="{h}">{t}</a>' for h, t in SEO_LINKS)}</nav></div>
<div class="foot-in"><p>© 2026 {B['name']} · {ADDR} · {B['phone']}</p>
<nav aria-label="Footer">{"".join(f'<a href="{h}">{t}</a>' for h, t in NAV)}</nav></div></div></footer>"""

def affiliate_grid():
    if not AFFILIATE:
        return ""
    cards = "".join(f"""<article class="aff"><div class="aff-img"><img src="{p['img']}" alt="{p['name']}" loading="lazy"></div>
<div class="aff-meta"><span class="k">{p.get('brand','')}</span><h3>{p['name']}</h3><p>{p.get('note','')}</p>
<div class="aff-row"><b>{p.get('price','')}</b><a class="btn btn-sm" href="{p['url']}" target="_blank" rel="sponsored nofollow noopener">Buy now {ARR}</a></div></div></article>""" for p in AFFILIATE)
    return f'<div class="affs">{cards}</div>'

def page(path, title, desc, body):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{head(title, desc, path)}
</head><body>
{header(path)}
<main>{body}</main>
{visit()}
</body></html>"""

# ---------- Home ----------
home = f"""
<section class="hero2">
<figure class="h2-media"><div class="h2-frame">
<img src="assets/hero-gent.jpg" alt="Man with swept-back silver-streaked hair and a sculpted salt-and-pepper beard" width="1179" height="1454" fetchpriority="high">
<span class="h2-tag t1"><i></i>01 · Swept-back cut, natural silver kept</span>
<span class="h2-tag t2"><i></i>02 · Beard sculpted &amp; lined</span>
<span class="h2-issue">The Q · Sarasota · Est. 2021</span>
</div></figure>
<div class="h2-copy"><div class="h2-inner">
<p class="eyebrow">Men's grooming · Downtown Sarasota</p>
<h1><span class="l"><span>The cut</span></span><span class="l"><span>that carries</span></span><span class="l"><span><em>the room.</em></span></span></h1>
<p class="lede">Precision cuts, seamless fades and natural gray blending from master stylist Susy. One chair, by appointment, and her full attention from start to finish.</p>
<div class="acts"><a class="btn" href="{B['book']}" target="_blank" rel="noopener">Book an appointment {ARR}</a><a class="btn btn-line" href="#shop">Shop products</a></div>
<a class="h2-by" href="#meet"><img src="assets/susy.jpg" alt="" width="44" height="44"><span><b>Every cut by Susy</b><small>Master barber &amp; stylist · 10+ years</small></span></a>
<div class="stats"><div><b>4.9★</b><span>66 Google reviews</span></div><div><b>10+</b><span>Years behind the chair</span></div><div><b>1</b><span>Chair. Your time.</span></div></div>
</div></div>
</section>
{ticker()}
<section class="sec" id="services"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">Service menu</p><h2>Every service, done by Susy.</h2></div>
<p>No hand-offs and no assembly line. Prices and times exactly as listed in our booking system.</p></div>
<div class="menu">{menu()}</div>
<div class="menu-foot"><p class="muted">Gift cards from $50 · Book online in under a minute</p><a class="btn" href="{B['book']}" target="_blank" rel="noopener">See open times {ARR}</a></div>
</div></section>
{shop_section()}
<section class="sec" id="meet"><div class="wrap about">
<div class="ph"><img src="assets/susy.jpg" alt="Portrait of Susy" loading="lazy" width="1000" height="1000"></div>
<div><p class="eyebrow">Meet Susy</p><h2>The reason clients don't go anywhere else.</h2>
<div class="body"><p>Susy has spent more than a decade perfecting men's hair. Her clients know her for fades that blend clean every time, executive cuts that still look right three weeks later, and gray blending so natural nobody can tell.</p>
<p>The Q is built around that standard: one chair, appointments only, and the kind of consistency you only get from the same expert hands every visit.</p></div>
<div class="pillars"><div><b>Precision</b><span>Clean lines, seamless blends.</span></div><div><b>Consistency</b><span>Same expert, every visit.</span></div><div><b>Discretion</b><span>Private, unhurried, on time.</span></div></div>
</div></div></section>
<section class="sec on-dark review"><div class="wrap"><p class="stars" aria-label="4.9 out of 5 stars">★★★★★</p><h2>4.9 stars across 66 Google reviews.</h2>
<p>Read what Sarasota's best-groomed men say, then see for yourself.</p>
<div class="acts" style="justify-content:center"><a class="btn btn-brass" href="{B['book']}" target="_blank" rel="noopener">Book your first visit {ARR}</a></div></div></section>
{cta()}
"""

# ---------- Shop ----------
shop = f"""
<section class="page-hero"><div class="wrap"><p class="eyebrow">The Q Shop</p><h1>Products for the morning after your cut.</h1>
<p class="lede">Styling, beard and hair-care essentials hand-picked by Susy, plus gift cards for any service. Order online or pick up in the salon.</p>
<div class="acts"><a class="btn" href="{B['shop']}" target="_blank" rel="noopener">Shop on Squire {ARR}</a><a class="btn btn-line" href="{B['book']}" target="_blank" rel="noopener">Book a cut</a></div></div></section>
{shop_section("Shop by need", "Everything Susy reaches for.")}
<section class="sec" id="picks"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">Susy's picks</p><h2>Tools &amp; extras she recommends</h2></div>
<p>Trimmers, combs and grooming gear Susy trusts for between-visit touch-ups.{"" if AFFILIATE else " Her full list is coming soon; ask her at your next appointment."}</p></div>
{affiliate_grid()}
<p class="disclose muted">Some links on this page are affiliate links. If you buy through them, The Q Salon may earn a small commission at no extra cost to you.</p>
</div></section>
{cta("Fresh cut first, then the products to keep it.")}
"""

FAQ_COMMON = [
    ("Where are you located?", f"We're at {ADDR}, in downtown Sarasota."),
    ("What are your hours?", "Monday through Friday, 9 AM to about 2 PM, by appointment. We're closed Saturday and Sunday."),
    ("Do you take walk-ins?", "It's one chair, so booking ahead is the way to guarantee a time. Booking online takes under a minute."),
]

def faq_schema(faqs):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}) + "</script>"

def seo_page(h1, eyebrow, lede, sections, faqs, svc_filter, related=None):
    items = [s for s in SERVICES if s[0] in svc_filter]
    rel = related or ["mens-haircut-sarasota.html", "skin-fade-sarasota.html", "mens-hair-color-sarasota.html", "executive-haircut-sarasota.html"]
    names = dict(SEO_LINKS)
    rel_html = "".join(f'<a href="{h}">{names.get(h, h)}</a>' for h in rel)
    return f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lede">{lede}</p>
<div class="acts"><a class="btn" href="{B['book']}" target="_blank" rel="noopener">Book now {ARR}</a><a class="btn btn-line" href="index.html#services">Full menu</a></div></div></section>
<section class="sec"><div class="wrap split"><div class="sticky"><div class="side"><p class="eyebrow">Pricing</p>{menu(items)}
<a class="btn btn-sm" style="margin-top:18px" href="{B['book']}" target="_blank" rel="noopener">Book this {ARR}</a></div></div>
<div class="prose">{sections}
<h2>Questions</h2><div class="faq">{"".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)}</div>
<h2>Related services</h2><div class="related">{rel_html}</div></div></div></section>
{faq_schema(faqs)}
{shop_section("Keep it sharp", "Products for between visits.")}
{cta()}"""

haircut = seo_page("Men's haircuts in downtown Sarasota", "Men's haircut · Sarasota, FL",
    "Classic and executive cuts from a master stylist with 10+ years behind the chair. One chair, by appointment, no rushing.",
    f"""<h2>A haircut built around how you wear it</h2>
<p>Every cut starts with a short consultation: how you style it, how often you come in, and how it should look in week three, not just day one. Susy cuts with scissors and clippers to suit your hair type, then finishes and shows you how to style it at home.</p>
<h2>Classic or Executive?</h2>
<p>The <strong>Classic Haircut</strong> ($60, about 45 minutes) is a precise scissor-and-clipper cut, styled to finish. The <strong>Executive Haircut</strong> ($80, about an hour) adds extra time and detail work, the right pick before an interview, an event, or when you want the full experience.</p>
<h2>Convenient to downtown</h2>
<p>We're at {ADDR}, a short walk from Main Street and Five Points, and an easy stop for anyone working downtown, in the Rosemary District or along Fruitville Road.</p>""",
    FAQ_COMMON, {"Classic Haircut", "Executive Haircut", "Kid's Haircut (under 12)"})

fade = seo_page("Skin fades with a clean, seamless blend", "Skin fade · Sarasota, FL",
    "Skin fades in downtown Sarasota: low, mid or high, with crisp lines and no visible steps.",
    """<h2>What makes a good fade</h2>
<p>A skin fade lives or dies on the blend. Susy takes the sides down to the skin and works up through each guard until there's no visible line, then sharpens the edges so it reads clean from every angle.</p>
<h2>Low, mid or high</h2>
<ul><li><strong>Low fade:</strong> starts just above the ear; subtle and office-friendly.</li><li><strong>Mid fade:</strong> the most popular; balanced and sharp.</li><li><strong>High fade:</strong> bold contrast, pairs well with textured tops.</li></ul>
<p>Not sure which suits your head shape? Ask during your appointment and Susy will recommend one.</p>
<h2>Keeping it sharp</h2>
<p>Fades grow out fastest of any style. Most clients rebook every two to three weeks to keep the blend tight.</p>""",
    FAQ_COMMON + [("How long does a skin fade take?", "About an hour, including the finish and styling. It's $80.")],
    {"Skin Fade", "Executive Haircut"})

color = seo_page("Gray blending that looks like you", "Men's hair color · Sarasota, FL",
    "Natural-looking men's color and gray blending in downtown Sarasota. Softens the gray without the flat, dyed look.",
    """<h2>Blend, don't cover</h2>
<p>Full-coverage dye on men's hair often looks flat and grows out with a hard line. Our <strong>Natural Look Color &amp; Style</strong> blends the gray instead, leaving some of it in so the result reads as your own hair, just a few years fresher.</p>
<h2>What to expect</h2>
<p>The appointment runs about an hour and 15 minutes and includes your color, a cut refresh and styling, for $130. Most clients come back every four to six weeks to keep it consistent.</p>
<h2>Low maintenance by design</h2>
<p>Because the color is blended rather than solid, regrowth is soft and gradual. Ask about color-safe shampoo in the salon to make it last longer.</p>""",
    FAQ_COMMON + [("Will it look dyed?", "No. Gray blending is designed to leave natural dimension, so it softens gray rather than hiding it completely.")],
    {"Natural Look Color & Style"})

ALL = {s[0] for s in SERVICES}
CUTS = {"Classic Haircut", "Executive Haircut", "Skin Fade"}

barber = seo_page("A barber in Sarasota who knows your name", "Barber · Sarasota, FL",
    "Looking for a barber in Sarasota? The Q is a private, one-chair men's salon: master stylist Susy, appointments only, and no waiting room.",
    f"""<h2>Barbershop craft, salon-level detail</h2>
<p>Most men searching for a barber in Sarasota want three things: a clean cut, no long wait, and someone who remembers how they like it. The Q delivers all three. Susy combines barbering technique, tight fades and sharp lines, with the scissor work and consultation of a high-end men's salon.</p>
<h2>What you can book</h2>
<ul><li><strong>Classic Haircut</strong>, $60: scissor and clipper cut, styled to finish.</li><li><strong>Executive Haircut</strong>, $80: extra time and detail.</li><li><strong>Skin Fade</strong>, $80: low, mid or high, blended seamlessly.</li><li><strong>Natural Look Color &amp; Style</strong>, $130: gray blending.</li><li><strong>Gentleman's Facial</strong>, $75, and <strong>kids' cuts</strong>, $30.</li></ul>
<h2>No walk-in lottery</h2>
<p>Because it's one chair, every client has a reserved time. Book online in under a minute and you'll be in the chair when you arrive, Monday through Friday, 9 AM to 2 PM.</p>""",
    FAQ_COMMON + [("How much is a haircut?", "Classic Haircut $60, Executive Haircut and Skin Fade $80, Kid's Haircut $30."),
                  ("Is The Q a barbershop or a salon?", "Both. It's a men's hair salon with barbering skills: fades, line-ups and clipper work, plus scissor cuts and men's color.")],
    ALL, ["mens-haircut-sarasota.html", "skin-fade-sarasota.html", "executive-haircut-sarasota.html", "mens-grooming-sarasota.html"])

executive = seo_page("The Executive Haircut", "Executive haircut · Sarasota, FL",
    "Sarasota's executive men's haircut: an hour with a master stylist, extra detail work, and a finish built for the boardroom.",
    """<h2>What makes it executive</h2>
<p>The Executive Haircut gives Susy a full hour. That extra time goes into the details most cuts skip: a cleaner neckline, refined texture on top, balanced weight around the ears, and a finish that holds through a long day.</p>
<h2>Who books it</h2>
<p>Professionals before interviews, presentations and events, grooms and wedding parties, and anyone who wants the best version of their cut instead of the fastest one.</p>
<h2>Price and timing</h2>
<p>$80, about one hour. Pair it with a Gentleman's Facial before a big day.</p>""",
    FAQ_COMMON + [("What's the difference between Classic and Executive?", "Time and detail. The Classic is a precise 45-minute cut for $60; the Executive is a full hour with extra finishing work for $80.")],
    {"Executive Haircut", "Classic Haircut", "Gentleman's Facial"}, ["mens-haircut-sarasota.html", "mens-facial-sarasota.html", "skin-fade-sarasota.html", "barber-sarasota.html"])

facial = seo_page("A Gentleman's Facial in Sarasota", "Men's facial · Sarasota, FL",
    "A 45-minute men's facial in Sarasota: cleanse, exfoliate and hydrate. Built for Florida sun and daily shaving.",
    """<h2>Why men book a facial</h2>
<p>Sun, salt air, humidity and daily shaving are hard on skin. The Gentleman's Facial deep-cleans pores, exfoliates dull skin and restores hydration, so you leave looking rested rather than polished.</p>
<h2>What happens in 45 minutes</h2>
<ul><li>Cleanse and steam to open pores</li><li>Exfoliation to clear buildup and ingrown-prone areas</li><li>Hydration matched to your skin</li><li>A few simple at-home tips</li></ul>
<h2>Pair it</h2>
<p>Add it to an Executive Haircut before an event, or book it on its own once a month. $75.</p>""",
    FAQ_COMMON + [("Is a facial worth it for men?", "Yes, especially in Florida. Regular facials help with clogged pores, razor irritation and sun-dried skin.")],
    {"Gentleman's Facial", "Executive Haircut"}, ["executive-haircut-sarasota.html", "mens-grooming-sarasota.html", "grooming-guide.html", "barber-sarasota.html"])

kids = seo_page("Kids' haircuts in Sarasota, without the chaos", "Kids' haircuts · Sarasota, FL",
    "Calm, comfortable haircuts for boys under 12 in Sarasota. $30, about 30 minutes, with the same master stylist who cuts Dad's hair.",
    """<h2>A quiet chair, not a busy shop</h2>
<p>Busy barbershops can overwhelm kids. At The Q there's one chair and no crowd, so younger clients settle in and sit still, and the cut comes out cleaner.</p>
<h2>Book father and son together</h2>
<p>Many dads book back-to-back appointments: kid's cut first, then their own. It's one trip and both of you leave sharp.</p>
<h2>Price</h2><p>$30 for boys under 12, about 30 minutes.</p>""",
    FAQ_COMMON + [("What age is the kid's haircut for?", "Boys under 12. Teens book the Classic Haircut.")],
    {"Kid's Haircut (under 12)", "Classic Haircut"}, ["mens-haircut-sarasota.html", "barber-sarasota.html", "skin-fade-sarasota.html", "grooming-guide.html"])

grooming = seo_page("Men's grooming in Sarasota, all in one chair", "Men's grooming · Sarasota, FL",
    "Haircuts, fades, gray blending, facials and grooming products from one master stylist. The full men's grooming routine, handled.",
    """<h2>One expert for your whole look</h2>
<p>Most men split grooming across a barbershop, a color appointment and a drugstore shelf. At The Q, Susy handles your cut, your color, your skin and the products you use at home, so everything works together.</p>
<h2>Build your routine</h2>
<ul><li><strong>Every 2–3 weeks:</strong> skin fade or tight cut</li><li><strong>Every 3–5 weeks:</strong> Classic or Executive Haircut</li><li><strong>Every 4–6 weeks:</strong> Natural Look Color &amp; Style</li><li><strong>Monthly:</strong> Gentleman's Facial</li></ul>
<h2>At home</h2><p>Ask Susy what to use; the products she finishes with are in the Q Shop.</p>""",
    FAQ_COMMON + [("How often should men get a haircut?", "Every two to three weeks for fades, three to five weeks for longer cuts.")],
    ALL, ["barber-sarasota.html", "mens-facial-sarasota.html", "mens-hair-color-sarasota.html", "grooming-guide.html"])

def area_page(area, drive, local):
    return seo_page(f"Men's haircuts for {area}", f"Men's haircut · {area}, FL",
        f"{area} men book with Susy at The Q Salon for Men: precision cuts, skin fades and gray blending, {drive}.",
        f"""<h2>Worth the short drive</h2>
<p>{local} The Q is a private, one-chair men's salon, so your appointment starts on time and Susy's attention stays on you.</p>
<h2>Popular with {area} clients</h2>
<ul><li><strong>Executive Haircut</strong> ($80) for professionals</li><li><strong>Skin Fade</strong> ($80) kept sharp every few weeks</li><li><strong>Natural Look Color &amp; Style</strong> ($130) for gray blending</li></ul>
<h2>Easy to book</h2><p>Book online in under a minute, Monday through Friday, 9 AM to 2 PM. Or call {B['phone']} and our front desk will text you the link.</p>""",
        FAQ_COMMON, CUTS | {"Natural Look Color & Style"},
        ["barber-sarasota.html", "skin-fade-sarasota.html", "executive-haircut-sarasota.html", "mens-hair-color-sarasota.html"])

lwr = area_page("Lakewood Ranch", "about 25 minutes from Lakewood Ranch", "Lakewood Ranch has plenty of chain barbershops and busy salons. Clients who want something better make the drive downtown.")
siesta = area_page("Siesta Key", "about 15 minutes from Siesta Key", "Sun, salt and humidity are rough on hair. Siesta Key clients rely on Susy for cuts that hold their shape and gray blending that doesn't fade brassy in the sun.")
longboat = area_page("Longboat Key", "about 20 minutes from Longboat Key", "Longboat Key clients expect a refined, unhurried experience. That's exactly how The Q is built.")

GUIDE = [
    ("How to tell when your fade needs a refresh", "Run your hand up the side of your head. If you can feel a clear line where short meets long, the blend has grown out. For most men that's around day 14 to 21."),
    ("The two-minute styling routine", "Towel-dry until damp, work a pea-sized amount of product between your palms until it disappears, then apply back to front. Finish with fingers, not a comb, for natural texture."),
    ("Pomade, clay or cream?", "Pomade gives shine and slick control. Clay gives matte texture and strong hold for thicker hair. Cream gives light, natural hold for finer hair. If you're not sure, ask Susy what she finished your cut with."),
    ("Why gray blending beats box dye", "Box dye covers everything in one flat shade and grows out with a hard line. Blending keeps some gray, so regrowth is soft and the result looks like your own hair."),
    ("Protect your color from the Florida sun", "Use a color-safe shampoo, rinse with cool water, and wear a hat on the boat or beach. UV and chlorine are what turn blended color brassy."),
    ("Stop razor bumps", "Exfoliate twice a week, shave with the grain after a warm shower, and finish with a fragrance-free moisturizer. A monthly Gentleman's Facial helps clear ingrown-prone areas."),
    ("Beard care in humidity", "Wash your beard two or three times a week, not daily, and use a few drops of beard oil on damp hair to stop frizz and itch."),
    ("How to ask for the haircut you want", "Bring a photo, say how you style it day to day, and tell your stylist how long you go between cuts. That last detail changes how a cut should be built."),
]
guide = f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">Grooming guide</p><h1>Tips from Susy's chair</h1>
<p class="lede">Simple, practical grooming advice for men in Sarasota: fades, styling, gray blending, skin and beard care.</p>
<div class="acts"><a class="btn" href="{B['book']}" target="_blank" rel="noopener">Book with Susy {ARR}</a><a class="btn btn-line" href="shop.html">Shop products</a></div></div></section>
<section class="sec"><div class="wrap split"><div class="sticky"><div class="side"><p class="eyebrow">In this guide</p>
{"".join(f'<p style="margin-top:10px"><a class="link" href="#tip-{i}">{t}</a></p>' for i, (t, _) in enumerate(GUIDE, 1))}</div></div>
<div class="prose">{"".join(f'<h2 id="tip-{i}">{t}</h2><p>{b}</p>' for i, (t, b) in enumerate(GUIDE, 1))}
<h2>Related services</h2><div class="related">{"".join(f'<a href="{h}">{t}</a>' for h, t in SEO_LINKS[:8])}</div></div></div></section>
{shop_section("Keep it sharp", "Products for between visits.")}
{cta()}"""

PAGES = [
    ("index.html", "The Q Salon for Men", "Men's haircuts, skin fades and gray blending in downtown Sarasota at 1415 1st St. Book with master stylist Susy and shop grooming products.", home),
    ("shop.html", "The Q Shop · The Q Salon for Men", "Shop men's styling, beard and hair-care products and gift cards from The Q Salon for Men in Sarasota.", shop),
    ("mens-haircut-sarasota.html", "Men's Haircut Sarasota · The Q Salon", "Men's haircuts in downtown Sarasota from $60. Classic and executive cuts by a master stylist at 1415 1st St. Book online.", haircut),
    ("skin-fade-sarasota.html", "Skin Fade Sarasota · The Q Salon", "Skin fades in downtown Sarasota for $80. Low, mid and high fades with a seamless blend. Book online at The Q Salon for Men.", fade),
    ("mens-hair-color-sarasota.html", "Men's Gray Blending Sarasota · The Q Salon", "Natural men's hair color and gray blending in downtown Sarasota. Natural Look Color & Style, $130. Book at The Q Salon for Men.", color),
    ("barber-sarasota.html", "Barber in Sarasota · The Q Salon for Men", "Looking for a barber in Sarasota? Private one-chair men's salon with master stylist Susy. Haircuts from $60, skin fades $80. Book online.", barber),
    ("executive-haircut-sarasota.html", "Executive Haircut Sarasota · The Q Salon", "The Executive Haircut in Sarasota: an hour with a master stylist and extra detail work, $80. Book online at The Q Salon for Men.", executive),
    ("mens-facial-sarasota.html", "Men's Facial Sarasota · The Q Salon", "Gentleman's Facial in Sarasota: 45-minute men's facial to cleanse, exfoliate and hydrate, $75. Book at The Q Salon for Men.", facial),
    ("kids-haircut-sarasota.html", "Kids' Haircut Sarasota · The Q Salon", "Calm kids' haircuts in Sarasota for boys under 12, $30. One chair, no crowd. Book father-and-son appointments online.", kids),
    ("mens-grooming-sarasota.html", "Men's Grooming Sarasota · The Q Salon", "Men's grooming in Sarasota: haircuts, fades, gray blending, facials and products from one master stylist. Book online.", grooming),
    ("mens-haircut-lakewood-ranch.html", "Men's Haircut Lakewood Ranch · The Q Salon", "Men's haircuts for Lakewood Ranch: precision cuts, skin fades and gray blending with master stylist Susy. Book online.", lwr),
    ("mens-haircut-siesta-key.html", "Men's Haircut Siesta Key · The Q Salon", "Men's haircuts for Siesta Key: cuts, skin fades and sun-proof gray blending with master stylist Susy. Book online.", siesta),
    ("mens-haircut-longboat-key.html", "Men's Haircut Longboat Key · The Q Salon", "Men's haircuts for Longboat Key: refined cuts, fades and gray blending with master stylist Susy. Book online.", longboat),
    ("grooming-guide.html", "Men's Grooming Guide · The Q Salon", "Practical men's grooming tips from Sarasota master stylist Susy: fades, styling products, gray blending, razor bumps and beard care.", guide),
]

if __name__ == "__main__":
    os.makedirs("dist", exist_ok=True); os.makedirs("preview", exist_ok=True)
    for path, title, desc, body in PAGES:
        html = page(path, title, desc, body)
        open(f"dist/{path}", "w").write(html)
        if path == "index.html":
            inner = re.sub(r"(?s)^<!doctype html>\s*<html[^>]*><head>.*?<meta name=\"viewport\"[^>]*>\s*", "", html)
            inner = inner.replace("</head><body>", "").replace("</body></html>", "")
            open("preview/index.html", "w").write(inner)
        else:
            open(f"preview/{path}", "w").write(html)
    urls = "".join(f"<url><loc>{B['site']}/{'' if p=='index.html' else p.replace('.html','')}</loc></url>" for p, *_ in PAGES)
    open("dist/sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open("dist/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {B['site']}/sitemap.xml\n")
    open("dist/_redirects", "w").write("/downtown-sarasota-barbershop /mens-haircut-sarasota 301\n/about / 301\n/gallery / 301\n/book " + B['book'] + " 302\n")
    print("built", len(PAGES), "pages")
