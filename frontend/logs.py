import streamlit as st
import pandas as pd

def show_logs():
    st.title("Logs & Historique des Anomalies")

    # Vérifier si les données existent en session
    if "connexions_data" in st.session_state and not st.session_state.connexions_data.empty:
        stats_anomalies = st.session_state.connexions_data[st.session_state.connexions_data["statut"] == "Suspect"]
        
        if not stats_anomalies.empty:
            st.write("Détails des anomalies détectées")

            # Recherche avancée sur protocole, ID et service
            st.subheader("Recherche avancée")
            search_query = st.text_input("Rechercher par protocole, ID ou service", placeholder="Ex: TCP, 12345, http...")

            if search_query:
                stats_anomalies = stats_anomalies[
                    stats_anomalies["protocol_type"].astype(str).str.contains(search_query, case=False) |
                    stats_anomalies["id"].astype(str).str.contains(search_query, case=False) |
                    stats_anomalies["service"].astype(str).str.contains(search_query, case=False)
                ]

            # Affichage du tableau des anomalies
            st.dataframe(stats_anomalies)

            # Bouton d'export des anomalies en CSV
            st.download_button(
                "📥 Exporter les anomalies (CSV)",
                data=stats_anomalies.to_csv(index=False, encoding="utf-8-sig"),
                file_name="anomalies.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucune anomalie détectée dans les données actuelles.")
    else:
        st.warning("⚠️ Aucune donnée disponible. Veuillez charger les connexions depuis la page Tableau de bord.")
