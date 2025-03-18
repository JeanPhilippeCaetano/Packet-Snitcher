import streamlit as st
import plotly.express as px
import pandas as pd

def show_anomalies():
    st.title("Détection d'Anomalies")


    if "connexions_data" in st.session_state and not st.session_state.connexions_data.empty:
        anomalies_data = st.session_state.connexions_data[st.session_state.connexions_data["statut"] == "Suspect"]
        
        if not anomalies_data.empty:
            st.write("Anomalies détectées :")
            st.dataframe(anomalies_data)

            
            anomalies_par_protocole = anomalies_data["protocol_type"].value_counts().reset_index()
            anomalies_par_protocole.columns = ["Protocole", "Nombre d'anomalies"]

            # Graphique des anomalies par protocole
            st.subheader("Répartition des anomalies par protocole")
            anomalies_chart = px.bar(anomalies_par_protocole, 
                                     x="Protocole", 
                                     y="Nombre d'anomalies", 
                                     title="Nombre d'anomalies par protocole",
                                     labels={"Protocole": "Protocole", "Nombre d'anomalies": "Nombre"})
            st.plotly_chart(anomalies_chart, use_container_width=True)
        else:
            st.info(" Aucune anomalie détectée dans les données actuelles.")
    else:
        st.warning("⚠️ Aucune donnée disponible. Veuillez charger les connexions depuis la page Tableau de bord.")
