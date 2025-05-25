# Projet « Maladies Cardiaques »  
*Prédiction du risque de maladie cardiaque par apprentissage automatique*

> Réalisé en Python / Jupyter Notebook par **Candice Giami**, **Joe Haïfa** et **Tom Huguet**

---

## Contexte
Les maladies cardiaques sont la première cause de mortalité dans le monde.  
L’objectif de ce projet est :

1. **Explorer et nettoyer** le jeu de données `heart_disease_data.csv` (18 variables, 918 patients).  
2. **Former et comparer** trois modèles de classification :  
   - Régression logistique  
   - k-Nearest Neighbors (KNN)  
   - Random Forest  
3. **Mettre à disposition** le meilleur modèle via :  
   - une application **desktop** (Tkinter) 
   - une **API + site web** (Flask + HTML/CSS/JS)
4. **Restituer** les résultats dans un rapport PDF, des notebooks d’analyse et un tableau de bord **Power BI**.

---

### Application bureau (Tkinter)

```bash
python app.py
```

Une fenêtre s’ouvre ; renseignez les champs cliniques, choisissez l’algorithme, puis **Prédire**.
Le résultat & la probabilité s’affichent dans une pop-up.


### Application web + API

```bash
python web.py
# Flask écoute par défaut sur http://127.0.0.1:5000
```

Le terminal affiche un lien ; cliquez-dessus pour ouvrir le formulaire web.
Les prédictions sont faites en AJAX, sans recharger la page.


### Tableau de bord Power BI

Ouvrir `viz.pbix` :

---

*Bon lancement !*
