#!/usr/bin/env python3
"""
Top Tech Drops - Mooncool price drop, rescued from a 0-view album into a reel.
House format (getripping-derived) in TTD's dark/cyan palette. Bar Race structure:
bars ranked by what you actually save. 1080x1920, 30fps, silent.
Figures are the merchant's listed prices as captured 2026-11-14 and are on screen
with that date, because listed prices move.
"""
import base64, pathlib, subprocess

D   = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/ttd2')
FB  = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/bir/fonts')
OUT = D/'out'; OUT.mkdir(parents=True, exist_ok=True)

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

FONTS = "".join(
  f"@font-face{{font-family:'Inter';src:url(data:font/ttf;base64,{b64(FB/f)}) "
  f"format('truetype');font-weight:{w};font-style:normal}}"
  for f, w in [('Inter-Regular.ttf',400), ('Inter-Medium.ttf',500),
               ('Inter-SemiBold.ttf',600), ('Inter-Bold.ttf',700),
               ('Inter-ExtraBold.ttf',800)])

CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0A0D11; --line:rgba(140,190,220,.055);
  --ink:#F2F6F8; --dim:rgba(242,246,248,.44);
  --cyan:#3FB6E8; --cyan2:#7FD4F5; --deep:#12303E;
  --card:#151A20; --edge:rgba(140,190,220,.14);
  --shadow:0 34px 70px rgba(0,0,0,.55), 0 4px 12px rgba(0,0,0,.4);
}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--bg)}
body{font-family:'Inter';color:var(--ink);-webkit-font-smoothing:antialiased}
#grid{position:absolute;inset:0;
  background-image:linear-gradient(var(--line) 1px,transparent 1px),
                   linear-gradient(90deg,var(--line) 1px,transparent 1px);
  background-size:70px 70px}
.stage{position:absolute;inset:0;opacity:0}

.cap{position:absolute;top:224px;left:66px;right:66px;text-align:center;
  font-weight:500;font-size:70px;line-height:92px;letter-spacing:-.018em;color:var(--dim)}
.cap b{font-weight:700;color:var(--ink)}
.cap .hl{font-weight:700;color:#06212C;background:var(--cyan);
  box-shadow:0 0 0 10px var(--cyan);border-radius:3px}

.card{position:absolute;background:var(--card);border:1px solid var(--edge);
  border-radius:26px;box-shadow:var(--shadow)}
.chead{display:flex;align-items:center;gap:13px;padding:26px 32px 0}
.ctitle{font:600 25px/1 'Inter';color:var(--dim);letter-spacing:.08em;text-transform:uppercase}

/* bar race rows */
.race{position:absolute;left:66px;right:66px;top:600px}
.row{margin-bottom:38px}
.row .top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:14px}
.row .nm{font:700 36px/1.1 'Inter';letter-spacing:-.015em}
.row .sv{font:800 44px/1 'Inter';color:var(--cyan)}
.track{height:34px;border-radius:999px;background:rgba(140,190,220,.09);overflow:hidden}
.track i{display:block;height:100%;border-radius:999px;
  background:linear-gradient(90deg,var(--deep),var(--cyan))}
.row .pr{display:flex;gap:18px;align-items:baseline;margin-top:13px}
.row .was{font:500 29px/1 'Inter';color:var(--dim);position:relative}
.row .was:after{content:'';position:absolute;left:-3px;right:-3px;top:52%;height:3px;
  background:rgba(242,246,248,.4)}
.row .now{font:700 33px/1 'Inter'}

.big{font:800 168px/1 'Inter';letter-spacing:-.05em;color:var(--cyan)}
.unit{font:700 42px/1 'Inter';color:var(--dim)}
.rowline{display:flex;justify-content:space-between;align-items:center;padding:24px 32px;
  border-top:1px solid rgba(140,190,220,.1)}
.rowline .k{font:500 30px/1 'Inter';color:var(--dim)}
.rowline .v{font:700 34px/1 'Inter'}

