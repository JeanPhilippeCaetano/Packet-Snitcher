import streamlit as st
import plotly.express as px

def show_anomalies():
    st.title("Détection d'Anomalies")
    
    data = st.session_state.get("connexions_data")
    
    if data is None or data.empty:
        st.warning("⚠️ Aucune donnée disponible. Veuillez charger les connexions depuis la page Tableau de bord.")
        return
    
    anomalies_data = data[data["statut"] == "Suspect"]
    
    if anomalies_data.empty:
        st.info("Aucune anomalie détectée dans les données actuelles.")
        return
    
    st.write("### Anomalies détectées :")
    st.dataframe(anomalies_data)
    
    # Répartition des anomalies par protocole
    anomalies_par_protocole = anomalies_data["protocol_type"].value_counts().reset_index()
    anomalies_par_protocole.columns = ["Protocole", "Nombre d'anomalies"]
    
    st.subheader("Répartition des anomalies par protocole")
    st.plotly_chart(px.bar(anomalies_par_protocole, x="Protocole", y="Nombre d'anomalies", 
                           title="Nombre d'anomalies par protocole", labels={"Protocole": "Protocole", "Nombre d'anomalies": "Nombre"}),
                    use_container_width=True)