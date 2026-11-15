#!/usr/bin/env python3
"""Vintage Vault — 'what makes old turquoise worth money' reel. 1080x1920, music-ready."""
import base64, pathlib, subprocess

D = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/vvreel')
FONTS = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/vvfonts')
IMG = pathlib.Path('/home/claude/ka-assets/amb/vv')
OUT = D/'out'; OUT.mkdir(parents=True, exist_ok=True)

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

FONT_CSS = f"""
@font-face{{font-family:'Fraunces';src:url(data:font/ttf;base64,{b64(FONTS/'Fraunces-Bold.ttf')}) format('truetype');font-weight:700}}
@font-face{{font-family:'Inter';src:url(data:font/ttf;base64,{b64(FONTS/'Inter-Regular.ttf')}) format('truetype');font-weight:400}}
@font-face{{font-family:'Inter';src:url(data:font/ttf;base64,{b64(FONTS/'Inter-Medium.ttf')}) format('truetype');font-weight:500}}
"""

CUFF   = b64(IMG/'navajo-kingman-cuff.jpg')
NECK   = b64(IMG/'navajo-pearl-necklace.jpg')

# Vintage Vault brand: ivory #FBF6EE, blush #F3DCD3, burgundy #7E2A3B, gold #B68A4E
CSS = FONT_CSS + """
*{margin:0;padding:0;box-sizing:border-box}
:root{--ivory:#FBF6EE;--blush:#F3DCD3;--burg:#7E2A3B;--gold:#B68A4E;--ink:#2A1A1E}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--ivory)}
body{font-family:'Inter',system-ui;color:var(--ink);-webkit-font-smoothing:antialiased}
.stage{position:absolute;inset:0;opacity:0}
.stage.dark{background:var(--ink);color:var(--ivory)}
.stage.burg{background:var(--burg);color:var(--ivory)}
.eyebrow{font:500 28px/1 'Inter';letter-spacing:.26em;text-transform:uppercase;color:var(--gold)}
.h{font:700 94px/1.04 'Fraunces';letter-spacing:-.015em}
.h.sm{font:700 74px/1.08 'Fraunces'}
.p{font:400 38px/1.5 'Inter';opacity:.84}
.pad{position:absolute;left:86px;right:86px}
.rule{height:2px;background:var(--gold);width:110px}
.num{font:700 46px/1 'Fraunces';color:var(--gold)}
.photo{position:absolute;left:0;right:0;display:flex;align-items:center;justify-content:center}
.photo img{max-width:880px;max-height:880px;object-fit:contain;border:3px solid var(--gold)}
.chip{display:inline-block;border:2px solid var(--gold);color:var(--gold);
  font:500 32px/1 'Inter';letter-spacing:.06em;padding:19px 32px;border-radius:999px;text-transform:uppercase}
.foot{position:absolute;left:86px;right:86px;bottom:94px;display:flex;justify-content:space-between;align-items:baseline}
.brand{font:700 36px/1 'Fraunces'}
.meta{font:400 26px/1 'Inter';opacity:.45}
.price{font:700 58px/1 'Fraunces';color:var(--gold)}
"""

