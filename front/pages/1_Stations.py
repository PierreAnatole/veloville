import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import sys

sys.path.append('../veloville')
import api_client
import commun
from api.services.front_service import get_communes

st.title("Stations")
if "page_stations" not in st.session_state:
    st.session_state["page_stations"] = 1

if "commune" not in st.session_state:
    st.session_state["commune"] = "Toutes"

if commun.est_connecte():
    st.sidebar.write(f"Connecté en tant que `{st.session_state['username']}`")
    st.sidebar.write(f"rôle : `{st.session_state['role']}`")
    if st.sidebar.button("deconnexion"):
        commun.deconnecter()
        st.rerun()

@st.cache_data(ttl="1h")
def get_communes_from_service():
    return(get_communes())

commune=st.selectbox("Commune", ["Toutes"]+get_communes_from_service())
st.session_state["commune"] = commune

try:
    stations = api_client.obtenir(
        "/stations",
        params={"commune" : st.session_state["commune"], "page": st.session_state["page_stations"], "page_size": 20}
    )
except api_client.ErreurApi as erreur:
    st.error(erreur.message)
else:
    st.dataframe(stations["resultats"], width='stretch')
    st.caption(f"Page {stations['page']} / {stations['pages']} — {stations['total']} éléments")

    precedent, suivant = st.columns(2)
    with precedent:
        if st.button("Précédent", disabled=stations["page"] <= 1):
            st.session_state["page_stations"] -= 1
            st.rerun()
    with suivant:
        if st.button("Suivant", disabled=stations["page"] >= stations["pages"]):
            st.session_state["page_stations"] += 1
            st.rerun()