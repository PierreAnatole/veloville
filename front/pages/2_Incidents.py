"""Écran Incidents.

À compléter : tableau filtrable par statut ; pour le rôle exploitant, changement de
statut d'un incident via l'API.
"""
import streamlit as st

import api_client
import commun

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
    st.dataframe(incidents["resultats"], use_container_width=True)
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

if commun.est_connecte():
    st.sidebar.write(f"Connecté en tant que `{st.session_state['username']}`")
    st.sidebar.write(f"rôle : `{st.session_state['role']}`")
    if st.sidebar.button("deconnexion"):
        commun.deconnecter()
        st.rerun()