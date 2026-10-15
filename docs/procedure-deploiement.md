# Procédure de déploiement  
#### Prérequis  
- postgresql, avec préférablement une interface graphique (pg admin4)  
- un éditeur de code (VS Code par exemple)  
- python 3.14.7.  
  
#### Installation de l'environnement virtuel  
> Pour isoler les dépendances, une environnement virtuel est fortemment recommandé.  
  
Créer un environnement virtuel :  
`python -m venv .venv`

Activer l'environnement virtuel :
`./.venv/Scripts/activate`  
  
#### Installation des dépendances  
Installer les dependances avec `pip install -r requirements.txt`  
  
#### Création et chargement de la base de données  
> Creation de la base de données :  
  
Créer la base de donnée avec le nom : `veloville`, en utilisant `CREATE DATABASE veloville` ou l'interface de pgadmin.    
  
> Creation du schema  
  
Créer les tables en executant le script `sql/schema.sql`  

> Chargement des tables  
  
Charger la base de données en executant le script `scripts/importer.py`  

Charger les utilisateurs en executant le script `sql/comptes.sql`  
  
#### Initialiser les variables d'environnement  
Créer un fichier `.env` à la racine du projet, en copiant le fichier `.env.example`  
Modifier les variables par defaut si besoin  
Modifier absolument les variables suivantes :  
> DATABASE URL  
  
Modifier le nom et mot de passe de postgres ainsi le port sur lequel la base de donnée à été créee.  
  
> JWT_SECRET  
  
Generer un JWT secret à l'aide du script `scripts/generate_jwt_secret.py`
#### Démarage de l'API  
Démarrer l'API avec la commande `uvicorn api.main:app --reload`  
  
#### Démarage du front  
Sur un deuxième terminal, démarrer le front avec la commande `streamlit run front/app.py`