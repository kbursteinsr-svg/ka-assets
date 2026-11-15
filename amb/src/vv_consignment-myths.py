#!/usr/bin/env python3
"""
Vintage Vault - remake of the page's best post (385 views): three consignment
myths. House format (getripping-derived) in VV's ivory/burgundy/gold palette,
Fraunces for headings. Myth struck through, truth revealed, one at a time.
Page name verified against Meta: "Vintage Vault" - no article. Do not "fix" it.
1080x1920, 30fps, silent. Comment-based CTA.
"""
import base64, pathlib, subprocess

D   = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/vv2')
FB  = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/bir/fonts')
VF  = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/vvfonts')
OUT = D/'out'; OUT.mkdir(parents=True, exist_ok=True)

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

FONTS = "".join(
  f"@font-face{{font-family:'Inter';src:url(data:font/ttf;base64,{b64(FB/f)}) "
  f"format('truetype');font-weight:{w};font-style:normal}}"
  for f, w in [('Inter-Regular.ttf',400), ('Inter-Medium.ttf',500),
               ('Inter-SemiBold.ttf',600), ('Inter-Bold.ttf',700)]
) + (f"@font-face{{font-family:'Fraunces';src:url(data:font/ttf;base64,"
     f"{b64(VF/'Fraunces-Bold.ttf')}) format('truetype');font-weight:700}}")

CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --paper:#FBF6EE; --line:rgba(126,42,59,.055);
  --ink:#2A1A1E; --dim:rgba(42,26,30,.42);
  --burg:#7E2A3B; --gold:#B68A4E; --blush:#F3DCD3; --sand:#F2E4D4;
  --card:#FFFFFF; --edge:rgba(126,42,59,.12);
  --shadow:0 34px 70px rgba(90,45,40,.15), 0 4px 12px rgba(90,45,40,.06);
}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--paper)}
body{font-family:'Inter';color:var(--ink);-webkit-font-smoothing:antialiased}
#grid{position:absolute;inset:0;
  background-image:linear-gradient(var(--line) 1px,transparent 1px),
                   linear-gradient(90deg,var(--line) 1px,transparent 1px);
  background-size:70px 70px}
.stage{position:absolute;inset:0;opacity:0}

.cap{position:absolute;top:228px;left:70px;right:70px;text-align:center;
  font-weight:500;font-size:68px;line-height:90px;letter-spacing:-.018em;color:var(--dim)}
.cap b{font-weight:700;color:var(--ink)}
.cap .hl{font-weight:700;color:var(--ink);background:var(--sand);
  box-shadow:0 0 0 10px var(--sand);border-radius:3px}
.cap .fr{font-family:'Fraunces';font-weight:700;color:var(--burg)}

.card{position:absolute;background:var(--card);border:1px solid var(--edge);
  border-radius:26px;box-shadow:var(--shadow)}
.ctitle{font:600 24px/1 'Inter';color:var(--dim);letter-spacing:.14em;text-transform:uppercase}

.myth{padding:30px 36px 34px}
.myth .lab{display:inline-block;font:700 23px/1 'Inter';letter-spacing:.13em;
  text-transform:uppercase;color:#fff;background:var(--burg);
  padding:12px 18px;border-radius:999px}
.myth .txt{font:700 46px/1.34 'Inter';letter-spacing:-.018em;margin-top:20px}
.myth .txt span{display:inline-block;position:relative}
.myth.off .txt{color:var(--dim)}
.myth.off .txt span:after{content:'';position:absolute;left:-9px;right:-9px;top:52%;
  height:8px;background:var(--burg);border-radius:4px}

.truth{padding:30px 36px 36px;border-top:1px solid var(--edge);background:#FDFaf5;
  border-radius:0 0 26px 26px}
.truth .lab{display:inline-block;font:700 23px/1 'Inter';letter-spacing:.13em;
  text-transform:uppercase;color:#4A3312;background:var(--gold);
  padding:12px 18px;border-radius:999px}
.truth .txt{font:500 38px/1.44 'Inter';margin-top:20px;color:var(--ink)}

