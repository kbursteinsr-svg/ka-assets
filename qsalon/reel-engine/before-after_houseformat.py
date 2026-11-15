#!/usr/bin/env python3
"""
The Q Salon for Men - "Before / After", house format, Q Salon palette.

Source: Susy's own before/after of a grown-out mullet taken back to a
textured crop with a high skin fade. Shot while she was at Ana Molinari
Salon Spa, so every frame is cropped tight - the multi-station room and
its dress-form mannequin are out of shot. The work is hers; the room is
not the Q Salon's, so nothing in the copy claims a location.

Copy describes only what is visible in the two photographs. No timings,
no dialogue, no claims about the client.

Music only - captions carry the script. 1080x1920, 30fps, 15.8s.
"""
import base64, pathlib, subprocess, sys

D   = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/ba')
FT  = D.parent/'qsfonts'/'ttf'
CUT = D.parent/'susyfootage'/'cuts'
OUT = D/'out'; OUT.mkdir(parents=True, exist_ok=True)

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def face(fam, fn, w):
    return (f"@font-face{{font-family:'{fam}';src:url(data:font/ttf;base64,{b64(FT/fn)}) "
            f"format('truetype');font-weight:{w};font-style:normal}}")

FONTS = "".join([
  face('Hanken', 'hanken-grotesk-latin-400-normal.ttf', 400),
  face('Hanken', 'hanken-grotesk-latin-500-normal.ttf', 500),
  face('Hanken', 'hanken-grotesk-latin-600-normal.ttf', 600),
  face('Hanken', 'hanken-grotesk-latin-700-normal.ttf', 700),
  face('Marcellus', 'marcellus-latin-400-normal.ttf', 400),
  face('DMMono', 'dm-mono-latin-500-normal.ttf', 500),
])

BEFORE = b64(CUT/'before.jpg')
AFTER  = b64(CUT/'after.jpg')
SUSY   = b64(D.parent/'gm'/'assets'/'susy.jpg')

CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --navy:#14202e; --line:rgba(214,185,132,.052);
  --card:#1B2838; --edge:rgba(214,185,132,.13);
  --ink:#F3F0EA; --dim:rgba(243,240,234,.40);
  --brass:#D6B984; --brassdeep:#B99A63;
  --shadow:0 34px 70px rgba(0,0,0,.50), 0 4px 12px rgba(0,0,0,.32);
}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--navy)}
body{font-family:'Hanken';color:var(--ink);-webkit-font-smoothing:antialiased}
#grid{position:absolute;inset:0;
  background-image:linear-gradient(var(--line) 1px,transparent 1px),
                   linear-gradient(90deg,var(--line) 1px,transparent 1px);
  background-size:70px 70px}
#vig{position:absolute;inset:0;background:
  radial-gradient(120% 70% at 50% 16%, rgba(214,185,132,.055), transparent 62%)}
.stage{position:absolute;inset:0;opacity:0}

.cap{position:absolute;top:232px;left:66px;right:66px;text-align:center;
  font-weight:500;font-size:70px;line-height:92px;letter-spacing:-.018em;color:var(--dim)}
.cap b{font-weight:700;color:var(--ink)}
.cap .hl{font-weight:700;color:#1B2230;background:var(--brass);
  box-shadow:0 0 0 10px var(--brass);border-radius:3px}
.cap .mc{font-family:'Marcellus';font-weight:400;color:var(--brass)}

.card{position:absolute;background:var(--card);border:1px solid var(--edge);
  border-radius:24px;box-shadow:var(--shadow);overflow:hidden}
