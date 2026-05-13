import os
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

from src.extract_cripto_data import extract_bitcoin_data
from src.transform_cripto_data import data_tranform
from src.load_cripto_data import load_cripto

env_path = Path(__file__).resolve().parent.parent / '.config' / '.env'
load_dotenv(env_path)
url = os.getenv('url_api')
api_key = os.getenv('API_KEY')
headers = {
    "Authorization": f"Bearer {api_key}"
}



def pipeline():
    try:
        extract_bitcoin_data(url, headers)
        df = data_tranform()
        load_cripto(df, 'cripto_info')

    except Exception as e:
        print(e)

pipeline()
