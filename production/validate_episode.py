#!/usr/bin/env python3
"""Validate BOSS DE RIEN episode JSON without calling paid or external APIs."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIBLE = ROOT / "boss_de_rien_bible.json"
EPISODE_DIR = ROOT / "production" / "episodes"

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)

def main() -> None:
    bible = json.loads(BIBLE.read_text(encoding="utf-8"))
    known_characters = set(bible.get("personnages", {}))
    known_locations = set(bible.get("lieux", []))
    files = sorted(EPISODE_DIR.glob("E*.json"))
    if not files:
        fail("Aucun épisode E*.json trouvé.")
    for path in files:
        episode = json.loads(path.read_text(encoding="utf-8"))
        if not re.fullmatch(r"E\d{3}", episode.get("id", "")):
            fail(f"{path.name}: identifiant invalide.")
        scenes = episode.get("scenes", [])
        if not scenes:
            fail(f"{path.name}: aucune scène.")
        total = 0
        scene_ids = set()
        for scene in scenes:
            sid = scene.get("id")
            if not sid or sid in scene_ids:
                fail(f"{path.name}: identifiant de scène absent ou dupliqué: {sid}")
            scene_ids.add(sid)
            duration = scene.get("duration_seconds")
            if not isinstance(duration, int) or duration < 1:
                fail(f"{path.name}/{sid}: durée invalide.")
            total += duration
            if scene.get("location") not in known_locations:
                fail(f"{path.name}/{sid}: lieu inconnu.")
            unknown = set(scene.get("characters", [])) - known_characters
            if unknown:
                fail(f"{path.name}/{sid}: personnages inconnus: {sorted(unknown)}")
            if not scene.get("image_prompt", "").strip():
                fail(f"{path.name}/{sid}: image_prompt vide.")
            if not scene.get("action", "").strip():
                fail(f"{path.name}/{sid}: action vide.")
            for line in scene.get("dialogue", []):
                if line.get("character") not in known_characters:
                    fail(f"{path.name}/{sid}: locuteur inconnu.")
                if not line.get("text", "").strip():
                    fail(f"{path.name}/{sid}: réplique vide.")
        target = episode.get("target_duration_seconds")
        if total != target:
            fail(f"{path.name}: durée des scènes={total}s, cible={target}s.")
        print(f"OK {path.name}: {len(scenes)} scènes, {total}s, personnages={', '.join(sorted(set(episode.get('cast', []))))}")
    print(f"Validation terminée: {len(files)} épisode(s). Aucun appel API effectué.")

if __name__ == "__main__":
    main()
