#!/usr/bin/env python3
"""Vérifie les fondations actuelles de BOSS DE RIEN."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md", "universe/series-bible.md", "universe/continuity.md",
    "universe/asset-policy.md", "assets/characters/registry.json",
    "assets/ASSET-LICENSES.md",
    "assets/characters/CHAR-KEVIN/character-brief.md",
    "assets/characters/CHAR-JUNIOR/character-brief.md",
    "assets/characters/CHAR-MAYA/character-brief.md",
    "episodes/proof-kevin/scene.html", "production/render-proof.mjs",
    ".github/workflows/render-kevin-proof.yml",
]
missing = [p for p in required if not (ROOT / p).is_file()]
if missing:
    print("FICHIERS MANQUANTS:")
    print("\n".join(missing))
    sys.exit(1)

try:
    registry = json.loads((ROOT / "assets/characters/registry.json").read_text(encoding="utf-8"))
except Exception as exc:
    print(f"JSON personnages invalide: {exc}")
    sys.exit(1)

characters = registry.get("characters", [])
ids = [c.get("id") for c in characters]
if len(ids) != len(set(ids)):
    print("Erreur: IDs de personnages en double.")
    sys.exit(1)
expected = {"CHAR-KEVIN", "CHAR-JUNIOR", "CHAR-MAYA"}
if not expected.issubset(set(ids)):
    print("Erreur: il manque un personnage principal.")
    sys.exit(1)

scene = (ROOT / "episodes/proof-kevin/scene.html").read_text(encoding="utf-8")
for marker in ("window.renderFrame=render", "window.__FILM_READY=true", "function kevin(t)"):
    if marker not in scene:
        print(f"Scène de preuve incomplète : {marker}")
        sys.exit(1)

renderer = (ROOT / "production/render-proof.mjs").read_text(encoding="utf-8")
for marker in ("playwright", "FPS*DURATION", "screenshot"):
    if marker not in renderer:
        print(f"Moteur de rendu incomplet : {marker}")
        sys.exit(1)

print("OK: structure actuelle valide")
print(f"OK: {len(characters)} personnages enregistrés")
print("OK: scène animée de Kévin et moteur image par image présents")
print("NOTE: la qualité finale doit être jugée sur le MP4 rendu.")
