import os
import sys
sys.path.append('../veloville')
from api.services.fiabilisation import *

dirname = os.path.dirname(__file__)

STATION_FILENAME="stations.csv"
TRAJET_FILENAME="trajets.csv"
INCIDENT_FILENAME="incidents.csv"

PATH_STATION_DATA=f"{dirname}/../data/{STATION_FILENAME}"
PATH_TRAJET_DATA=f"{dirname}/../data/{TRAJET_FILENAME}"
PATH_INCIDENT_DATA=f"{dirname}/../data/{INCIDENT_FILENAME}"

PATH_WARNING_REJECT_LOG=f"{dirname}/../docs/journal_rejets.csv"

def main() -> None:
    df_station=pd.read_csv(f"{PATH_STATION_DATA}")
    df_trajet=pd.read_csv(f"{PATH_TRAJET_DATA}")
    df_incident=pd.read_csv(f"{PATH_INCIDENT_DATA}")
    station_filtre=df_station.copy()
    trajet_filtre=df_trajet.copy()
    incident_filtre=df_incident.copy()

    reject_logs=[]

    # retire et log les doublons
    station_filtre=doublon(station_filtre, reject_logs, STATION_FILENAME, "station_id")
    trajet_filtre=doublon(trajet_filtre, reject_logs, TRAJET_FILENAME, "trajet_id")
    incident_filtre=doublon(incident_filtre, reject_logs, INCIDENT_FILENAME, "incident_id")

    # Station
    station_filtre=station_capacite_sup_zero(station_filtre, reject_logs)

    # incident
    incident_filtre=incident_technicien_manquant(incident_filtre, reject_logs)
    incident_filtre=incident_statut_casse_incorrecte(incident_filtre, reject_logs)
    incident_filtre=incident_cible_velo_ou_station(incident_filtre, reject_logs)
    incident_filtre=incident_date_resolution_avant_date_signalement(incident_filtre, reject_logs)
    incident_filtre=incident_station_id_invalide(incident_filtre, reject_logs, station_filtre)

    # trajet
    trajet_filtre=trajet_duree_sup_zero(trajet_filtre, reject_logs)
    trajet_filtre=trajet_station_depart_invalide(trajet_filtre, reject_logs, station_filtre)
    trajet_filtre=trajet_station_arrivee_invalide(trajet_filtre, reject_logs, station_filtre)

    df_reject_log=pd.DataFrame([vars(log) for log in reject_logs])

    # affichage pour vérifier le nombre de total de lignes traitées
    initial=len(df_station)+len(df_incident)+len(df_trajet)
    restante=len(station_filtre)+len(incident_filtre)+len(trajet_filtre)
    supprimee=len(df_reject_log[df_reject_log["decision"]=="rejet"])
    print(f"""lignes initiales : {initial}
lignes supprimees : {supprimee}
lignes restantes : {restante}
lignes supprimees+restantes : {supprimee+restante}""")
    
    df_reject_log.to_csv(PATH_WARNING_REJECT_LOG)

if __name__ == "__main__":
    main()