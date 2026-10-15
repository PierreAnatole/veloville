"""Écran Incidents.

À compléter : tableau filtrable par statut ; pour le rôle exploitant, changement de
statut d'un incident via l'API.
"""
import streamlit as st

import api_client
import commun

if commun.est_connecte():
    st.sidebar.write(f"Connecté en tant que `{st.session_state['username']}`")
    st.sidebar.write(f"rôle : `{st.session_state['role']}`")
    if st.sidebar.button("deconnexion"):
        commun.deconnecter()
        st.rerun()