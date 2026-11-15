#!/usr/bin/env python3
"""Build It Right — 'Before you buy a combo kit' reel. 1080x1920, music-ready (silent)."""
import base64, json, os, subprocess, pathlib

D = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/bir')
FONTS, IMG, OUT = D/'fonts', D/'img', D/'out'
OUT.mkdir(exist_ok=True)

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

FONT_CSS = f"""
@font-face{{font-family:'Anton';src:url(data:font/ttf;base64,{b64(FONTS/'Anton.ttf')}) format('truetype');font-weight:400}}
@font-face{{font-family:'Inter';src:url(data:font/ttf;base64,{b64(FONTS/'Inter-SemiBold.ttf')}) format('truetype');font-weight:600}}
@font-face{{font-family:'Inter';src:url(data:font/ttf;base64,{b64(FONTS/'Inter-Regular.ttf')}) format('truetype');font-weight:400}}
"""

DEWALT = b64(IMG/'dewalt.jpg')
MILW   = b64(IMG/'milwaukee.jpg')

# charcoal / safety-yellow / bone — industrial, lets the product photos carry their own colour
CSS = FONT_CSS + """
*{margin:0;padding:0;box-sizing:border-box}
:root{--ink:#14181c;--bone:#f4f2ee;--amber:#f5b301;--line:rgba(244,242,238,.18)}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--ink)}
body{font-family:'Inter',system-ui;color:var(--bone);-webkit-font-smoothing:antialiased}
.stage{position:absolute;inset:0;opacity:0}
.eyebrow{font:600 30px/1 'Inter';letter-spacing:.22em;text-transform:uppercase;color:var(--amber)}
.h{font:400 112px/0.94 'Anton';letter-spacing:-.01em;text-transform:uppercase}
.h.sm{font-size:86px}
.p{font:400 40px/1.45 'Inter';color:rgba(244,242,238,.82)}
.pad{position:absolute;left:84px;right:84px}
.num{font:400 150px/1 'Anton';color:var(--amber);opacity:.98}
.rule{height:3px;background:var(--amber);width:120px}
.photo{position:absolute;left:0;right:0;display:flex;align-items:center;justify-content:center}
.photo img{max-width:912px;max-height:912px;object-fit:contain;border-radius:10px}
.chip{display:inline-block;border:3px solid var(--amber);color:var(--amber);
  font:600 34px/1 'Inter';letter-spacing:.06em;padding:20px 34px;border-radius:999px;text-transform:uppercase}
.price{font:400 92px/1 'Anton';color:var(--bone)}
.strike{position:relative;color:rgba(244,242,238,.45)}
.strike:after{content:'';position:absolute;left:-4px;right:-4px;top:52%;height:5px;background:var(--amber)}
.foot{position:absolute;left:84px;right:84px;bottom:92px;display:flex;justify-content:space-between;align-items:baseline}
.brand{font:400 40px/1 'Anton';letter-spacing:.02em}
.meta{font:400 28px/1 'Inter';color:rgba(244,242,238,.5)}
.bar{position:absolute;left:0;bottom:0;height:8px;background:var(--amber)}
"""

