# VéloVille — Plateforme de valorisation des données

À compléter : présentation du projet, prérequis, installation, lancement de
l'API et du front, exécution des tests, liens vers la documentation
(docs/), auteur et version.
# Presentation du projet
Le Projet comporte une base de donnée postgresql, une API fastAPI et un front streamlit. Les objectifs de ce projet sont :

1. Disposer d'une base de données unique, fiable et documentée des stations, des trajets et des incidents.
2. Automatiser l'import et la fiabilisation des exports, avec un journal des données écartées.
3. Exposer les données et trois indicateurs par une API sécurisée, afin que d'autres outils puissent les consommer.
4. Offrir aux équipes une restitution simple, consultable depuis un poste de travail ou une tablette, sans compétence technique.
5. Distinguer ce que peut faire un exploitant (suivre et traiter les incidents) de ce que peut faire la direction (consulter).

# Depoloiement
Pour le déploiement de l'application, se référer au fichier procedure-deploiement.md.

# Tests
Pour lancer les tests unitaire et d'integration :  
`python -m pytest -v`  

Pour evaluer le coverage des tests de l'application :
`pytest --cov=api/services --cov-report=term-missing `

Le coverage du dossier services est de 76%.

# Choix écoresponsables
> En adéquation avec la partie 7.5 du cahier des charges, l'application doit être écoresponsable.  
  
- L'application ne charge pas les donénes automatiquement, seulement avec un script lancable manuellement
- Tous les gros résultats sont paginés, ce qui permet de faire des appels plus légers à la base de donnée
- Certaines données sont mises en cache (1h), la liste des stations et la liste des incidents permettant le menu déroulant des pages station et incident, car il n'est pas necessaire d'appeller la base de donnée à chaque clic sur l'application
- seules les dépendances utiles au projet sont importees

# Changements d'architecture du projet
Quelques modifications sur le squelette de base du fichier :
Le fichier `models.py` est devenu un dossier, contenant chacun les modeles ORM utilisés, pour améliorer la clarté du code. Le fichier `schemas.py` est aussi un dossier contenant chacun des fichier représentant un format Pydantic d'entrée ou de sortie des données (pour l'API). Les fichiers concernants la sécurité sont regroupés dans un dossier `securité`. 