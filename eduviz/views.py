from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import plotly.express as px
import pandas as pd
from django.shortcuts import render
from .forms import DataForm
from .forms import BarChartForm
from .forms import ScatterPlotForm
from .forms import ChoroplethMapForm

api_url = 'https://mutt-correct-mongoose.ngrok-free.app/data'

PARAMETER_NAMES = {
    'in_energia_inexistente': 'Energia Inexistente',
    'in_laboratorio_informatica': 'Laboratório de Informática',
    'in_computador': 'Computador',
    'in_equip_multimidia': 'Equipamento Multimídia',
    'in_desktop_aluno': 'Desktop para Aluno',
    'in_comp_portatil_aluno': 'Computador Portátil para Aluno',
    'in_tablet_aluno': 'Tablet para Aluno',
    'in_internet': 'Internet',
    'in_internet_alunos': 'Internet para Alunos',
    'in_internet_administrativo': 'Internet Administrativa',
    'in_internet_aprendizagem': 'Internet para Aprendizagem',
    'in_acesso_internet_computador': 'Acesso à Internet via Computador',
    'in_aces_internet_disp_pessoais': 'Acesso à Internet via Dispositivos Pessoais'
}

def get_data_from_api(parameter, estados, anos):
    data = []
    for estado in estados:
        params = {
            'parameter': parameter,
            'estado': estado,
            'ano': anos
        }
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            api_data = response.json()
            for ano, estados_data in api_data[parameter].items():
                for estado_data in estados_data:
                    estado = estado_data['estado']
                    valor = estado_data['count_not_equals_zero']
                    total = estado_data['total_count']
                    data.append([estado, int(ano), parameter, valor, total])
        else:
            print(f"Erro ao obter dados da API: {response.status_code}")
    return data

def choropleth_map(request):
    if request.method == 'POST':
        form = ChoroplethMapForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            parameter = form.cleaned_data['parameter']

            data = get_data_from_api(parameter, 'SC',[year])

            if data:
                df = pd.DataFrame(data, columns=['Estado', 'Ano', 'Parâmetro', PARAMETER_NAMES[parameter], 'Total'])
                df[PARAMETER_NAMES[parameter]] = pd.to_numeric(df[PARAMETER_NAMES[parameter]], errors='coerce')

                fig = px.choropleth(df, locations='Estado', locationmode='ISO-3', color=PARAMETER_NAMES[parameter], 
                                    hover_name='Estado', title=f'{PARAMETER_NAMES[parameter]} em {year}', 
                                    color_continuous_scale='Viridis')
                graph_html = fig.to_html(full_html=False)
            else:
                graph_html = '<p>Erro ao obter dados da API.</p>'
            
            return render(request, 'graph.html', {'form': form, 'graph_html': graph_html})
    else:
        form = ChoroplethMapForm()

    return render(request, 'graph.html', {'form': form})

def scatter_chart(request):
    if request.method == 'POST':
        form = ScatterPlotForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            states = form.cleaned_data['states']
            parameter_x = form.cleaned_data['parameter_x']
            parameter_y = form.cleaned_data['parameter_y']

            data_x = get_data_from_api(parameter_x, states, [year])
            data_y = get_data_from_api(parameter_y, states, [year])

            if data_x and data_y:
                df_x = pd.DataFrame(data_x, columns=['Estado', 'Ano', 'Parâmetro', PARAMETER_NAMES[parameter_x], 'Total'])
                df_y = pd.DataFrame(data_y, columns=['Estado', 'Ano', 'Parâmetro', PARAMETER_NAMES[parameter_y], 'Total'])

                df_x[PARAMETER_NAMES[parameter_x]] = pd.to_numeric(df_x[PARAMETER_NAMES[parameter_x]], errors='coerce')
                df_y[PARAMETER_NAMES[parameter_y]] = pd.to_numeric(df_y[PARAMETER_NAMES[parameter_y]], errors='coerce')

                df = pd.merge(df_x[['Estado', PARAMETER_NAMES[parameter_x]]], df_y[['Estado', PARAMETER_NAMES[parameter_y]]], on='Estado')

                fig = px.scatter(df, x=PARAMETER_NAMES[parameter_x], y=PARAMETER_NAMES[parameter_y], color='Estado', title=f'Relação entre {PARAMETER_NAMES[parameter_x]} e {PARAMETER_NAMES[parameter_y]} em {year}')
                graph_html = fig.to_html(full_html=False)
            else:
                graph_html = '<p>Erro ao obter dados da API.</p>'
            
            return render(request, 'scatter_chart.html', {'form': form, 'graph_html': graph_html})
    else:
        form = ScatterPlotForm()

    return render(request, 'scatter_chart.html', {'form': form})

