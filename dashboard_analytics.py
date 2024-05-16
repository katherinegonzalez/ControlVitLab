from dash import html
from dash import Dash, html, dash_table, dcc
from bd_conf import conn
import pandas as pd
import pymysql
from dash_bootstrap_components import Row, Col, Button, Card, CardBody, Container
from joblib import load
import joblib

import numpy as np

import sklearn
print('sklearn------>', sklearn.__version__)

print('JOBLIB------>', joblib.__version__)

df_empty = pd.DataFrame()

# Cargar modelos entrenados
kmeans = joblib.load('modelosClasificacion/modelo_frecuencia_cardiaca.pkl')
df_clasificado = pd.read_csv('modeloClustering/datos_clasificados.csv')

cluster_0 = df_clasificado.loc[df_clasificado['Clusters']==0]
cluster_1 = df_clasificado.loc[df_clasificado['Clusters']==1]
cluster_2 = df_clasificado.loc[df_clasificado['Clusters']==2]
cluster_3 = df_clasificado.loc[df_clasificado['Clusters']==3]

cluster_0['riesgo'] = np.where( (cluster_0['n_frec'] == 'alto') | (cluster_0['n_sis'] == 'alto') | (cluster_0['n_dis'] == 'alto'), 'Alto',
                      np.where( (cluster_0['n_frec'] == 'medio') | (cluster_0['n_sis'] == 'medio') | (cluster_0['n_dis'] == 'medio'), 'Medio',
                      'Normal') )

cluster_1['riesgo'] = np.where( (cluster_1['n_frec'] == 'alto') | (cluster_1['n_sis'] == 'alto') | (cluster_1['n_dis'] == 'alto'), 'Alto',
                      np.where( (cluster_1['n_frec'] == 'medio') | (cluster_1['n_sis'] == 'medio') | (cluster_1['n_dis'] == 'medio'), 'Medio',
                      'Normal') )

cluster_2['riesgo'] = np.where( (cluster_2['n_frec'] == 'alto') | (cluster_2['n_sis'] == 'alto') | (cluster_2['n_dis'] == 'alto'), 'Alto',
                      np.where( (cluster_2['n_frec'] == 'medio') | (cluster_2['n_sis'] == 'medio') | (cluster_2['n_dis'] == 'medio'), 'Medio',
                      'Normal') )

cluster_3['riesgo'] = np.where( (cluster_3['n_frec'] == 'alto') | (cluster_3['n_sis'] == 'alto') | (cluster_3['n_dis'] == 'alto'), 'Alto',
                      np.where( (cluster_3['n_frec'] == 'medio') | (cluster_3['n_sis'] == 'medio') | (cluster_3['n_dis'] == 'medio'), 'Medio',
                      'Normal') )

riesgo_cluster_0 = round(cluster_0['riesgo'].value_counts()/len(cluster_0)*100, 2)
riesgo_cluster_1 = round(cluster_1['riesgo'].value_counts()/len(cluster_1)*100, 2)
riesgo_cluster_2 = round(cluster_2['riesgo'].value_counts()/len(cluster_2)*100, 2)
riesgo_cluster_3 = round(cluster_3['riesgo'].value_counts()/len(cluster_3)*100, 2)



data_riesgo_cluster = [
    {
        "Grupo de Pacientes": "Grupo 1",
        "Porcentaje Total de Riesgo Alto (%)": riesgo_cluster_0.get('Alto', 0),
        "Porcentaje Total de Riesgo Medio (%)": riesgo_cluster_0.get('Medio', 0),
        "Porcentaje Total de Valores Sin Riesgo (%)": riesgo_cluster_0.get('Normal', 0)
    },
    {
        "Grupo de Pacientes": "Grupo 2",
        "Porcentaje Total de Riesgo Alto (%)": riesgo_cluster_1.get('Alto', 0),
        "Porcentaje Total de Riesgo Medio (%)": riesgo_cluster_1.get('Medio', 0),
        "Porcentaje Total de Valores Sin Riesgo (%)": riesgo_cluster_1.get('Normal', 0)
    },
    {
        "Grupo de Pacientes": "Grupo 3",
        "Porcentaje Total de Riesgo Alto (%)": riesgo_cluster_2.get('Alto', 0),
        "Porcentaje Total de Riesgo Medio (%)": riesgo_cluster_2.get('Medio', 0),
        "Porcentaje Total de Valores Sin Riesgo (%)": riesgo_cluster_2.get('Normal', 0)
    },
    {
        "Grupo de Pacientes": "Grupo 4",
        "Porcentaje Total de Riesgo Alto (%)": riesgo_cluster_3.get('Alto', 0),
        "Porcentaje Total de Riesgo Medio (%)": riesgo_cluster_3.get('Medio', 0),
        "Porcentaje Total de Valores Sin Riesgo (%)": riesgo_cluster_3.get('Normal', 0)
    }
]

