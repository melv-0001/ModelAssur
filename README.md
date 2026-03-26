###  Vitrine du projet

# 📊 Analyse Intelligente des Sinistres Automobiles

## 📝 Contexte et Objectif
Ce projet vise à optimiser le traitement des déclarations de sinistres pour les assureurs. L'objectif est d'automatiser la catégorisation de plus de 4000 descriptions rédigées librement par les assurés pour accélérer la prise de décision.

## 🧠 Méthodologie "Niveau Pro"
Le système utilise une **approche hybride** combinant IA de pointe et règles métier :
1. **Prétraitement (NLP) :** Nettoyage, normalisation et passage en minuscules pour réduire le bruit.
2. **Représentation (Sentence-BERT) :** Transformation des textes en vecteurs numériques via le modèle `all-MiniLM-L6-v2` pour capturer le sens profond.
3. **Clustering (K-Means) :** Regroupement automatique en 4 catégories clés (Bris de glace, Accident, Stationnement, etc.).
4. **Similarité Cosinus :** Recherche de cas historiques similaires pour assister les gestionnaires et détecter d'éventuelles fraudes.

## 🛠️ Stack Technologique
- **Langage :** Python
- **IA/ML :** Scikit-Learn, Sentence-Transformers (BERT)
- **Frontend :** Streamlit pour un dashboard interactif et intuitif
- **Données :** Pandas, Pickle pour la sérialisation du modèle

## 🚀 Installation et Utilisation
1. Cloner le dépôt : `git clone ...`
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer l'application : `streamlit run src/app.py`
```

### Les `requirements.txt`
Ce fichier permet à n'importe qui de réinstaller ton environnement en une ligne.
```text
pandas
scikit-learn
sentence-transformers
streamlit
plotly
matplotlib
```
