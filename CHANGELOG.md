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