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
