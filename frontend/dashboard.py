import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://backend:8000/data"
PREDICT_URL = "http://backend:8000/predict"

def fetch_data_from_api(endpoint: str, params: dict = None):
    """Gère la récupération des données de l'API."""
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API : {e}")
        return None

@st.cache_data 
def fetch_connection_data(limit: int):
    """Récupère les données de connexion depuis l'API et filtre les colonnes nécessaires"""
    data = fetch_data_from_api(f"{API_URL}/{limit}")
    if data:
        return pd.DataFrame(data)[["id", "statut", "protocol_type", "service", "src_bytes", "dst_bytes"]]
    return pd.DataFrame()

def get_data_from_api(conn_id: int):
    """Récupère les données d'une connexion spécifique depuis l'API."""
    data = fetch_data_from_api(f"{PREDICT_URL}/{conn_id}")
    if data:
        return pd.DataFrame([{
            "id": data.get("id"),
            "protocol_type": data.get("protocol_type"),
            "service": data.get("service"),
            "src_bytes": data.get("src_bytes"),
            "dst_bytes": data.get("dst_bytes")
        }])
    return None

def predict_single_connection(conn_id: int):
    """Effectue une prédiction pour une connexion spécifique."""
    prediction_data = fetch_data_from_api(f"{PREDICT_URL}/{conn_id}")
    if prediction_data and isinstance(prediction_data, dict):
        return prediction_data.get("statut", prediction_data.get("prediction"))
    return None

def show_dashboard():
    st.title("Surveillance Réseau")

    limit = st.slider("Nombre de connexions à charger :", 10, 500, 50)

    if "connexions_data" not in st.session_state or st.session_state.limit != limit:
        if st.button("Charger les données"):
            connexions_data = fetch_connection_data(limit)
            if not connexions_data.empty:
                st.session_state.connexions_data = connexions_data
                st.session_state.limit = limit

    if "connexions_data" in st.session_state and not st.session_state.connexions_data.empty:
        connexions_data = st.session_state.connexions_data

        st.write("**Données des connexions réseau :**")
        st.dataframe(connexions_data)

        st.subheader("Répartition des connexions")
        connexions_par_statut = connexions_data.groupby(["statut", "protocol_type", "service"]).size().reset_index(name="Nombre de connexions")

        bar_chart = px.bar(
            connexions_par_statut,
            x="statut",
            y="Nombre de connexions",
            color="protocol_type",
            barmode="group",
            title="Nombre de connexions par statut, protocole et service",
            labels={"statut": "Statut", "Nombre de connexions": "Nombre"}
        )
        st.plotly_chart(bar_chart, use_container_width=True)

        nb_suspect = (connexions_data["statut"] == "Suspect").sum()
        col1, col2 = st.columns(2)
        with col1:
            st.success("Réseau opérationnel")
        with col2:
            st.error(f"⚠️ Alertes : {nb_suspect} connexions suspectes")

    else:
        st.warning("Aucune donnée disponible. Cliquez sur 'Charger les données'.")

    st.subheader("Simulation d'une connexion")

    if "connexions_data" in st.session_state and not st.session_state.connexions_data.empty:
        min_id, max_id = int(st.session_state.connexions_data["id"].min()), int(st.session_state.connexions_data["id"].max())
    else:
        min_id, max_id = 1, 500

    conn_id = st.slider("Sélectionnez l'ID de la connexion :", min_value=min_id, max_value=max_id, step=1)

    data_from_api = get_data_from_api(conn_id)
    prediction_status = predict_single_connection(conn_id)

    if data_from_api is not None:
        if prediction_status is not None:
            data_from_api['status'] = prediction_status
            st.write("**Détails de la connexion sélectionnée :**")
            st.table(data_from_api)

            if prediction_status == "Normal":
                st.success("Cette connexion est considérée comme **Normale**.")
            else:
                st.error("⚠️ Cette connexion est suspecte !")
        else:
            st.warning("La prédiction n'a pas pu être effectuée. Vérifiez la structure de la réponse de l'API.")
    else:
        st.warning("Aucune donnée disponible pour cette connexion.")
