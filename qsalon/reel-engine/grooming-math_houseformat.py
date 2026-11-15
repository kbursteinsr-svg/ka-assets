#!/usr/bin/env python3
"""
The Q Salon for Men - "Grooming Math", rebuilt in the locked house format
(getripping-derived) in Q Salon's navy/brass/stone palette, with Will's VO.

Copy is the APPROVED copy from the 2026-11-16 cut, read back off its frames and
re-staged - nothing invented. Page name "The Q Salon for Men" is verified and
must not be shortened.

VO: 2026-11-16_grooming-math_vo.mp3, 23.90s, Will - Relaxed Optimist.
Phrase onsets: 4.56 6.84 9.62 10.92 12.48 17.92 21.80 23.80
1080x1920, 30fps.
"""
import base64, pathlib, subprocess

D   = pathlib.Path('/tmp/claude-0/-home-claude/4034ec82-b6e9-51b3-8724-903b5291379b/scratchpad/gm')
FT  = D.parent/'qsfonts'/'ttf'
A   = D/'assets'
VO  = pathlib.Path('/home/claude/ka-assets/qsalon/reels/audio/2026-11-16_grooming-math_vo.mp3')
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

BARBER = b64(A/'barber.jpg')
SUSY   = b64(A/'susy.jpg')

CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --navy:#14202e; --line:rgba(214,185,132,.052);
  --card:#1B2838; --edge:rgba(214,185,132,.13);
  --ink:#F3F0EA; --dim:rgba(243,240,234,.40);
  --brass:#D6B984; --brassdeep:#B99A63; --glow:rgba(214,185,132,.17);
  --track:rgba(243,240,234,.10);
  --shadow:0 34px 70px rgba(0,0,0,.46), 0 4px 12px rgba(0,0,0,.30);
}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--navy)}
body{font-family:'Hanken';color:var(--ink);-webkit-font-smoothing:antialiased}
#grid{position:absolute;inset:0;
  background-image:linear-gradient(var(--line) 1px,transparent 1px),
                   linear-gradient(90deg,var(--line) 1px,transparent 1px);
  background-size:70px 70px}
#vig{position:absolute;inset:0;background:
  radial-gradient(120% 70% at 50% 18%, rgba(214,185,132,.055), transparent 62%)}
.stage{position:absolute;inset:0;opacity:0}

/* ---- top-anchored two-weight caption, house format ---- */
.cap{position:absolute;top:232px;left:70px;right:70px;text-align:center;
  font-weight:500;font-size:70px;line-height:92px;letter-spacing:-.018em;color:var(--dim)}
.cap b{font-weight:700;color:var(--ink)}
.cap .hl{font-weight:700;color:#1B2230;background:var(--brass);
  box-shadow:0 0 0 10px var(--brass);border-radius:3px}
.cap .mc{font-family:'Marcellus';font-weight:400;color:var(--brass)}
.cap .st{font-weight:700;color:var(--ink);display:inline-block;position:relative}
.cap .st:after{content:'';position:absolute;left:-12px;right:-12px;top:52%;
  height:7px;background:var(--brass);border-radius:4px;
  transform-origin:left center;transform:scaleX(var(--sx,0))}

.eyebrow{font:500 25px/1 'DMMono';letter-spacing:.22em;text-transform:uppercase;
  color:var(--brass);display:flex;align-items:center;gap:18px}
.eyebrow:before{content:'';width:46px;height:1px;background:var(--brassdeep)}

.card{position:absolute;background:var(--card);border:1px solid var(--edge);
  border-radius:24px;box-shadow:var(--shadow)}

/* ---- scene 1: the fraction ---- */
.frac{display:flex;align-items:center;justify-content:center;
  font-family:'Marcellus';color:var(--brass);line-height:1}
