# Moteur de production

Objectif : pipeline reproductible pour format vertical 9:16, avec Blender pour la scène 3D, puis FFmpeg pour l'encodage et le mixage. La première étape est un test automatisé de la structure du projet ; aucun rendu final n'est encore validé.

Les scripts de rendu devront :
1. lire la fiche de l'épisode et les identifiants d'assets ;
2. réutiliser les modèles enregistrés dans la bibliothèque ;
3. générer les scènes/animations et sous-titres ;
4. exporter un MP4 H.264/AAC 1080x1920 ;
5. vérifier la durée, le format et la lisibilité du fichier ;
6. sauvegarder le fichier source et les métadonnées avec l'épisode.

Ne pas faire dépendre la bibliothèque d'assets des runners GitHub Actions temporaires.


## Mini générateur d'assets 3D

Le script `production/asset_generator.py` génère un fichier Blender modifiable (`.blend`) et une fiche PNG pour chaque personnage :
- `kevin` : afro bouclé, sweat anthracite, cordons clairs et couronne jaune ;
- `junior` : casquette bleue, lunettes et veste bleue ;
- `maya` : coiffure tressée, veste rose et bijoux dorés.

Le workflow GitHub Actions `Générateur d'assets personnages` lance les trois générations et publie trois artefacts séparés, conservés 14 jours. Depuis GitHub, ouvrir **Actions → Générateur d'assets personnages → dernier lancement → Artifacts**.

Commande locale Blender :
```bash
blender -b -t 2 --python production/asset_generator.py -- --character kevin --out output/assets --size 480
```

**Limite connue :** c'est un générateur procédural de base, pas un système de sculpture IA, de retopologie ni de rig facial professionnel. Les modèles générés doivent être inspectés et améliorés ; la génération réussie ne signifie pas que la qualité artistique est validée. Les fichiers publiés comme artefacts GitHub expirent après 14 jours : récupérer et sauvegarder les fichiers nécessaires.
