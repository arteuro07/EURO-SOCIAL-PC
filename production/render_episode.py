"""Build a 60-second vertical motion-comic episode from FLUX stills.

This is a motion-comic/animatic: camera movement is synthesized from still images.
It is not a generative-video model. Scene images are generated independently, so
character identity can still vary; review the artifact before publishing.
"""
import base64
import json
import os
import subprocess
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / "production" / "episodes" / "E001.json"
ASSETS = ROOT / "assets" / "episodes" / "E001"
OUT = ROOT / "dist" / "BOSS_DE_RIEN_E001.mp4"
ACCOUNT = os.environ["CLOUDFLARE_ACCOUNT_ID"]
TOKEN = os.environ["CLOUDFLARE_API_TOKEN"]
MODEL = "@cf/black-forest-labs/flux-1-schnell"
API = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/{MODEL}"
FPS = 25
WIDTH, HEIGHT = 1080, 1920


def call_flux(prompt: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 1000:
        print(f"Image déjà présente : {path}")
        return
    response = requests.post(
        API,
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"prompt": prompt, "steps": 4},
        timeout=240,
    )
    response.raise_for_status()
    ctype = response.headers.get("content-type", "")
    if "json" in ctype:
        data = response.json()
        if not data.get("success", True):
            raise RuntimeError(json.dumps(data.get("errors", data)))
        encoded = data.get("result", {}).get("image")
        if not encoded:
            raise RuntimeError("Cloudflare n'a retourné aucune image")
        raw = base64.b64decode(encoded)
    else:
        raw = response.content
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("Image FLUX invalide (PNG attendu)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    print(f"Image créée : {path}")


def timestamp(seconds: float) -> str:
    whole = int(seconds)
    millis = int(round((seconds - whole) * 1000))
    hours, rem = divmod(whole, 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def main() -> None:
    bible = json.loads((ROOT / "boss_de_rien_bible.json").read_text(encoding="utf-8"))
    episode = json.loads(EPISODE.read_text(encoding="utf-8"))
    ASSETS.mkdir(parents=True, exist_ok=True)
    segments = []
    subtitles = []
    elapsed = 0.0

    cast_descriptions = " ".join(
        f"{bible['personnages'][key]['nom']}: {bible['personnages'][key]['prompt_image']}."
        for key in episode["cast"]
    )
    for index, scene in enumerate(episode["scenes"], start=1):
        image = ASSETS / f"{scene['id']}.png"
        prompt = (
            f"{scene['image_prompt']}. {cast_descriptions} "
            f"Location: {scene['location']}. Action: {scene['action']}. "
            f"{episode['visual_style']}. Vertical 9:16 composition, "
            "clear foreground silhouettes, expressive readable faces, "
            "rich saturated colors, polished cel shading, detailed background, "
            "dynamic cinematic lighting. Keep character clothing and hairstyles "
            "as described. No speech bubbles, no letters, no captions, no logos, no watermark."
        )
        call_flux(prompt, image)
        duration = int(scene["duration_seconds"])
        segment = ASSETS / f"{scene['id']}.mp4"
        # Slow alternating camera drift creates a restrained motion-comic feel.
        zoom_expr = "min(1.12,zoom+0.00018)" if index % 2 else "if(eq(on,1),1.12,max(1.0,zoom-0.00018))"
        vf = (
            f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            f"zoompan=z='{zoom_expr}':d={duration * FPS}:"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"s={WIDTH}x{HEIGHT}:fps={FPS},setsar=1,format=yuv420p"
        )
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(image),
            "-vf", vf, "-t", str(duration), "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            str(segment)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        segments.append(segment)

        lines = scene.get("dialogue", [])
        slot = duration / max(1, len(lines))
        for j, line in enumerate(lines):
            start = elapsed + j * slot
            end = min(elapsed + duration, start + slot)
            character = bible["personnages"][line["character"]]["nom"].upper()
            text = f"{character} : {line['text']}".replace("\n", " ")
            subtitles.append(
                f"{len(subtitles)+1}\n{timestamp(start)} --> {timestamp(end)}\n{text}\n"
            )
        elapsed += duration

    concat = ASSETS / "concat.txt"
    concat.write_text("".join(f"file '{p.resolve()}'\n" for p in segments), encoding="utf-8")
    srt = ASSETS / "subtitles.srt"
    srt.write_text("\n".join(subtitles), encoding="utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-vf", f"subtitles={srt}:force_style='FontName=DejaVu Sans,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=1,Alignment=2,MarginV=100'",
        "-t", str(episode["target_duration_seconds"]),
        "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-an", str(OUT)
    ], check=True)
    print(f"ÉPISODE PRÊT : {OUT}")


if __name__ == "__main__":
    main()
