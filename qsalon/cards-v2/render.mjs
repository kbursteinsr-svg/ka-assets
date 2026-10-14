// Renders the 90 Q Salon GBP post cards (1200x900) from cards.json.
// Usage: node render.mjs [day ...]   (no args = all 90)
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
const require = createRequire(process.env.PW_REQUIRE || import.meta.url);
const { chromium } = require('playwright');

const HERE = path.dirname(new URL(import.meta.url).pathname);
const ASSETS = path.resolve(HERE, '../site/dist/assets');
const cards = JSON.parse(fs.readFileSync(path.join(HERE, 'cards.json'), 'utf8'));
const only = process.argv.slice(2).map(Number);
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const title = t => esc(t).split(' ').map(w => w.includes('-') ? `<span style="white-space:nowrap">${w}</span>` : w).join(' ');
const font = f => 'file://' + path.join(HERE, 'fonts', f);
const img = p => 'file://' + path.join(ASSETS, p);

const CSS = `
@font-face{font-family:Marcellus;src:url(${font('marcellus-latin-400-normal.woff2')})}
@font-face{font-family:Hanken;font-weight:400;src:url(${font('hanken-grotesk-latin-400-normal.woff2')})}
@font-face{font-family:Hanken;font-weight:500;src:url(${font('hanken-grotesk-latin-500-normal.woff2')})}
@font-face{font-family:Hanken;font-weight:600;src:url(${font('hanken-grotesk-latin-600-normal.woff2')})}
@font-face{font-family:DMMono;font-weight:500;src:url(${font('dm-mono-latin-500-normal.woff2')})}
:root{--navy:#14202e;--navy2:#1d2b3d;--cream:#f3f0ea;--paper:#f8f6f1;--gold:#d6b984;--gold-d:#a5814c;--ink:#14202e;--muted:#4b5666}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1200px;height:900px;overflow:hidden}
.card{width:1200px;height:900px;position:relative;overflow:hidden;font-family:Hanken,sans-serif}
.col{display:flex;flex-direction:column;height:100%}
.eyebrow{display:flex;align-items:center;gap:18px;font-family:DMMono;font-weight:500;text-transform:uppercase;white-space:nowrap;color:var(--gold-d)}
.eyebrow i{display:block;width:40px;height:1.5px;background:currentColor;flex:none}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
h1{font-family:Marcellus;font-weight:400;text-wrap:balance}
.dek{text-wrap:pretty}
.pill{align-self:flex-start;display:inline-flex;align-items:center;gap:12px;background:var(--gold);color:var(--navy);font-weight:600;border-radius:999px;white-space:nowrap}
.pill svg{width:20px;height:20px}
.foot{display:flex;align-items:flex-end;justify-content:space-between;border-top:1px solid}
.brand{font-family:Marcellus;letter-spacing:.06em;line-height:1}
.url{font-family:DMMono;font-weight:500;letter-spacing:.24em;text-transform:uppercase;color:var(--gold-d);margin-top:12px}

/* ---- full-width type card ---- */
.type{background:radial-gradient(120% 90% at 85% 10%,#22334a 0%,var(--navy) 60%);color:var(--cream)}
.type .frame{position:absolute;inset:28px;border:1px solid rgba(214,185,132,.32);pointer-events:none}
.type .wm{position:absolute;right:-60px;bottom:-250px;font-family:Marcellus;font-size:760px;line-height:1;color:var(--gold);opacity:.045}
.type .col{padding:92px 96px 84px;position:relative}
.type .eyebrow{font-size:18px;letter-spacing:.3em;color:var(--gold)}
.type h1{font-size:96px;line-height:1.04;max-width:960px}
.type .dek{font-size:32px;line-height:1.45;color:rgba(243,240,234,.78);max-width:860px;margin-top:34px}
.type .foot{border-color:rgba(214,185,132,.28);padding-top:34px}
.type .brand{font-size:32px}
.type .url{font-size:15px;color:var(--gold)}
.type .pill{font-size:23px;padding:19px 32px}

/* ---- split card: text left, picture right ---- */
.split{display:grid;grid-template-columns:600px 600px}
.split .col{padding:76px 64px 64px 72px}
.split .eyebrow{font-size:16px;letter-spacing:.26em}
.split h1{font-size:70px;line-height:1.06}
.split .dek{font-size:27px;line-height:1.45;margin-top:28px}
.split .pill{font-size:21px;padding:17px 28px;margin-top:40px}
.split .foot{padding-top:30px}
.split .brand{font-size:27px}
.split .url{font-size:13px}
.split.light .text{background:var(--cream);color:var(--ink)}
.split.light .dek{color:var(--muted)}
.split.light .foot{border-color:rgba(20,32,46,.14)}
.split.dark .text{background:var(--navy);color:var(--cream)}
.split.dark .eyebrow,.split.dark .url{color:var(--gold)}
.split.dark .dek{color:rgba(243,240,234,.76)}
.split.dark .foot{border-color:rgba(214,185,132,.28)}
.split.light .pill{background:var(--navy);color:var(--cream)}

.pic{position:relative;overflow:hidden}
.pic.photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 22%}
.pic.photo:after{content:"";position:absolute;inset:0;box-shadow:inset 1px 0 0 rgba(214,185,132,.5)}
.pic.shop{background:radial-gradient(80% 60% at 50% 45%,#ffffff 0%,var(--paper) 70%);border-left:6px solid var(--gold)}
.pic.shop .stage{position:absolute;left:40px;right:40px;top:56px;bottom:110px}
.pic.shop img{position:absolute;mix-blend-mode:multiply;object-fit:contain}
.pic.shop .cap{position:absolute;left:0;right:0;bottom:52px;text-align:center;font-family:DMMono;font-weight:500;font-size:14px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold-d)}
.pic.shop .cap b{display:block;width:40px;height:1.5px;background:var(--gold);margin:0 auto 18px}
.pic.giftp{background:radial-gradient(90% 70% at 50% 40%,#2a3d56 0%,var(--navy) 70%)}
.gc{position:absolute;left:50%;top:46%;width:440px;height:277px;transform:translate(-50%,-50%) rotate(-7deg);border-radius:22px;
  background:linear-gradient(135deg,#f1dcae 0%,#d6b984 38%,#b28a52 62%,#e9cf9a 100%);box-shadow:0 40px 80px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.6);color:var(--navy);padding:34px 38px;display:flex;flex-direction:column}
.gc .q{font-family:Marcellus;font-size:30px;letter-spacing:.08em;line-height:1.1}
.gc .q small{display:block;font-family:DMMono;font-size:12px;letter-spacing:.34em;margin-top:8px;opacity:.8}
.gc .lbl{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end}
.gc .lbl span{font-family:DMMono;font-weight:500;font-size:14px;letter-spacing:.32em}
.gc .lbl strong{font-family:Marcellus;font-weight:400;font-size:44px;line-height:1}
.gc2{transform:translate(-44%,-30%) rotate(5deg);background:linear-gradient(135deg,#22344b,#14202e);box-shadow:0 30px 60px rgba(0,0,0,.4);opacity:.95}
.pic.giftp .cap{position:absolute;left:0;right:0;bottom:52px;text-align:center;font-family:DMMono;font-weight:500;font-size:14px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold)}
`;

