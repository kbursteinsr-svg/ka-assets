#!/usr/bin/env python3
"""Top Tech Drops — 'wrong size power station' reel. 1080x1920, music-ready."""
import base64, pathlib, subprocess

D = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/ttdreel')
FB = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/bir/fonts')
IMG = pathlib.Path('/home/claude/ka-assets/amb/ttd')
OUT = D/'out'; OUT.mkdir(parents=True, exist_ok=True)

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

FONT_CSS = f"""
@font-face{{font-family:'Anton';src:url(data:font/ttf;base64,{b64(FB/'Anton.ttf')}) format('truetype')}}
@font-face{{font-family:'Inter';src:url(data:font/ttf;base64,{b64(FB/'Inter-Regular.ttf')}) format('truetype');font-weight:400}}
@font-face{{font-family:'Inter';src:url(data:font/ttf;base64,{b64(FB/'Inter-SemiBold.ttf')}) format('truetype');font-weight:600}}
"""
BIG = b64(IMG/'bluetti-elite320.jpg')
SML = b64(IMG/'bluetti-elite200v2.jpg')

# Top Tech Drops: black ground, cyan accent
CSS = FONT_CSS + """
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#07090c;--cyan:#3FB6E8;--white:#F2F6F8;--dim:rgba(242,246,248,.72)}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--bg)}
body{font-family:'Inter',system-ui;color:var(--white);-webkit-font-smoothing:antialiased}
.stage{position:absolute;inset:0;opacity:0}
.pad{position:absolute;left:84px;right:84px}
.eyebrow{font:600 28px/1 'Inter';letter-spacing:.24em;text-transform:uppercase;color:var(--cyan)}
.h{font:400 104px/0.96 'Anton';text-transform:uppercase;letter-spacing:-.005em}
.h.sm{font-size:80px}
.p{font:400 38px/1.46 'Inter';color:var(--dim)}
.rule{height:3px;background:var(--cyan);width:118px}
.num{font:400 128px/1 'Anton';color:var(--cyan)}
.photo{position:absolute;left:0;right:0;display:flex;align-items:center;justify-content:center}
.photo img{object-fit:contain;background:#fff;border-radius:18px;padding:14px;
 border:2px solid rgba(63,182,232,.45);filter:drop-shadow(0 22px 48px rgba(0,0,0,.65))}
.chip{display:inline-block;border:3px solid var(--cyan);color:var(--cyan);
 font:600 32px/1 'Inter';letter-spacing:.07em;padding:19px 32px;border-radius:999px;text-transform:uppercase}
.col{position:absolute;top:980px;width:430px;text-align:center}
.col .cap{font:400 60px/1 'Anton';color:var(--cyan)}
.col .nm{font:600 30px/1.3 'Inter';margin-top:14px}
.col .pr{font:400 54px/1 'Anton';margin-top:16px}
.col .use{font:400 26px/1.4 'Inter';color:var(--dim);margin-top:12px}
.foot{position:absolute;left:84px;right:84px;bottom:92px;display:flex;justify-content:space-between;align-items:baseline}
.brand{font:400 38px/1 'Anton';letter-spacing:.03em}
.meta{font:400 26px/1 'Inter';color:rgba(242,246,248,.42)}
"""

