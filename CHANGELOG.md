# Journal des versions

Format recommandé : une section par version, les changements regroupés en
« Ajouté », « Modifié », « Corrigé ».

## [0.1.0] - 2026-10-13
### Ajouté
- Modification du squelette fourni : les fichiers `models.py`, `schemas.py` et `securite.py` deviennent des dossiers qui contiennent les modeles, les schemas et la securité.
- Initialisation du projet

## [0.1.1] - 2026-10-13
### Ajouté
- ajout du mcd et du mld
- ajout du script de création de base de donnée schemas.sql et des index

## [0.1.2] - 2026-10-13
### Modifié  
- schema.sql : ajout d'une règle de contrainte sur incident.date_resolution.

### Corrigé  
- correction d'une faute d'ortographe sur station.latitude et modification du mcd et mld pour tenir en compte de cette modification

### Ajouté
- schema-donnees.md

## [0.1.3] - 2026-10-13
### Ajouté
- demarrage importer.py

## [0.1.4] - 2026-10-14
### Ajouté
- ajout des fonctions de fiabilisation des données dans api/services/fiabilisation.py
- ajout du script importer.py pour utiliser les fonctions de fiabilisation.py sur toutes les données. Commit juste avant d'envoyer les données en base de donnée.
- ajout des fonctions de fiabilisation des données utilisées dans le script d'import dans schema-donnees.md

## [0.1.5] - 2026-10-14
### Ajouté
- ajout d'une règle de fiabilisation pour la colonne `depart_horodatage` de la table `trajet`.
- export des trois tables en format csv dans la base de donnée.

## [0.1.6] - 2026-10-14
### Ajouté
- Ajout de la section audit dans le schema de données.
- ajout des trois indicateurs

## [0.1.7] - 2026-10-14
### Ajouté
- ajout du fichier database
- ajout des 4 modeles
- ajout du schema users