import streamlit as st
import pandas as pd
import plotly.express as px

def show_statistics():
    st.title("Statistiques Réseau")

    # Récupérer les données depuis la mémoire (déjà stockées)
    if "connexions_data" not in st.session_state or st.session_state.connexions_data.empty:
        st.warning("Aucune donnée disponible. Chargez d'abord les données dans le Tableau de bord.")
        return
    
    connexions_data = st.session_state.connexions_data

  
    total_connexions = len(connexions_data)
    total_suspectes = (connexions_data["statut"] == "Suspect").sum()
    pourcentage_suspectes = (total_suspectes / total_connexions) * 100 if total_connexions > 0 else 0
    connexions_actives = connexions_data["service"].nunique() 
    anomalies_detectees = total_suspectes 

    #Affichage des métriques
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Connexions Totales", total_connexions)
    col2.metric("⚠️ Connexions Suspectes", f"{pourcentage_suspectes:.2f} %")
    col3.metric("Services Actifs", connexions_actives)
    col4.metric("Anomalies Détectées", anomalies_detectees)

    #Graphique 1 : Connexions par service
    st.subheader("🖧 Activité des services réseau")
    service_counts = connexions_data["service"].value_counts().reset_index()
    service_counts.columns = ["Service", "Nombre de connexions"]
    
    service_chart = px.bar(service_counts, 
                           x="Service", 
                           y="Nombre de connexions",
                           title="Utilisation des services réseau",
                           color="Nombre de connexions",
                           color_continuous_scale="blues")
    st.plotly_chart(service_chart, use_container_width=True)

    #Graphique 2 : Répartition des tailles de paquets envoyés
    st.subheader("📦 Distribution des tailles de paquets")
    packet_chart = px.histogram(connexions_data, 
                                x="src_bytes", 
                                nbins=30,
                                title="Distribution des tailles des paquets envoyés",
                                labels={"src_bytes": "Bytes envoyés"},
                                color_discrete_sequence=["#FFA07A"])
    st.plotly_chart(packet_chart, use_container_width=True)
