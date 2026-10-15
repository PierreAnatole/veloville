"""Écran Incidents.

À compléter : tableau filtrable par statut ; pour le rôle exploitant, changement de
statut d'un incident via l'API.
"""
import streamlit as st
import sys

sys.path.append('../veloville')
import api_client
import commun
from api.services.front_service import get_incident_ids

st.title("Incidents")
if "page_incidents" not in st.session_state:
    st.session_state["page_incidents"] = 1

if "statut" not in st.session_state:
    st.session_state["statut"] = "Tous"
statut=st.selectbox("Statut", ["Tous", "ouvert", "en_cours", "resolu"])
st.session_state["statut"] = statut

try:
    incidents = api_client.obtenir(
        "/incidents",
        params={"statut" : st.session_state["statut"], "page": st.session_state["page_incidents"], "page_size": 20}
    )
except api_client.ErreurApi as erreur:
    st.error(erreur.message)
else:
    st.dataframe(incidents["resultats"], width='stretch')
    st.caption(f"Page {incidents['page']} / {incidents['pages']} — {incidents['total']} éléments")

    precedent, suivant = st.columns(2)
    with precedent:
        if st.button("Précédent", disabled=incidents["page"] <= 1):
            st.session_state["page_incidents"] -= 1
            st.rerun()
    with suivant:
        if st.button("Suivant", disabled=incidents["page"] >= incidents["pages"]):
            st.session_state["page_incidents"] += 1
            st.rerun()

@st.cache_data(ttl="1h")
def get_incidents_from_service():
    return get_incident_ids()
if commun.est_connecte():
    st.sidebar.write(f"Connecté en tant que `{st.session_state['username']}`")
    st.sidebar.write(f"rôle : `{st.session_state['role']}`")
    if st.sidebar.button("deconnexion"):
        commun.deconnecter()
        st.rerun()

    # pas implémenté
    if st.session_state['role']=="direction" :
        with st.form("Changer le statut d'un incident"):
            st.error("Pas implémenté")
            incident_id=st.selectbox("Incident", get_incidents_from_service())
            nouveau_statut=st.selectbox("Nouveau statut", ["ouvert", "en_cours", "resolu"])
            changer_statut = st.form_submit_button("Appliquer")
    else :
        st.error("Vous n'avez pas le droit de modifier un incident (seul le rôle 'direction' est autorisé)")
else :
        st.error("Vous n'avez pas le droit de modifier un incident (non connecté)")