.pill{display:inline-flex;align-items:center;background:var(--cyan);color:#06212C;
  font:700 31px/1 'Inter';padding:20px 34px;border-radius:999px;
  box-shadow:0 14px 30px rgba(63,182,232,.3)}
.pill.ghost{background:transparent;color:var(--ink);border:2px solid var(--edge)}
.note{font:500 26px/1.4 'Inter';color:var(--dim)}

.foot{position:absolute;left:66px;right:66px;bottom:92px;display:flex;
  justify-content:space-between;align-items:baseline}
.brand{font:800 34px/1 'Inter';letter-spacing:-.02em}
.meta{font:500 25px/1 'Inter';color:var(--dim)}
"""

# saving drives the bar length - the race is "what do you actually keep"
ITEMS = [
  ("Mooncool TK2 PRO E-Trike", 720, 100.0, "$2,599.99", "$1,879.99"),
  ("POP Folding E-Bike",       620,  86.1, "$1,699.99", "$1,079.99"),
  ("Trike Cargo Trailer",      150,  20.8,   "$299.99",   "$149.99"),
  ("Bike/Trike Accessory Pack", 36,   5.0,   "$119.99",    "$83.99"),
]

rows = "".join(
  f'<div class="row" data-pop="{i+1}">'
  f'<div class="top"><div class="nm">{n}</div>'
  f'<div class="sv">&minus;$<span data-count="{s}">0</span></div></div>'
  f'<div class="track"><i data-fill="{w}"></i></div>'
  f'<div class="pr"><div class="was">{was}</div><div class="now">{now}</div></div></div>'
  for i, (n, s, w, was, now) in enumerate(ITEMS))

S = [
 dict(s=0.0, e=3.8, h="""
  <div class="cap">Mooncool quietly dropped<br>the TK2 PRO by <span class="hl">$720</span></div>
  <div class="card" data-rise="1" style="left:140px;top:700px;width:800px;padding-bottom:34px">
    <div class="chead"><div class="ctitle">Marked down on their site</div></div>
    <div style="padding:30px 32px 0;text-align:center">
      <span class="big" data-count="4">0</span></div>
    <div style="padding:6px 32px 0;text-align:center" class="note">
      items marked down, not just the trike</div>
  </div>"""),

 dict(s=3.8, e=11.0, h=f"""
  <div class="cap">Ranked by what<br>you actually <b>keep</b></div>
  <div class="race">{rows}</div>
  <div style="position:absolute;left:66px;right:66px;top:1500px;text-align:center">
    <span class="note">Listed prices as shown on the merchant's site, 14 Nov 2026</span></div>"""),

 dict(s=11.0, e=15.4, h="""
  <div class="cap">One code at checkout:<br><span class="hl">AFFMC5</span></div>
  <div class="card" data-rise="1" style="left:120px;top:720px;width:840px;padding-bottom:12px">
    <div class="chead"><div class="ctitle">Biggest drop</div></div>
    <div style="padding:22px 32px 26px;font:700 50px/1.14 'Inter';letter-spacing:-.02em">
      Mooncool TK2 PRO<br>Electric Trike</div>
    <div class="rowline"><div class="k">Was</div>
      <div class="v" style="color:var(--dim)">$2,599.99</div></div>
    <div class="rowline"><div class="k">Now</div>
      <div class="v" style="color:var(--cyan)">$1,879.99</div></div>
    <div class="rowline"><div class="k">New customers</div>
      <div class="v">Code AFFMC5</div></div>
  </div>"""),

 # Page name verified against Meta: "Top Tech Drops"
 dict(s=15.4, e=20.0, h="""
  <div class="cap">Follow <b>Top Tech Drops</b><br>for the tech deals<br>worth buying</div>
  <div style="position:absolute;left:66px;right:66px;top:760px;text-align:center">
    <span class="pill">Links in the comments</span></div>
  <div style="position:absolute;left:120px;right:120px;top:900px;text-align:center">
    <span class="note">All four links and the code are in the first comment.<br>
    Affiliate links &mdash; we may earn a commission at no extra cost to you.</span></div>"""),
]

