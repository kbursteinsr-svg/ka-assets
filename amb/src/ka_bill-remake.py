#!/usr/bin/env python3
"""
Kris Anthony — remake of the page's only true outlier.
Original: "Bill had an idea and a script - no camera, no editor, no crew."
1,045 views vs a page median around 165. House format (getripping-derived).
1080x1920, 30fps, silent by design - trending audio goes on in the composer.
"""
import base64, pathlib, subprocess

D   = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/ka')
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
  --paper:#FAFAF9; --line:rgba(26,20,14,.055);
  --ink:#121212; --dim:rgba(18,18,18,.40);
  --amber:#9D5D23; --amberlt:#C8832F; --sand:#F0E4D2; --tan:#DBC7A9;
  --warn:#DF305A; --card:#FFFFFF; --edge:rgba(40,30,20,.09);
  --shadow:0 34px 70px rgba(70,52,34,.16), 0 4px 12px rgba(70,52,34,.06);
}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--paper)}
body{font-family:'Inter';color:var(--ink);-webkit-font-smoothing:antialiased}
#grid{position:absolute;inset:0;
  background-image:linear-gradient(var(--line) 1px,transparent 1px),
                   linear-gradient(90deg,var(--line) 1px,transparent 1px);
  background-size:70px 70px}
.stage{position:absolute;inset:0;opacity:0}

.cap{position:absolute;top:232px;left:70px;right:70px;text-align:center;
  font-weight:500;font-size:70px;line-height:92px;letter-spacing:-.018em;color:var(--dim)}
.cap b{font-weight:700;color:var(--ink)}
.cap .hl{font-weight:700;color:var(--ink);background:var(--sand);
  box-shadow:0 0 0 10px var(--sand);border-radius:3px}

.card{position:absolute;background:var(--card);border:1px solid var(--edge);
  border-radius:26px;box-shadow:var(--shadow)}
.chead{display:flex;align-items:center;gap:13px;padding:26px 32px 0}
.dot{width:13px;height:13px;border-radius:50%}
.ctitle{font:600 25px/1 'Inter';color:var(--dim);letter-spacing:.07em;text-transform:uppercase}

/* a page of script, with ruled lines */
.doc{padding:28px 34px 34px}
.doc .ln{height:15px;border-radius:999px;background:rgba(40,30,20,.085);margin-top:19px}
.doc .ln.s{width:52%} .doc .ln.m{width:78%} .doc .ln.l{width:94%}
.doc .hd{font:700 40px/1.2 'Inter';letter-spacing:-.02em;margin-bottom:8px}

/* the three things you don't need */
.need{position:absolute;width:290px;background:var(--card);border:1px solid var(--edge);
  border-radius:22px;box-shadow:var(--shadow);padding:30px 26px;text-align:center}
.need .ic{font:800 56px/1 'Inter';color:var(--dim)}
.need .nm{font:700 34px/1 'Inter';margin-top:18px;position:relative;display:inline-block}
.need.off .nm:after{content:'';position:absolute;left:-12px;right:-12px;top:50%;
  height:9px;background:var(--warn);border-radius:5px}
.need.off{opacity:.62}
.need .x{position:absolute;top:-16px;right:-16px;width:52px;height:52px;border-radius:50%;
  background:var(--warn);color:#fff;font:700 30px/52px 'Inter';text-align:center;
  box-shadow:0 10px 22px rgba(223,48,90,.34)}

/* render / result card */
.player{position:relative;border-radius:20px;overflow:hidden;background:#15110D;
  height:330px;display:flex;align-items:center;justify-content:center;margin:26px 32px 0}
.player .play{width:104px;height:104px;border-radius:50%;background:rgba(255,255,255,.93);
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 14px 34px rgba(0,0,0,.4)}
.player .tri{width:0;height:0;border-left:34px solid #15110D;border-top:21px solid transparent;
  border-bottom:21px solid transparent;margin-left:9px}
.bar{height:16px;border-radius:999px;background:rgba(40,30,20,.08);overflow:hidden;margin:0 32px}
.bar i{display:block;height:100%;border-radius:999px;background:var(--amberlt)}
.rowline{display:flex;justify-content:space-between;align-items:center;padding:24px 32px}
.rowline .k{font:500 30px/1 'Inter';color:var(--dim)}
.rowline .v{font:700 34px/1 'Inter'}
.big{font:800 150px/1 'Inter';letter-spacing:-.045em}
.unit{font:700 42px/1 'Inter';color:var(--dim);margin-left:10px}

.pill{display:inline-flex;align-items:center;gap:12px;background:var(--amberlt);
  color:#fff;font:700 30px/1 'Inter';padding:19px 32px;border-radius:999px;
  box-shadow:0 14px 28px rgba(157,93,35,.32)}
.pill.ghost{background:var(--card);color:var(--ink);border:2px solid var(--edge);
  box-shadow:var(--shadow)}

.foot{position:absolute;left:70px;right:70px;bottom:92px;display:flex;
  justify-content:space-between;align-items:baseline}
