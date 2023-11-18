import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
from urllib.parse import quote
import dash_bootstrap_components as dbc

# Carregar o conjunto de dados
url = 'dados_credito_ficticios.csv'
df = pd.read_csv(url)

# Inicializar o aplicativo Dash com o estilo Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do aplicativo
app.layout = dbc.Container(
    [
        html.H1("Visualização Interativa de Dados - Conjunto de Dados de Crédito"),

        # Dropdown para seleção da variável
        dcc.Dropdown(
            id='dropdown-variavel',
            options=[
                {'label': coluna, 'value': coluna} for coluna in df.columns
            ],
            value='salario_anual',  # Valor padrão
            style={'width': '50%'}
        ),

        # Dropdown para seleção da gráfico
        dcc.Dropdown(
            id='dropdown-tipo-grafico',
            options=[
                {'label': 'Gráfico de Dispersão', 'value': 'scatter'},
                {'label': 'Gráfico de Barras', 'value': 'bar'},
                {'label': 'Gráfico de Linhas', 'value': 'line'},
            ],
            value='line',  # Valor padrão
            style={'width': '50%'}
        ),

        # Gráfico de dispersão interativo
        dcc.Graph(
            id='grafico-dinamico',
            config={'displayModeBar': False},
        ),

        # Botão de exportação estilizado com Dash Bootstrap Components
        dbc.Button(
            'Exportar Dados',
            id='exportar-dados',
            color='success',
            className='mt-3'
        ),
    ],
    fluid=True,
)

# Callback para atualizar o gráfico com base na variável selecionada
@app.callback(
    Output('grafico-dinamico', 'figure'),
    [Input('dropdown-variavel', 'value'),Input('dropdown-tipo-grafico','value')]

)
def atualizar_grafico(variavel_selecionada, tipo_grafico):
    if tipo_grafico == 'scatter':
        figura = px.scatter(df, x='id', y=variavel_selecionada)
    elif tipo_grafico == 'bar':
        figura = px.bar(df, x='id', y=variavel_selecionada)
    elif tipo_grafico == 'line':
        figura = px.line(df, x='id', y=variavel_selecionada)
    else:
        figura = px.scatter(df, x='id', y=variavel_selecionada)

    figura.update_layout(
        title=f'{tipo_grafico.capitalize()}- {variavel_selecionada}',
        xaxis_title='id',
        yaxis_title=variavel_selecionada
    )
    return figura

# Callback para exportar dados quando o botão é clicado
@app.callback(
    Output('exportar-dados', 'href'),
    [Input('dropdown-variavel', 'value')],
    prevent_initial_call=True
)
def exportar_dados(variavel_selecionada):
    csv_string = df.to_csv(index=False, encoding='utf-8', sep=';')
    csv_string = "data:text/csv;charset=utf-8," + quote(csv_string)
    return csv_string

# Executar o aplicativo Dash
if __name__ == '__main__':
    app.run_server(debug=True)
