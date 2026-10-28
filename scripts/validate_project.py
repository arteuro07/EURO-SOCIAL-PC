#!/usr/bin/env python3
"""Vérifie la structure et les données de base de EURO SOCIAL PC."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md",
    "universe/series-bible.md",
    "universe/continuity.md",
    "universe/asset-policy.md",
    "episodes/001-mission-sandwich.md",
    "assets/characters/registry.json",
    "assets/ASSET-LICENSES.md",
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

episode = (ROOT / "episodes/001-mission-sandwich.md").read_text(encoding="utf-8")
for marker in ("00–05 s", "05–18 s", "18–38 s", "38–52 s", "52–60 s", "ÉPISODE 002"):
    if marker not in episode:
        print(f"Découpage incomplet : {marker}")
        sys.exit(1)

print("OK: structure du projet valide")
print(f"OK: {len(characters)} personnages enregistrés")
print("OK: épisode E001 possède ses 5 séquences et son accroche vers E002")
print("NOTE: ce test valide les données, pas un rendu vidéo.")