.brand{font:800 34px/1 'Inter';letter-spacing:-.02em}
.meta{font:500 25px/1 'Inter';color:var(--dim)}
"""

S = [
 # 1 — the setup, kept verbatim from the winner
 dict(s=0.0, e=3.8, h="""
  <div class="cap">Bill had an idea<br>and <b>a script</b></div>
  <div class="card" data-rise="1" style="left:150px;top:660px;width:780px">
    <div class="chead">
      <div class="dot" style="background:#E8674F"></div>
      <div class="dot" style="background:#E8A93F"></div>
      <div class="dot" style="background:#C8832F"></div>
      <div class="ctitle" style="margin-left:10px">script · draft 1</div>
    </div>
    <div class="doc">
      <div class="hd">That was the whole<br>starting point.</div>
      <div class="ln l"></div><div class="ln m"></div><div class="ln l"></div>
      <div class="ln s"></div>
    </div>
  </div>"""),

 # 2 — the contrarian core: the three things he didn't have
 dict(s=3.8, e=8.6, h="""
  <div class="cap">No camera. No editor.<br><b>No crew.</b></div>
  <div class="need off" data-pop="1" style="left:75px;top:740px">
    <div class="x">&times;</div><div class="ic">CAM</div><div class="nm">Camera</div></div>
  <div class="need off" data-pop="2" style="left:395px;top:740px">
    <div class="x">&times;</div><div class="ic">EDIT</div><div class="nm">Editor</div></div>
  <div class="need off" data-pop="3" style="left:715px;top:740px">
    <div class="x">&times;</div><div class="ic">CREW</div><div class="nm">Crew</div></div>
  <div style="position:absolute;left:70px;right:70px;top:1130px;text-align:center">
    <span class="pill ghost">Everything people think they need first</span></div>"""),

 # 3 — the result
 dict(s=8.6, e=13.4, h="""
  <div class="cap">A finished video<br><span class="hl">in minutes</span></div>
  <div class="card" data-rise="1" style="left:120px;top:640px;width:840px;padding-bottom:30px">
    <div class="chead"><div class="ctitle">rendering</div></div>
    <div class="player"><div class="play"><div class="tri"></div></div></div>
    <div style="height:26px"></div>
    <div class="bar"><i data-fill="100"></i></div>
    <div class="rowline"><div class="k">Source</div><div class="v">One script</div></div>
    <div class="rowline" style="padding-top:0">
      <div class="k">People involved</div><div class="v">Just Bill</div></div>
  </div>
  <div style="position:absolute;left:70px;right:70px;top:1466px;text-align:center">
    <div class="big" style="font-size:134px">MINUTES</div>
    <div style="font:500 34px/1.4 'Inter';color:var(--dim);margin-top:16px">
      from the same script he started with</div>
  </div>"""),

 # 4 — CTA. Page name verified against Meta: "Kris Anthony"
 dict(s=13.4, e=18.0, h="""
  <div class="cap">Follow <b>Kris Anthony</b><br>for the AI tools that<br>actually finish the job</div>
  <div class="card" data-rise="1" style="left:160px;top:720px;width:760px;padding-bottom:30px">
    <div class="chead"><div class="ctitle">What Bill used</div></div>
    <div style="padding:22px 32px 0;font:700 46px/1.16 'Inter';letter-spacing:-.02em">
      Agent Opus</div>
    <div class="rowline" style="margin-top:14px">
      <div class="k">Script in, finished video out</div>
      <div class="v" style="color:var(--amber)">Free trial</div></div>
  </div>
  <div style="position:absolute;left:70px;right:70px;top:1180px;text-align:center">
    <span class="pill">Link in the comments</span></div>"""),
]

def build(scenes):
    body = "".join(
      f'<div class="stage" data-s="{x["s"]}" data-e="{x["e"]}">{x["h"]}'
      f'<div class="foot"><div class="brand">Kris Anthony</div>'
      f'<div class="meta">Building with AI, in public</div></div></div>' for x in scenes)
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
      var d=(+c.dataset.rise-1)*0.10;
      var p=ease(Math.min(1,Math.max(0,(L-d)/0.42)));
      c.style.transform='perspective(1600px) rotateX('+((1-p)*9)+'deg) translateY('
        +((1-p)*54)+'px)';
      c.style.opacity=Math.min(1,p*1.5);
    }});
    // the three cards strike through one at a time - that is the whole point
    el.querySelectorAll('[data-pop]').forEach(function(c){{
      var i=+c.dataset.pop-1, d=0.14+i*0.17;
      var p=ease(Math.min(1,Math.max(0,(L-d)/0.26)));
      c.style.transform='translateY('+((1-p)*46)+'px) scale('+(0.92+p*0.08)+')';
      c.style.opacity=p;
    }});
    el.querySelectorAll('[data-count]').forEach(function(n){{
      var tgt=+n.dataset.count, dec=+(n.dataset.dec||0);
      n.textContent=(tgt*ease(Math.min(1,L/0.6))).toFixed(dec);
    }});
    el.querySelectorAll('[data-fill]').forEach(function(f){{
      f.style.width=(ease(Math.min(1,Math.max(0,(L-0.15)/0.55)))*+f.dataset.fill)+'%';
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
mp4 = D/'KrisAnthony_bill-remake.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(FPS),'-i',f'{OUT}/f%05d.jpg',
  '-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p',
  '-vf','scale=1080:1920','-movflags','+faststart', str(mp4)], check=True)
print('built', mp4)
