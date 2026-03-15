from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.operators.bash import BashOperator
from datetime import datetime
import requests
import pandas as pd
import os

# Configuration - VERIFIE BIEN CET ID
PROJECT_ID = "velib-pipeline-project" 
DATASET_ID = "velib_raw"
TABLE_ID = "stations_status"

def extract_and_load():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/usr/local/airflow/google_key.json"

    # Nouvelle URL pour TOUT avoir (Courbevoie inclus)
    url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json"
    response = requests.get(url)
    data = response.json()
    
    # CORRECTIF ICI : 
    # Si c'est une liste (cas du /export), on l'utilise direct. 
    # Sinon (cas du /records), on cherche 'results'.
    if isinstance(data, list):
        records = data
    else:
        records = data.get('results', [])
    
    df = pd.DataFrame(records)
    
    # On extrait lat/lon
    if 'coordonnees_geo' in df.columns:
        df['lat'] = df['coordonnees_geo'].apply(lambda x: x.get('lat') if isinstance(x, dict) else None)
        df['lon'] = df['coordonnees_geo'].apply(lambda x: x.get('lon') if isinstance(x, dict) else None)
    
    cols_to_keep = ['stationcode', 'name', 'numbikesavailable', 'numdocksavailable', 'lat', 'lon']
    df = df[[c for c in cols_to_keep if c in df.columns]].copy()
    
    df['extraction_date'] = datetime.now().isoformat()
    df = df.astype(str)

    from google.cloud import bigquery
    client = bigquery.Client()
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result() 
    print(f"Chargement réussi : {len(df)} lignes envoyées.")

with DAG(
    dag_id='velib_to_bigquery',
    start_date=datetime(2026, 3, 14),
    schedule='@hourly',
    catchup=False
) as dag:

    task_extract_load = PythonOperator(
        task_id='extract_and_load_velib',
        python_callable=extract_and_load
    )


    # Tâche pour lancer la transformation dbt
    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command=(
            'cd /usr/local/airflow/include/velib_transform && '
            'dbt run --profiles-dir .'
        )
    )
    

    # Définition de l'ordre (le flux)
    task_extract_load >> run_dbt