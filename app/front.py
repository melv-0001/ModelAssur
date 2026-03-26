import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from backend.logic import analyse_sinistre, df
from collections import Counter

st.set_page_config(page_title="Dashboard Assurance", layout="wide")

st.title("📊 Dashboard Assurance")

menu = st.sidebar.selectbox("Menu", ["Analyse", "Dashboard"])

# -------- ANALYSE --------
if menu == "Analyse":
    st.header("Analyse d'une déclaration")

    text = st.text_area("Entrer une déclaration")

    if st.button("Analyser") and text:
        result = analyse_sinistre(text)

        st.metric("Catégorie", result["categorie"])
        st.metric("Confiance", result["confiance"])

        st.subheader("Cas similaires")
        for r in result["similaires"]:
            st.write(f"- {r['text']} ({round(r['score'], 2)})")

# -------- DASHBOARD --------
if menu == "Dashboard":
    st.header("Statistiques")

    st.subheader("Répartition des catégories")
    st.bar_chart(df["categorie"].value_counts())

    words = " ".join(df["clean_text"]).split()
    common = Counter(words).most_common(10)

    st.subheader("Mots fréquents")
    for w, c in common:
        st.write(f"{w} : {c}")