const ARROW = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 10h11M11 5l5 5-5 5"/></svg>';
const PHONE = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.2 15.2 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>';
const pill = c => `<span class="pill">${c.call ? PHONE : ''}${esc(c.cta)}${c.call ? '' : ARROW}</span>`;
const eyebrow = c => `<div class="eyebrow" data-a="${esc(c.theme + ' · ' + c.geo)}" data-b="${esc(c.theme)}"><i></i><span>${esc(c.theme + ' · ' + c.geo)}</span></div>`;
const foot = (c, withPill) => `<div class="foot"><div><div class="brand">THE Q SALON FOR MEN</div><div class="url">theqsalonsrq.com</div></div>${withPill ? pill(c) : ''}</div>`;

function productStage(list) {
  const n = list.length, W = 520, H = 734; // stage size
  let boxes;
  if (n === 1) boxes = [[(W - 470) / 2, (H - 470) / 2, 470]];
  else if (n === 2) boxes = [[0, 10, 350], [W - 350, H - 360, 350]];
  else if (n === 3) { const t = (H - 340 - 30 - 250) / 2; boxes = [[(W - 340) / 2, t, 340], [W / 2 - 260, t + 370, 250], [W / 2 + 10, t + 370, 250]]; }
  else { const s = 250, g = 20, t = (H - 2 * s - g) / 2, l = (W - 2 * s - g) / 2; boxes = [[l, t, s], [l + s + g, t, s], [l, t + s + g, s], [l + s + g, t + s + g, s]]; }
  return list.map((p, i) => { const [x, y, s] = boxes[i]; return `<img src="${img('shop/' + p + '.jpg')}" style="left:${x}px;top:${y}px;width:${s}px;height:${s}px">`; }).join('');
}

