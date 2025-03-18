import streamlit as st

# Configuration de la page
st.set_page_config(page_title="NetMonitor", layout="wide")


try:
    from dashboard import show_dashboard
    from anomalies import show_anomalies
    from statistics import show_statistics
    from logs import show_logs
except ImportError:
    st.error("⚠️ Erreur d'importation des modules. Vérifiez les noms des fichiers !")


if "page" not in st.session_state:
    st.session_state.page = "Tableau de bord"



st.sidebar.title("Navigation")

if st.sidebar.button("Tableau de bord"):
    st.session_state.page = "Tableau de bord"

if st.sidebar.button(f"Anomalies"):
    st.session_state.page = "Anomalies"

if st.sidebar.button("Statistiques"):
    st.session_state.page = "Statistiques"

if st.sidebar.button("Logs & Historique"):
    st.session_state.page = "Logs & Historique"


pages = {
    "Tableau de bord": show_dashboard,
    "Anomalies": show_anomalies,
    "Statistiques": show_statistics,
    "Logs & Historique": show_logs,
}

pages[st.session_state.page]()
