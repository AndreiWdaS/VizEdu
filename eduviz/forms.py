from django import forms

YEARS = [(year, year) for year in range(2014, 2022)]
STATES = [
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
]
PARAMETERS = [
    ('in_energia_inexistente', 'Energia Inexistente'),
    ('in_laboratorio_informatica', 'Laboratório de Informática'),
    ('in_computador', 'Computador'),
    ('in_equip_multimidia', 'Equipamento Multimídia'),
    ('in_desktop_aluno', 'Desktop para Aluno'),
    ('in_comp_portatil_aluno', 'Computador Portátil para Aluno'),
    ('in_tablet_aluno', 'Tablet para Aluno'),
    ('in_internet', 'Internet'),
    ('in_internet_alunos', 'Internet para Alunos'),
    ('in_internet_administrativo', 'Internet Administrativa'),
    ('in_internet_aprendizagem', 'Internet para Aprendizagem'),
    ('in_acesso_internet_computador', 'Acesso à Internet via Computador'),
    ('in_aces_internet_disp_pessoais', 'Acesso à Internet via Dispositivos Pessoais')
]

class DataForm(forms.Form):
    start_year = forms.ChoiceField(
        choices=YEARS,
        label='Ano Inicial',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    end_year = forms.ChoiceField(
        choices=YEARS,
        label='Ano Final',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    states = forms.MultipleChoiceField(
        choices=STATES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Estados'
    )
    parameter = forms.ChoiceField(
        choices=PARAMETERS,
        label='Parâmetro',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class BarChartForm(forms.Form):
    year = forms.ChoiceField(
        choices=YEARS,
        label='Ano',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    states = forms.MultipleChoiceField(
        choices=STATES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Estados'
    )
    parameter = forms.ChoiceField(
        choices=PARAMETERS,
        label='Parâmetro',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ScatterPlotForm(forms.Form):
    year = forms.ChoiceField(
        choices=YEARS,
        label='Ano',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    states = forms.MultipleChoiceField(
        choices=STATES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Estados'
    )
    parameter_x = forms.ChoiceField(
        choices=PARAMETERS,
        label='Parâmetro X',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    parameter_y = forms.ChoiceField(
        choices=PARAMETERS,
        label='Parâmetro Y',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ChoroplethMapForm(forms.Form):
    year = forms.ChoiceField(
        choices=YEARS,
        label='Ano',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    parameter = forms.ChoiceField(
        choices=PARAMETERS,
        label='Parâmetro',
        widget=forms.Select(attrs={'class': 'form-control'})
    )