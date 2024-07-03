import requests
import plotly.express as px
import pandas as pd

# Configurações da API
api_url = 'https://mutt-correct-mongoose.ngrok-free.app/data'  # Atualize com o URL correto da sua API
parameters = ['in_computador']  # Parâmetros que deseja consultar
estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP','SE','TO']
anos = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

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
                    valor = estado_data['total_count']  # Supondo que 'total_count' é o valor que você deseja plotar
                    data.append([estado, int(ano), parameter, valor])
        else:
            print(f"Erro ao obter dados da API: {response.status_code}")
            return None
    return data

# Obter dados da API
api_data = get_data_from_api(parameters, estados, anos)
if api_data is None:
    print("Erro ao obter dados da API.")
else:
    # Criar DataFrame com os dados obtidos
    df = pd.DataFrame(api_data, columns=['Estado', 'Ano', 'Parâmetro','Valor'])

    # Criar o gráfico de linha interativo com dropdown
    fig = px.line(df, x='Ano', y='Valor', color='Estado', title='Evolução dos Dados por Estado (2014-2021)',
                  labels={'Valor': 'Valor', 'Ano': 'Ano'})

    # Adicionar dropdown para selecionar o estado
    estado_buttons = []
    for estado in estados:
        visible = [estado == val for val in df['Estado']]
        estado_buttons.append(dict(
            label=estado,
            method='update',
            args=[{'visible': visible}]
        ))


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
            }
        ]
    )

    print(df)
    html_path = 'C:/Users/vitor/PycharmProjects/projeto/eduviz/templates/teste.html'
    fig.write_html(html_path)
    print(f"Gráfico salvo em {html_path}")