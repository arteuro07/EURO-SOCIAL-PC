# EURO SOCIAL PC — studio de séries courtes

Studio de production gratuit, contrôlé depuis Android/Termux, pour créer des épisodes verticaux de **BOSS DE RIEN**. Ce dépôt conserve la bible narrative, les scripts, les métadonnées et les outils de production. Les fichiers lourds (modèles 3D, textures, voix et vidéos) doivent aussi être sauvegardés dans une bibliothèque persistante sur le téléphone.

## Objectif de production
- Épisodes cibles : 60 secondes, format vertical 9:16.
- Style visé : animation stylisée hybride 2D/3D, comédie d'action et rythme rapide.
- Langue : français familier, expressions africaines/nouchi utilisées naturellement et compréhensibles.
- Publication : manuelle par l'utilisateur. Aucune publication TikTok automatique n'est configurée.
- Budget : outils libres/gratuits ; aucun service payant requis par défaut.

## Organisation
- `universe/` : bible, continuité, relations et mystères.
- `episodes/` : scénario, dialogues, timing, légende et hashtags.
- `assets/characters/` : modèles, rigs, apparences, poses, voix et biographies.
- `assets/locations/` : décors réutilisables.
- `assets/props/` : objets récurrents.
- `assets/audio/` : sons et preuves de licence.
- `production/` : scripts de rendu et paramètres.
- `.github/workflows/` : tests automatisés sur GitHub Actions.

## Règles de continuité
1. Réutiliser les identifiants d'assets existants au lieu de recréer un personnage.
2. Avant chaque épisode, lire la bible et le registre des épisodes.
3. Toute nouvelle révélation doit être ajoutée à la chronologie.
4. Introduire les nouveaux personnages progressivement, avec une raison narrative.
5. Ne jamais enregistrer de mot de passe, jeton ou secret dans le dépôt.
6. Un workflow réussi n'est pas une preuve de vidéo publiable : vérifier le fichier MP4 et le lire avant publication.

## Premier épisode
Voir [Épisode 001 — Mission Sandwich](episodes/001-mission-sandwich.md).

## Limites honnêtes
GitHub Actions fournit des machines temporaires avec des quotas. Ce dépôt ne promet ni rendu 3D illimité, ni GPU gratuit, ni viralité. Les assets originaux doivent être sauvegardés hors du runner temporaire, notamment sur le téléphone.
