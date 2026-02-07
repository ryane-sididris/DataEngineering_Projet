# Projet Data Engineering : Pokedex Analytics

Ce projet est une application web permettant l'extraction, le stockage et l'analyse de données depuis le site PokemonDB. Il a été réalisé dans le cadre du module de Data Engineering.

## Architecture et Choix Techniques

L'application repose sur une architecture hybride pour pallier les limitations techniques liées à l'émulation de navigateurs (Chromium/Selenium) sur les architectures Apple Silicon (M1/M2/M3) via Docker.

* **Extraction (Scraping)** : Python + Selenium. Le script s'exécute en local pour garantir la stabilité du driver Chrome et permettre une visualisation du processus.
* **Base de Données** : MongoDB. La base de données est conteneurisée via Docker pour assurer la persistance et l'isolation des données.
* **Interface Utilisateur** : Streamlit. Permet la visualisation des données et le déclenchement du scraping via une interface web.

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
source .venv/bin/activate
pip install -r requirements.txt

3. Lancement de l'Application
L'application Streamlit sert de point d'entrée pour le scraping et la visualisation.
commande :
streamlit run app/main.py

## Fonctionnalités

* **Mise à jour des données (ETL)** : Un bouton dans l'interface déclenche le script de scraping qui extrait les données en temps réel et met à jour la base MongoDB.
* **Visualisation** : Tableau de bord interactif affichant les statistiques des Pokémon.
* **Filtrage** : Possibilité de filtrer par Type et par puissance d'attaque.
* **Analyse** : Graphique de corrélation entre l'Attaque et la Défense.

## Auteurs
Ryane SID IDRIS et Sofiane MOUHOUB