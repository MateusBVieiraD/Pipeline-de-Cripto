import pandas as pd
import json
from pathlib import Path
from decimal import Decimal

path_name = Path(__file__).parent.parent / 'data' / 'btc_info.json'

columns_to_drop = ['data', 'explorer']
columns_to_rename = {
    "timestamp": "data_hora",
    "id": "cripto_id",
    "rank": "rank",
    "symbol": "simbolo",
    "name": "nome",
    "supply": "total_de_moedas",
    "maxSupply": "total_maximo_de_moedas",
    "marketCapUsd": "captacao_do_mercado_dolar",
    "volumeUsd24Hr": "volume_de_dolares_24hrs",
    "priceUsd": "preco_dolar",
    "changePercent24Hr": "porcentagem_mudanca_24hrs",
    "vwap24Hr": "preco_medio_ponderado_24hrs",
}

# único timestamp pra fazer a normalização
norm_datetime = 'data_hora' 

columns_to_round = ["supply", "maxSupply", "marketCapUsd", "volumeUsd24Hr", "priceUsd", "changePercent24Hr", "vwap24Hr"]

def create_dataframe(path_name: str) -> pd.DataFrame:
    path = path_name

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    
    with open(path) as f:
        data = json.load(f)

    # transformação do json em um dataframe
    df = pd.json_normalize(data)

    return df

def normalize_data_column(df: pd.DataFrame) -> pd.DataFrame:
    data_df = pd.json_normalize(df['data'].apply(lambda x: x[0]))

    # como a alteração de nomeclatura das colunas será feita no futuro, mantive o nome delas
    df = pd.concat([df, data_df], axis=1)

    return df

def round_columns(df: pd.DataFrame, columns_to_convert: list[str]) -> pd.DataFrame:


    for i in range(len(df)):
        for column in columns_to_convert:
            if column == "changePercent24Hr":
                df.loc[i, column] = str(round(float(df.loc[i, column]), 2)) + '%'
            else:
                df.loc[i, column] = str(round(float(df.loc[i, column]), 2))

    
    return df



def drop_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.drop(columns=columns)
    df = df.dropna(axis=1, how='all')
    print(f"Colunas dropadas: {columns}.")


    return df

def rename_columns(df: pd.DataFrame, columns_names: dict[str,str]) -> pd.DataFrame:
    df = df.rename(columns=columns_names)

    print("Colunas renomeadas!")
    return df

def normalize_datetime(df: pd.DataFrame, column: str):
    df[column] = pd.to_numeric(df[column], errors='coerce')

    df[column] = pd.to_datetime(df[column], unit='ms', utc=True, errors='coerce').dt.tz_convert("America/Sao_Paulo")
    
    print("Datetime ajustado!")
    return df

def data_tranform() -> pd.DataFrame:
    print("Iniciando as transformações...")
    df = create_dataframe(path_name)
    df = normalize_data_column(df)
    df = round_columns(df, columns_to_round)
    df = drop_columns(df, columns_to_drop)
    df = rename_columns(df, columns_to_rename)
    df = normalize_datetime(df, norm_datetime)

    print("Transformações concluídas!")
    return df