function html(c) {
  if (c.kind === 'type') {
    return `<div class="card type"><div class="frame"></div><div class="col">${eyebrow(c)}
      <div class="mid"><h1 data-max="2">${title(c.title)}</h1><p class="dek">${esc(c.dek)}</p></div>${foot(c, true)}</div></div>`;
  }
  const tone = c.kind === 'product' ? 'dark' : 'light';
  let pic;
  if (c.kind === 'product') pic = `<div class="pic shop"><div class="stage">${productStage(c.products)}</div><div class="cap"><b></b>Susy's picks · The Q Shop</div></div>`;
  else if (c.kind === 'susy') pic = `<div class="pic photo"><img src="${img(c.photo + '.jpg')}"></div>`;
  else pic = `<div class="pic giftp"><div class="gc gc2"></div><div class="gc"><div class="q">THE Q SALON<small>FOR MEN · SARASOTA</small></div><div class="lbl"><span>GIFT CARD</span><strong>$50+</strong></div></div><div class="cap">Any service or product</div></div>`;
  return `<div class="card split ${tone}"><div class="text"><div class="col">${eyebrow(c)}
    <div class="mid"><h1 data-max="3">${title(c.title)}</h1><p class="dek">${esc(c.dek)}</p>${pill(c)}</div>${foot(c, false)}</div></div>${pic}</div>`;
}

// Fit rules: eyebrow on one line (drop the area name if needed), headline within its line limit.
const FIT = `(() => {
  const eb = document.querySelector('.eyebrow'), sp = eb.querySelector('span');
  const room = () => eb.parentElement.clientWidth - parseFloat(getComputedStyle(eb.parentElement).paddingLeft) - parseFloat(getComputedStyle(eb.parentElement).paddingRight);
  if (eb.scrollWidth > room()) sp.textContent = eb.dataset.b;
  let ls = parseFloat(getComputedStyle(eb).letterSpacing);
  while (eb.scrollWidth > room() && ls > 2) { ls -= 0.5; eb.style.letterSpacing = ls + 'px'; }
  const h = document.querySelector('h1'), max = +h.dataset.max;
  let fs = parseFloat(getComputedStyle(h).fontSize);
  const lines = () => Math.round(h.getBoundingClientRect().height / (fs * 1.06));
  while (lines() > max && fs > 40) { fs -= 2; h.style.fontSize = fs + 'px'; }
  const mid = document.querySelector('.mid'); let over = mid.scrollHeight > mid.clientHeight + 1;
  return { lines: lines(), fs, over, eyebrow: sp.textContent };
})()`;

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 1 });
const report = [];
for (const c of cards) {
  if (only.length && !only.includes(c.day)) continue;
  const tmp = path.join(HERE, 'out', '_card.html');
  fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body>${html(c)}</body></html>`);
  await page.goto('file://' + tmp, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const r = await page.evaluate(FIT);
  const file = path.join(HERE, 'out', 'q' + String(c.day).padStart(2, '0') + '.png');
  await page.screenshot({ path: file });
  report.push({ day: c.day, kind: c.kind, ...r });
}
await browser.close();
fs.writeFileSync(path.join(HERE, 'out', 'report.json'), JSON.stringify(report, null, 1));
const flagged = report.filter(r => r.over || r.fs < (r.kind === 'type' ? 96 : 70));
console.log('rendered', report.length, 'flagged', JSON.stringify(flagged));