SCENES = [
 dict(start=0.0, end=3.8, cls="burg", html="""
   <div class="pad" style="top:600px">
     <div class="eyebrow">Check the drawer</div>
     <div class="rule" style="margin:32px 0 44px"></div>
     <div class="h">Old turquoise<br>is worth more<br>than people<br>think.</div>
     <div class="p" style="margin-top:44px">Three things decide whether a piece is<br>worth forty dollars or four figures.</div>
   </div>"""),

 dict(start=3.8, end=8.4, cls="", html="""
   <div class="pad" style="top:470px">
     <div class="num">01</div>
     <div class="h sm" style="margin-top:20px">Is it signed?</div>
     <div class="p" style="margin-top:34px">Navajo and Zuni silversmiths stamp a hallmark
     inside the cuff. A known maker's mark can multiply the value of the same stone.</div>
   </div>"""),

 dict(start=8.4, end=13.0, cls="", html=f"""
   <div class="pad" style="top:300px">
     <div class="num">02</div>
     <div class="h sm" style="margin-top:20px">Natural or<br>stabilized?</div>
     <div class="p" style="margin-top:30px">Untreated stone is the one collectors chase.
     Stabilized turquoise is common and worth far less.</div>
   </div>
   <div class="photo" style="top:1000px;height:700px"><img style="max-height:700px;max-width:700px" src="data:image/jpeg;base64,{CUFF}"></div>"""),

 dict(start=13.0, end=17.6, cls="", html="""
   <div class="pad" style="top:470px">
     <div class="num">03</div>
     <div class="h sm" style="margin-top:20px">Weigh it</div>
     <div class="p" style="margin-top:34px">Old pieces were hand-worked in heavy-gauge
     sterling. Weight in grams is one of the first things a serious buyer asks for.</div>
   </div>"""),

 dict(start=17.6, end=22.4, cls="dark", html=f"""
   <div class="pad" style="top:230px">
     <div class="eyebrow">Listed right now</div>
   </div>
   <div class="photo" style="top:340px;height:880px"><img src="data:image/jpeg;base64,{NECK}"></div>
   <div class="pad" style="top:1300px">
     <div class="h sm">Vintage Navajo<br>sterling, 107 grams</div>
     <div style="margin-top:28px"><span class="price">$1,500</span></div>
     <div class="p" style="margin-top:18px;font-size:32px">Asking price on eBay today</div>
   </div>"""),

 dict(start=22.4, end=27.0, cls="burg", html="""
   <div class="pad" style="top:560px">
     <div class="eyebrow">Two ways in</div>
     <div class="rule" style="margin:32px 0 44px"></div>
     <div class="h sm">Shop the pieces<br>in the comments.<br><br>Or comment WORTH<br>and we'll tell you<br>what yours is.</div>
     <div style="margin-top:52px"><span class="chip">Follow Vintage Vault</span></div>
   </div>"""),
]

def build_html(scenes):
    body = "".join(
      f'<div class="stage {s["cls"]}" data-s="{s["start"]}" data-e="{s["end"]}">{s["html"]}'
      f'<div class="foot"><div class="brand">Vintage Vault</div>'
      f'<div class="meta">Sarasota &amp; Bradenton</div></div></div>' for s in scenes)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{body}
<script>
window.TOTAL={scenes[-1]['end']};
window.render=function(t){{
  var T=window.TOTAL*t;
  document.querySelectorAll('.stage').forEach(function(el){{
    var s=+el.dataset.s,e=+el.dataset.e,o=0,dy=0;
    if(T>=s-0.45&&T<=e+0.1){{
      var i=Math.min(1,Math.max(0,(T-s)/0.45));
      var ou=Math.min(1,Math.max(0,(e-T)/0.32));
      o=Math.min(i,ou); dy=(1-i)*22;
    }}
    el.style.opacity=o; el.style.transform='translateY('+dy+'px)';
  }});
}};
window.render(0);
</script></body></html>"""

html_path = D/'reel.html'; html_path.write_text(build_html(SCENES))
TOTAL = SCENES[-1]['end']; FPS = 30
(D/'render.js').write_text(f"""
const {{chromium}}=require('playwright');
(async()=>{{const b=await chromium.launch();
 const p=await b.newPage({{viewport:{{width:1080,height:1920}},deviceScaleFactor:1}});
 await p.goto('file://{html_path}',{{waitUntil:'load'}}); await p.waitForTimeout(600);
 const n=Math.round({TOTAL}*{FPS});
 for(let i=0;i<n;i++){{ await p.evaluate(t=>window.render(t), i/(n-1));
   await p.screenshot({{path:'{OUT}/f'+String(i).padStart(5,'0')+'.jpg',quality:95,type:'jpeg'}}); }}
 console.log('frames',n); await b.close();}})();
""")
subprocess.run(['node', str(D/'render.js')], check=True)
mp4 = D/'VintageVault_turquoise-worth.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(FPS),'-i',f'{OUT}/f%05d.jpg',
  '-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p',
  '-vf','scale=1080:1920','-movflags','+faststart',str(mp4)], check=True)
print('built', mp4)
