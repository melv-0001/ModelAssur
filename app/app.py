import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------- CONFIG --------------------
st.set_page_config(page_title="IA Assurance", layout="wide")

# -------------------- STYLE --------------------
st.markdown("""
<style>
body {
    background-color: #f5f9ff;
}
.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}
h1, h2, h3 {
    color: #0b3c5d;
}
</style>
""", unsafe_allow_html=True)

# -------------------- MODEL --------------------
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# -------------------- DATA (SIMULATION) --------------------
@st.cache_data
def load_data():
    data = pd.DataFrame({
        "description": [
            "accident en marche arrière",
            "vitre cassée pendant la nuit",
            "collision avec un autre véhicule",
            "vol de pièces dans la voiture",
            "rayure sur le véhicule garé"
        ],
        "categorie": [
            "accident_circulation",
            "vandalisme",
            "accident_circulation",
            "vol",
            "vandalisme"
        ]
    })
    return data

df = load_data()

# Precompute embeddings
embeddings = model.encode(df['description'].tolist())

# -------------------- HEADER --------------------
st.title("Plateforme d'Analyse de Sinistres")

# -------------------- INPUT --------------------
user_input = st.text_area("Décrire le sinistre")

if user_input:
    input_embedding = model.encode([user_input])

    similarities = cosine_similarity(input_embedding, embeddings)[0]
    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]

    predicted_category = df.iloc[best_idx]['categorie']

    # -------------------- METRICS --------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Catégorie détectée", predicted_category)
    col2.metric("Score de similarité", f"{best_score:.2%}")
    col3.metric("Cas le plus proche", df.iloc[best_idx]['description'])

    # -------------------- FRAUD ALERT --------------------
    if best_score > 0.95:
        st.error("⚠️ Alerte : Similarité très élevée avec un cas existant. Risque de fraude ou duplication.")

    # -------------------- DECISION SUPPORT --------------------
    st.subheader("Aide à la décision")

    if predicted_category == "accident_circulation":
        st.info("➡️ Action recommandée : Envoyer un expert pour évaluation du véhicule.")
    elif predicted_category == "vol":
        st.info("➡️ Action recommandée : Vérifier le dépôt de plainte avant indemnisation.")
    elif predicted_category == "vandalisme":
        st.info("➡️ Action recommandée : Automatiser le remboursement si preuves fournies.")
    else:
        st.info("➡️ Action recommandée : Analyse manuelle requise.")

    # -------------------- SIMILAR CASES --------------------
    st.subheader("Cas similaires")
    similar_df = df.copy()
    similar_df['score'] = similarities
    similar_df = similar_df.sort_values(by='score', ascending=False).head(5)

    st.dataframe(similar_df)

# -------------------- DASHBOARD --------------------
st.header("Dashboard")

# Distribution des catégories
fig1 = px.pie(df, names='categorie', title="Répartition des sinistres")
st.plotly_chart(fig1, use_container_width=True)

# Longueur moyenne des descriptions

df['length'] = df['description'].apply(len)
length_df = df.groupby('categorie')['length'].mean().reset_index()

fig2 = px.bar(length_df, x='categorie', y='length', title="Longueur moyenne des descriptions")
st.plotly_chart(fig2, use_container_width=True)
