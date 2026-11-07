import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const OUT=process.env.OUT_DIR || 'out';
const WIDTH=720, HEIGHT=1280, FPS=24, DURATION=8;
await fs.rm(OUT,{recursive:true,force:true});
await fs.mkdir(path.join(OUT,'frames'),{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const page=await browser.newPage({viewport:{width:WIDTH,height:HEIGHT},deviceScaleFactor:1});
page.on('pageerror',e=>{throw e});
await page.goto('file://'+path.resolve('episodes/proof-kevin/scene.html'));
await page.waitForFunction(()=>window.__FILM_READY===true);
for(let frame=0;frame<FPS*DURATION;frame++){
  const t=frame/FPS;
  await page.evaluate(t=>window.renderFrame(t),t);
  await page.screenshot({path:path.join(OUT,'frames',String(frame).padStart(4,'0')+'.png')});
}
await browser.close();
console.log('Rendered',FPS*DURATION,'frames');
