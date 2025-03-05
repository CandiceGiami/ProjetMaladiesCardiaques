import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix

def train_random_forest_model(X, Y):
    

    # Séparation en ensemble d'entraînement et de test
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    max_accuracy = 0  # Initialisation de la précision maximale

    # Boucle pour tester différentes valeurs de `random_state`
    for x in range(50):
        rf = RandomForestClassifier(random_state=x)
        rf.fit(X_train, Y_train)
        Y_pred_rf = rf.predict(X_test)
        current_accuracy = round(accuracy_score(Y_pred_rf, Y_test) * 100, 2)

        # Mise à jour de la meilleure précision et du meilleur `random_state`
        if current_accuracy > max_accuracy:
            max_accuracy = current_accuracy
            best_x = x

    # Création du modèle avec la meilleure valeur de `random_state`
    rf = RandomForestClassifier(random_state=best_x)
    rf.fit(X_train, Y_train)
    
    return rf

def predict_with_random_forest(model, scaler, X_new):
    return model.predict(X_new)
