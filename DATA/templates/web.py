from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import os
import sys 

# Chemin absolu du dossier racine (un niveau au-dessus de templates)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ajouter le dossier racine au PATH pour importer algo_python
sys.path.append(base_dir)

from algo_python.knn_model import train_knn_model, predict_with_knn
from algo_python.random_forest_model import train_random_forest_model, predict_with_random_forest
from algo_python.regression_logistique_model import train_regression_model, predict_with_regression

app = Flask(__name__)
# Chemin vers le fichier CSV (dans le dossier racine)
file_path = os.path.join(base_dir, "donnée_malades_cardiaques.csv")

df = pd.read_csv(file_path, index_col=0)

X = df.drop(columns=['Maladie_cardiaque'])
Y = df['Maladie_cardiaque']

# Entraîner les modèles
knn_model = train_knn_model(X, Y)
rf_model = train_random_forest_model(X, Y)
rl_model, scaler = train_regression_model(X, Y)

app = Flask(__name__, template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates")))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json['features']
        features = np.array(data).reshape(1, -1)
        features_scaled = scaler.transform(features)

        knn_proba = knn_model.predict_proba(features_scaled)[0]
        rf_proba = rf_model.predict_proba(features_scaled)[0]
        rl_proba = rl_model.predict_proba(features_scaled)[0]

        return jsonify({
            "knn": int(knn_model.predict(features_scaled)[0]),
            "knn_proba": knn_proba.tolist(),
            "rf": int(rf_model.predict(features_scaled)[0]),
            "rf_proba": rf_proba.tolist(),
            "rl": int(rl_model.predict(features_scaled)[0]),
            "rl_proba": rl_proba.tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
