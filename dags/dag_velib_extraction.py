from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.operators.bash import BashOperator
from datetime import datetime
import requests
import pandas as pd
import os

# Configuration
PROJECT_ID = "velib-pipeline-project" 
DATASET_ID = "velib_raw"
TABLE_ID = "stations_status"

def extract_and_load():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/usr/local/airflow/google_key.json"
    
    # URL v1.0 (souvent plus stable pour les gros volumes sans API Key)
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&rows=1000"
    
    print(f"🚀 Appel de l'API robuste : {url}")
    response = requests.get(url)
    data = response.json()
    
    # Extraction des champs (fields) pour la v1.0
    records = [r['fields'] for r in data.get('records', [])]
    print(f"📊 Nombre de stations récupérées : {len(records)}")
    
    if not records:
        raise ValueError("L'API v1.0 n'a toujours rien renvoyé. Problème de connexion réseau ?")

    df = pd.DataFrame(records)
    print(f"🔎 Colonnes réelles : {df.columns.tolist()}")
    
    df['extraction_date'] = datetime.now().isoformat()
    df = df.astype(str)

    from google.cloud import bigquery
    client = bigquery.Client()
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result() 
    print(f"✅ Chargement réussi vers {table_id}")

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

    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command=(
            'cd /usr/local/airflow/include/velib_transform && '
            'dbt run --profiles-dir .'
        )
    )

    task_extract_load >> run_dbt