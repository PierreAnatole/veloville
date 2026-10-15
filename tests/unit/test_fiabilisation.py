"""Tests unitaires des règles de fiabilisation.

À compléter : un test par règle, cas nominal et cas de rejet.
"""
import pandas as pd
import sys

sys.path.append('../veloville')
from api.services.fiabilisation import *


def test_station_capacite_sup_zero():
    # Arrange
    df_initial=pd.DataFrame([
        {"station_id" : "S001", "capacite" : 5},
        {"station_id" : "S003", "capacite" : -5}
    ])
    logs=[]

    # Act
    df_filtre=station_capacite_sup_zero(df_initial, logs)
    motif=logs[0].motif
    decision=logs[0].decision

    # Assert
    assert motif == "valeur nulle ou négative"
    assert decision == "rejet"
    assert len(df_initial) == 2
    assert len(df_filtre) == 1
    assert len(logs) == 1

def test_incident_technicien_manquant():
    # Arrange
    df_initial=pd.DataFrame(
        [{"incident_id" : "I2026-0001", "technicien" : "technicien1"},
        {"incident_id" : "I2026-0003"}
    ])
    logs=[]

    # Act
    df_filtre=incident_technicien_manquant(df_initial, logs)
    motif=logs[0].motif
    decision=logs[0].decision

    # Assert
    assert motif == "technicien manquant"
    assert decision == "signalement"
    assert len(df_initial) == 2
    assert len(df_filtre) == 2
    assert len(logs) == 1

def test_incident_statut_casse_incorrecte():
    # Arrange
    df_initial=pd.DataFrame(
        [{"incident_id" : "I2026-0001", "statut" : "en_cours"},
        {"incident_id" : "I2026-0002", "statut" : "EN_COURS"},
        {"incident_id" : "I2026-0003", "statut" : "reSolU"},
    ])
    logs=[]

    # Act
    df_filtre=incident_statut_casse_incorrecte(df_initial, logs)
    motif=logs[0].motif
    decision=logs[0].decision

    # Assert
    assert motif == "casse ou format incorrect"
    assert decision == "normalisation"
    assert df_filtre.iloc[1]["statut"]=="en_cours"
    assert df_filtre.iloc[2]["statut"]=="resolu"
    assert len(df_initial) == 3
    assert len(df_filtre) == 3
    assert len(logs) == 2

def test_incident_cible_velo_ou_station():
    # Arrange
    df_initial=pd.DataFrame(
        [{"incident_id" : "I2026-0001", "cible" : "velo", "velo_id" : "velo1"},
        {"incident_id" : "I2026-0002", "cible" : "velo", "station_id" : "station2"},
        {"incident_id" : "I2026-0003", "cible" : "station"},
    ])
    logs=[]

    # Act
    df_filtre=incident_cible_velo_ou_station(df_initial, logs)
    motif=logs[0].motif
    decision=logs[0].decision

    # Assert
    assert motif == "valeur incorrecte ou ne correspond pas à la bonne cible velo_id ou station_d"
    assert decision == "rejet"
    assert len(df_initial) == 3
    assert len(df_filtre) == 1
    assert len(logs) == 2

def test_incident_date_resolution_avant_date_signalement():
    # Arrange
    df_initial=pd.DataFrame(
        [{"incident_id" : "I2026-0001", "date_signalement" : "2000-01-01", "date_resolution" : "2025-01-01"},
        {"incident_id" : "I2026-0001", "date_signalement" : "2025-01-01", "date_resolution" : "2000-01-01"}
    ])
    logs=[]

    # Act
    df_filtre=incident_date_resolution_avant_date_signalement(df_initial, logs)
    motif=logs[0].motif
    decision=logs[0].decision

    # Assert
    assert motif == "la date de resolution est antérieure à la date de signalement"
    assert decision == "rejet"
    assert len(df_initial) == 2
    assert len(df_filtre) == 1
    assert len(logs) == 1

def test_incident_station_id_invalide():
    # Arrange
    df_initial=pd.DataFrame(
        [{"incident_id" : "I2026-0001", "cible" : "station", "station_id" : "S001"},
        {"incident_id" : "I2026-0002", "cible" : "station", "station_id" : "S002"},
    ])
    df_station=pd.DataFrame([{"station_id" : "S001"}])
    logs=[]

    # Act
    df_filtre=incident_station_id_invalide(df_initial, logs, df_station)
    motif=logs[0].motif
    decision=logs[0].decision

    # Assert
    assert motif == "l'id de station n'existe pas dans la table station"
    assert decision == "rejet"
    assert len(df_initial) == 2
    assert len(df_filtre) == 1
    assert len(logs) == 1

def test_trajet_depart_format_date():
    # Arrange
    df_initial=pd.DataFrame(
        [{"trajet_id" : "T480001", "depart_horodatage" : "2000-01-01"},
        {"trajet_id" : "T480002", "depart_horodatage" : "01/01/2000"}
    ])
    logs=[]
    
    # Act
    df_filtre=trajet_depart_format_date(df_initial, logs)
    motif=logs[0].motif
    decision=logs[0].decision

    assert motif=="la date est du format JJ/MM/AAAA au lieu du format AAAA-MM-JJ"
    assert decision == "normalisation"
    assert df_filtre.iloc[1]["depart_horodatage"]=="2000-01-01"
    assert len(df_initial) == 2
    assert len(df_filtre) == 2
    assert len(logs) == 1

def test_trajet_duree_sup_zero():
    # Arrange
    df_initial=pd.DataFrame([
        {"trajet_id" : "T480001", "duree_secondes" : 5},
        {"trajet_id" : "T480002", "duree_secondes" : -5}
    ])
    logs=[]

    # Act
    df_filtre=trajet_duree_sup_zero(df_initial, logs)
    motif=logs[0].motif
    decision=logs[0].decision

    # Assert
    assert motif == "valeur nulle ou négative"
    assert decision == "rejet"
    assert len(df_initial) == 2
    assert len(df_filtre) == 1
    assert len(logs) == 1

def test_trajet_station_depart_invalide():
    # Arrange
    df_initial=pd.DataFrame([
        {"trajet_id" : "T480001", "station_depart" : "S001"},
        {"trajet_id" : "T480002", "station_depart" : "S002"}
    ])
    df_station=pd.DataFrame([{"station_id" : "S001"}])
    logs=[]

    # Act
    df_filtre=trajet_station_depart_invalide(df_initial, logs, df_station)
    motif=logs[0].motif
    decision=logs[0].decision

    # Assert
    assert motif == "l'id de station de depart n'existe pas dans la table station"
    assert decision == "rejet"
    assert len(df_initial) == 2
    assert len(df_filtre) == 1
    assert len(logs) == 1

def test_trajet_station_arrivee_invalide():
    # Arrange
    df_initial=pd.DataFrame([
        {"trajet_id" : "T480001", "station_arrivee" : "S001"},
        {"trajet_id" : "T480002", "station_arrivee" : "S002"}
    ])
    df_station=pd.DataFrame([{"station_id" : "S001"}])
    logs=[]

    # Act
    df_filtre=trajet_station_arrivee_invalide(df_initial, logs, df_station)
    motif=logs[0].motif
    decision=logs[0].decision

    # Assert
    assert motif == "l'id de station d'arrivee n'existe pas dans la table station"
    assert decision == "rejet"
    assert len(df_initial) == 2
    assert len(df_filtre) == 1
    assert len(logs) == 1