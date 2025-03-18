from scripts.ModelManagement import ModelManagement
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# Configuration de connexion à la base PostgreSQL
DATABASE_URL = "postgresql://user:password@db:5432/kdd_cup99"
engine = create_engine(DATABASE_URL)

model_path = "kdd_model.pkl"
dm = ModelManagement(0, 0)
dm.load(model_path)

# Charger les données depuis PostgreSQL à chaque démarrage
def load_data(query):
    return pd.read_sql(query, engine)


# Préparer les données selon les instructions fournies
def prepare_data(df):
    df['label'] = np.where(df['label'] == 'normal', 0, 1)
    X = df.drop(columns=['label', 'id'])
    X_encoded = pd.get_dummies(X, columns=['protocol_type', 'service', 'flag'])
    return X_encoded

@app.get("/data/{limit}")
def get_data(limit: int):
    try:
        query = "SELECT * FROM connexions;"
        df = load_data(query)

        if df.empty:
            raise HTTPException(status_code=404, detail="Aucune donnée trouvée")

        # Conversion du label
        df['label'] = np.where(df['label'] == 'normal', 0, 1)

        # Séparation des anomalies et données normales
        anomalies = df[df['label'] == 1]
        normales = df[df['label'] == 0]

        nb_anomalies = int(limit * 0.05)
        nb_normales = limit - nb_anomalies

        # Échantillonnage forcé avec 5% d'anomalies
        sample_anomalies = anomalies.sample(n=min(nb_anomalies, len(anomalies)), replace=False, random_state=42)
        sample_normales = normales.sample(n=min(nb_normales, len(normales)), replace=False, random_state=42)

        df_sample = pd.concat([sample_normales, sample_anomalies]).sample(frac=1, random_state=42)

        # Préparation des données
        X_encoded = prepare_data(df_sample)

        train_columns = dm.model.feature_names_in_
        X_aligned = X_encoded.reindex(columns=train_columns, fill_value=0)

        predictions = dm.predict(X_aligned)

        df_result = df_sample.drop(columns=['label']).copy()
        df_result['statut'] = ['Normal' if pred == 0 else 'Suspect' for pred in predictions]

        return df_result.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")


# Route pour effectuer la prédiction et obtenir les données d'un ID spécifique
@app.get("/predict/{id}")
def predict_single(id: int):
    try:
        query = f"SELECT * FROM connexions WHERE id = {id};"
        df = load_data(query)

        if df.empty:
            raise HTTPException(status_code=404, detail="ID non trouvé dans la base")

        X_encoded = prepare_data(df)
        # Assurer que les colonnes correspondent à celles du modèle
        train_columns = dm.model.feature_names_in_
        X_aligned = X_encoded.reindex(columns=train_columns, fill_value=0)

        prediction = dm.predict(X_aligned)
        prediction_status = 'Normal' if prediction.tolist()[0] == 0 else 'Suspect'
        
        # Création du DataFrame final avec la prédiction
        df_result = df.drop(columns=['label']).copy() if 'label' in df.columns else df.copy()
        df_result['statut'] = prediction_status
        
        # Conversion directe en JSON
        return df_result.to_dict(orient="records")[0]  # Renvoie un seul objet JSON (pas une liste)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")
    

@app.get("/test_model")
def test_model_loading():
    if dm.model:
        return {"message": "Le modèle a été chargé avec succès"}
    else:
        return {"message": "Erreur lors du chargement du modèle"}

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}