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

> FLUX.1 Schnell accepte uniquement le prompt et le paramètre steps (fixé à 4) : aucun seed n'est envoyé. Le générateur crée une image maîtresse par personnage et un décor par lieu. Une image maîtresse sert de référence visuelle ; elle ne garantit pas à elle seule une identité parfaite dans de nouvelles générations. Les designs doivent être vérifiés et approuvés avant la production.