S = [
 dict(s=0.0,e=3.8,h="""
  <div class="pad" style="top:600px">
    <div class="eyebrow">Before the next outage</div>
    <div class="rule" style="margin:32px 0 44px"></div>
    <div class="h">Most people<br>buy the wrong<br>size power<br>station.</div>
    <div class="p" style="margin-top:44px">They compare the big number on the box.<br>It's the wrong number.</div>
  </div>"""),

 dict(s=3.8,e=8.6,h="""
  <div class="pad" style="top:450px">
    <div class="num">01</div>
    <div class="h sm" style="margin-top:16px">Watts vs<br>watt-hours</div>
    <div class="p" style="margin-top:36px">Watts decide <i>what</i> you can run. Watt-hours decide
    <i>how long</i> it runs. A big output number with a small battery dies in an hour.</div>
  </div>"""),

 dict(s=8.6,e=13.4,h="""
  <div class="pad" style="top:450px">
    <div class="num">02</div>
    <div class="h sm" style="margin-top:16px">Add up what<br>you actually<br>plug in</div>
    <div class="p" style="margin-top:36px">A full-size fridge settles around 150 watts once it's
    running, but spikes far higher every time the compressor kicks in. Size for the spike.</div>
  </div>"""),

 dict(s=13.4,e=18.0,h="""
  <div class="pad" style="top:450px">
    <div class="num">03</div>
    <div class="h sm" style="margin-top:16px">Check the<br>battery type</div>
    <div class="p" style="margin-top:36px">Look for LiFePO4 on the spec sheet. It holds up to
    thousands of charge cycles where older lithium packs fade after a few hundred.</div>
  </div>"""),

 dict(s=18.0,e=23.4,h=f"""
  <div class="pad" style="top:250px">
    <div class="eyebrow">Two that fit most homes</div>
    <div class="h sm" style="margin-top:26px">Pick by hours,<br>not by price.</div>
  </div>
  <div class="photo" style="top:620px;height:340px;left:84px;width:430px">
    <img style="max-width:360px;max-height:330px" src="data:image/jpeg;base64,{SML}"></div>
  <div class="photo" style="top:620px;height:340px;right:84px;left:auto;width:430px">
    <img style="max-width:360px;max-height:330px" src="data:image/jpeg;base64,{BIG}"></div>
  <div class="col" style="left:84px">
    <div class="cap">2080Wh</div>
    <div class="nm">BLUETTI Elite 200 V2</div>
    <div class="pr">$899</div>
    <div class="use">Fridge, phones, lights<br>through a short outage</div>
  </div>
  <div class="col" style="right:84px">
    <div class="cap">3200Wh</div>
    <div class="nm">BLUETTI Elite 320</div>
    <div class="pr">$1,249</div>
    <div class="use">Adds to a longer one,<br>or runs more at once</div>
  </div>
  <div class="pad" style="top:1480px">
    <div class="p" style="font-size:30px">Prices on eBay today.</div>
  </div>"""),

 dict(s=23.4,e=28.0,h="""
  <div class="pad" style="top:600px">
    <div class="eyebrow">No hype, just specs</div>
    <div class="rule" style="margin:32px 0 44px"></div>
    <div class="h">Follow<br>Top Tech Drops<br>for gear picks<br>that hold up.</div>
    <div style="margin-top:58px"><span class="chip">Link in the comments</span></div>
  </div>"""),
]

def build(scenes):
    body="".join(f'<div class="stage" data-s="{x["s"]}" data-e="{x["e"]}">{x["h"]}'
      f'<div class="foot"><div class="brand">TOP TECH DROPS</div>'
      f'<div class="meta">Gear worth the money</div></div></div>' for x in scenes)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}
<script>window.TOTAL={scenes[-1]['e']};
window.render=function(t){{var T=window.TOTAL*t;
 document.querySelectorAll('.stage').forEach(function(el){{
  var s=+el.dataset.s,e=+el.dataset.e,o=0,dy=0;
  if(T>=s-0.45&&T<=e+0.1){{var i=Math.min(1,Math.max(0,(T-s)/0.42));
   var ou=Math.min(1,Math.max(0,(e-T)/0.30)); o=Math.min(i,ou); dy=(1-i)*24;}}
  el.style.opacity=o; el.style.transform='translateY('+dy+'px)';}});}};
window.render(0);</script></body></html>"""

hp=D/'reel.html'; hp.write_text(build(S))
TOTAL=S[-1]['e']; FPS=30
(D/'render.js').write_text(f"""
const {{chromium}}=require('playwright');
(async()=>{{const b=await chromium.launch();
 const p=await b.newPage({{viewport:{{width:1080,height:1920}},deviceScaleFactor:1}});
 await p.goto('file://{hp}',{{waitUntil:'load'}}); await p.waitForTimeout(600);
 const n=Math.round({TOTAL}*{FPS});
 for(let i=0;i<n;i++){{await p.evaluate(t=>window.render(t), i/(n-1));
  await p.screenshot({{path:'{OUT}/f'+String(i).padStart(5,'0')+'.jpg',quality:95,type:'jpeg'}});}}
 console.log('frames',n); await b.close();}})();
""")
subprocess.run(['node',str(D/'render.js')],check=True)
mp4=D/'TopTechDrops_power-station-size.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(FPS),'-i',f'{OUT}/f%05d.jpg',
 '-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p',
 '-vf','scale=1080:1920','-movflags','+faststart',str(mp4)],check=True)
print('built',mp4)
