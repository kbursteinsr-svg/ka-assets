"""Build a seekable 1080x1920 Q Salon reel page from a JSON config.

Config: {"total": seconds, "scenes": [{"start": s, "end": s, "html": "..."}], "progress": true}
Inside scene html, any element with data-in="0.4" fades/rises in 0.4s after the scene starts.
data-count="45" on an element counts its number up while it enters.
data-bar="0.75" on an element grows its width to 75% while it enters.
"""
import base64, json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / 'fonts'

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def font_css():
    faces = [
        ('Marcellus', 400, F/'fontsource-marcellus-5.3.0/files/marcellus-latin-400-normal.woff2'),
        ('Hanken Grotesk', 400, F/'fontsource-hanken-grotesk-5.3.0/files/hanken-grotesk-latin-400-normal.woff2'),
        ('Hanken Grotesk', 500, F/'fontsource-hanken-grotesk-5.3.0/files/hanken-grotesk-latin-500-normal.woff2'),
        ('Hanken Grotesk', 600, F/'fontsource-hanken-grotesk-5.3.0/files/hanken-grotesk-latin-600-normal.woff2'),
        ('DM Mono', 400, F/'fontsource-dm-mono-5.3.0/files/dm-mono-latin-400-normal.woff2'),
        ('DM Mono', 500, F/'fontsource-dm-mono-5.3.0/files/dm-mono-latin-500-normal.woff2'),
    ]
    return '\n'.join(
        f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{b64(p)}) format('woff2');}}"
        for n, w, p in faces)

CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0f1822}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;color:#f3f0ea;font-family:'Hanken Grotesk',sans-serif;
  background:radial-gradient(1200px 900px at 50% 38%,#22344a 0%,#14202e 55%,#0d1620 100%)}
#glow{position:absolute;width:1400px;height:1400px;left:-160px;top:-240px;border-radius:50%;
  background:radial-gradient(circle,rgba(214,185,132,.16),rgba(214,185,132,0) 60%)}
#frame{position:absolute;inset:40px;border:1.5px solid rgba(214,185,132,.35)}
#mark{position:absolute;left:84px;top:96px;display:flex;align-items:center;gap:22px;z-index:5}
#mark .q{width:84px;height:84px;border-radius:50%;border:2px solid #d6b984;display:flex;align-items:center;justify-content:center;
  font-family:'Marcellus';font-size:50px;color:#d6b984;line-height:1;padding-bottom:4px}