SCENES = [
    # 0 HOOK
    dict(start=0.0, end=3.6, html="""
      <div class="pad" style="top:620px">
        <div class="eyebrow">Before you buy</div>
        <div class="rule" style="margin:34px 0 46px"></div>
        <div class="h">Three things<br>to check on a<br>combo kit.</div>
        <div class="p" style="margin-top:46px">Most people check the tool count. That's the<br>least important number on the box.</div>
      </div>"""),
    # 1
    dict(start=3.6, end=8.0, html="""
      <div class="pad" style="top:470px">
        <div class="num">01</div>
        <div class="h sm" style="margin-top:18px">The battery<br>platform</div>
        <div class="p" style="margin-top:38px">You're not buying a kit. You're buying into a
        system you'll keep adding to for ten years. Pick the one your crew already runs.</div>
      </div>"""),
    # 2
    dict(start=8.0, end=12.4, html="""
      <div class="pad" style="top:470px">
        <div class="num">02</div>
        <div class="h sm" style="margin-top:18px">Brushless<br>motors</div>
        <div class="p" style="margin-top:38px">Longer runtime, less heat, far less to wear out.
        If the listing doesn't say brushless, it isn't.</div>
      </div>"""),
    # 3
    dict(start=12.4, end=16.8, html="""
      <div class="pad" style="top:470px">
        <div class="num">03</div>
        <div class="h sm" style="margin-top:18px">Amp hours,<br>not tools</div>
        <div class="p" style="margin-top:38px">Two 4Ah batteries beat four 2Ah batteries every
        day. Small packs mean you're charging instead of working.</div>
      </div>"""),
    # 4 PRODUCT
    dict(start=16.8, end=21.6, html=f"""
      <div class="pad" style="top:250px">
        <div class="eyebrow">Checks all three</div>
      </div>
      <div class="photo" style="top:360px;height:912px"><img src="data:image/jpeg;base64,{DEWALT}"></div>
      <div class="pad" style="top:1330px">
        <div class="h sm">DeWalt 20V MAX<br>9-tool kit</div>
        <div class="p" style="margin-top:26px">Brushless &middot; two 4Ah batteries &middot; charger</div>
        <div style="margin-top:34px"><span class="price">$729.95</span></div>
      </div>"""),
    # 5 CTA
    dict(start=21.6, end=26.0, html="""
      <div class="pad" style="top:600px">
        <div class="eyebrow">Straight answers</div>
        <div class="rule" style="margin:34px 0 46px"></div>
        <div class="h">Follow<br>Build It Right<br>for tool and<br>job advice<br>that holds up.</div>
        <div style="margin-top:60px"><span class="chip">Link in the comments</span></div>
      </div>"""),
]

def frame_html(scenes):
    body = "".join(
        f'<div class="stage" data-s="{s["start"]}" data-e="{s["end"]}">{s["html"]}'
        f'<div class="foot"><div class="brand">BUILD IT RIGHT</div>'
        f'<div class="meta">facebook.com/BuildItRightFL</div></div></div>'
        for s in scenes)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{body}<div class="bar" id="bar"></div>
<script>
window.TOTAL={scenes[-1]['end']};
window.render=function(t){{
  var T=window.TOTAL*t;
  document.querySelectorAll('.stage').forEach(function(el){{
    var s=+el.dataset.s, e=+el.dataset.e, o=0, dy=0;
    if(T>=s-0.45 && T<=e+0.1){{
      var inP=Math.min(1,Math.max(0,(T-s)/0.42));
      var outP=Math.min(1,Math.max(0,(e-T)/0.30));
      o=Math.min(inP,outP);
      dy=(1-inP)*26;
    }}
    el.style.opacity=o; el.style.transform='translateY('+dy+'px)';
  }});
  document.getElementById('bar').style.width=(t*1080)+'px';
}};
window.render(0);
</script></body></html>"""

html_path = D/'reel.html'
html_path.write_text(frame_html(SCENES))

TOTAL = SCENES[-1]['end']
FPS = 30
render_js = f"""
const {{chromium}} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{viewport:{{width:1080,height:1920}}, deviceScaleFactor:1}});
  await p.goto('file://{html_path}', {{waitUntil:'load'}});
  await p.waitForTimeout(600);
  const total = {TOTAL}, fps = {FPS};
  const n = Math.round(total*fps);
  for (let i=0;i<n;i++) {{
    await p.evaluate(t => window.render(t), i/(n-1));
    await p.screenshot({{path:'{OUT}/f'+String(i).padStart(5,'0')+'.jpg', quality:95, type:'jpeg'}});
  }}
  console.log('frames', n);
  await b.close();
}})();
"""
(D/'render.js').write_text(render_js)
subprocess.run(['node', str(D/'render.js')], check=True)

mp4 = D/'BuildItRight_combo-kit-checklist.mp4'
subprocess.run([
    'ffmpeg','-y','-v','error','-framerate',str(FPS),'-i',f'{OUT}/f%05d.jpg',
    '-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p',
    '-vf','scale=1080:1920','-movflags','+faststart', str(mp4)], check=True)
print('built', mp4)
