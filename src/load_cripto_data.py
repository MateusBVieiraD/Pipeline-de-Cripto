import os
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / '.config' / '.env'
load_dotenv(env_path)

user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')
# host = 'host.docker.internal'
host = 'localhost'

def get_engine() -> create_engine:
    print(f"Conectando no Database: {database} porta 5432")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}/{database}"
    )

engine = get_engine()

def load_cripto(df: pd.DataFrame, table_name: str):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )

    print("Dados carregados!")

    df_check = pd.read_sql(f"SELECT * FROM {table_name};", con=engine)
    print(f"Total de registros: {len(df_check)}")

