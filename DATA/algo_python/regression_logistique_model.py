from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def train_regression_model(X, Y, test_size=0.2, random_state=42):
    # Débogage : afficher la forme de X
    print("Shape de X avant la séparation : ", X.shape)
    
    # Séparation des données en train et test
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=random_state)

    # Débogage : afficher la forme de X_train et X_test après séparation
    print("Shape de X_train après séparation : ", X_train.shape)
    print("Shape de X_test après séparation : ", X_test.shape)

    # Normalisation sur toutes les features (16)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Débogage : vérifier la forme de X_train_scaled après normalisation
    print("Shape de X_train_scaled après normalisation : ", X_train_scaled.shape)

    X_test_scaled = scaler.transform(X_test)
    
    # Débogage : vérifier la forme de X_test_scaled après normalisation
    print("Shape de X_test_scaled après normalisation : ", X_test_scaled.shape)

    # Optimisation des hyperparamètres avec GridSearchCV
    param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100]}
    log_reg = GridSearchCV(LogisticRegression(penalty='l2', solver='liblinear', max_iter=1000), param_grid, cv=5)
    log_reg.fit(X_train_scaled, y_train)

    # Meilleur modèle
    best_model = log_reg.best_estimator_
    
    # Débogage : vérifier les paramètres du meilleur modèle
    print("Meilleur modèle trouvé : ", best_model)

    return best_model, scaler  # Retourne aussi le scaler

def predict_with_regression(model, X_new):
    # Débogage : afficher la forme de X_new
    print("Shape de X_new avant transformation : ", X_new.shape)
    
      # Transformation de X_new
    print("Shape de X_new_scaled après transformation : ", X_new)
    
    # Prédiction avec le modèle
    predictions = model.predict(X_new)
    
    return predictions


