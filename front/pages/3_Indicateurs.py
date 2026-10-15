"""Écran Indicateurs.

À compléter : trois st.metric et trois tableaux issus des trois endpoints
/indicateurs. Aucun graphique.
"""
import streamlit as st
from datetime import datetime

from api.services.indicateurs import activite_par_jour, stations_actives,incidents_par_statut
import commun

st.title("Indicateurs")
if commun.est_connecte():
    st.sidebar.write(f"Connecté en tant que `{st.session_state['username']}`")
    st.sidebar.write(f"rôle : `{st.session_state['role']}`")
    if st.sidebar.button("deconnexion"):
        commun.deconnecter()
        st.rerun()

if "date_de_debut" not in st.session_state:
    st.session_state["date_de_debut"] = "2026-08-20"

if "date_de_fin" not in st.session_state:
    st.session_state["date_de_fin"] = "2026-08-30"

if "limite" not in st.session_state:
    st.session_state["limite"] = 10


st.header("Activité par jour")
debut=st.date_input("Début de période", value=datetime(2026,8,23))
fin=st.date_input("Fin de période", value=datetime(2026,8,31))
st.dataframe(
    activite_par_jour(str(debut),str(fin))
    .rename(columns={"nb_trajets" : "nombre de trajets"}),
    hide_index=True
)

st.header("Stations les plus actives")
limite=st.number_input("nombre de resultats", min_value=0, value=10)
st.dataframe(stations_actives(limite)
    .rename(columns={"station_id" : "id de station", "nom" : "nom de station", "nb_trajets" : "nombre de trajets"}),
    hide_index=True
)

st.header("Incidents par statut")
st.dataframe(incidents_par_statut()
    .rename(columns={"nb_incidents" : "nombre d'incidents", "delai_moyen_resolution_heures" : "delai de resolution moyen en heure"}),
    hide_index=True
)