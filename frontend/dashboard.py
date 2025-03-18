import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://backend:8000/data"
PREDICT_URL = "http://backend:8000/predict"

def fetch_connection_data(limit=int):
    """Récupère les données de connexion depuis l'API et filtre les colonnes nécessaires"""
    try:
        response = requests.get(f"{API_URL}/{limit}")
        response.raise_for_status()
        data = pd.DataFrame(response.json())

        return data[["id", "statut", "protocol_type", "service", "src_bytes", "dst_bytes"]]
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API : {e}")
        return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur 


def get_data_from_api(conn_id: int):
    """Récupère les données de la connexion depuis l'API"""
    try:
        # Appel de l'API pour obtenir les données d'un ID spécifique
        response = requests.get(f"{API_URL}/id/{conn_id}")
        response.raise_for_status() 

        data = response.json()
        filtered_data = {key: data[key] for key in ["id", "protocol_type", "service", "src_bytes", "dst_bytes"] if key in data}
            
        if filtered_data:
            df_result = pd.DataFrame([filtered_data])
            return df_result
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API : {e}")
        return None
     
def predict_single_connection(conn_id: int):
    """Effectue une prédiction pour une connexion spécifique"""
    try:
        response = requests.get(f"{PREDICT_URL}/{conn_id}")
        response.raise_for_status()
        prediction_data = response.json()

        
        if prediction_data:
            # Vérifiez la structure réelle de la réponse
            if isinstance(prediction_data, dict) and "statut" in prediction_data:
                return prediction_data["statut"]
            else:
                # Adaptez selon la structure réelle de votre API
                return prediction_data.get("prediction", prediction_data)
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API pour la prédiction : {e}")
        return None

def show_dashboard():
    st.title("🔍 Surveillance Réseau")

    # Charger les données
    limit = st.slider("Nombre de connexions à charger :", 10, 500, 50)

    if "connexions_data" not in st.session_state or st.session_state.limit != limit:
        if st.button("Charger les données"):
            connexions_data = fetch_connection_data(limit)

            if not connexions_data.empty:
                # Stocker les données et la limite en session
                st.session_state.connexions_data = connexions_data
                st.session_state.limit = limit

    # Affichage des connexions réseau
    if "connexions_data" in st.session_state and not st.session_state.connexions_data.empty:
        connexions_data = st.session_state.connexions_data

        st.write("**Données des connexions réseau :**")
        st.dataframe(connexions_data)

        # Graphique du nombre de connexions par statut
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

        # Alertes de connexions suspectes
        nb_suspect = (connexions_data["statut"] == "Suspect").sum()
        col1, col2 = st.columns(2)
        with col1:
            st.success("Réseau opérationnel")
        with col2:
            st.error(f"⚠️ Alertes : {nb_suspect} connexions suspectes")

    else:
        st.warning("Aucune donnée disponible. Cliquez sur 'Charger les données'.")

   # Simulation d'une connexion unique
    st.subheader("Simulation d'une connexion")

    # Définir les limites d'ID (si les données existent dans session_state)
    if "connexions_data" in st.session_state and not st.session_state.connexions_data.empty:
        min_id, max_id = int(st.session_state.connexions_data["id"].min()), int(st.session_state.connexions_data["id"].max())
    else:
        min_id, max_id = 1, 500  # Valeurs par défaut si aucune donnée disponible

    conn_id = st.slider("Sélectionnez l'ID de la connexion :", min_value=min_id, max_value=max_id, step=1)

    # Récupération des données de l'API pour la connexion spécifiée
    data_from_api = get_data_from_api(conn_id)
    
    prediction_status = predict_single_connection(conn_id)

    if data_from_api is not None:
       
        if prediction_status is not None:
            # Ajouter le statut de prédiction aux données
            data_from_api['status'] = prediction_status
            
            # Affichage des détails de la connexion dans un tableau
            st.write("**Détails de la connexion sélectionnée :**")
            st.table(data_from_api)  # Affiche les données dans un tableau
            
            # Affichage d'un message pour indiquer si la connexion est normale ou suspecte
            if prediction_status == "Normal":
                st.success("Cette connexion est considérée comme **Normale**.")
            else:
                st.error("⚠️ Cette connexion est suspecte !")
        else:
            st.warning("La prédiction n'a pas pu être effectuée. Vérifiez la structure de la réponse de l'API.")
    else:
        st.warning("Aucune donnée disponible pour cette connexion.")