.card img{display:block;width:100%}
.tag{position:absolute;left:28px;top:28px;
  font:500 26px/1 'DMMono';letter-spacing:.20em;text-transform:uppercase;
  color:#16212E;background:var(--brass);padding:15px 22px;border-radius:999px}
.tag.ghost{background:rgba(22,33,46,.76);color:var(--brass);
  border:1px solid rgba(214,185,132,.45)}

.eyebrow{font:500 25px/1 'DMMono';letter-spacing:.22em;text-transform:uppercase;
  color:var(--brass);display:flex;align-items:center;gap:18px}
.eyebrow:before{content:'';width:46px;height:1px;background:var(--brassdeep)}
.spec{margin-top:46px}
.srow{display:flex;justify-content:space-between;align-items:baseline;
  padding:30px 0;border-bottom:1px solid rgba(214,185,132,.13)}
.srow:last-child{border-bottom:none}
.swhere{font:600 46px/1 'Hanken';letter-spacing:-.01em}
.swhat{font-family:'Marcellus';font-weight:400;font-size:44px;color:var(--brass)}

.portrait{width:300px;height:300px;border-radius:50%;object-fit:cover;
  border:3px solid var(--brass);box-shadow:0 20px 46px rgba(0,0,0,.45)}
.pill{display:inline-flex;align-items:center;background:var(--brass);color:#16212E;
  font:700 34px/1 'Hanken';padding:25px 46px;border-radius:999px;
  box-shadow:0 16px 34px rgba(214,185,132,.22)}
.handle{font:500 29px/1 'DMMono';letter-spacing:.11em;color:var(--dim)}

.foot{position:absolute;left:70px;right:70px;bottom:92px;display:flex;
  justify-content:space-between;align-items:baseline}
.brand{font:400 37px/1 'Marcellus';letter-spacing:.015em;color:var(--ink)}
.meta{font:500 24px/1 'DMMono';letter-spacing:.17em;text-transform:uppercase;color:var(--dim)}
"""

# Both photo cards sit at the same place and size, so the cut between them
# lands as a match cut - the head stays put and only the hair changes.
PHOTO = "left:170px;top:560px;width:740px"

S = [
 dict(s=0.0, e=3.40, fi=0.34, fo=0.005, h=f"""
  <div class="cap">Nobody walks in<br>looking like the <b>after</b></div>
  <div class="card" data-rise="0" style="{PHOTO}">
    <img data-zoom="1" src="data:image/jpeg;base64,{BEFORE}">
    <div class="tag ghost">Before</div>
  </div>"""),

 # hard cut, not a dissolve - the snap is the whole point of the reveal
 dict(s=3.40, e=7.00, fi=0.005, fo=0.26, h=f"""
  <div class="cap">That's the <span class="hl">job</span></div>
  <!-- no data-rise: the reveal must land as a cut, not drift in -->
  <div class="card" style="{PHOTO}">
    <img data-zoom="1" src="data:image/jpeg;base64,{AFTER}">
    <div class="tag">After</div>
  </div>"""),

 # "one appointment" would be a claim two photographs cannot support -
 # the copy stays with what is visible in them
 dict(s=7.00, e=10.60, fi=0.34, fo=0.26, h="""
  <div class="cap">Three things<br><b>changed</b></div>
  <div class="card" data-rise="0" style="left:90px;top:640px;width:900px;padding:56px 64px 60px">
    <div class="eyebrow">What changed</div>
    <div class="spec">
      <div class="srow" data-rise="0"><span class="swhere">Back</span>
        <span class="swhat">Length off</span></div>
      <div class="srow" data-rise="1"><span class="swhere">Sides</span>
        <span class="swhat">Skin fade</span></div>
      <div class="srow" data-rise="2"><span class="swhere">Top</span>
        <span class="swhat">Textured crop</span></div>
    </div>
  </div>"""),

 dict(s=10.60, e=15.80, fi=0.34, fo=0.26, h=f"""
  <div style="position:absolute;left:0;right:0;top:206px;text-align:center">
    <img class="portrait" data-pop="1" src="data:image/jpeg;base64,{SUSY}"></div>
  <div class="cap" style="top:570px">Follow <b>The Q Salon for Men</b><br>
    for <span class="hl">before and afters</span><br>like this one</div>
  <div style="position:absolute;left:0;right:0;top:1120px;text-align:center" data-reveal="0.34">
    <span class="pill">Book &middot; link in bio</span></div>
  <div style="position:absolute;left:0;right:0;top:1262px;text-align:center" data-reveal="0.42">
    <span class="handle">@theqsalon_srq</span></div>"""),
]

def build(scenes):
    body = "".join(
      f'<div class="stage" data-s="{x["s"]}" data-e="{x["e"]}" data-fi="{x["fi"]}" data-fo="{x["fo"]}">{x["h"]}'
      f'<div class="foot"><div class="brand">The Q Salon</div>'
      f'<div class="meta">For Men &middot; Sarasota</div></div></div>' for x in scenes)
    total = scenes[-1]['e']
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div id="grid"></div><div id="vig"></div>{body}
<script>
window.TOTAL={total};
function ease(p){{return 1-Math.pow(1-p,3);}}
window.render=function(t){{
  var T=window.TOTAL*t;
  document.querySelectorAll('.stage').forEach(function(el){{
    var s=+el.dataset.s, e=+el.dataset.e, fi=+el.dataset.fi, fo=+el.dataset.fo, o=0;
    var inP=Math.min(1,Math.max(0,(T-s)/fi));
    var outP=Math.min(1,Math.max(0,(e+fo*0.75-T)/fo));
    if(T>=s-0.5 && T<=e+0.30) o=Math.min(inP,outP);
    el.style.opacity=o;
    if(o<=0){{el.style.visibility='hidden';return;}}
    el.style.visibility='visible';
    var L=Math.min(1,Math.max(0,(T-s)/(e-s)));
    el.querySelectorAll('[data-rise]').forEach(function(c){{
      var i=+c.dataset.rise, d=i*0.11;
      var p=ease(Math.min(1,Math.max(0,(L-d)/0.40)));
      c.style.transform='perspective(1700px) rotateX('+((1-p)*8).toFixed(2)
        +'deg) translateY('+((1-p)*48).toFixed(1)+'px)';
      c.style.opacity=Math.min(1,p*1.6);
    }});
    el.querySelectorAll('[data-zoom]').forEach(function(c){{
      c.style.transform='scale('+(1.012+0.040*L).toFixed(4)+')';
    }});
    el.querySelectorAll('[data-pop]').forEach(function(c){{
      var p=ease(Math.min(1,Math.max(0,(L-0.04)/0.30)));
      c.style.transform='scale('+(0.90+0.10*p).toFixed(3)+')';
      c.style.opacity=p;
    }});
    el.querySelectorAll('[data-reveal]').forEach(function(c){{
      var st0=parseFloat(c.dataset.reveal); if(!(st0>0)) st0=0.40;
      var p=ease(Math.min(1,Math.max(0,(L-st0)/0.22)));
      c.style.opacity=p;
      c.style.transform='translateY('+((1-p)*22).toFixed(1)+'px)';
    }});
  }});
}};
window.render(0);
</script></body></html>"""

hp = D/'reel.html'; hp.write_text(build(S))
TOTAL = S[-1]['e']; FPS = 30

if '--check' in sys.argv:
    marks = [9.2, 11.2, 13.0, 15.0]
    (D/'check.js').write_text(f"""
const {{chromium}}=require('playwright');
const marks={marks};
(async()=>{{const b=await chromium.launch();
 const p=await b.newPage({{viewport:{{width:1080,height:1920}},deviceScaleFactor:1}});
 await p.goto('file://{hp}',{{waitUntil:'load'}}); await p.waitForTimeout(900);
 for(let i=0;i<marks.length;i++){{
   await p.evaluate(t=>window.render(t), marks[i]/{TOTAL});
   await p.screenshot({{path:'{D}/chk'+i+'.jpg',quality:92,type:'jpeg'}});}}
 console.log('checked',marks.length); await b.close();}})();
""")
    subprocess.run(['node', str(D/'check.js')], check=True)
    from PIL import Image, ImageDraw
    ims=[]
    for i,m in enumerate(marks):
        im=Image.open(D/f'chk{i}.jpg'); im.thumbnail((360,640))
        d=ImageDraw.Draw(im); d.rectangle([0,0,78,26], fill='black')
        d.text((6,6), f'{m}s', fill='yellow')
        ims.append(im)
    cols=3; cw,ch=ims[0].size; rows=(len(ims)+cols-1)//cols
    sheet=Image.new('RGB',(cols*(cw+6)+6, rows*(ch+6)+6),'white')
    for i,im in enumerate(ims):
        sheet.paste(im,(6+(i%cols)*(cw+6), 6+(i//cols)*(ch+6)))
    sheet.save(D/'checksheet.jpg',quality=90)
    print('check sheet at', D/'checksheet.jpg'); sys.exit(0)

(D/'render.js').write_text(f"""
const {{chromium}}=require('playwright');
(async()=>{{const b=await chromium.launch();
 const p=await b.newPage({{viewport:{{width:1080,height:1920}},deviceScaleFactor:1}});
 await p.goto('file://{hp}',{{waitUntil:'load'}}); await p.waitForTimeout(900);
 const n=Math.round({TOTAL}*{FPS});
 for(let i=0;i<n;i++){{await p.evaluate(t=>window.render(t), i/(n-1));
  await p.screenshot({{path:'{OUT}/f'+String(i).padStart(5,'0')+'.jpg',quality:95,type:'jpeg'}});}}
 console.log('frames',n); await b.close();}})();
""")
subprocess.run(['node', str(D/'render.js')], check=True)
subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(FPS),'-i',f'{OUT}/f%05d.jpg',
  '-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p',
  '-vf','scale=1080:1920','-movflags','+faststart', str(D/'_silent.mp4')], check=True)
print('silent built')
