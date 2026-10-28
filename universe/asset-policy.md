# Politique de bibliothèque d'assets

## Identifiants stables
- Personnages : `CHAR-...`
- Lieux : `LOC-...`
- Accessoires : `PROP-...`
- Audio : `AUD-...`
- Versions : `v001`, `v002`, etc. Ne pas remplacer silencieusement un asset déjà utilisé dans un épisode publié.

## Dossier par personnage
Chaque personnage devrait contenir :
- `model/` : source 3D et exports ;
- `rig/` : squelette/contrôleurs ;
- `textures/` : textures originales ;
- `expressions/` et `poses/` : bibliothèque réutilisable ;
- `voice/` : voix et notes de prononciation, avec consentement/licence ;
- `character.json` : ID, apparence, palette, traits, voix, version et épisodes utilisés.

## Provenance et sauvegarde
Pour chaque fichier externe, noter la source, la licence, l'auteur et les restrictions dans `assets/ASSET-LICENSES.md`. Garder les fichiers lourds dans la bibliothèque locale du téléphone et faire des sauvegardes. Git convient aux scripts et petits fichiers ; les quotas GitHub et Git LFS ne sont pas illimités. Les runners GitHub Actions sont temporaires : ne pas compter sur eux pour conserver les assets.

## Contrôle avant publication
- Vérifier la licence de chaque modèle, son, police, texture et musique.
- Vérifier que le MP4 est lisible, en 9:16, avec audio et sous-titres corrects.
- Lire l'épisode complet sur téléphone avant publication manuelle.
