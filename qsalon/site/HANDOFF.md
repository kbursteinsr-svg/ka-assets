# The Q Salon for Men: website handoff (for a new chat)

Paste or attach this file in a new chat. It covers everything needed to make small edits and do SEO on **theqsalonsrq.com**.

---

## 1. The business (facts to keep consistent everywhere)

| | |
|---|---|
| Name | The Q Salon for Men |
| Stylist | Susy: master barber & stylist, 10+ years, the only barber (one chair) |
| Address | 1415 1st St, Sarasota, FL 34236 (downtown) |
| Phone | (941) 340-2389 (answered by the AI receptionist "Monica", who texts the booking link) |
| Hours | Mon–Fri 9 AM – 2 PM, by appointment. Closed Sat & Sun |
| Booking | SQUIRE only: https://getsqr.co/susy-r-6 (site shortcut: theqsalonsrq.com/book) |
| Email | info@theqsalonsrq.com (Google Workspace) |
| Google Business Profile | Place ID `ChIJB1LNsmpBw4gR9zjOVKOkWkk` · Maps: https://maps.google.com/maps?cid=5285718134082124023 · Review link: https://search.google.com/local/writereview?placeid=ChIJB1LNsmpBw4gR9zjOVKOkWkk · GBP categories: Hair salon (primary), Barber shop, Facial spa · Service areas: Sarasota, Longboat Key, Lakewood Ranch, Siesta Key, Lido Key, Sarasota County · Opened Nov 2021 |
| Reviews shown on site | 4.9★ from 66 Google reviews (hard-coded; update when it changes) |

**Services & prices:** Classic Haircut $60 (45 min) · Executive Haircut $80 (1 hr) · Skin Fade $80 (1 hr) · Natural Look Color & Style (gray blending) $130 (1 hr 15 min) · Gentleman's Facial $75 (45 min) · Kid's Haircut, under 12, $30 (30 min) · Gift cards from $50.

---

## 2. Where the site lives

- **Live:** https://theqsalonsrq.com (www.theqsalonsrq.com is set as the primary domain in Netlify)
- **Hosting:** Kris's Netlify account. Site/project name **tranquil-yeot-e8ab44** (https://tranquil-yeot-e8ab44.netlify.app). Deployed by **drag-and-drop**: Netlify → Deploys → drop a zip of the `dist/` folder.
- **DNS:** Squarespace Domains (account.squarespace.com/domains → theqsalonsrq.com → DNS). Records:
  - A `@` → 75.2.60.5 (Netlify)
  - CNAME `www` → tranquil-yeot-e8ab44.netlify.app
  - **Do not touch** MX (smtp.google.com), SPF TXT, `google._domainkey` DKIM, or `_dmarc` records. They run info@ email. Do not switch nameservers to Netlify.
- **Source code:** GitHub `kbursteinsr-svg/ka-assets`, folder **`qsalon/site/`**
  - `build.py` is the generator. All pages, copy, CSS, schema, sitemap, robots and redirects come from this one file.
  - `dist/` is the built site (what gets deployed)
  - `dist/assets/`: `susy.jpg` (Susy portrait, used in "Meet Susy", the hero "Every cut by Susy" pill and og:image) and `hero-gent.jpg` (hero photo, supplied by Kris)

### How to edit and ship
```bash
git clone https://github.com/kbursteinsr-svg/ka-assets
cd ka-assets/qsalon/site
# edit build.py
python3 build.py            # rebuilds dist/ (prints "built 14 pages")
cd dist && zip -qr ../theqsalonsrq-site.zip . # index.html must be at the zip root
```
Then send Kris the zip to drag into Netlify → Deploys. Commit the `build.py` and `dist/` changes back to `ka-assets`.

Check pages after deploy. The cloud workspace can't reach netlify.app directly, so use an n8n HTTP Request workflow (Kris's n8n: kbdigitalmkt.app.n8n.cloud) or ask Kris to look.

---

## 3. Site map (14 pages)

| URL | Page |
|---|---|
| `/` | Home: hero, service menu, shop teaser, Meet Susy (`#meet`), reviews band, CTA, visit/hours |
| `/shop` | The Q Shop: product categories + gift cards (links go to SQUIRE); "Susy's picks" affiliate section says "coming soon" |
| `/barber-sarasota` | Barber in Sarasota |
| `/mens-haircut-sarasota` | Men's Haircut Sarasota |
| `/executive-haircut-sarasota` | Executive Haircut |
| `/skin-fade-sarasota` | Skin Fade Sarasota |
| `/mens-hair-color-sarasota` | Men's Gray Blending |
| `/mens-facial-sarasota` | Men's Facial |
| `/kids-haircut-sarasota` | Kids' Haircuts |
| `/mens-grooming-sarasota` | Men's Grooming |
| `/mens-haircut-lakewood-ranch` | Area page |
| `/mens-haircut-siesta-key` | Area page |
| `/mens-haircut-longboat-key` | Area page |
| `/grooming-guide` | Tips from Susy's chair |

