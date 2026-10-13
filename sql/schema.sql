DROP TABLE IF EXISTS station CASCADE;
DROP TABLE IF EXISTS incident CASCADE;
DROP TABLE IF EXISTS trajet CASCADE;
DROP TABLE IF EXISTS utilisateur CASCADE;

CREATE TABLE station(
	station_id CHAR(4) PRIMARY KEY,
	nom VARCHAR(100) NOT NULL,
	commune VARCHAR(50) NOT NULL,
	capacite INTEGER NOT NULL CHECK (capacite>0),
	latitutude NUMERIC(8,5) NOT NULL,
	longitude NUMERIC(8,5) NOT NULL,
	date_mise_en_service DATE NOT NULL
);

CREATE TABLE trajet(
	trajet_id VARCHAR(12) PRIMARY KEY,
	velo_id VARCHAR(8) NOT NULL,
	depart_horodatage TIMESTAMP NOT NULL,
	duree_secondes INTEGER NOT NULL CHECK (duree_secondes>0),
	type_usager VARCHAR(15) NOT NULL CHECK (type_usager in ('abonne', 'occasionnel')),
	usager_ref CHAR(9),
	station_depart CHAR(4) NOT NULL,
	station_arrivee CHAR(4),
	FOREIGN KEY(station_depart) REFERENCES station(station_id),
	FOREIGN KEY(station_arrivee) REFERENCES station(station_id)
);

CREATE TABLE incident(
	incident_id VARCHAR(12) PRIMARY KEY,
	date_signalement TIMESTAMP NOT NULL,
	cible VARCHAR(10) NOT NULL CHECK (cible in ('velo', 'station')),
	velo_id CHAR(5),
	type_incident VARCHAR(30) NOT NULL,
	statut VARCHAR(10) NOT NULL CHECK (statut in ('ouvert', 'en_cours', 'resolu')),
	date_resolution TIMESTAMP,
	technicien VARCHAR(50),
	station_id CHAR(4),
	CONSTRAINT velo_XOR_station CHECK (
		(cible='velo' AND velo_id IS NOT NULL AND station_id IS NULL)
		OR (cible='station' AND station_id IS NOT NULL AND velo_id IS NULL)
	),
	FOREIGN KEY(station_id) REFERENCES station(station_id)
);

CREATE TABLE utilisateur(
	id_utilisateur SERIAL PRIMARY KEY,
	username VARCHAR(50) NOT NULL UNIQUE,
	mot_de_passe_hash VARCHAR(150),
	role VARCHAR(50) CHECK (role in ('exploitant', 'direction'))
);

-- ---------------------------------------------------------------
-- 5. Index utiles aux filtres et aux indicateurs
-- ---------------------------------------------------------------
CREATE INDEX IF NOT EXISTS index_incident_join_station
ON incident(station_id);

CREATE INDEX IF NOT EXISTS statut_incident
ON incident(statut);