.frac .n{font-size:236px;align-self:flex-start;margin-top:8px}
.frac .sl{font-size:350px;margin:0 4px;color:var(--brassdeep)}
.frac .d{font-size:236px;align-self:flex-end;margin-bottom:8px}
.frac .pr{font-size:142px;align-self:flex-start;margin:16px 0 0 14px;color:var(--brassdeep)}
.subline{font:500 32px/1 'DMMono';letter-spacing:.20em;text-transform:uppercase;
  color:var(--dim);text-align:center}
.ruler{position:relative;height:52px;margin:0 auto;overflow:hidden}
.ruler i{position:absolute;bottom:0;width:3px;background:var(--brassdeep);opacity:.62}

/* ---- scenes 2-3: the hold meters ---- */
.row{margin-top:62px}
.row:first-child{margin-top:0}
.rhead{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:22px}
.rlab{font:600 50px/1 'Hanken';letter-spacing:-.01em}
.rval{font:500 42px/1 'DMMono';color:var(--brass);letter-spacing:.01em}
.track{height:20px;border-radius:10px;background:var(--track);overflow:hidden}
.bar{height:100%;width:0;border-radius:10px;
  background:linear-gradient(90deg,var(--brassdeep),var(--brass))}
.row.off .rlab,.row.off .rval{color:var(--dim)}
.row.off .bar{background:rgba(214,185,132,.34)}
.row.pending{opacity:.26}
.row.pending .rlab,.row.pending .rval{color:var(--dim)}

/* ---- scene 4: the turn ---- */
.shot{width:100%;display:block;border-radius:18px}
.truth{font-family:'Marcellus';font-weight:400;font-size:62px;line-height:1.28;
  color:var(--brass);text-align:center}

/* ---- scene 5: CTA ---- */
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

def ruler(n=25):
    out = []
    for i in range(n):
        tall = (i % 4 == 0)
        h = 40 if tall else 20
        out.append(f"<i style='left:{i*32}px;height:{h}px'></i>")
    return "".join(out)

def hold_rows(active, delays):
    """All three rows always render, so the card keeps one height across
    scenes 2 and 3 and the cut between them doesn't jump. `active` is the row
    currently landing; earlier rows sit dimmed, later ones wait at low opacity
    with an empty track.

    `delays` is the per-row fill delay as a fraction of THIS scene. A row that
    was already full at the end of the previous scene gets a negative delay so
    it starts full - otherwise its meter visibly snaps back to empty and
    re-fills at the cut, which is the one thing a carried value must not do.
    """
    rows = [("Skin fade", "2 weeks", 33), ("Short cut", "3–4 weeks", 58),
            ("Longer style", "5–6 weeks", 92)]
    out = []
    for i, (lab, val, pct) in enumerate(rows):
        if i > active - 1:
            cls, fill, rise = " pending", 0, ""
        elif i < active - 1:
            cls, fill, rise = " off", pct, f" data-rise='{i}'"
        else:
            cls, fill, rise = "", pct, f" data-rise='{i}'"
        out.append(
          f"<div class='row{cls}'{rise}>"
          f"<div class='rhead'><span class='rlab'>{lab}</span>"
          f"<span class='rval'>{val}</span></div>"
          f"<div class='track'><div class='bar' data-fill='{fill}' "
          f"data-delay='{delays[i]}'></div></div></div>")
    return "".join(out)

# Fill delays are set from Will's phrase onsets, as a fraction of each scene.
# Scene 2 runs 4.56-8.80: "skin fade" lands at 4.56, "short cut" at 6.84.
# Scene 3 runs 8.80-12.48: the first two carry over full, "longer style"
# lands at 9.62.
D2 = [0.04, round((6.84 - 4.56) / (8.80 - 4.56), 3), 0]
D3 = [-1, -1, round((9.62 - 8.80) / (12.48 - 8.80), 3)]

