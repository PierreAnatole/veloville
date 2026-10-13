# Schéma de données  
#### Table station  
station = (<ins>`station_id`</ins> VARCHAR(10), `nom` VARCHAR(100), `commune` VARCHAR(50), `capacite` INTEGER, `latitude` NUMERIC(8,5), `longitude` NUMERIC(8,5), `date_mise_en_service` DATE);  
> Table representant une station.  
> `station_id` : id de la table, de ce format : S + 3 chiffres (ex. S001). RG1 : la station est identifiée de manière unique par station_id.  
> `nom` : commune et lieu (ex. Lille - Gare).  
> `commune` : commune d'implantation (9 communes de la métropole).  
> `capacite` : Nombre de points d'attaches. RG1 : c'est un entier superieur à 0.  
> `latitude` : Coordonnée WGS84, 8 chiffres dont 5 décimales.  
> `longitude` : Coordonnée WGS84, 8 chiffres dont 5 décimales.  
> `date_mise_en_service` : Date d'ouverture de la station, format AAAA-MM-JJ.  
  
###### Règles de gestion concernées :  
> RG1 : Une station est identifiée de façon unique par station_id. Sa capacité est un entier strictement positif.  
  
La règle est enforcée par une contrainte de clé primaire sur station_id et par un une contrainte SQL :`CHECK (capacite>0)`
  
#### Table incident  
incident = (<ins>`incident_id`</ins> VARCHAR(12), `date_signalement` TIMESTAMP, `cible` VARCHAR(10), `velo_id` CHAR(5), `type_incident` VARCHAR(30), `statut` VARCHAR(10), `date_resolution` TIMESTAMP, `technicien` VARCHAR(50), `#station_id`);  
> Table representant un incident.  
> `incident_id` : id de la table, de ce format : I2026- + 4 chiffres (ex. I2026-0001).  
> `date_signalement` : Date et heure du signalement, format AAAA-MM-JJ HH:MM.  
> `cible`	: Nature de l'équipement concerné. RG6 : doit correspondre à `velo` ou `station`.  
> `velo_id` : référence vélo, ou vide. RG6 : Renseigné si et seulement si cible = velo.  
> `station_id` : référence station_id, ou vide. RG6 : Renseigné si et seulement si cible = station. RG6 : station_id doit exister dans la table station.  
> `type_incident` : type de l'incident. Catégorie : vandalisme, selle abimee, eclairage HS, chaine deraillee, ecran borne illisible, pneu creve, frein defectueux, borne hors service.  
> `statut` : État de traitement. RG7 : le statut est de l'une de ces 3 catégorie valeurs : ouvert, en_cours ou resolu. RG7 : les transitions autorisées sont ouvert -> en_cours, ouvert -> resolu et en_cours -> resolu. Un incident résolu n'évolue plus.  
> `date_resolution` : date de résolution de l'incident, format AAAA-MM-JJ HH:MM, ou vide. RG8 : Renseignée uniquement si le statut est resolu. RG8 : La date est postérieure ou égale au signalement.  
> `technicien` : Technicien en charge, RG8 : Renseigné en principe dès la prise en charge. RG8 : peut être nul, son absence n'empêche pas l'enregistrement mais doit être signalé.  

###### Règles de gestion concernées :
> RG6 : Un incident vise soit un vélo, soit une station, jamais les deux ni aucun : cible détermine laquelle des deux références est renseignée. Une station visée doit exister dans le référentiel.  
  
