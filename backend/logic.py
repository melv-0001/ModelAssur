import re
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_data.pkl")

# Nettoyage
def clean_text(text):
    text = str(text).lower()
    text = text.replace("’", "'")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Charger données (cache)
@st.cache_resource
def load_data():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

data = load_data()

df = data["df"]
kmeans = data["kmeans"]
cluster_embeddings = data["cluster_embeddings"]
cluster_data = data["cluster_data"]
mapping = data["mapping"]

# Charger modèle (cache)
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Analyse
def analyse_sinistre(text, top_k=3):

    if not text.strip():
        return {"type": "inconnu", "categorie": "inconnu", "confiance": 0, "similaires": []}
import re
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_data.pkl")

# Nettoyage
def clean_text(text):
    text = str(text).lower()
    text = text.replace("’", "'")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Charger données (cache)
@st.cache_resource
def load_data():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

data = load_data()

df = data["df"]
kmeans = data["kmeans"]
cluster_embeddings = data["cluster_embeddings"]
cluster_data = data["cluster_data"]
mapping = data["mapping"]

# Charger modèle (cache)
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Analyse
def analyse_sinistre(text, top_k=3):

    if not text.strip():
        return {"type": "inconnu", "categorie": "inconnu", "confiance": 0, "similaires": []}

    text_clean = clean_text(text)
    emb = model.encode([text_clean])

    similarities = cosine_similarity(emb, kmeans.cluster_centers_)[0]
    cluster_id = int(np.argmax(similarities))
    confidence = float(np.max(similarities))    # niveau de similarité au centre de cluster
   

    category_info = mapping.get(cluster_id, {"type": "autre", "label": "inconnu"})

    subset = cluster_data[cluster_id]
    subset_emb = cluster_embeddings[cluster_id]

    scores = cosine_similarity(emb, subset_emb)[0]
    top_idx = scores.argsort()[-top_k:][::-1]
    top_scores = np.sort(scores)[-top_k:]
    belonging_score = float(np.mean(top_scores))  # similarité aux points du cluster

    results = [
        {"text": subset["Circonstances"].iloc[i], "score": float(scores[i])}
        for i in top_idx
    ]

    return {
        "type": category_info["type"],
        "categorie": category_info["label"],
        "confiance": round(confidence, 3),
        "similaires": results
    }
    