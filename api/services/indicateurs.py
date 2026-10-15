"""Calcul des trois indicateurs (module métier testé).

À compléter : activite_par_jour
stations_actives(session, limite) et incidents_par_statut(session).
Les routeurs ne font qu'appeler ces fonctions.
# """
import sys
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

sys.path.append('../veloville')
from api.services.fiabilisation import *
from api.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

# Indicateur 1 : nombre de trajets par jour de départ sur la période demandée (bornes incluses),
# un élément par jour comportant au moins un trajet, trié par jour croissant. Sans paramètre, toute la période connue.
def activite_par_jour(date_debut = "", date_fin = "") :
    df=pd.read_sql_table("trajet", con=engine)
    df_activite=df.copy()

    if date_debut :
        df_activite=df_activite[(df_activite['depart_horodatage']>=date_debut)]
    if date_fin :
        df_activite=df_activite[(df_activite['depart_horodatage']<=date_fin)]

    df_activite=(
        df_activite.groupby([df_activite['depart_horodatage'].dt.date])["trajet_id"].count()
        .reset_index()
        .rename(columns={"depart_horodatage" : "jour", "trajet_id" : "nb_trajets"})
        .sort_values("jour")
    )
    return df_activite
# Indicateur 2 : les limite stations ayant le plus de mouvements (nb_departs + nb_arrivees)
# ordre décroissant puis station_id croissant ; une arrivée inconnue ne compte pour aucune station.
def stations_actives(limite=10) :
    df_trajet=pd.read_sql_table("trajet", con=engine)
    df_station=pd.read_sql_table("station", con=engine)

    df_station_c=pd.read_sql_table("station", con=engine)
    df_depart=df_trajet.copy()
    df_arrivee=df_trajet.copy()

    df_depart=df_depart.groupby("station_depart")["trajet_id"].count().reset_index().rename(columns={"station_depart" : "station_id", "trajet_id" : "nb_trajets"})
    df_arrivee=df_arrivee.groupby("station_arrivee")["trajet_id"].count().reset_index().rename(columns={"station_arrivee" : "station_id", "trajet_id" : "nb_trajets"})

    df_union=pd.concat([df_depart, df_arrivee])
    df_union=(
        df_union.groupby("station_id")["nb_trajets"].sum()
        .reset_index()
        .sort_values(['nb_trajets', 'station_id'], ascending=[False, True])
        .head(limite)
    )
    df_union=pd.merge(df_union, df_station_c, on='station_id')
    return df_union[["station_id", "nom", "nb_trajets"]]

# Indicateur 3 : nombre d'incidents par statut (un élément par statut présent en base) et délai moyen
# de résolution en heures, calculé sur les incidents resolu dont date_resolution est renseignée, arrondi à une décimale ; null si aucun incident résolu.
def incidents_par_statut():
    df_incident=pd.read_sql_table("incident", con=engine)
    df_incident_statut=df_incident.copy()

    df_incident_statut['delai_moyen_resolution_heures'] = (df_incident_statut['date_resolution'] - df_incident_statut['date_signalement']).dt.components['hours']

    df_incident_statut=(
        df_incident_statut.groupby(['statut']).agg({
            'incident_id': 'count',
            'delai_moyen_resolution_heures': np.nanmean
        })
        .reset_index()
        .rename(columns={"incident_id" : "nb_incidents"})
    )
    return df_incident_statut