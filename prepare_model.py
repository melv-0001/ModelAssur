import pandas as pd
import re
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Charger données
df = pd.read_excel("data/Test IA analyse des circonstances.xlsx")

df = df.dropna()
df = df.drop_duplicates(subset=["Circonstances"])
df = df.reset_index(drop=True)

df["clean_text"] = df["Circonstances"].apply(clean_text)

print("📊 Données prêtes")

# Modèle
model = SentenceTransformer('all-MiniLM-L6-v2')

print("🧠 Encodage...")
embeddings = model.encode(df["clean_text"].tolist(), show_progress_bar=True)

# Clustering
kmeans = KMeans(n_clusters=4, random_state=42)
df["cluster"] = kmeans.fit_predict(embeddings)

# Mapping métier
mapping = {
    0: {"type": "dommage", "label": "bris de glace"},
    1: {"type": "accident", "label": "collision avec tiers"},
    2: {"type": "stationnement", "label": "sinistre parking"},
    3: {"type": "accident", "label": "accident circulation"}
}

df["categorie"] = df["cluster"].map(lambda x: mapping[x]["label"])

# Pré-calcul
cluster_embeddings = {}
cluster_data = {}

for c in df["cluster"].unique():
    idx = df[df["cluster"] == c].index
    cluster_embeddings[c] = embeddings[idx]
    cluster_data[c] = df[df["cluster"] == c].reset_index(drop=True)

# Sauvegarde
with open("model_data.pkl", "wb") as f:
    pickle.dump({
        "df": df,
        "kmeans": kmeans,
        "cluster_embeddings": cluster_embeddings,
        "cluster_data": cluster_data,
        "mapping": mapping
    }, f)

print("✅ model_data.pkl créé")