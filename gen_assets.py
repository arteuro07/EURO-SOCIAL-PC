"""Generate the BOSS DE RIEN image library with Cloudflare Workers AI / FLUX.1 schnell.

Existing files are skipped. A seed is a reproducibility hint, not an identity lock.
"""
import base64
import json
import os
import time
from pathlib import Path

import requests

ACCOUNT = os.environ["CLOUDFLARE_ACCOUNT_ID"]
TOKEN = os.environ["CLOUDFLARE_API_TOKEN"]
MODEL = "@cf/black-forest-labs/flux-1-schnell"
URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/{MODEL}"
STEPS = 4  # FLUX.1 schnell uses a fixed four-step inference process.
STYLE = (
    "original cinematic shonen manga illustration, expressive clean black ink lineart, "
    "rich vibrant color palette, polished cel shading, nuanced anime facial features, "
    "professional character concept art, consistent design, crisp details"
)
BACKGROUNDS = {
    "quartier": "Lively contemporary West African neighborhood street, colorful small shops, modest concrete buildings, corrugated metal awnings, overhead wires, warm late-afternoon sunlight",
    "terrain": "Dusty neighborhood football pitch in West Africa, simple wooden goalposts, surrounding low-rise homes, red earth, dramatic golden-hour sky",
    "maquis": "Welcoming open-air West African maquis restaurant at night, simple tables and chairs, warm bulbs, subtle colorful neon accents, cinematic nighttime atmosphere"
}
ROOT = Path("assets")


def decode_image(response: requests.Response) -> bytes:
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        payload = response.json()
        if not payload.get("success", True):
            raise RuntimeError(json.dumps(payload.get("errors", payload), ensure_ascii=False))
        encoded = payload.get("result", {}).get("image")
        if not encoded:
            raise RuntimeError(f"Réponse JSON sans image: {response.text[:500]}")
        return base64.b64decode(encoded)
    if not response.content:
        raise RuntimeError("Réponse image vide")
    return response.content


def generate(prompt: str, output: Path) -> None:
    if output.exists() and output.stat().st_size > 0:
        print(f"SKIP déjà présent : {output}")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {"prompt": prompt, "steps": STEPS}
    for attempt in range(1, 4):
        try:
            response = requests.post(
                URL,
                headers={"Authorization": f"Bearer {TOKEN}"},
                json=payload,
                timeout=180,
            )
            if response.status_code == 200:
                image_bytes = decode_image(response)
                if not image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
                    raise RuntimeError("Le résultat reçu n'est pas un PNG valide")
                output.write_bytes(image_bytes)
                print(f"OK : {output}")
                return
            print(f"HTTP {response.status_code}, essai {attempt}: {response.text[:300]}")
        except Exception as exc:
            print(f"Erreur essai {attempt}: {exc}")
        if attempt < 3:
            time.sleep(5 * attempt)
    raise RuntimeError(f"Échec après 3 essais : {output}")


def main() -> None:
    bible_path = Path("boss_de_rien_bible.json")
    bible = json.loads(bible_path.read_text(encoding="utf-8"))

    for key, info in bible["personnages"].items():
        base = info["prompt_image"]
        prompt = (
            f"{base}, {STYLE}, "
            "full body character master reference, neutral relaxed standing pose, "
            "front three-quarter view, entire body and shoes visible, "
            "single character centered, clean pure white studio background, "
            "no extra people, no text, no watermark"
        )
        generate(prompt, ROOT / "characters" / key / "master.png")

    for place in bible["lieux"]:
        description = BACKGROUNDS.get(place)
        if not description:
            continue
        prompt = (
            f"{description}, {STYLE}, detailed wide establishing shot, "
            "environment concept art, no people, no characters, no text, no watermark"
        )
        generate(prompt, ROOT / "backgrounds" / f"{place}.png")


if __name__ == "__main__":
    main()
