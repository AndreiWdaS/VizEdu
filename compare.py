import requests
import plotly.express as px
import pandas as pd
import json

# Configurações da API
api_url = 'https://mutt-correct-mongoose.ngrok-free.app/data'
parameters = ['in_computador']
estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
           'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
anos = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]


# Função para obter dados da API
def get_data_from_api(parameters, estados, anos):
    data = []
    for parameter in parameters:
        params = {
            'parameter': parameter,
            'estado': estados,
            'ano': anos
        }
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            api_data = response.json()
            for ano, estados_data in api_data[parameter].items():
                for estado_data in estados_data:
                    estado = estado_data['estado']
                    valor = estado_data['count_not_equals_zero']
                    data.append([estado, int(ano), parameter, valor])
        else:
            print(f"Erro ao obter dados da API: {response.status_code}")
            return None
    return data


def get_data_from_json(file_path, parameters, estados, anos):
    data = []

    # Carregar os dados do arquivo JSON
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    # Iterar sobre os parâmetros
    for parameter in parameters:
        if parameter in json_data:
            for ano, estados_data in json_data[parameter].items():
                if int(ano) in anos:  # Verifica se o ano está na lista de anos fornecida
                    for estado_data in estados_data:
                        estado = estado_data['estado']
                        if estado in estados:  # Verifica se o estado está na lista de estados fornecida
                            valor = estado_data['count_not_equals_zero']
                            data.append([estado, int(ano), parameter, valor])
        else:
            print(f"Parâmetro {parameter} não encontrado no JSON")
            return None

    return data


# data = get_data_from_api(parameters, estados, anos)
data = get_data_from_json(parameters, estados, anos)
if data is None:
    print("Erro ao obter dados da API.")
else:
    # Criar DataFrame com os dados obtidos
    df = pd.DataFrame(data, columns=['Estado', 'Ano', 'Parâmetro'])

    # Criar o gráfico de linha interativo com dropdown
    fig = px.line(df, x='Ano', y='Valor', color='Estado', title='Evolução dos Dados por Estado (2014-2021)',
                  labels={'Parâmetro': 'Parâmetro', 'Ano': 'Ano'})

    # Adicionar dropdown para selecionar o estado
    estado_buttons = []
    for estado in estados:
        visible = [estado == val for val in df['Estado']]
        estado_buttons.append(dict(
            label=estado,
            method='update',
            args=[{'visible': visible}]
        ))

    # Adicionar dropdown para selecionar o valor
    valores_unicos = df['Parâmetro'].unique()
    valor_buttons = ['in_computador']

    fig.update_layout(
        updatemenus=[
            {
                'buttons': estado_buttons,
                'direction': 'down',
                'showactive': True,
                'x': 0.17,
                'xanchor': 'left',
                'y': 1.15,
                'yanchor': 'top',
                'pad': {'r': 10, 't': 10}
            },
            {
                'buttons': valor_buttons,
                'direction': 'down',
                'showactive': True,
                'x': 0.37,
                'xanchor': 'left',
                'y': 1.15,
                'yanchor': 'top',
                'pad': {'r': 10, 't': 10}
            }
        ]
    )

    html_path = 'eduviz/templates/teste2.html'
    fig.write_html(html_path)
    print(f"Gráfico salvo em {html_path}")