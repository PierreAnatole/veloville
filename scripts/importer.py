"""Import et fiabilisation des trois exports CSV dans PostgreSQL.

À compléter : lire data/stations.csv, data/trajets.csv et data/incidents.csv,
appliquer les règles de fiabilisation (api/services/fiabilisation.py),
charger les lignes valides, journaliser les rejets et les avertissements.
Le script doit être idempotent : deux exécutions successives laissent la
base dans le même état.

Usage prévu : python scripts/importer.py [--dossier data]
"""
import os
import pandas as pd

dirname = os.path.dirname(__file__)

PATH_STATION_DATA=f"{dirname}/../data/stations.csv"
PATH_TRAJET_DATA=f"{dirname}/../data/trajets.csv"
PATH_INCIDENT_DATA=f"{dirname}/../data/incidents.csv"

SHORT_PATH_STATION_DATA="stations.csv"
SHORT_PATH_TRAJET_DATA="trajets.csv"
SHORT_PATH_INCIDENT_DATA="incidents.csv"

PATH_WARNING_REJECT_LOG=f"{dirname}/../docs/journal_rejets.csv"

class LogEntry():
    def __init__(self, fichier_source, identifiant, colonne, valeur, motif, decision) : 
        self.fichier_source=fichier_source
        self.identifiant=identifiant
        self.colonne=colonne
        self.valeur=valeur
        self.motif=motif
        self.decision=decision

def doublon(df, fichier):
    df_doublons=df[df.duplicated()]
    
    for index, row in df_doublons.iterrows():
        entry=LogEntry(
            fichier_source=fichier,
            identifiant=index,
            colonne="toutes",
            valeur=df_doublons.loc[index], # TODO
            motif="doublon",
            decision="rejet"
        )
        print(entry.valeur)

def main() -> None:
    df_station=pd.read_csv(f"{PATH_STATION_DATA}")
    df_trajet=pd.read_csv(f"{PATH_TRAJET_DATA}")
    df_incident=pd.read_csv(f"{PATH_INCIDENT_DATA}")

    doublon(df_station, SHORT_PATH_STATION_DATA)
    doublon(df_trajet, SHORT_PATH_TRAJET_DATA)
    doublon(df_incident, SHORT_PATH_INCIDENT_DATA)

    df_reject_log=pd.DataFrame([{"fichier source" : "", "identifiant" : "", "colonne" : "", "valeur" : "", "motif" : "", "décision" : ""}])
    reject_log=[
        {"fichier_source" : "1"},
        {"fichier_source" : "2"}
    ]
    df_reject_log=pd.DataFrame(reject_log)
    df_reject_log.to_csv(PATH_WARNING_REJECT_LOG)


if __name__ == "__main__":
    main()
