import streamlit as st
from pathlib import Path

from utils.data import load_data
from utils.charts import bar_quality, scatter_geo, histogram_score
from utils.chatbot import DataAnalysisAssistant

st.set_page_config(
    page_title="TP3 – Open Data App",
    layout="wide"
)

# Chargement des données
@st.cache_data
def get_data():
    path = Path("data/processed")
    files = list(path.glob("*.parquet"))
    if not files:
        st.error("Aucun fichier Parquet trouvé")
        st.stop()
    return load_data(files[0])


df = get_data()

# Titre
st.title("TP3 – Application Open Data")
st.markdown("Exploration des données de géocodage issues du TP2")

# KPI - Métriques personnalisées
c1, c2, c3, c4 = st.columns(4)
c1.metric("📍 Total adresses géocodées", len(df))
c2.metric("⭐ Score médian", f"{df['score'].median():.2f}")
c3.metric("✅ Taux de qualité excellente", f"{(df['qualite'] == 'excellente').sum() / len(df) * 100:.1f}%")
c4.metric("📊 Colonnes analysées", len(df.columns))

# Visualisations
st.header("📈 Visualisations Interactives")

# Organiser en colonnes
col1, col2 = st.columns(2)

# Graphique pleine largeur
st.subheader("Analyse géographique")
st.plotly_chart(scatter_geo(df), use_container_width=True)

with col1:
    st.subheader("Distribution des scores")
    st.plotly_chart(histogram_score(df), use_container_width=True)

with col2:
    st.subheader("Qualité par catégorie")
    st.plotly_chart(bar_quality(df), use_container_width=True)

# Chatbot
st.header("Assistant IA")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = DataAnalysisAssistant(df)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ecris une ou plusieurs questions sur le dataset"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chatbot.analyze(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