S = [
 # 1 - the number
 dict(s=0.0, e=4.56, h=f"""
  <div class="cap"><span class="mc">Grooming</span> <b>math</b></div>
  <div class="card" data-rise="0" style="left:90px;top:660px;width:900px;padding:56px 64px 66px">
    <div class="eyebrow">Hair growth</div>
    <div class="frac" data-pop="1" style="margin-top:24px">
      <span class="n">1</span><span class="sl">&frasl;</span><span class="d">2</span>
      <span class="pr">&Prime;</span></div>
    <div class="ruler" data-wipe="1" style="width:768px;margin-top:22px">{ruler()}</div>
    <div class="subline" style="margin-top:34px">Of growth every month</div>
  </div>"""),

 # 2 - first two holds
 dict(s=4.56, e=8.80, h=f"""
  <div class="cap">How long a <b>cut holds</b></div>
  <div class="card" data-rise="0" style="left:90px;top:660px;width:900px;padding:56px 64px 70px">
    <div class="eyebrow" style="margin-bottom:54px">By the length you wear</div>
    {hold_rows(2, D2)}
  </div>"""),

 # 3 - all three
 dict(s=8.80, e=12.48, h=f"""
  <div class="cap">How long a <b>cut holds</b></div>
  <div class="card" data-rise="0" style="left:90px;top:660px;width:900px;padding:56px 64px 70px">
    <div class="eyebrow" style="margin-bottom:54px">By the length you wear</div>
    {hold_rows(3, D3)}
  </div>"""),

 # 4 - the turn. Copy is verbatim from the approved cut: the strike falls on
 # "more haircuts." only, and the truth line arrives after it lands.
 dict(s=12.48, e=17.92, h=f"""
  <div class="cap" data-strike="1">Sharp men don't get<br>
    <span class="st">more haircuts.</span></div>
  <div class="card" data-rise="0" style="left:90px;top:620px;width:900px;padding:22px">
    <div style="overflow:hidden;border-radius:18px">
      <img class="shot" data-zoom="1" src="data:image/jpeg;base64,{BARBER}"></div>
  </div>
  <div class="truth" data-reveal="0.30"
       style="position:absolute;left:90px;right:90px;top:1320px">
    They book before<br>they need one.</div>"""),

 # 5 - CTA
 dict(s=17.92, e=24.40, h=f"""
  <div style="position:absolute;left:0;right:0;top:206px;text-align:center">
    <img class="portrait" data-pop="1" src="data:image/jpeg;base64,{SUSY}"></div>
  <div class="cap" style="top:570px">Follow <b>The Q Salon for Men</b><br>
    for grooming math that<br><span class="hl">makes you look better</span></div>
  <div style="position:absolute;left:0;right:0;top:1120px;text-align:center" data-reveal="0.56">
    <span class="pill">Book &middot; link in bio</span></div>
  <div style="position:absolute;left:0;right:0;top:1262px;text-align:center" data-reveal="0.63">
    <span class="handle">@theqsalon_srq</span></div>"""),
]

