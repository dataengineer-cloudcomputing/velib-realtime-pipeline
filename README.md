# 🚲 Vélib Real-Time Monitoring Pipeline

Ce projet déploie une **Modern Data Stack** complète pour surveiller en temps réel la disponibilité des vélos en libre-service dans la métropole parisienne.

---

## 🇫🇷 Version Française

### 📋 Présentation
L'objectif est de démontrer un flux de données industriel (End-to-End) : de l'extraction d'une API publique jusqu'à la visualisation géographique, en passant par un entrepôt de données cloud.

### 🏗️ Architecture
- **Orchestration** : Airflow (via Astro CLI) pour piloter le flux.
- **Ingestion** : Script Python extrayant ~1450 stations de l'API Open Data Paris.
- **Stockage** : Google BigQuery (Data Warehouse).
- **Transformation** : dbt (Data Build Tool) pour le nettoyage et le typage géospatial.
- **Visualisation** : Looker Studio pour le dashboard cartographique.

### 🚀 Guide de démarrage rapide
1. **Cloner le projet** : `git clone <URL_DU_DEPOT>`
2. **Configuration** : Placez votre fichier `google_key.json` (clé de compte de service GCP) à la racine du projet.
3. **Lancement** : Exécutez `astro dev start` dans votre terminal.
4. **Utilisation** : Accédez à Airflow (`localhost:8080`) et activez le DAG. Les données seront automatiquement traitées et envoyées vers BigQuery.

---

### 🔗 [Link to the map Looker Studio] : https://lookerstudio.google.com/u/0/reporting/922fff75-3148-492c-bdfc-cb90219018e2/page/ATFsF

---

## 🇬🇧 English Version

### 📋 Overview
This project demonstrates a professional End-to-End data pipeline: from public API extraction to geographic visualization, using a cloud data warehouse.

### 🏗️ Architecture
- **Orchestration**: Airflow (via Astro CLI) to manage the workflow.
- **Ingestion**: Python script extracting ~1450 stations from the Paris Open Data API.
- **Storage**: Google BigQuery (Data Warehouse).
- **Transformation**: dbt (Data Build Tool) for cleaning and geospatial typing.
- **Visualization**: Looker Studio for the mapping dashboard.

### 🚀 Quick Start Guide
1. **Clone the project**: `git clone <URL_DU_REPO>`
2. **Setup**: Place your `google_key.json` (GCP Service Account key) in the project root.
3. **Start**: Run `astro dev start` in your terminal.
4. **Run**: Access Airflow (`localhost:8080`) and trigger the DAG. Data will be automatically processed and loaded into BigQuery.

---

## 💡 Use Case: Energy & Smart Grids (Enedis)
Cette architecture est directement adaptable à la supervision de réseaux électriques :
- **Monitoring** : Remplacer les vélos par la charge des transformateurs ou bornes IRVE.
- **Maintenance** : Visualisation en temps réel des zones de tension ou des pannes.
- **Scalabilité** : Capacité à gérer des milliers de points de mesure géolocalisés.

  
