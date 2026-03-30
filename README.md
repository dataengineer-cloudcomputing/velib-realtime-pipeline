# 🚲 Monitoring Temps-Réel Velib Métropole (Pipeline Data)

## 📌 Présentation du Projet
Ce projet met en place un pipeline de données automatisé pour monitorer la disponibilité des vélos (mécaniques vs électriques) sur l'ensemble du réseau Velib Métropole en région Ile-de-France.

L'objectif est d'offrir une visibilité en temps réel sur l'état des stations pour optimiser la maintenance et l'usage des bornes électriques.

## 🏗️ Architecture Technique
Le projet repose sur une stack moderne de Data Engineering :
* **Extraction** : API Open Data Paris (v1.0) via Python (Requests/Pandas).
* **Orchestration** : **Apache Airflow** (exécution horaire).
* **Stockage (Data Warehouse)** : **Google BigQuery**.
* **Transformation** : **dbt** (Data Build Tool) pour le nettoyage et la logique métier.
* **Visualisation** : **Google Looker Studio**.



## 🛠️ Pipeline de Données
### 1. Extraction (Airflow)
Le DAG récupère les données de ~1400 stations. Contrairement aux versions standards, ce pipeline extrait spécifiquement le détail des vélos mécaniques (`mechanical`) et électriques (`ebike`) pour une analyse fine.

### 2. Transformation (dbt)
Les données brutes sont transformées pour :
* Calculer le statut opérationnel de la station (HORS SERVICE, VERT UNIQUEMENT, BLEU UNIQUEMENT, etc.).
* Convertir les coordonnées géographiques pour la cartographie.
* Nettoyer les types de données pour BigQuery.

### 3. Visualisation (Looker Studio)
Un tableau de bord interactif permet de :
* Visualiser la position GPS exacte des stations.
* Identifier les pannes via un code couleur métier.
* Consulter le détail précis (Verts vs Bleus) au survol des stations.

## 🚀 Installation & Utilisation
1. Cloner le repo.
2. Placer le DAG dans votre dossier Airflow.
3. Configurer les credentials Google Cloud (`google_key.json`).
4. Lancer `dbt run` pour initialiser les tables de production.

# 🚲 Real-Time Monitoring of Velib Métropole (Data Pipeline)

## 📌 Project Overview
This project implements an automated data pipeline to monitor the availability of bicycles (mechanical vs. electric) across the entire Velib Métropole network in Ile-de-France.

The goal is to provide real-time visibility into station status to optimize maintenance and usage of electric charging stations.

## 🏗️ Technical Architecture
The project is built on a modern data engineering stack:
* **Extraction**: Open Data Paris API (v1.0) via Python (Requests/Pandas).
* **Orchestration**: **Apache Airflow** (hourly execution).
* **Storage (Data Warehouse)**: **Google BigQuery**.
* **Transformation**: **dbt** (Data Build Tool) for data cleaning and business logic.
* **Visualization**: **Google Looker Studio**.

------------------------------------------------------------------------------------

## 🛠️ Data Pipeline
### 1. Extraction (Airflow)
The DAG retrieves data from ~1,400 stations. Unlike standard versions, this pipeline specifically extracts details for mechanical (`mechanical`) and electric (`ebike`) bikes for detailed analysis.

### 2. Transformation (dbt)
The raw data is transformed to:
* Calculate the station’s operational status (OUT OF SERVICE, GREEN ONLY, BLUE ONLY, etc.).
* Convert geographic coordinates for mapping.
* Clean the data types for BigQuery.

### 3. Visualization (Looker Studio)
An interactive dashboard allows you to:
* View the exact GPS location of the stations.
* Identify outages using a color-coded system.
* View detailed information (Green vs. Blue) when hovering over stations.

## 🚀 Installation & Usage
1. Clone the repo.
2. Place the DAG in your Airflow folder.
3. Configure Google Cloud credentials (`google_key.json`).
4. Run `dbt run` to initialize the production tables.
