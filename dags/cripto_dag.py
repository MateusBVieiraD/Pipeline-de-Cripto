import sys

sys.path.insert(0, '/opt/airflow/src')

from extract_cripto_data import extract_bitcoin_data
from transform_cripto_data import data_tranform
from load_cripto_data import load_cripto

import os
from airflow.decorators import dag, task
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd


env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')
headers = {
    "Authorization": f"Bearer {API_KEY}"
}
url = os.getenv('url_api')

@dag(
    dag_id= 'Pipeline_Cripto',
    description='Pipeline ETL - Bitcoin',
    schedule='*/5 * * * *',
    start_date=datetime(2026, 5, 13),
    catchup=False,
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    }
)
def cripto_pipeline():

    @task
    def extraction():
        extract_bitcoin_data(url, headers)
    
    @task
    def transform():
       df = data_tranform()
       # transformação do df em parquet temporariamente pra carregar na task de load
       df = df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)

    @task
    def load():
        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_cripto(df, 'cripto_info')

    extraction() >> transform() >> load()

cripto_pipeline()