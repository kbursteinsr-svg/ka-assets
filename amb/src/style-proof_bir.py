#!/usr/bin/env python3
"""
Style proof — @getripping format, rebuilt in our own pipeline.
Build It Right content. 1080x1920, 30fps, music-ready (silent).
Everything here is HTML + CSS 3D + Playwright. No new tools.
"""
import base64, pathlib, subprocess

D   = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/gr')
FB  = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/bir/fonts')
IMG = pathlib.Path('/home/claude/ka-assets/amb/bir')
OUT = D/'out'; OUT.mkdir(parents=True, exist_ok=True)

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

FONTS = "".join(
  f"@font-face{{font-family:'Inter';src:url(data:font/ttf;base64,{b64(FB/f)}) "
  f"format('truetype');font-weight:{w};font-style:normal}}"
  for f, w in [('Inter-Regular.ttf',400), ('Inter-Medium.ttf',500),
               ('Inter-SemiBold.ttf',600), ('Inter-Bold.ttf',700),
               ('Inter-ExtraBold.ttf',800)])

DEWALT = b64(IMG/'dewalt-20v-9tool.jpg')

CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --paper:#FAFAF9; --line:rgba(26,20,14,.055);
  --ink:#121212; --dim:rgba(18,18,18,.40);
  --amber:#9D5D23; --amberlt:#C8832F; --tan:#DBC7A9; --sand:#F0E4D2;
  --warn:#DF305A; --card:#FFFFFF; --edge:rgba(40,30,20,.09);
  --shadow:0 34px 70px rgba(70,52,34,.16), 0 4px 12px rgba(70,52,34,.06);
}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--paper)}
body{font-family:'Inter';color:var(--ink);-webkit-font-smoothing:antialiased}

/* graph-paper ground, measured off the reference at ~70px cells */
#grid{position:absolute;inset:0;
  background-image:linear-gradient(var(--line) 1px,transparent 1px),
                   linear-gradient(90deg,var(--line) 1px,transparent 1px);
  background-size:70px 70px}

.stage{position:absolute;inset:0;opacity:0}

/* ---- caption band: top-anchored, two weights on one line ---- */
.cap{position:absolute;top:232px;left:70px;right:70px;text-align:center;
  font-weight:500;font-size:70px;line-height:92px;letter-spacing:-.018em;
  color:var(--dim)}
.cap b{font-weight:700;color:var(--ink)}
.cap .hl{font-weight:700;color:var(--ink);background:var(--sand);
  box-shadow:0 0 0 10px var(--sand);border-radius:3px}
.cap .hlw{font-weight:700;color:#fff;background:var(--warn);
  box-shadow:0 0 0 10px var(--warn);border-radius:3px}

/* ---- the 3D deck ---- */
.deck{position:absolute;left:50%;top:680px;width:980px;margin-left:-490px;
  transform-style:preserve-3d}
.tile{position:absolute;background:var(--card);border:1px solid var(--edge);
  border-radius:18px;box-shadow:var(--shadow);padding:22px 24px}
.tile .tl{font:600 22px/1 'Inter';color:var(--dim);letter-spacing:.09em;
  text-transform:uppercase}
.tile .tn{font:800 54px/1 'Inter';margin-top:14px;letter-spacing:-.03em}
.tile.on{border-color:var(--amberlt);box-shadow:0 0 0 3px rgba(200,131,47,.22),var(--shadow)}
.tile.on .tn{color:var(--amber)}

.card{position:absolute;background:var(--card);border:1px solid var(--edge);
  border-radius:26px;box-shadow:var(--shadow)}
.chead{display:flex;align-items:center;gap:14px;padding:26px 32px 0}
.dot{width:14px;height:14px;border-radius:50%}
.ctitle{font:600 26px/1 'Inter';color:var(--dim);letter-spacing:.06em;text-transform:uppercase}

.row{display:flex;justify-content:space-between;align-items:center;
  padding:26px 32px;border-top:1px solid rgba(40,30,20,.07)}
.row .k{font:500 32px/1 'Inter';color:var(--dim)}
.row .v{font:700 34px/1 'Inter'}
.strike{position:relative;color:rgba(18,18,18,.78)}
.strike:after{content:'';position:absolute;left:-14px;right:-14px;top:52%;
  height:12px;background:var(--warn);border-radius:6px}
