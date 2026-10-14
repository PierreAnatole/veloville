"""Règles de fiabilisation des données (module métier testé).

À compléter : fonctions pures, sans accès à la base, qui normalisent ou rejettent
une valeur ou une ligne : horodatages, identifiants de vélo, statuts
d'incident, durées, références de station, cohérence des dates,
doublons. Chaque fonction retourne la valeur normalisée ou signale le
motif de rejet. Ces fonctions sont appelées par scripts/importer.py et
couvertes par tests/unit/.
"""
import pandas as pd

class LogEntry():
    def __init__(self, fichier_source, identifiant, colonne, valeur, motif, decision) : 
        self.fichier_source=fichier_source
        self.identifiant=identifiant
        self.colonne=colonne
        self.valeur=valeur
        self.motif=motif
        self.decision=decision

# retire les doublons, peut fonctionner pour plusieurs csv
def doublon(df, logs, fichier, nom_id):
    df_doublons=df[df.duplicated()]
    df_sans_doublons=df[~df.duplicated()]
    
    for index, row in df_doublons.iterrows():
        entry=LogEntry(
            fichier_source=fichier,
            identifiant=row[nom_id],
            colonne="toutes",
            valeur=df_doublons.loc[index],
            motif="doublon",
            decision="rejet"
        )
        logs.append(entry)

    return df_sans_doublons

# station
def station_capacite_sup_zero(df, logs) :
    filtre=df["capacite"]<=0
    df_incorrect=df[filtre]
    df_clean=df[~filtre]

    for index, row in df_incorrect.iterrows():
        entry=LogEntry(
            fichier_source="stations.csv",
            identifiant=row["station_id"],
            colonne="capacite",
            valeur=row["capacite"],
            motif="valeur nulle ou négative",
            decision="rejet"
        )
        logs.append(entry)

    return df_clean

# incident
def incident_technicien_manquant(df, logs) :
    filtre=df["technicien"].isna()
    df_incorrect=df[filtre]

    for index, row in df_incorrect.iterrows():
        entry=LogEntry(
            fichier_source="incidents.csv",
            identifiant=row["technicien"],
            colonne="technicien",
            valeur="",
            motif="technicien manquant",
            decision="signalement"
        )
        logs.append(entry)
    return df

def incident_statut_casse_incorrecte(df, logs) :
    filtre=(
         (df["statut"].str.lower().isin(["ouvert", "en cours", "en_cours", "resolu"])) # normalise seulement les valeurs proche du format demandé
        & (~(df["statut"].isin(["ouvert", "en_cours", "resolu"])))
    )
    df_incorrect=df[filtre]

    for index, row in df_incorrect.iterrows():
        entry=LogEntry(
            fichier_source="incidents.csv",
            identifiant=row["incident_id"],
            colonne="statut",
            valeur=row["statut"],
            motif="casse ou format incorrect",
            decision="normalisation"
        )
        logs.append(entry)
    df["statut"]=df["statut"].str.lower()
    df["statut"]=df["statut"].str.replace(r' ', '_', regex=True)
    return df

def incident_cible_velo_ou_station(df, logs) :
    filtre=(
         ~(df["cible"].isin(['velo', "station"])) # la cible n'est pas une station ou un velo
         | (
              ((df["cible"]=='velo') & ((df["velo_id"].isna()) | (df["station_id"].notna()))) # la cible est un velo mais pas de velo_id, ou station_id present
              | ((df["cible"]=='station') & ((df["station_id"].isna()) | (df["velo_id"].notna()))) # la cible est une station mais pas de station_id, ou velo_id present
        )
    )
    df_incorrect=df[filtre]
    df_clean=df[~filtre]

    for index, row in df_incorrect.iterrows():
        entry=LogEntry(
            fichier_source="incidents.csv",
            identifiant=row["incident_id"],
            colonne="cible",
            valeur=row["cible"],
            motif="valeur incorrecte ou ne correspond pas à la bonne cible velo_id ou station_d",
            decision="rejet"
        )
        logs.append(entry)

    return df_clean

def incident_date_resolution_avant_date_signalement(df, logs) :
    filtre=(df["date_resolution"]<df["date_signalement"])
    df_incorrect=df[filtre]
    df_clean=df[~filtre]

    for index, row in df_incorrect.iterrows():
        entry=LogEntry(
            fichier_source="incidents.csv",
            identifiant=row["incident_id"],
            colonne="date_resolution, date_signalement",
            valeur=f"resolution : {row['date_resolution']}, signalement : {row["date_signalement"]}",
            motif="la date de resolution est antérieure à la date de signalement",
            decision="rejet"
        )
        logs.append(entry)
            
    return df_clean

def incident_station_id_invalide(df, logs, stations):
    ids_station=stations["station_id"].to_list()

    filtre=(df["cible"]=="station") & (~(df["station_id"].isin(ids_station)))
    df_incorrect=df[filtre]
    df_clean=df[~filtre]

    for index, row in df_incorrect.iterrows():
        entry=LogEntry(
            fichier_source="incidents.csv",
            identifiant=row["incident_id"],
            colonne="station_id",
            valeur=row['station_id'],
            motif="l'id de station n'existe pas dans la table station",
            decision="rejet"
        )
        logs.append(entry)
            
    return df_clean


# trajet
def trajet_duree_sup_zero(df, logs) :
    filtre=df["duree_secondes"]<=0
    df_incorrect=df[filtre]
    df_clean=df[~filtre]

    for index, row in df_incorrect.iterrows():
        entry=LogEntry(
            fichier_source="trajets.csv",
            identifiant=row["trajet_id"],
            colonne="duree_secondes",
            valeur=row["duree_secondes"],
            motif="valeur nulle ou négative",
            decision="rejet"
        )
        logs.append(entry)

    return df_clean

def trajet_station_depart_invalide(df, logs, stations):
    ids_station=stations["station_id"].to_list()

    filtre=~(df["station_depart"].isin(ids_station))
    df_incorrect=df[filtre]
    df_clean=df[~filtre]

    for index, row in df_incorrect.iterrows():
        entry=LogEntry(
            fichier_source="trajets.csv",
            identifiant=row["trajet_id"],
            colonne="station_depart",
            valeur=row['station_depart'],
            motif="l'id de station de depart n'existe pas dans la table station",
            decision="rejet"
        )
        logs.append(entry)
            
    return df_clean

def trajet_station_arrivee_invalide(df, logs, stations):
    ids_station=stations["station_id"].to_list()

    filtre=(
        (df["station_arrivee"].notna())
        & (~(df["station_arrivee"].isin(ids_station)))
    )
    df_incorrect=df[filtre]
    df_clean=df[~filtre]

    for index, row in df_incorrect.iterrows():
        entry=LogEntry(
            fichier_source="trajets.csv",
            identifiant=row["trajet_id"],
            colonne="station_arrivee",
            valeur=row['station_arrivee'],
            motif="l'id de station d'arrivee n'existe pas dans la table station",
            decision="rejet"
        )
        logs.append(entry)
            
    return df_clean