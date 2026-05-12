import requests
import json
from pathlib import Path

def extract_bitcoin_data(url: str, cab:dict[str, str]):
    response = requests.get(url, headers=cab)
    data = response.json()

    output_path = 'data/btc_info.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f'arquivo salvo em {output_path}')
    return data
    