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

## [0.1.8] - 2026-10-15
### Ajouté
- ajout et complétion des schema incidents.py et trajets.py
- ajout de la pagination pour ces schemas

### Modifié  
- securite/indicateurs.py, renommage des colonnes conformement au sujet
- modification d'une contrainte check dans schema.sql

## [1.0.0] - 2026-10-15
### Ajouté
- ajout des 4 routeurs incidents.py, indicateurs.py, stations.py et trajets.py
- declaration de ces routeurs dans le main

## [1.1.0] - 2026-10-15
### Ajouté
- ajout de la procedure de déploiement  
- ajout d'un script de generation de jwt secret  
- ajout de la partie sécurité de l'application :  
    - ajout des configurations manquantes dans config.py
    - ajout des fichiers security.py et depencencies.py qui gerent tous les deux les fonctions de sécurité et gestion de role de l'application
    - ajout de la route POST auth/login
    - sécurisation de la route PUT /incidents/{incident_id}/statut

## [1.1.2] - 2026-10-15
### Ajouté
- ajout de la page d'accueil en front app.py
- ajout de api_client.py permettane de centraliser les appels API
- ajout de front/commun.py pour permettre de gerer la connexion des utilisateurs et des roles
- ajout de la premiere page 1_Stations.py
- ajout de services/front/service pour isoler la logique metier de streamlit

### Modifié  
- routers/stations.py pour permettre de filtrer les communes