alert_colors =  {
    'normal': '#81c784',
    'alto': '#ff00008c',
    'medio': '#ffa50085',
    'no_data': '#b5b5b5'
}

# Define los colores y su significado
color_info = [
    {'color': alert_colors['alto'], 'text': 'Riesgo Alto'},
    {'color': alert_colors['medio'], 'text': 'Riesgo Medio'},
    {'color': alert_colors['normal'], 'text': 'Sin riesgo'}
]

def cell_color(grupo):
    return {
        'if': {
            'filter_query': '{Grupo de Pacientes} = "'+grupo+'"',
            'column_id': 'Grupo de Pacientes'
        },
        'backgroundColor': '#0d6efd99',
        'color': 'black',
        'fontWeight': '600'
    }

def row_color(grupo, risk_grade):
    return {
        'if': {
            'filter_query': '{Grupo de Pacientes} = "'+grupo+'"'
        },
        'backgroundColor': alert_colors[risk_grade],
        'column_id': ['Porcentaje de Riesgo Alto', 'Porcentaje de Riesgo Medio', 'Porcentaje de Valores Sin Riesgo']
    }

data_conditional = [
    row_color('Grupo 1', 'medio'),
    cell_color('Grupo 1'),
    row_color('Grupo 2', 'normal'),
    cell_color('Grupo 2'),
    row_color('Grupo 3', 'alto'),
    cell_color('Grupo 3'),
    row_color('Grupo 4', 'medio'),
    cell_color('Grupo 4')
]

def layout_table(data, data_conditional):
    return Row(
        Col([
            dcc.Loading(
                id="loading-1",
                type="default",
                children=[
                    dash_table.DataTable(
                        id='datatable',
                        data=data,
                        page_size=20,
                        style_header={
                            'textAlign': 'center',  # Alinear texto a la izquierda
                            'backgroundColor': '#0d6efd99',  # Fondo de la cabecera
                            'fontFamily': 'Arial, sans-serif',
                            'fontWeight': '600',
                            'paddingLeft': '15px',  # Padding izquierdo
                            'paddingRight': '15px',  # Padding derecho
                        },
                        style_header_conditional=[  # Estilo condicional para el encabezado
                            {
                                'if': {'column_editable': False},  # Solo aplicar a las columnas no editables
                                'backgroundColor': '#0d6efd99',  # Color de fondo del encabezado
                                'color': 'black',  # Color del texto del encabezado
                                'height': 'auto',  # Alto automático para el encabezado
                            }
                        ],
                        style_cell={
                            'textAlign': 'center',
                            'minWidth': '50px',  # Ancho mínimo de la celda
                            'width': '100px',  # Ancho predeterminado de la celda
                            'maxWidth': '200px',
                            'height': '100px',  # Ancho máximo de la celda
                            'whiteSpace': 'normal',  # Permitir saltos de línea
                        },
                        style_table={'overflowX': 'auto', 'width': '100%'},
                        style_data_conditional=data_conditional
                    ),
                ]
            )],width=8, style={'margin': '30px auto'} # Centrar la tabla y asignarle un ancho
        )
    )

def layout_analytics():
    return html.Div([
    html.H3('Analítica de Pacientes', style={"margin": "30px 10px"}),
    html.P('Se han clasificado 4 grupos de pacientes acuerdo a los patrones encontrados en todo sellos', style={"margin": "30px 10px"}),
    Row([
        Col([
            Row([
                Col([
                    html.Div(style={'backgroundColor': color['color'], 'height': '20px', 'width': '20px'})
                ], width=2),
                Col([
                    html.Div(color['text'])
                ], width=10),
            ]) for color in color_info
            
        ], width=4, style={'border': '1px solid black', 'padding': '20px 12px'})
    ], className="mb-3", style={"margin": "30px 10px"}),
    layout_table(data_riesgo_cluster, data_conditional)
])