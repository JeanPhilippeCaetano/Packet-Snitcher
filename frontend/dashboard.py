import streamlit as st
import pandas as pd
import requests
import plotly.express as px


API_URL = "http://backend:8000/data" 

def fetch_connection_data(limit=int):
    """Récupère les données de connexion depuis l'API et filtre les colonnes nécessaires"""
    try:
        response = requests.get(f"{API_URL}/{limit}")
        response.raise_for_status()
        data = pd.DataFrame(response.json())

        return data[["statut", "protocol_type", "service", "src_bytes", "dst_bytes"]]
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API : {e}")
        return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur 




def show_dashboard():
    st.title("Surveillance Réseau")

    # Slider pour le nombre de connexions
    limit = st.slider("Nombre de connexions à charger :", 10, 500, 50)


    if "connexions_data" not in st.session_state or st.session_state.limit != limit:
        if st.button(" Charger les données"):
            connexions_data = fetch_connection_data(limit)

            if not connexions_data.empty:
                # Stocker les données et la limite en session
                st.session_state.connexions_data = connexions_data
                st.session_state.limit = limit

    # Vérifie si on a bien des données en session pour affichage
    if "connexions_data" in st.session_state and not st.session_state.connexions_data.empty:
        connexions_data = st.session_state.connexions_data

        st.write("Données des connexions réseau :")
        st.dataframe(connexions_data)

        # Compter le nombre de connexions par statut
        connexions_par_statut = connexions_data.groupby(["statut", "protocol_type", "service"]).size().reset_index(name="Nombre de connexions")

        # Graphique du nombre de connexions par statut
        st.subheader(" Répartition des connexions")
        bar_chart = px.bar(connexions_par_statut, 
                           x="statut", 
                           y="Nombre de connexions",
                           color="protocol_type",
                           barmode="group",
                           title="Nombre de connexions par statut, protocole et service",
                           labels={"statut": "Statut", "Nombre de connexions": "Nombre"})
        st.plotly_chart(bar_chart, use_container_width=True)

        #  Affichage du statut du réseau
        nb_suspect = (connexions_data["statut"] == "Suspect").sum()
        col1, col2 = st.columns(2)
        with col1:
            st.success(" Réseau opérationnel")
        with col2:
            st.error(f"⚠️ Alertes : {nb_suspect} connexions suspectes")
    else:
        st.warning("Aucune donnée disponible. Cliquez sur 'Charger les données'.")
