import os
import sys
from sqlalchemy import create_engine
from pandas.io.sql import DatabaseError

sys.path.append('../veloville')
from api.services.fiabilisation import *
from api.config import DATABASE_URL
print(DATABASE_URL)

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
    trajet_filtre=trajet_depart_format_date(trajet_filtre, reject_logs)
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

    # export des logs
    df_reject_log.to_csv(PATH_WARNING_REJECT_LOG)



    # export en base de donnée
    engine = create_engine(DATABASE_URL)

    def insert_station(df_station, engine) :
        data_types={
            "station_id" : "str",
            "nom" : "str",
            "commune" : "str",
            "capacite" : "int",
            "latitude" : "float",
            "longitude" : "float",
            "date_mise_en_service" : "datetime64[ns]"
        }
        df_station=df_station.astype(data_types)
        try :
            df_station.to_sql(name='station', con=engine, if_exists="append", index=False)
        except DatabaseError as e :
            print("la station 'trajet' à déja été remplie")

    def insert_incident(df_station, engine) :
        data_types={
            "incident_id" : "str",
            "date_signalement" : "datetime64[ns]",
            "cible" : "str",
            "velo_id" : "str",
            "station_id" : "str",
            "type_incident" : "str",
            "statut" : "str",
            "date_resolution" : "datetime64[ns]",
            "technicien" : "str"
        }
        df_station=df_station.astype(data_types)
        try :
            df_station.to_sql(name='incident', con=engine, if_exists="append", index=False)
        except DatabaseError as e :
            print("la table 'incident' à déja été remplie")

    def insert_trajet(df_station, engine) :
        data_types={
            "trajet_id" : "str",
            "velo_id" : "str",
            "depart_horodatage" : "datetime64[ns]",
            "station_depart" : "str",
            "station_arrivee" : "str",
            "duree_secondes" : "int",
            "type_usager" : "str",
            "usager_ref": "str"
        }
        df_station=df_station.astype(data_types)
        try :
            df_station.to_sql(name='trajet', con=engine, if_exists="append", index=False)
        except DatabaseError as e:
            print("la table 'trajet' à déja été remplie")
    
    insert_station(station_filtre, engine)
    insert_incident(incident_filtre, engine)
    insert_trajet(trajet_filtre, engine)

if __name__ == "__main__":
    main()