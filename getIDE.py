import requests

def fetch_data(parameter, estado, ano):
    base_url = "https://mutt-correct-mongoose.ngrok-free.app/data"
    params = {
        "parameter": parameter,
        "estado": estado,
        "ano": ano
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()  # Supondo que a API retorne dados em formato JSON
    else:
        print(f"Erro ao acessar a API: {response.status_code}")
        return None


# Exemplo de uso
parameter = "in_computador"
estado = "SC"
ano = 2021

data = fetch_data(parameter, estado, ano)
if data:
    print(data)