.num{font-family:'Fraunces';font-weight:700;font-size:40px;color:var(--gold)}
.pill{display:inline-flex;align-items:center;background:var(--burg);color:#fff;
  font:700 31px/1 'Inter';padding:20px 34px;border-radius:999px;
  box-shadow:0 14px 30px rgba(126,42,59,.26)}
.pill.ghost{background:transparent;color:var(--burg);border:2px solid var(--gold)}
.note{font:500 27px/1.45 'Inter';color:var(--dim)}

.foot{position:absolute;left:70px;right:70px;bottom:92px;display:flex;
  justify-content:space-between;align-items:baseline}
.brand{font:700 36px/1 'Fraunces';letter-spacing:-.01em}
.meta{font:500 25px/1 'Inter';color:var(--dim)}
"""

MYTHS = [
  ("01", ["It's only worth it for", "designer labels"],
   "Quality everyday pieces sell too &mdash; denim,<br>outerwear and bags all move."),
  ("02", ["You'll wait months", "to see money"],
   "You're paid once your item sells and the<br>buyer's return window closes. We list fast."),
  ("03", ["They'll lowball you"],
   "You get an honest, realistic range up front,<br>in writing, before anything is listed."),
]

def myth_scene(n, lines, truth, start, end):
    # each line carries its own strike, so a two-line myth reads as crossed out
    myth = "<br>".join(f"<span>{l}</span>" for l in lines)
    return dict(s=start, e=end, h=f"""
  <div class="cap"><span class="num">{n}</span><br>What people<br><b>assume</b></div>
  <div class="card" data-rise="1" style="left:90px;top:650px;width:900px">
    <div class="myth off"><div><span class="lab">Myth</span></div>
      <div class="txt">{myth}</div></div>
    <div class="truth" data-reveal="1"><div><span class="lab">Truth</span></div>
      <div class="txt">{truth}</div></div>
  </div>""")

S = [
 dict(s=0.0, e=3.8, h="""
  <div class="cap">Three things people get<br>wrong about <span class="fr">consignment</span></div>
  <div class="card" data-rise="1" style="left:160px;top:720px;width:760px;padding-bottom:36px">
    <div style="padding:34px 36px 0"><div class="ctitle">Sarasota &amp; Bradenton</div></div>
    <div style="padding:22px 36px 0;font:700 52px/1.18 'Fraunces';color:var(--burg)">
      And what's<br>actually true.</div>
    <div style="padding:22px 36px 0" class="note">
      We hear all three every week.</div>
  </div>"""),
 myth_scene(*MYTHS[0], 3.8, 8.6),
 myth_scene(*MYTHS[1], 8.6, 13.4),
 myth_scene(*MYTHS[2], 13.4, 18.2),
 dict(s=18.2, e=23.0, h="""
  <div class="cap">Follow <b>Vintage Vault</b><br>for what your pieces<br>are actually worth</div>
  <div style="position:absolute;left:70px;right:70px;top:800px;text-align:center">
    <span class="pill">Comment WORTH</span></div>
  <div style="position:absolute;left:140px;right:140px;top:930px;text-align:center">
    <span class="note">Tell us what you've got and we'll give you<br>
    an honest range &mdash; free, no obligation.</span></div>"""),
]

def build(scenes):
    body = "".join(
      f'<div class="stage" data-s="{x["s"]}" data-e="{x["e"]}">{x["h"]}'
      f'<div class="foot"><div class="brand">Vintage Vault</div>'
      f'<div class="meta">Consignment &amp; resale</div></div></div>' for x in scenes)
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
    // the truth panel arrives after the myth has been struck out
    el.querySelectorAll('[data-reveal]').forEach(function(c){{
      var p=ease(Math.min(1,Math.max(0,(L-0.30)/0.30)));
      c.style.opacity=p;
      c.style.transform='translateY('+((1-p)*20)+'px)';
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
mp4 = D/'VintageVault_consignment-myths.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(FPS),'-i',f'{OUT}/f%05d.jpg',
  '-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p',
  '-vf','scale=1080:1920','-movflags','+faststart', str(mp4)], check=True)
print('built', mp4)