.mlab{display:flex;justify-content:space-between;padding:12px 32px 0;
  font:600 22px/1 'Inter';color:var(--dim);letter-spacing:.05em;text-transform:uppercase}
.seg{display:flex;gap:6px;height:22px}
.seg span{flex:1;border-radius:999px;background:rgba(40,30,20,.08);overflow:hidden}
.seg span i{display:block;height:100%;border-radius:999px;background:var(--warn)}

.big{font:800 180px/1 'Inter';letter-spacing:-.045em}
.unit{font:700 46px/1 'Inter';color:var(--dim);margin-left:10px}

.meter{height:22px;border-radius:999px;background:rgba(40,30,20,.08);overflow:hidden}
.meter i{display:block;height:100%;border-radius:999px;background:var(--amberlt)}
.meter.red i{background:var(--warn)}

.pill{display:inline-flex;align-items:center;gap:12px;background:var(--amberlt);
  color:#fff;font:700 30px/1 'Inter';padding:18px 30px;border-radius:999px;
  box-shadow:0 14px 28px rgba(157,93,35,.32)}
.pill.ghost{background:var(--card);color:var(--ink);border:2px solid var(--edge);
  box-shadow:var(--shadow)}
.pill.warn{background:var(--warn);box-shadow:0 14px 28px rgba(223,48,90,.3)}

.shot{position:absolute;background:#fff;border:1px solid var(--edge);
  border-radius:26px;box-shadow:var(--shadow);display:flex;align-items:center;
  justify-content:center;padding:26px}
.shot img{max-width:100%;max-height:100%;object-fit:contain}

/* brand footer, same on every scene */
.foot{position:absolute;left:70px;right:70px;bottom:92px;display:flex;
  justify-content:space-between;align-items:baseline}
.brand{font:800 34px/1 'Inter';letter-spacing:-.02em}
.meta{font:500 25px/1 'Inter';color:var(--dim)}
"""

# ---------------------------------------------------------------- scenes
S = [
 # 1 — the receding deck of lookalike kits
 dict(s=0.0, e=3.6, h="""
  <div class="cap">Most people pick a kit<br>by the <b>tool count</b></div>
  <div class="deck" data-deck="1">
