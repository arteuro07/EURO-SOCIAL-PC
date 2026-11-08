# BOSS DE RIEN

Nouvelle base officielle du projet.

## Direction
Série animée courte, humour + action, esthétique manga cinématique originale, couleurs riches et décors inspirés d'un quartier africain contemporain.

## Pipeline
1. Bible créative et fiches personnages.
2. Génération des images avec Cloudflare Workers AI — FLUX.1 schnell.
3. Sélection et validation des designs.
4. Storyboards et animation.
5. Assemblage des épisodes verticaux 9:16.

## Génération des images
Le workflow **Générer les assets** lance `gen_assets.py`. Il utilise les secrets GitHub :
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`

Les fichiers existants sont ignorés. Les images sont enregistrées dans `assets/`.

> La seed seule ne garantit pas l'identité d'un personnage entre plusieurs générations. Les sorties doivent être vérifiées et les designs approuvés avant la production.