def build(scenes):
    body = "".join(
      f'<div class="stage" data-s="{x["s"]}" data-e="{x["e"]}">{x["h"]}'
      f'<div class="foot"><div class="brand">The Q Salon</div>'
      f'<div class="meta">For Men &middot; Sarasota</div></div></div>' for x in scenes)
    total = scenes[-1]['e']
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div id="grid"></div><div id="vig"></div>{body}
<script>
window.TOTAL={total};
function ease(p){{return 1-Math.pow(1-p,3);}}
function eo(p){{return p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;}}
window.render=function(t){{
  var T=window.TOTAL*t;
  document.querySelectorAll('.stage').forEach(function(el){{
    var s=+el.dataset.s, e=+el.dataset.e, o=0;
    var inP=Math.min(1,Math.max(0,(T-s)/0.40));
    var outP=Math.min(1,Math.max(0,(e+0.20-T)/0.26));
    if(T>=s-0.5 && T<=e+0.30) o=Math.min(inP,outP);
    el.style.opacity=o;
    if(o<=0){{el.style.visibility='hidden';return;}}
    el.style.visibility='visible';
    var L=Math.min(1,Math.max(0,(T-s)/(e-s)));

    // staggered 3D card rise, easing from tilted to flat
    el.querySelectorAll('[data-rise]').forEach(function(c){{
      var i=+c.dataset.rise, d=i*0.10;
      var p=ease(Math.min(1,Math.max(0,(L-d)/0.42)));
      c.style.transform='perspective(1700px) rotateX('+((1-p)*9).toFixed(2)
        +'deg) rotateY('+((1-p)*-4).toFixed(2)+'deg) translateY('+((1-p)*54).toFixed(1)+'px)';
      c.style.opacity=Math.min(1,p*1.5);
    }});

    // the number lands with a settle
    el.querySelectorAll('[data-pop]').forEach(function(c){{
      var p=ease(Math.min(1,Math.max(0,(L-0.06)/0.34)));
      c.style.transform='scale('+(0.90+0.10*p).toFixed(3)+')';
      c.style.opacity=p;
    }});

    // ruler ticks wipe across
    el.querySelectorAll('[data-wipe]').forEach(function(c){{
      var p=ease(Math.min(1,Math.max(0,(L-0.18)/0.46)));
      c.style.clipPath='inset(0 '+((1-p)*100).toFixed(1)+'% 0 0)';
    }});

    // meters fill, each on its own delay, and keep drifting the whole scene
    el.querySelectorAll('[data-fill]').forEach(function(c){{
      var d=+c.dataset.delay, target=+c.dataset.fill;
      var p=eo(Math.min(1,Math.max(0,(L-d)/0.52)));
      c.style.width=(target*p).toFixed(2)+'%';
    }});

    // slow push-in on the photo
    el.querySelectorAll('[data-zoom]').forEach(function(c){{
      c.style.transform='scale('+(1.015+0.045*L).toFixed(4)+')';
    }});

    // the strike draws left to right, then the truth rises under it
    el.querySelectorAll('[data-strike]').forEach(function(c){{
      var p=eo(Math.min(1,Math.max(0,(L-0.12)/0.17)));
      c.style.setProperty('--sx', p.toFixed(3));
    }});
    el.querySelectorAll('[data-reveal]').forEach(function(c){{
      var st0=parseFloat(c.dataset.reveal); if(!(st0>0)) st0=0.46;
      var p=ease(Math.min(1,Math.max(0,(L-st0)/0.24)));
      c.style.opacity=p;
      c.style.transform='translateY('+((1-p)*22).toFixed(1)+'px)';
    }});
  }});
}};
window.render(0);
</script></body></html>"""

hp = D/'reel.html'; hp.write_text(build(S))
TOTAL = S[-1]['e']; FPS = 30

import sys
if '--check' in sys.argv:
    # preview the scene beats before committing to a full render
    marks = [5.0, 7.4, 8.9, 9.9, 11.6, 12.3]
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
    for i, m in enumerate(marks):
        subprocess.run(['ffmpeg','-v','error','-i',str(D/f'chk{i}.jpg'),
            '-vf', f"scale=440:-1,drawtext=text='{m}s':fontcolor=yellow:fontsize=26:"
                   "x=10:y=10:box=1:boxcolor=black@0.75",
            str(D/f'_c{i:02d}.jpg'),'-y'], check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(D/'_c%02d.jpg'),
        '-vf','tile=3x2:padding=6:color=white','-frames:v','1',
        str(D/'checksheet.jpg'),'-y'], check=True)
    print('check sheet at', D/'checksheet.jpg')
    sys.exit(0)
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

silent = D/'_silent.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(FPS),'-i',f'{OUT}/f%05d.jpg',
  '-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p',
  '-vf','scale=1080:1920','-movflags','+faststart', str(silent)], check=True)

# VO at the Q Salon level: loudnorm I=-18 TP=-2, 0.4s lead-in already in the read
mp4 = D/'TheQSalon_grooming-math.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(silent),'-i',str(VO),
  '-filter_complex','[1:a]loudnorm=I=-18:TP=-2:LRA=11,apad[a]',
  '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000',
  '-shortest','-movflags','+faststart', str(mp4)], check=True)
print('built', mp4)
