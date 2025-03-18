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

# Route pour effectuer la prédiction sur un nouvel échantillon (données entrantes)
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
        X_encoded = X_encoded.reindex(columns=train_columns, fill_value=0)
        # # Assure l'alignement avec les colonnes attendues par le modèle
        # df_full = load_data("SELECT * FROM connexions LIMIT 10;")
        # reference_encoded = prepare_data(df_full)
        # X_encoded = X_encoded.reindex(columns=reference_encoded.columns, fill_value=0)
        print(X_encoded)
        prediction = dm.predict(X_encoded)
        print(prediction)
        return {"id": id, "prediction": 'Normal' if prediction.tolist()[0] == 0 else 'Suspect'}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")
    
@app.get("/predict_all/{limit}")
def predict_all(limit: int):
    try:
        query = f"SELECT * FROM connexions LIMIT {limit};"
        df = load_data(query)

        if df.empty:
            raise HTTPException(status_code=404, detail="Aucune donnée trouvée")

        X_encoded = prepare_data(df)
         # Assurer que les colonnes correspondent à celles du modèle
        train_columns = dm.model.feature_names_in_
        X_encoded = X_encoded.reindex(columns=train_columns, fill_value=0)

        predictions = dm.predict(X_encoded)

        results = [{"id": int(df.iloc[i]['id']), "prediction": 'Normal' if pred == 0 else 'Suspect'} for i, pred in enumerate(predictions)]

        return {"results": results}

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