def line_chart(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            start_year = form.cleaned_data['start_year']
            end_year = form.cleaned_data['end_year']
            states = form.cleaned_data['states']
            parameter = form.cleaned_data['parameter']

            years = list(range(int(start_year), int(end_year) + 1))
            data = get_data_from_api(parameter, states, years)

            if data:
                df = pd.DataFrame(data, columns=['Estado', 'Ano', 'Parâmetro', 'Valor', 'Total'])
                df[PARAMETER_NAMES[parameter]] = pd.to_numeric(df['Valor'], errors='coerce')
                fig = px.line(df, x='Ano', y=PARAMETER_NAMES[parameter], color='Estado', title=f'Número de escolas com {PARAMETER_NAMES[parameter]}')
                graph_html = fig.to_html(full_html=False)
            else:
                graph_html = '<p>Erro ao obter dados da API.</p>'
            
            return render(request, 'line_chart.html', {'form': form, 'graph_html': graph_html})
    else:
        form = DataForm()

    return render(request, 'line_chart.html', {'form': form})

def bar_chart(request):
    if request.method == 'POST':
        form = BarChartForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            states = form.cleaned_data['states']
            parameter = form.cleaned_data['parameter']

            data = get_data_from_api(parameter, states, [year])

            if data:
                df = pd.DataFrame(data, columns=['Estado', 'Ano', 'Parâmetro', f'Escolas com {PARAMETER_NAMES[parameter]}', 'Total'])
                df[f'Escolas com {PARAMETER_NAMES[parameter]}'] = pd.to_numeric(df[f'Escolas com {PARAMETER_NAMES[parameter]}'], errors='coerce')
                df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
                df[f'Escolas sem {PARAMETER_NAMES[parameter]}'] = df['Total'] - df[f'Escolas com {PARAMETER_NAMES[parameter]}']

                # Cria um DataFrame separado para o gráfico
                df_melted = df.melt(id_vars=['Estado'], value_vars=[f'Escolas com {PARAMETER_NAMES[parameter]}', f'Escolas sem {PARAMETER_NAMES[parameter]}'], var_name='Tipo', value_name='Quantidade')

                fig = px.bar(df_melted, x='Estado', y='Quantidade', color='Tipo', barmode='stack', title=f'Dados de {PARAMETER_NAMES[parameter]} em {year}')
                graph_html = fig.to_html(full_html=False)
            else:
                graph_html = '<p>Erro ao obter dados da API.</p>'
            
            return render(request, 'bar_chart.html', {'form': form, 'graph_html': graph_html})
    else:
        form = BarChartForm()

    return render(request, 'bar_chart.html', {'form': form})

# Create your views here.
def index(request):
    return render(request, 'index.html')

def pagina_brasil(request):
    return render(request, 'brasil.html')

def pagina_charts(request):
    return render(request, 'charts.html')

def pagina_historico(request):
    return render(request, 'Historico')

def pagina_login(request):
    return render(request,'Login.html')

def pagina_perfil(request):
    return render(request, '.html')
def teste(request):
    return render(request, 'teste.html')
def termos(request):
    return render(request, 'termos.html')

def quemsomos(request):
    return render(request, 'quemsomos.html')

def censo(request):
    return render(request, 'censo.html')