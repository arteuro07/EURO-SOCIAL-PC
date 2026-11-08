#!/usr/bin/env python3
"""BOSS DE RIEN — deterministic 2D compositing and FFmpeg episode renderer."""
from __future__ import annotations
import argparse, json, math, os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
W, H = 720, 1280
FPS = 24

def load_font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def cover(img: Image.Image, size=(W, H)) -> Image.Image:
    img = img.convert("RGB")
    scale = max(size[0] / img.width, size[1] / img.height)
    nw, nh = round(img.width * scale), round(img.height * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left, top = (nw-size[0])//2, (nh-size[1])//2
    return img.crop((left, top, left+size[0], top+size[1]))

def placeholder_scene(scene, t):
    # Only for engine smoke tests; production scenes should provide a background image.
    top = tuple(scene.get("color_top", [30, 20, 55]))
    bottom = tuple(scene.get("color_bottom", [210, 75, 65]))
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        q = y / max(1, H-1)
        c = tuple(int(top[i]*(1-q)+bottom[i]*q) for i in range(3))
        for x in range(W): px[x,y] = c
    d = ImageDraw.Draw(im, "RGBA")
    for i in range(9):
        x = (i*113 + int(t*28)) % (W+180) - 90
        d.ellipse((x, 170+i*95, x+210, 380+i*95), fill=(255,190,90,22))
    d.polygon([(0,900),(120,700),(250,900),(390,640),(560,900),(720,720),(720,1280),(0,1280)], fill=(12,15,30,160))
    d.text((42, 90), scene.get("label", "BOSS DE RIEN"), font=load_font(28, True), fill=(255,255,255,210))
    return im

def add_character(canvas, item, t):
    path = ROOT / item["image"]
    if not path.exists():
        raise FileNotFoundError(f"Personnage introuvable: {path}")
    sprite = Image.open(path).convert("RGBA")
    target_h = int(item.get("height", 620))
    target_w = max(1, int(sprite.width * target_h / sprite.height))
    sprite = sprite.resize((target_w,target_h), Image.Resampling.LANCZOS)
    x = int(item.get("x", (W-target_w)//2) + item.get("move_x", 0)*math.sin(t*2*math.pi/max(0.1,item.get("duration",1))))
    y = int(item.get("y", H-target_h-80) + item.get("move_y", 0)*math.sin(t*4))
    canvas.alpha_composite(sprite, (x,y))

def draw_caption(canvas, text):
    if not text: return
    d = ImageDraw.Draw(canvas, "RGBA")
    font = load_font(35, True)
    max_width = W-90
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = (current+" "+word).strip()
        if d.textbbox((0,0), trial, font=font)[2] <= max_width: current = trial
        else:
            if current: lines.append(current)
            current = word
    if current: lines.append(current)
    lines = lines[:3]
    line_h = 48
    box_h = len(lines)*line_h+34
    y0 = H-box_h-72
    d.rounded_rectangle((28,y0,W-28,H-55), radius=22, fill=(8,8,18,205), outline=(255,255,255,100), width=2)
    for i,line in enumerate(lines):
        box = d.textbbox((0,0),line,font=font)
        x = (W-(box[2]-box[0]))//2
        d.text((x,y0+14+i*line_h),line,font=font,fill=(255,255,255,255),stroke_width=1,stroke_fill=(0,0,0,255))

def render_frame(scene, t):
    bg_path = scene.get("background")
    if bg_path:
        p = ROOT / bg_path
        if not p.exists(): raise FileNotFoundError(f"Décor introuvable: {p}")
        base = cover(Image.open(p))
    else:
        base = placeholder_scene(scene,t)
    # Slow camera push-in / pan, keeping the final canvas vertical.
    zoom = float(scene.get("zoom", 1.06))
    progress = t / max(float(scene["duration"]), 0.001)
    z = 1.0 + (zoom-1.0)*progress
    nw, nh = int(W*z), int(H*z)
    base = base.resize((nw,nh),Image.Resampling.LANCZOS)
    pan_x = int((nw-W)*float(scene.get("pan_x",0.0))*progress)
    pan_y = int((nh-H)*float(scene.get("pan_y",0.0))*progress)
    base = base.crop((pan_x,pan_y,pan_x+W,pan_y+H)).convert("RGBA")
    for character in scene.get("characters",[]): add_character(base,character,t)
    draw_caption(base, scene.get("caption",""))
    return base.convert("RGB")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--storyboard",default="episodes/demo/storyboard.json")
    ap.add_argument("--output",default="dist/BOSS-DE-RIEN-demo.mp4")
    ap.add_argument("--width",type=int,default=720)
    ap.add_argument("--height",type=int,default=1280)
    ap.add_argument("--fps",type=int,default=FPS)
    ap.add_argument("--upscale",action="store_true",help="Export final file at 1080x1920")
    args=ap.parse_args()
    global W,H,FPS
    W,H,FPS=args.width,args.height,args.fps
    data=json.loads((ROOT/args.storyboard).read_text(encoding="utf-8"))
    scenes=data.get("scenes",[])
    if not scenes: raise ValueError("Le storyboard ne contient aucune scène.")
    if any(float(s.get("duration",0))<=0 for s in scenes): raise ValueError("Chaque scène doit avoir une durée positive.")
    total=sum(float(s["duration"]) for s in scenes)
    out=ROOT/args.output
    out.parent.mkdir(parents=True,exist_ok=True)
    cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for si,scene in enumerate(scenes,1):
            count=round(float(scene["duration"])*FPS)
            for frame in range(count):
                t=frame/FPS
                image=render_frame(scene,t)
                proc.stdin.write(image.tobytes())
            print(f"Scène {si}/{len(scenes)} rendue ({scene['duration']} s)",flush=True)
        proc.stdin.close()
        code=proc.wait()
        if code: raise RuntimeError(f"FFmpeg a échoué (code {code})")
    except Exception:
        if proc.stdin and not proc.stdin.closed: proc.stdin.close()
        proc.kill()
        raise
    if args.upscale:
        temp=out.with_name(out.stem+"-720p.mp4")
        out.replace(temp)
        up=["ffmpeg","-y","-loglevel","error","-i",str(temp),"-vf","scale=1080:1920:flags=lanczos","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
        subprocess.run(up,check=True)
        temp.unlink()
    print(f"VIDÉO_OK={out.relative_to(ROOT)}")
    print(f"DURÉE={total:.2f}s | FORMAT={'1080x1920' if args.upscale else f'{W}x{H}'} | FPS={FPS}")

if __name__=="__main__":
    main()
