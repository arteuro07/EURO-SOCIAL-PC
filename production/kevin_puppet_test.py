#!/usr/bin/env python3
"""Prototype d'animation articulée de Kévin — rendu image par image."""
import math, os, subprocess
from PIL import Image, ImageDraw

W, H, FPS, DURATION = 540, 960, 24, 4
OUT = "dist/kevin-puppet"
os.makedirs(OUT, exist_ok=True)

def line(draw, pts, fill, width):
    draw.line(pts, fill=fill, width=width, joint="curve")

def frame(i):
    t = i / FPS
    im = Image.new("RGB", (W, H), (18, 22, 42))
    d = ImageDraw.Draw(im)
    # Décor graphique simple
    d.rectangle((0, 735, W, H), fill=(31, 38, 59))
    for x in range(20, W, 90):
        d.rectangle((x, 560, x+48, 735), fill=(38, 46, 68))
        d.rectangle((x+9, 580, x+18, 610), fill=(242, 174, 76))
    # Ombre au sol
    d.ellipse((145, 845, 395, 885), fill=(10, 13, 27))
    bob = int(5 * math.sin(t * math.tau * 1.2))
    cx, cy = 270, 430 + bob
    # Jambes et chaussures
    line(d, [(235, 650+bob), (220, 820)], (75, 57, 52), 42)
    line(d, [(310, 650+bob), (325, 820)], (75, 57, 52), 42)
    d.ellipse((174, 798, 244, 844), fill=(22, 25, 35))
    d.ellipse((292, 798, 362, 844), fill=(22, 25, 35))
    # Bras articulés : oscillation visible
    a = math.sin(t * math.tau * 1.0) * 28
    for shoulder, ang in [((190, 470+bob), -25-a), ((350, 470+bob), 25+a)]:
        rad = math.radians(ang)
        elbow = (shoulder[0] + int(105*math.sin(rad)), shoulder[1] + int(105*math.cos(rad)))
        hand = (elbow[0] + int(92*math.sin(rad+0.15)), elbow[1] + int(92*math.cos(rad+0.15)))
        line(d, [shoulder, elbow], (31, 34, 48), 62)
        line(d, [shoulder, elbow], (52, 57, 76), 48)
        d.ellipse((elbow[0]-24, elbow[1]-24, elbow[0]+24, elbow[1]+24), fill=(91, 52, 43))
        line(d, [elbow, hand], (91, 52, 43), 35)
        d.ellipse((hand[0]-19, hand[1]-19, hand[0]+19, hand[1]+19), fill=(112, 66, 52))
    # Torse / hoodie
    d.rounded_rectangle((168, 425+bob, 372, 690+bob), radius=48, fill=(38, 43, 58), outline=(11, 14, 27), width=7)
    d.polygon([(245, 440+bob), (270, 485+bob), (295, 440+bob)], fill=(18, 21, 34))
    d.arc((220, 440+bob, 320, 545+bob), 15, 165, fill=(118, 124, 145), width=5)
    d.text((258, 570+bob), "♛", fill=(232, 184, 82), stroke_width=1)
    # Cou
    d.rectangle((244, 370+bob, 296, 455+bob), fill=(105, 61, 49))
    # Tête légèrement mobile
    head_x = int(5 * math.sin(t * math.tau * 0.6))
    hy = 285 + bob
    d.ellipse((175+head_x, hy-115, 365+head_x, hy+115), fill=(112, 66, 52), outline=(30, 22, 25), width=7)
    # Afro
    d.ellipse((165+head_x, hy-145, 375+head_x, hy-15), fill=(24, 20, 22), outline=(10, 10, 15), width=5)
    for x,y,r in [(190,-105,28),(225,-137,31),(265,-145,30),(305,-135,32),(345,-103,27),(177,-70,24),(360,-65,22)]:
        d.ellipse((x+head_x-r, hy+y-r, x+head_x+r, hy+y+r), fill=(24,20,22))
    # Sourcils / yeux
    d.arc((205+head_x, hy-25, 250+head_x, hy+5), 190, 345, fill=(24,18,19), width=8)
    d.arc((285+head_x, hy-25, 330+head_x, hy+5), 190, 345, fill=(24,18,19), width=8)
    blink = (i % 72 in (0,1))
    if blink:
        line(d, [(211+head_x,hy+15),(245+head_x,hy+15)], (20,16,18), 6)
        line(d, [(292+head_x,hy+15),(326+head_x,hy+15)], (20,16,18), 6)
    else:
        d.ellipse((215+head_x, hy+3, 239+head_x, hy+35), fill=(245,235,218))
        d.ellipse((297+head_x, hy+3, 321+head_x, hy+35), fill=(245,235,218))
        d.ellipse((224+head_x, hy+10, 235+head_x, hy+32), fill=(20,18,20))
        d.ellipse((306+head_x, hy+10, 317+head_x, hy+32), fill=(20,18,20))
    # Nez et bouche animée (parole)
    d.polygon([(265+head_x,hy+28),(253+head_x,hy+62),(274+head_x,hy+62)], fill=(82,45,39))
    opening = 5 + int(15 * abs(math.sin(t * math.tau * 3.2)))
    d.ellipse((246+head_x, hy+76, 292+head_x, hy+76+opening), fill=(48,13,19), outline=(43,17,19), width=3)
    # Ligne de mouvement discrète
    d.text((24, 28), "BOSS DE RIEN  •  TEST PERSONNAGE", fill=(239, 196, 105))
    return im

for n in range(FPS * DURATION):
    frame(n).save(f"{OUT}/frame-{n:03d}.png")
subprocess.run([
    "ffmpeg", "-y", "-framerate", str(FPS), "-i", f"{OUT}/frame-%03d.png",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    f"{OUT}/KEVIN-PUPPET-TEST.mp4"
], check=True)
subprocess.run([
    "ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate",
    "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1",
    f"{OUT}/KEVIN-PUPPET-TEST.mp4"
], check=True)