""" + "".join(
      f'<div class="tile{" on" if i==4 else ""}" style="left:{(i%3)*340}px;'
      f'top:{(i//3)*220}px;width:300px;height:180px">'
      f'<div class="tl">Combo kit</div><div class="tn">{n}-TOOL</div></div>'
      for i, n in enumerate([5,7,9,6,9,8,12,9,10])) + """
  </div>"""),

 # 2 — the number that doesn't matter
 dict(s=3.6, e=7.6, h="""
  <div class="cap">That's the <span class="hlw">least useful</span><br>number on the box</div>
  <div class="card" data-rise="1" style="left:120px;top:660px;width:840px">
    <div class="chead">
      <div class="dot" style="background:#E8674F"></div>
      <div class="dot" style="background:#E8A93F"></div>
      <div class="dot" style="background:#C8832F"></div>
      <div class="ctitle" style="margin-left:10px">What the box says</div>
    </div>
    <div style="padding:30px 32px 10px;text-align:center">
      <span class="big strike">9</span><span class="unit">TOOLS</span>
    </div>
    <div class="row"><div class="k">Brushless motors</div><div class="v">Not stated</div></div>
    <div class="row"><div class="k">Battery size</div>
      <div class="v" style="color:var(--warn)">2.0Ah &times; 2</div></div>
    <div class="row" style="padding-bottom:34px">
      <div class="k">What that runs</div><div class="v">About 20 min</div></div>
  </div>"""),

 # 3 — the number that does
 dict(s=7.6, e=12.0, h="""
  <div class="cap">Two <span class="hl">4Ah</span> batteries beat<br>four 2Ah batteries</div>
  <div class="card" data-rise="1" style="left:70px;top:680px;width:450px;padding-bottom:34px">
    <div class="chead"><div class="ctitle">2 &times; 4.0Ah</div></div>
    <div style="padding:22px 32px 0"><span class="big" style="font-size:140px"
      data-count="8" data-dec="1">0.0</span><span class="unit">Ah</span></div>
    <div class="mlab"><span>Longest single run</span></div>
    <div style="padding:10px 32px 0"><div class="meter"><i data-fill="100"></i></div></div>
    <div style="padding:22px 32px 0;font:500 28px/1.4 'Inter';color:var(--dim)">
      Two packs. One charging<br>while you work.</div>
  </div>
  <div class="card" data-rise="2" style="left:560px;top:680px;width:450px;padding-bottom:34px">
    <div class="chead"><div class="ctitle">4 &times; 2.0Ah</div></div>
    <div style="padding:22px 32px 0"><span class="big" style="font-size:140px"
      data-count="8" data-dec="1">0.0</span><span class="unit">Ah</span></div>
    <div class="mlab"><span>Longest single run</span></div>
    <div style="padding:10px 32px 0"><div class="seg">
      <span><i data-fill="100"></i></span><span><i data-fill="100"></i></span>
      <span><i data-fill="100"></i></span><span><i data-fill="100"></i></span></div></div>
    <div style="padding:22px 32px 0;font:500 28px/1.4 'Inter';color:var(--dim)">
      Same total. Four swaps,<br>four trips to the charger.</div>
  </div>
  <div style="position:absolute;left:70px;right:70px;top:1380px;text-align:center">
    <span class="pill ghost">Same amp hours. Not the same day.</span></div>"""),

 # 4 — product + CTA
 dict(s=12.0, e=16.4, h=f"""
  <div class="cap">Follow <b>Build It Right</b> for tool<br>advice that holds up</div>
  <div class="shot" data-rise="1" style="left:250px;top:600px;width:580px;height:500px">
    <img src="data:image/jpeg;base64,{DEWALT}"></div>
  <div class="card" data-rise="2" style="left:160px;top:1150px;width:760px;padding-bottom:30px">
    <div class="chead"><div class="ctitle">Checks all three</div></div>
    <div style="padding:20px 32px 0;font:700 44px/1.18 'Inter';letter-spacing:-.02em">
      DEWALT 20V MAX<br>9-tool kit</div>
    <div class="row" style="margin-top:20px">
      <div class="k">Brushless &middot; two 4Ah &middot; charger</div>
      <div class="v" style="color:var(--amber)">$729.95</div></div>
  </div>
  <div style="position:absolute;left:70px;right:70px;top:1540px;text-align:center">
    <span class="pill">Link in the comments</span></div>"""),
]

def build(scenes):
    body = "".join(
      f'<div class="stage" data-s="{x["s"]}" data-e="{x["e"]}">{x["h"]}'
      f'<div class="foot"><div class="brand">Build It Right</div>'
      f'<div class="meta">Tool &amp; job advice, Florida</div></div></div>' for x in scenes)
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
    // local progress drives the motion INSIDE the scene — this is what
    // carries the energy in the reference, not fast cutting
    var L=Math.min(1,Math.max(0,(T-s)/(e-s))), E=ease(Math.min(1,L*1.7));
    el.querySelectorAll('[data-deck]').forEach(function(d){{
      var rx=18-E*5, ry=-11+E*5, ty=40-E*40;
      d.style.transform='perspective(1700px) rotateX('+rx+'deg) rotateY('+ry
        +'deg) translateY('+ty+'px) scale('+(0.94+E*0.05)+')';
    }});
    el.querySelectorAll('[data-rise]').forEach(function(c,i){{
      var d=(+c.dataset.rise-1)*0.10;
      var p=ease(Math.min(1,Math.max(0,(L-d)/0.42)));
      c.style.transform='perspective(1600px) rotateX('+((1-p)*9)+'deg) translateY('
        +((1-p)*54)+'px)';
      c.style.opacity=Math.min(1,p*1.5);
    }});
    el.querySelectorAll('[data-count]').forEach(function(n){{
      var tgt=+n.dataset.count, dec=+(n.dataset.dec||0);
      n.textContent=(tgt*ease(Math.min(1,L/0.55))).toFixed(dec);
    }});
    el.querySelectorAll('[data-fill]').forEach(function(f){{
      f.style.width=(ease(Math.min(1,Math.max(0,(L-0.18)/0.5)))*+f.dataset.fill)+'%';
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
mp4 = D/'STYLE-PROOF_build-it-right.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(FPS),'-i',f'{OUT}/f%05d.jpg',
  '-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p',
  '-vf','scale=1080:1920','-movflags','+faststart', str(mp4)], check=True)
print('built', mp4)
