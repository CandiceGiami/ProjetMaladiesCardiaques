
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_knn_model(X, Y, n_neighbors=61, test_size=0.2, random_state=42):
    # Séparation des données
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=random_state)

    # Normalisation des données
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # Création et entraînement du modèle
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X_train, Y_train)

    # Évaluation du modèle
    Y_pred = model.predict(X_test)
    acc = accuracy_score(Y_test, Y_pred)
    report = classification_report(Y_test, Y_pred)
    
    return model

def predict_with_knn(model, scaler, X_new):
    return model.predict(X_new)