def build(scenes):
    body = "".join(
      f'<div class="stage" data-s="{x["s"]}" data-e="{x["e"]}">{x["h"]}'
      f'<div class="foot"><div class="brand">Top Tech Drops</div>'
      f'<div class="meta">Tech worth the money</div></div></div>' for x in scenes)
    total = scenes[-1]['e']
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div id="grid"></div>{body}
<script>
window.TOTAL={total};
function ease(p){{return 1-Math.pow(1-p,3);}}
window.render=function(t){{
  var T=window.TOTAL*t;
  document.querySelectorAll('.stage').forEach(function(el){{
    var s=+el.dataset.s, e=+el.dataset.e, o=0;
    var inP=Math.min(1,Math.max(0,(T-s)/0.40));
    var outP=Math.min(1,Math.max(0,(e-T)/0.28));
    if(T>=s-0.5 && T<=e+0.1) o=Math.min(inP,outP);
    el.style.opacity=o;
    if(o<=0){{el.style.visibility='hidden';return;}}
    el.style.visibility='visible';
    var L=Math.min(1,Math.max(0,(T-s)/(e-s)));
    el.querySelectorAll('[data-rise]').forEach(function(c){{
      var p=ease(Math.min(1,Math.max(0,L/0.42)));
      c.style.transform='perspective(1600px) rotateX('+((1-p)*9)+'deg) translateY('
        +((1-p)*54)+'px)';
      c.style.opacity=Math.min(1,p*1.5);
    }});
    el.querySelectorAll('[data-pop]').forEach(function(c){{
      var i=+c.dataset.pop-1, d=0.05+i*0.11;
      var p=ease(Math.min(1,Math.max(0,(L-d)/0.24)));
      c.style.transform='translateY('+((1-p)*34)+'px)';
      c.style.opacity=p;
    }});
    el.querySelectorAll('[data-count]').forEach(function(n){{
      var tgt=+n.dataset.count;
      var row=n.closest('[data-pop]');
      var d=row?0.05+(+row.dataset.pop-1)*0.11:0;
      var p=ease(Math.min(1,Math.max(0,(L-d)/0.46)));
      n.textContent=Math.round(tgt*p);
    }});
    el.querySelectorAll('[data-fill]').forEach(function(f){{
      var row=f.closest('[data-pop]');
      var d=row?0.05+(+row.dataset.pop-1)*0.11:0;
      var p=ease(Math.min(1,Math.max(0,(L-d)/0.5)));
      f.style.width=(p*+f.dataset.fill)+'%';
    }});
  }});
}};
window.render(0);
</script></body></html>"""

hp = D/'reel.html'; hp.write_text(build(S))
TOTAL = S[-1]['e']; FPS = 30
(D/'render.js').write_text(f"""
const {{chromium}}=require('playwright');
(async()=>{{const b=await chromium.launch();
 const p=await b.newPage({{viewport:{{width:1080,height:1920}},deviceScaleFactor:1}});
 await p.goto('file://{hp}',{{waitUntil:'load'}}); await p.waitForTimeout(700);
 const n=Math.round({TOTAL}*{FPS});
 for(let i=0;i<n;i++){{await p.evaluate(t=>window.render(t), i/(n-1));
  await p.screenshot({{path:'{OUT}/f'+String(i).padStart(5,'0')+'.jpg',quality:95,type:'jpeg'}});}}
 console.log('frames',n); await b.close();}})();
""")
subprocess.run(['node', str(D/'render.js')], check=True)
mp4 = D/'TopTechDrops_mooncool-price-drop.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(FPS),'-i',f'{OUT}/f%05d.jpg',
  '-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p',
  '-vf','scale=1080:1920','-movflags','+faststart', str(mp4)], check=True)
print('built', mp4)
