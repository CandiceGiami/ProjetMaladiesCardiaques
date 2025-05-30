import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import os
import sys

# Chemin absolu du dossier racine
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ajouter le dossier racine au PATH pour importer algo_python
sys.path.append(base_dir)

from algo_python.random_forest_model import train_random_forest_model
from algo_python.knn_model import train_knn_model
from algo_python.regression_logistique_model import train_regression_model

# Chemin absolu du dossier racine
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class HeartDiseaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Détection de maladie cardiaque")
        self.root.configure(bg="#e9f2f9")

        self.entries = {}
        self.scaler = None
        self.models = {}

        self.columns = [
            "Âge", "Sexe", "Tension_aurepos", "Cholestérol", "Glycémieà_jeun",
            "Fréquence_cardiaque_max", "Angine_d_effort", "Dépression_ST",
            "Type_de_douleur_thoracique_ASY", "Type_de_douleur_thoracique_ATA",
            "Type_de_douleur_thoracique_NAP", "Type_de_douleur_thoracique_TA",
            "ECG_au_repos_LVH", "ECG_au_repos_Normal", "ECG_au_repos_ST",
            "Pente_ST_Down", "Pente_ST_Flat", "Pente_ST_Up"
        ]
        self.target_column = "Maladie_cardiaque"

        self.load_and_prepare_data()
        self.create_widgets()

    def load_and_prepare_data(self):
        try:
            file_path = os.path.join(base_dir, "données", "donnée_malades_cardiaques.csv")

            # Debug : voir le chemin dans la console si besoin
            print("Chargement depuis :", file_path)

            try:
                df = pd.read_csv(file_path)
                if "Unnamed: 0" in df.columns:
                    df = df.drop(columns=["Unnamed: 0"])
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de chargement des données : {e}")
                self.root.destroy()
                return

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de chargement des données : {e}")
            self.root.destroy()
            return

        X = df[self.columns]
        y = df[self.target_column]

        # Entraînement des modèles
        self.models["Random Forest"] = train_random_forest_model(X, y)
        self.models["KNN"] = train_knn_model(X, y)
        model_lr, self.scaler = train_regression_model(X, y)
        self.models["Régression Logistique"] = model_lr

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Formulaire Patient", font=("Helvetica", 18, "bold"), bg="#e9f2f9")
        title_label.pack(pady=10)

        form_frame = tk.Frame(self.root, bg="#e9f2f9")
        form_frame.pack(padx=20, pady=10)

        for i, col in enumerate(self.columns):
            label = tk.Label(form_frame, text=col + " :", font=("Arial", 10), bg="#e9f2f9")
            label.grid(row=i, column=0, sticky="e", padx=5, pady=2)

            entry = tk.Entry(form_frame, font=("Arial", 10), width=25, relief="solid", bd=1)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.entries[col] = entry

        model_frame = tk.Frame(self.root, bg="#e9f2f9")
        model_frame.pack(pady=10)

        tk.Label(model_frame, text="Choisissez un modèle :", bg="#e9f2f9", font=("Arial", 11)).pack(side="left", padx=5)
        self.model_type = ttk.Combobox(model_frame, values=["Random Forest", "KNN", "Régression Logistique"], width=25, font=("Arial", 10))
        self.model_type.current(0)
        self.model_type.pack(side="left", padx=5)

        predict_btn = tk.Button(self.root, text="Prédire", command=self.predict, bg="#007acc", fg="white",
                                font=("Arial", 12), relief="raised", bd=3, padx=10, pady=5)
        predict_btn.pack(pady=20)

    def get_input_data(self):
        try:
            values = [float(self.entries[col].get()) for col in self.columns]
            return np.array(values).reshape(1, -1)
        except ValueError:
            raise ValueError("Veuillez entrer des valeurs numériques valides.")

    def predict(self):
        try:
            input_data = self.get_input_data()
            model_name = self.model_type.get()
            model = self.models[model_name]

            # Mise à l'échelle pour tous les modèles
            input_scaled = self.scaler.transform(input_data)

            # Prédiction
            prediction = model.predict(input_scaled)[0]

            # Probabilité réelle (classe "1" = malade)
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(input_scaled)[0]
                # Vérification de la classe "1" dans model.classes_
                malade_index = list(model.classes_).index(1)
                confidence = proba[malade_index]
            else:
                confidence = 0.0  # fallback

            # Affichage
            if prediction == 1:
                messagebox.showwarning("Risque détecté", f" Risque de maladie cardiaque\nConfiance : {confidence:.2f}")
            else:
                messagebox.showinfo("Aucun risque", f"Aucun risque détecté\nConfiance : {confidence:.2f}")

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HeartDiseaseApp(root)

    # Centrage de la fenêtre
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()
