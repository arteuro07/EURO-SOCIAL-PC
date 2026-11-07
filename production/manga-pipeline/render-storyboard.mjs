import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const OUT = process.env.OUT_DIR || 'out';
const STORYBOARD = process.env.STORYBOARD || 'episodes/proof-kevin/storyboard.json';
const storyboard = JSON.parse(await fs.readFile(STORYBOARD, 'utf8'));
const FPS = storyboard.fps;
const WIDTH = 720, HEIGHT = 1280;
const totalFrames = Math.round(storyboard.duration_seconds * FPS);

function shotAt(t) {
  return storyboard.shots.find(s => t >= s.start && t < s.end) || storyboard.shots.at(-1);
}
function cameraFor(shot, local, frame) {
  const size = shot.shot_size;
  const zoomBase = size === 'extreme-close-up' ? 2.65 : size === 'close-up' ? 1.62 : size === 'wide' ? 0.92 : 1.08;
  const move = shot.camera?.move || 'static';
  const intensity = Math.max(0, Math.min(1, shot.camera?.intensity || 0));
  const push = move === 'push-in' ? 1 + intensity * local : 1;
  const shake = move === 'shake' ? intensity * 11 : 0;
  const phase = frame * 1.73;
  let fx = 360, fy = 640;
  if (size === 'close-up') { fx = 480; fy = 570; }
  if (size === 'extreme-close-up') { fx = 360; fy = 285; }
  const zoom = zoomBase * push;
  const dx = 360 - fx * zoom + Math.sin(phase) * shake;
  const dy = 640 - fy * zoom + Math.cos(phase * 1.17) * shake;
  return `matrix(${zoom},0,0,${zoom},${dx},${dy})`;
}

await fs.rm(OUT, { recursive: true, force: true });
await fs.mkdir(path.join(OUT, 'frames'), { recursive: true });
const browser = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
const page = await browser.newPage({ viewport: { width: WIDTH, height: HEIGHT }, deviceScaleFactor: 1 });
page.on('pageerror', e => { throw e; });
await page.goto('file://' + path.resolve('episodes/proof-kevin/scene.html'));
await page.waitForFunction(() => window.__FILM_READY === true);

for (let frame = 0; frame < totalFrames; frame++) {
  const t = frame / FPS;
  const shot = shotAt(t);
  const local = Math.max(0, Math.min(1, (t - shot.start) / (shot.end - shot.start)));
  await page.evaluate(({ t, transform, dialogue, shotId }) => {
    const canvas = document.getElementById('film');
    canvas.style.transformOrigin = '0 0';
    canvas.style.transform = transform;
    window.renderFrame(t);
    const ctx = canvas.getContext('2d');
    if (dialogue) {
      ctx.save();
      ctx.fillStyle = 'rgba(7,12,22,.88)';
      ctx.strokeStyle = 'rgba(244,201,79,.95)';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.roundRect(48, 1090, 624, 112, 20);
      ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#fff';
      ctx.font = '800 27px system-ui,sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(dialogue, 360, 1146, 580);
      ctx.restore();
    }
    // Small editorial shot marker is useful in proof renders, never in final episodes.
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,.42)';
    ctx.fillRect(610, 24, 82, 30);
    ctx.fillStyle = '#fff';
    ctx.font = '600 13px system-ui,sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(shotId, 651, 44);
    ctx.restore();
  }, {
    t,
    transform: cameraFor(shot, local, frame),
    dialogue: (shot.dialogue || []).map(d => d.text).join(' '),
    shotId: shot.id
  });
  await page.screenshot({ path: path.join(OUT, 'frames', String(frame).padStart(4, '0') + '.png') });
}
await browser.close();
console.log(`Storyboard render complete: ${storyboard.shots.length} shots, ${totalFrames} frames at ${FPS} fps.`);
