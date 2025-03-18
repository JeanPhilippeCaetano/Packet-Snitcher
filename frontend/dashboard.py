import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://backend:8000/data"
PREDICT_URL = "http://backend:8000/predict"

def fetch_data_from_api(endpoint: str, params: dict = None):
    """Gère la récupération des données de l'API."""
    try:
        return requests.get(endpoint, params=params).json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API : {e}")
        return None

@st.cache_data
def fetch_connection_data(limit: int):
    """Récupère les données de connexion depuis l'API et filtre les colonnes nécessaires."""
    data = fetch_data_from_api(f"{API_URL}/{limit}")
    return pd.DataFrame(data, columns=["id", "statut", "protocol_type", "service", "src_bytes", "dst_bytes"]) if data else pd.DataFrame()

def get_data_from_api(conn_id: int):
    """Récupère les données d'une connexion spécifique depuis l'API."""
    data = fetch_data_from_api(f"{PREDICT_URL}/{conn_id}")
    return pd.DataFrame([{key: data.get(key) for key in ["id", "protocol_type", "service", "src_bytes", "dst_bytes"]}]) if data else None

def predict_single_connection(conn_id: int):
    """Effectue une prédiction pour une connexion spécifique."""
    prediction_data = fetch_data_from_api(f"{PREDICT_URL}/{conn_id}")
    return prediction_data.get("statut", prediction_data.get("prediction")) if prediction_data else None

def show_dashboard():
    st.title("Surveillance Réseau")
    
    limit = st.slider("Nombre de connexions à charger :", 10, 500, 50)
    
    if "connexions_data" not in st.session_state or st.session_state.limit != limit:
        if st.button("Charger les données"):
            st.session_state.connexions_data = fetch_connection_data(limit)
            st.session_state.limit = limit
    
    connexions_data = st.session_state.get("connexions_data")
    
    if connexions_data is not None and not connexions_data.empty:
        st.write("**Données des connexions réseau :**")
        st.dataframe(connexions_data)
        
        st.subheader("Répartition des connexions")
        connexions_par_statut = connexions_data.groupby(["statut", "protocol_type", "service"]).size().reset_index(name="Nombre de connexions")
        
        st.plotly_chart(px.bar(
            connexions_par_statut, x="statut", y="Nombre de connexions", color="protocol_type", barmode="group",
            title="Nombre de connexions par statut, protocole et service", labels={"statut": "Statut", "Nombre de connexions": "Nombre"}
        ), use_container_width=True)
        
        nb_suspect = (connexions_data["statut"] == "Suspect").sum()
        col1, col2 = st.columns(2)
        with col1:
            st.success("Réseau opérationnel")
        with col2:
            st.error(f"⚠️ Alertes : {nb_suspect} connexions suspectes")
    else:
        st.warning("Aucune donnée disponible. Cliquez sur 'Charger les données'.")
    
    st.subheader("Simulation d'une connexion")
    min_id, max_id = (1, 500) if connexions_data is None else (int(connexions_data["id"].min()), int(connexions_data["id"].max()))
    conn_id = st.slider("Sélectionnez l'ID de la connexion :", min_value=min_id, max_value=max_id, step=1)
    
    data_from_api = get_data_from_api(conn_id)
    prediction_status = predict_single_connection(conn_id)
    
    if data_from_api is not None and prediction_status is not None:
        data_from_api['status'] = prediction_status
        st.write("**Détails de la connexion sélectionnée :**")
        st.table(data_from_api)
        
        if prediction_status == "Normal":
            st.success("Cette connexion est considérée comme **Normale**.")
        else:
            st.error("⚠️ Cette connexion est suspecte !")
    else:
        st.warning("Aucune donnée disponible ou la prédiction n'a pas pu être effectuée.")