Redirects (`_redirects`): `/book` → SQUIRE (302), `/about` and `/gallery` → `/` (301), `/downtown-sarasota-barbershop` → `/mens-haircut-sarasota` (301).

**SEO already in place:** unique titles and meta descriptions, canonical tags pointing to `https://www.theqsalonsrq.com/...`, `HairSalon` JSON-LD with address, hours, phone and service offers, `sitemap.xml`, `robots.txt`, Open Graph tags, internal links between all service and area pages, and FAQ blocks on service pages.

---

## 4. Brand & design

- Colors: navy `#14202e`, brass `#b08d57` / light brass `#d6b984`, stone `#e8e3db` / `#f3f0ea`
- Fonts (Google Fonts): **Marcellus** (headings), **Hanken Grotesk** (body), **DM Mono** (labels/eyebrows)
- Voice: confident, polished, GQ-style. Never cheesy, flirty or salesy. Talk about Susy in the third person.
- Hero (Oct 1, 2026): editorial split. A framed portrait card of the man with a silver beard (`hero-gent.jpg`) on the left, with tags "01 · Swept-back cut, natural silver kept" / "02 · Beard sculpted & lined". Headline "The cut that carries the room." on the right, with an "Every cut by Susy" pill linking to `#meet`. Kris approved the smaller, framed size.

---

## 5. Rules & preferences (from Kris)

- **SQUIRE is the only booking path.** Every Book button goes to https://getsqr.co/susy-r-6. Never mention another calendar.
- No phone numbers or links inside Google Business Profile **post** text (Google rejects those). This doesn't apply to the website.
- Deploys: build and iterate in chat. Ship only when Kris says "ship it". He drags the zip into Netlify himself.
- Never ask for or handle passwords or API keys. Kris enters credentials himself.
- Kris prefers short, direct answers and exact click-by-click steps when he has to do something.

---

## 6. Open items & SEO ideas to start with

**Small fixes already noticed:**
1. Footer/visit block says **"Call or text (941) 340-2389"**. Calls go to Monica, but incoming texts aren't handled yet. Consider changing it to "Call" until texting (A2P approval) is live.
2. A "Powered by Netlify" badge showed on the live site. It comes from Netlify, not the code; check whether visitors see it and whether it can be turned off in Netlify.
3. The shop page has an affiliate disclosure but no affiliate products yet (Kris plans to add Amazon affiliate picks).
4. The review count (4.9★ / 66) is hard-coded in the hero and review band.

**SEO next steps:**
1. Add the site to **Google Search Console** (verify via a DNS TXT record in Squarespace) and submit `https://www.theqsalonsrq.com/sitemap.xml`.
2. Make sure the Google Business Profile website field uses `https://www.theqsalonsrq.com/` (it currently points to the www URL).
3. Add `aggregateRating` to the JSON-LD only if it matches real Google reviews, and add `sameAs` links (Instagram @theqsalon_srq, Google Maps URL).
4. Add `geo` coordinates and `areaServed` to the schema; consider `Service` schema per service page.
5. Add `og:image` per page and a proper 1200×630 social share image.
6. Image SEO: descriptive file names and alt text; compress `hero-gent.jpg` (≈260 KB) further or add WebP.
7. Add a real photo gallery of Susy's work, from the Drive folder "Q Salon — Susy Uploads", once she uploads.
8. Expand area pages with unique local content (landmarks, parking, distance from downtown) so they aren't thin or duplicate.
9. Add an FAQ schema block where FAQs exist, and an embedded Google Map on the home or visit section.
10. Check Core Web Vitals (PageSpeed Insights) on mobile after changes.

---

## 7. Related systems (don't break these)

- **GBP post engine** (n8n `CZEJxhzrQ7QndFUX`): posts 4×/week (Sun/Mon/Wed/Fri 7:50 AM ET). Post images are hosted on GitHub `ka-assets/qsalon/cards/`, not on the site.
- **Monica** (ElevenLabs voice agent on (941) 340-2389): asks the service and day, then texts the SQUIRE link only with the caller's yes.
- **Review requests** (n8n `MXXX2W29N4Ci3trh`): Susy's checkout form at https://kbdigitalmkt.app.n8n.cloud/form/qsalon-checkout sends a thank-you plus Google review link from info@ one hour later.
- **Content pipeline**: Drive folder "Q Salon — Susy Uploads" → n8n intake (`dffbu7IXPeortLTc`) captions photos → approval emails (`6q5E0dGpgB6YJmri`) → queue table `qsalon_content_queue`.