La règle est enforcée par deux contraintes SQL, l'une au niveau de `cible` : `CHECK (cible in ('velo', 'station'))` et l'autre au niveau de la table (OU exclusif sur les champs `id_station` et `id_velo` forçant l'un des deux scénarios) : `CONSTRAINT velo_XOR_station CHECK ((cible='velo' AND velo_id IS NOT NULL AND station_id IS NULL) OR (cible='station' AND station_id IS NOT NULL AND velo_id IS NULL))`. La règle pour la station visée est enforcée par une contrainte de clé étrangère sur la colonne `station_id` : `FOREIGN KEY(station_id) REFERENCES station(station_id)`  
   
> RG7 : Un incident est dans l'un des trois statuts ouvert, en_cours, resolu. Les transitions autorisées sont ouvert -> en_cours, ouvert -> resolu et en_cours -> resolu. Un incident résolu n'évolue plus.  
  
La règle est enforcée par une contrainte SQL sur `statut` : `CHECK (statut in ('ouvert', 'en_cours', 'resolu'))`. La contrainte sur les états de transition est enforcée dans le routeur `incidents.py`  
  
> RG8 : La date de résolution est renseignée si et seulement si l'incident est résolu, et elle est postérieure ou égale à la date de signalement. Le nom du technicien est attendu dès la prise en charge ; son absence est signalée mais n'empêche pas l'enregistrement.  
  
La règle est enforcée par une contrainte SQL sur le champ `date_resolution` : `CHECK ((date_resolution IS NULL AND statut!='resolu') OR (date_resolution IS NOT NULL AND statut='resolu') AND date_resolution>date_signalement)`  
  
#### Table trajet  
trajet = (<ins>`trajet_id`</ins> VARCHAR(12), `velo_id` VARCHAR(8), `depart_horodatage` TIMESTAMP, `duree_secondes` INTEGER, `type_usager` VARCHAR(15), `usager_ref` CHAR(9), `#station_depart`, `#station_arrivee`); 

> `trajet_id`	: id de la table, de ce format : T + 6 chiffres (ex. T480001).  
> `velo_id` : id du vélo emprubté, de ce format : V + 4 chiffres (ex. V1167).  
> `depart_horodatage` : Date et heure de retrait du vélo, format AAAA-MM-JJ HH:MM:SS.  
> `station_depart` : Station de retrait, référence station_id. RG2 : la station de départ est obligatoire. RG2 : la station de départ doit correspondre à un id_station dans la table station.  
> `station_arrivee` : Station de restitution, référence station_id. RG2, RG3 : peut être vide. RG2 : lorsque la station est renseignée elle doit correspondre à un id_station dans la table station.  
> `duree_secondes` : Durée de la location en secondes. RG4 : entier > 0.  
> `type_usager` : Type d'usager. abonne ou occasionnel.  
> `usager_ref` : Pseudonyme de l'abonné. RG5 : le pseudonyme est une version hachée et tronquée du numéro d'abonné. De ce format : texte, U + 8 caractères hexadécimaux, ou vide. RG5 : le champ est toujours vide pour un usager occasionnel.  
  
> RG2 : Un trajet relie deux stations du référentiel : la station de départ est obligatoire et doit exister ; la station d'arrivée, lorsqu'elle est renseignée, doit exister.  
  
La règle est enforcée par une contrainte de clé étrangère sur la colonne `station_depart` et `station_arrivee` : `FOREIGN KEY(station_depart) REFERENCES station(station_id)`, `FOREIGN KEY(station_arrivee) REFERENCES station(station_id)`. La station de depart obligatoire est enforcée par une contrainte `NOT NULL` sur la colonne `station_depart`.  
   
> RG3 : La station d'arrivée d'un trajet peut être inconnue (vélo non restitué au moment de l'export). Le trajet est conservé ; il ne compte pas comme arrivée pour aucune station.  
  
La règle est representée par l'absence en SQL de la contrainte `NOT NULL` sur la colonne `station_arrivee`.  
  
> RG4 : La durée d'un trajet est un entier strictement positif, exprimé en secondes.  
  
La règle est enforcée par une contrainte SQL sur la colonne `duree_secondes` : `CHECK (duree_secondes>0)`.  
  
> RG5 : Un trajet d'abonné porte un pseudonyme d'usager (usager_ref) ; un trajet d'usager occasionnel n'en porte pas. Aucune donnée directement identifiante n'est conservée.  
  
La règle est representée par l'absence en SQL de la contrainte `NOT NULL` sur la colonne `usager_ref` et par une contrainte sur la colonne `usager_ref` : `CHECK ((type_usager='abonne' AND usager_ref IS NOT NULL) OR (type_usager='occasionnel' AND usager_ref IS NULL))`  
  
#### Table utilisateur  
utilisateur = (<ins>`id_utilisateur`</ins> SERIAL, `username` VARCHAR(50), `mot_de_passe_hash` VARCHAR(150), `role` VARCHAR(50));  
> table representant un utilisateur  
> `id_utilisateur` : l'identifiant de l'utilisateur.  
> `username` : le nom de l'utilisateur, il doit être unique.  
> `mot_de_passe_hash` : le mot de passe hashé de l'utilisateur (Hachages bcrypt (\$2b\$, 12 tours) générés avec le paquet Python bcrypt).  
> `role` : le rôle de l'utilisateur. Il doit correspondre à `exploitant` ou `direction`.  