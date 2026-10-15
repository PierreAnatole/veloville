import streamlit as st

import api_client
import commun

if "page_items" not in st.session_state:
    st.session_state["page_items"] = 1

st.title("Connexion")

if not commun.est_connecte():
    # st.form soumet les deux champs ensemble (pas à chaque caractère).
    with st.form("connexion"):
        identifiant = st.text_input("Identifiant")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        soumettre = st.form_submit_button("Se connecter")

    if soumettre:
        try:
            # L'appel HTTP est délégué au client API centralisé.
            reponse = api_client.connexion(identifiant, mot_de_passe)
        except api_client.ErreurApi as erreur:
            st.error(erreur.message)
        else:
            # JWT conservé uniquement pour la session Streamlit en cours.
            commun.connecter(identifiant, reponse)
            st.rerun()

else :
    st.sidebar.write(f"Connecté en tant que `{st.session_state['username']}`")
    st.sidebar.write(f"rôle : `{st.session_state['role']}`")
    st.write(f"Connecté en tant que `{st.session_state['username']}`, rôle : `{st.session_state['role']}`")
    if st.sidebar.button("deconnexion"):
        commun.deconnecter()
        st.rerun()