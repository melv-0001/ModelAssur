import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from backend.logic import analyse_sinistre, df
from collections import Counter
from wordcloud import WordCloud

st.set_page_config(page_title="Dashboard Assurance", layout="wide")

st.title("📊 Dashboard Assurance")

menu = st.sidebar.selectbox("Menu", ["Dashboard","Overview", "Analyse","Analyse2"])

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

    st.subheader("Requêtes fréquentes")
    st.dataframe(df["clean_text"].value_counts().head(10).reset_index().rename(columns={"index": "Requête", "clean_text": "Fréquence"}))

    words = " ".join(df["clean_text"]).split()
    common = Counter(words).most_common(10)

    st.subheader("Mots fréquents")
    for w, c in common:
        st.write(f"{w} : {c}")

    st.subheader("Nuage de Mots - Tous les sinistres")
    words = " ".join(df["clean_text"]).split()
    text_all = " ".join(words)

    if text_all.strip():
        import matplotlib.pyplot as plt
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_all)
        
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

    

# -------- OVERVIEW --------
if menu == "Overview":
    st.header("📈 Vue d'ensemble des sinistres")
    st.write("Cette section pourrait inclure des graphiques plus avancés.")
    # Affichage du dataframe
    st.subheader("Visualisation des données globales")
    st.dataframe(df) 

    st.subheader("Données les plus recurrentes")
    st.dataframe(df["clean_text"].value_counts().head(20).reset_index().rename(columns={"index": "Requête", "clean_text": "Fréquence"}))

    st.subheader("Types de sinistres les plus fréquents")
    st.dataframe(df["categorie"].value_counts().head(10).reset_index().rename(columns={"index": "Type", "categorie": "Fréquence"}))

    st.subheader("Nuage de Mots par Catégorie")

    categories = df["categorie"].unique()
    selected_category = st.selectbox("Sélectionner une catégorie", categories)
    
    category_texts = df[df["categorie"] == selected_category]["clean_text"]
    text_data = " ".join(category_texts)
    
    if text_data.strip():
        import matplotlib.pyplot as plt
        
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_data)
        
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.write("Pas de données pour cette catégorie")



# -------- ANALYSE ENRICHIE --------
if menu == "Analyse2":
    st.header("🔍 Analyse Intelligente de Sinistre")
    
    text = st.text_area("Collez ici la description du sinistre :", height=150)

    while st.button("Lancer l'expertise IA") and text:
        result = analyse_sinistre(text)
        

        # Affichage en colonnes pro
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Type détecté", result["categorie"])
           
        with col2:
            # Couleur dynamique selon la confiance
            st.metric("Indice de confiance", f"{int(result['confiance']*100)}%")
        with col3:
            status = "✅ Fiable" if result["confiance"] > 0.6 else "⚠️ À vérifier"
            st.write(f"**Statut :** {status}")

        # Alerte Fraude / Similarité
        st.subheader("📋 Dossiers similaires (Aide à la décision)")
        for r in result["similaires"]:
            with st.expander(f"Cas similaire - Score: {round(r['score'], 2)}"):
                st.write(r['text'])
                if r['score'] > 0.95:
                    st.error("🚩 Attention : Similarité très élevée. Risque de fraude ou doublon.")
        
        # -------- AIDE À LA DÉCISION --------

        st.write("---")
        st.subheader("🎯 Tableau de Stratégies de Remédiation")
        
        strategies = []
        
        # Confiance faible
        if result["confiance"] < 0.70:
            strategies.append({
            "Détection IA": "Confiance < 70%",
            "Diagnostic / Risque": "Description ambiguë ou bruit",
            "Remède / Action suggérée": "Validation humaine obligatoire via un expert"
            })
        
        # Similarité élevée
        if result["similaires"] and result["similaires"][0]["score"] > 0.95:
            strategies.append({
            "Détection IA": "Similarité > 95%",
            "Diagnostic / Risque": "Risque de doublon ou fraude",
            "Remède / Action suggérée": "Comparer les dates et les plaques d'immatriculation"
            })
        
        # Catégories spécifiques
        if result["categorie"] == "Vol":
            strategies.append({
            "Détection IA": "Catégorie Vol",
            "Diagnostic / Risque": "Sinistre à coût élevé potentiel",
            "Remède / Action suggérée": "Expertise terrain immédiate pour vérifier les traces d'effraction"
            })
        
        if result["categorie"] == "Bris de glace":
            strategies.append({
            "Détection IA": "Catégorie Bris de glace",
            "Diagnostic / Risque": "Sinistre simple et fréquent",
            "Remède / Action suggérée": "Automatisation totale : Envoi direct vers réparateur partenaire"
            })
        
        if strategies:
            st.dataframe(strategies, use_container_width=True)
        else:
            st.info("✅ Aucune alerte détectée. Dossier nominatif.")

        # Feedback
        st.write("---")
        st.caption("L'IA a-t-elle vu juste ?")
        st.button("👍 Oui")
        st.button("👎 Non")