#mark .t{font-family:'Marcellus';font-size:30px;letter-spacing:.14em;color:#f3f0ea}
#mark .t small{display:block;font-family:'DM Mono';font-size:18px;letter-spacing:.32em;color:#d6b984;margin-top:6px}
#bar{position:absolute;left:84px;right:84px;bottom:110px;height:4px;background:rgba(243,240,234,.14);z-index:5}
#bar i{position:absolute;left:0;top:0;bottom:0;background:#d6b984;width:0}
.scene{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 96px;gap:34px;opacity:0}
.eyebrow{font-family:'DM Mono';font-size:30px;letter-spacing:.3em;text-transform:uppercase;color:#d6b984;display:flex;align-items:center;gap:22px}
.eyebrow:before{content:'';width:70px;height:2px;background:#d6b984;display:inline-block}
.h{font-family:'Marcellus';font-size:112px;line-height:1.06;color:#f3f0ea}
.h.xl{font-size:150px;line-height:1.0}
.h.md{font-size:90px}
.gold,.p.gold{color:#d6b984}
.p{font-size:50px;line-height:1.35;color:rgba(243,240,234,.86);max-width:860px}
.big{font-family:'Marcellus';font-size:380px;line-height:.9;color:#d6b984}
.unit{font-family:'DM Mono';font-size:40px;letter-spacing:.3em;text-transform:uppercase;color:#f3f0ea}
.chip{align-self:flex-start;font-family:'Hanken Grotesk';font-weight:600;font-size:46px;color:#14202e;background:#d6b984;
  padding:26px 46px;border-radius:999px}
.chip.ghost{background:transparent;color:#d6b984;border:2px solid #d6b984;font-weight:500}
.handle{font-family:'DM Mono';font-size:34px;letter-spacing:.12em;color:rgba(243,240,234,.75)}
.price{font-family:'Marcellus';font-size:200px;color:#d6b984;line-height:1}
.photo{width:560px;height:560px;border-radius:50%;overflow:hidden;border:3px solid #d6b984;align-self:center;
  box-shadow:0 30px 80px rgba(0,0,0,.45)}
.photo img{width:100%;height:100%;object-fit:cover}
.row{display:flex;gap:26px;align-items:center}
.weeks{display:flex;gap:16px}
.weeks div{flex:1;height:120px;border:2px solid rgba(214,185,132,.5);display:flex;align-items:center;justify-content:center;
  font-family:'DM Mono';font-size:34px;color:rgba(243,240,234,.8)}
.weeks div.bad{background:rgba(214,185,132,.18);border-color:#d6b984;color:#d6b984}
.barrow{display:flex;flex-direction:column;gap:14px}
.barrow .lab{display:flex;justify-content:space-between;font-size:42px}
.barrow .lab b{font-family:'DM Mono';font-weight:500;color:#d6b984}
.track{height:34px;background:rgba(243,240,234,.1);position:relative}
.track i{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,#b08d57,#d6b984);width:0}
.bgimg{position:absolute;inset:0;background-size:cover;background-position:center;z-index:0}
.shade{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(13,22,32,.55) 0%,rgba(13,22,32,.35) 35%,rgba(13,22,32,.82) 70%,rgba(13,22,32,.95) 100%)}
.scene.hasbg{justify-content:flex-end;padding-bottom:300px}
.scene>*:not(.bgimg):not(.shade){position:relative;z-index:2}
.shot{width:100%;aspect-ratio:16/9;overflow:hidden;border:2px solid rgba(214,185,132,.7);box-shadow:0 30px 80px rgba(0,0,0,.45)}
.shot.tall{width:600px;aspect-ratio:4/5;align-self:center}
.shot img{width:100%;height:100%;object-fit:cover;transform-origin:center}
.strike{position:relative;display:inline-block}
.strike:after{content:'';position:absolute;left:-6px;right:-6px;top:55%;height:6px;background:#d6b984;transform-origin:left;transform:scaleX(var(--s,0))}
"""

JS = r"""
const CFG = __CFG__;
const ease = x => x<0?0:x>1?1:1-Math.pow(1-x,3);
const clamp = x => x<0?0:x>1?1:x;
const scenes = [...document.querySelectorAll('.scene')];
window.seek = function(t){
  document.querySelector('#bar i').style.width = (100*clamp(t/CFG.total))+'%';
  const g = document.getElementById('glow');
  g.style.transform = `translate(${Math.sin(t*0.25)*60}px,${Math.cos(t*0.2)*50}px)`;
  scenes.forEach((el,i)=>{
    const s = CFG.scenes[i];
    const fin = clamp((t-s.start)/0.35), fout = s.last ? 1 : clamp((s.end - t)/0.3);
    const vis = (t>=s.start && t<=s.end+0.001) ? Math.min(fin,fout) : 0;
    el.style.opacity = vis;
    el.style.transform = `scale(${1+0.025*clamp((t-s.start)/(s.end-s.start))})`;
    el.querySelectorAll('.shot img').forEach(im=>{ im.style.transform = `scale(${1.02+0.10*clamp((t-s.start)/(s.end-s.start))})`; });
    const bg = el.querySelector('.bgimg'); if(bg){ bg.style.transform = `scale(${1.04+0.08*clamp((t-s.start)/(s.end-s.start))})`; }
    el.querySelectorAll('[data-in]').forEach(c=>{
      const d = parseFloat(c.dataset.in);
      const p = ease((t-s.start-d)/0.5);
      c.style.opacity = p;
      c.style.transform = `translateY(${(1-p)*36}px)`;
      if(c.dataset.count){ const n=parseFloat(c.dataset.count); c.textContent = Math.round(n*ease((t-s.start-d)/0.9)); }
      if(c.dataset.bar){ c.style.width = (100*parseFloat(c.dataset.bar)*ease((t-s.start-d)/0.9))+'%'; }
      if(c.dataset.strike!==undefined){ c.style.setProperty('--s', ease((t-s.start-d-0.5)/0.5)); }
    });
  });
};
window.seek(0);
"""

def build(cfg_path, out_path):
    cfg = json.loads(pathlib.Path(cfg_path).read_text())
    photo = ROOT.parent / 'qsalon-site/dist/assets/susy.jpg'
    photo_uri = 'data:image/jpeg;base64,' + b64(photo)
    cfg['scenes'][-1]['last'] = True
    import re
    def imgs(h):
        def rep(m):
            p = pathlib.Path(m.group(1)); mime = 'image/png' if p.suffix=='.png' else 'image/jpeg'
            return f'data:{mime};base64,{b64(p)}'
        return re.sub(r'\{\{IMG:([^}]+)\}\}', rep, h)
    def bgdiv(sc):
        if not sc.get('bg'): return ''
        p = pathlib.Path(sc['bg']); mime = 'image/png' if p.suffix=='.png' else 'image/jpeg'
        return f'<div class="bgimg" style="background-image:url(data:{mime};base64,{b64(p)})"></div><div class="shade"></div>'
    scenes = '\n'.join(f'<div class="scene{" hasbg" if s.get("bg") else ""}">{bgdiv(s)}{imgs(s["html"].replace("{{SUSY}}", photo_uri))}</div>' for s in cfg['scenes'])
    slim = {'total': cfg['total'], 'scenes': [{k: s[k] for k in ('start', 'end') } | ({'last': True} if s.get('last') else {}) for s in cfg['scenes']]}
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}{CSS}</style></head><body>
<div id="stage"><div id="glow"></div><div id="frame"></div>
<div id="mark"><div class="q">Q</div><div class="t">THE Q SALON<small>FOR MEN · SARASOTA</small></div></div>
{scenes}
<div id="bar"><i></i></div></div>
<script>{JS.replace('__CFG__', json.dumps(slim))}</script></body></html>"""
    pathlib.Path(out_path).write_text(html)

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
