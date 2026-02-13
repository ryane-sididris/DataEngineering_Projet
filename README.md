# Projet Data Engineering : Pokedex Analytics

Ce projet est une application web permettant l'extraction, le stockage et l'analyse de données depuis le site PokemonDB. Il a été réalisé dans le cadre du module de Data Engineering.

## Architecture et Choix Techniques

L'application repose sur une architecture hybride pour pallier les limitations techniques liées à l'émulation de navigateurs (Chromium/Selenium) sur les architectures Apple Silicon (M1/M2/M3) via Docker.

* **Extraction (Scraping)** : Python + Selenium. Le script s'exécute en local pour garantir la stabilité du driver Chrome et permettre une visualisation du processus.
* **Base de Données** : MongoDB. La base de données est conteneurisée via Docker pour assurer la persistance et l'isolation des données.
* **Interface Utilisateur** : Streamlit. Permet la visualisation des données et le déclenchement du scraping via une interface web.
* **Analyse de Données** : Utilisation de la librairie Altair pour générer des visualisations complexes (Heatmaps de densité) permettant une meilleure lecture de la distribution des statistiques.

## Pre-requis

* Docker Desktop installé et lancé.
* Python 3.9 ou supérieur.
* Navigateur Google Chrome installé.

## Installation et Lancement

1. Démarrage de la Base de Données
Le projet utilise Docker Compose pour orchestrer la base de données MongoDB.
commande :
docker-compose up -d mongo

2. Installation des dépendances Python
Il est recommandé d'utiliser un environnement virtuel.
commandes :
python3 -m venv .venv
source .venv/bin/activate (Mac/Linux) ou .venv\Scripts\activate (Windows).
pip install -r requirements.txt

3. Lancement de l'Application
L'application Streamlit sert de point d'entrée pour le scraping et la visualisation.
commande :
streamlit run app/main.py

## Fonctionnalités

-Mise à jour des données (ETL) : Pipeline automatisé extrayant les noms, types, statistiques et images. Gestion intelligente des Méga-Évolutions et variantes de formes.

-Dashboard Avancé : Visualisation interactive avec indicateurs clés (KPIs) dynamiques comparant la sélection actuelle aux moyennes globales du "marché" Pokémon.

-Filtrage Multicritères : Recherche textuelle, filtrage par Type, et réglage fin via sliders pour l'Attaque, la Défense et les PV.

-Tri Personnalisé : Possibilité de réorganiser la galerie par puissance, statistiques spécifiques ou ordre alphabétique.

-Analyses Globales : Heatmap de corrélation Attaque/Défense et graphiques de répartition par type pour identifier les tendances de la base de données.

## Auteurs
Ryane SID IDRIS et Sofiane MOUHOUB
