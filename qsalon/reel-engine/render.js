// node render.js reel.html outdir fps total [previewTimesCsv]
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const [html, out, fpsS, totalS, preview] = process.argv.slice(2);
  const fps = parseFloat(fpsS), total = parseFloat(totalS);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  const stage = await page.$('#stage');
  if (preview) {
    for (const t of preview.split(',')) {
      await page.evaluate(x => window.seek(x), parseFloat(t));
      await stage.screenshot({ path: path.join(out, `prev_${t}.jpg`), type: 'jpeg', quality: 85 });
    }
  } else {
    const n = Math.ceil(total * fps);
    for (let f = 0; f < n; f++) {
      await page.evaluate(x => window.seek(x), f / fps);
      await stage.screenshot({ path: path.join(out, `f${String(f).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 90 });
    }
  }
  await browser.close();
})();
