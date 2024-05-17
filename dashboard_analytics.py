from dash import html
from dash import Dash, html, dash_table, dcc
from bd_conf import conn
import pandas as pd
import pymysql
from dash_bootstrap_components import Row, Col, Button, Card, CardBody, Container
from joblib import load
import joblib
import plotly.express as px
import plotly.graph_objects as go

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

def addRiesgoCluster(): 
    cluster_0['riesgo'] = np.where( (cluster_0['n_frec'] == 'alto') | (cluster_0['n_sis'] == 'alto') | (cluster_0['n_dis'] == 'alto'), 'alto',
                        np.where( (cluster_0['n_frec'] == 'medio') | (cluster_0['n_sis'] == 'medio') | (cluster_0['n_dis'] == 'medio'), 'medio',
                        'normal') )

    cluster_1['riesgo'] = np.where( (cluster_1['n_frec'] == 'alto') | (cluster_1['n_sis'] == 'alto') | (cluster_1['n_dis'] == 'alto'), 'alto',
                        np.where( (cluster_1['n_frec'] == 'medio') | (cluster_1['n_sis'] == 'medio') | (cluster_1['n_dis'] == 'medio'), 'medio',
                        'normal') )

    cluster_2['riesgo'] = np.where( (cluster_2['n_frec'] == 'alto') | (cluster_2['n_sis'] == 'alto') | (cluster_2['n_dis'] == 'alto'), 'alto',
                        np.where( (cluster_2['n_frec'] == 'medio') | (cluster_2['n_sis'] == 'medio') | (cluster_2['n_dis'] == 'medio'), 'medio',
                        'normal') )

    cluster_3['riesgo'] = np.where( (cluster_3['n_frec'] == 'alto') | (cluster_3['n_sis'] == 'alto') | (cluster_3['n_dis'] == 'alto'), 'alto',
                        np.where( (cluster_3['n_frec'] == 'medio') | (cluster_3['n_sis'] == 'medio') | (cluster_3['n_dis'] == 'medio'), 'medio',
                        'normal') )
    
addRiesgoCluster()

riesgo_cluster_0 = round(cluster_0['riesgo'].value_counts()/len(cluster_0)*100, 2)
riesgo_cluster_1 = round(cluster_1['riesgo'].value_counts()/len(cluster_1)*100, 2)
riesgo_cluster_2 = round(cluster_2['riesgo'].value_counts()/len(cluster_2)*100, 2)
riesgo_cluster_3 = round(cluster_3['riesgo'].value_counts()/len(cluster_3)*100, 2)

riesgo_fc_cluster_0 = round(cluster_0['n_frec'].value_counts()/len(cluster_0)*100, 2)
riesgo_fc_cluster_1 = round(cluster_1['n_frec'].value_counts()/len(cluster_1)*100, 2)
riesgo_fc_cluster_2 = round(cluster_2['n_frec'].value_counts()/len(cluster_2)*100, 2)
riesgo_fc_cluster_3 = round(cluster_3['n_frec'].value_counts()/len(cluster_3)*100, 2)

riesgo_sis_cluster_0 = round(cluster_0['n_sis'].value_counts()/len(cluster_0)*100, 2)
riesgo_sis_cluster_1 = round(cluster_1['n_sis'].value_counts()/len(cluster_1)*100, 2)
riesgo_sis_cluster_2 = round(cluster_2['n_sis'].value_counts()/len(cluster_2)*100, 2)
riesgo_sis_cluster_3 = round(cluster_3['n_sis'].value_counts()/len(cluster_3)*100, 2)

riesgo_dis_cluster_0 = round(cluster_0['n_dis'].value_counts()/len(cluster_0)*100, 2)
riesgo_dis_cluster_1 = round(cluster_1['n_dis'].value_counts()/len(cluster_1)*100, 2)
riesgo_dis_cluster_2 = round(cluster_2['n_dis'].value_counts()/len(cluster_2)*100, 2)
riesgo_dis_cluster_3 = round(cluster_3['n_dis'].value_counts()/len(cluster_3)*100, 2)

def data_row_riesgo_cluster(grupo, riesgo_cluster, tipo_porcentaje):
    return {
        "Grupo de Pacientes": grupo,
        tipo_porcentaje+" de Riesgo Alto (%)": riesgo_cluster.get('alto', 0),
        tipo_porcentaje+" de Riesgo Medio (%)": riesgo_cluster.get('medio', 0),
        tipo_porcentaje+" de Valores Sin Riesgo (%)": riesgo_cluster.get('normal', 0)
    }

data_riesgo_cluster = [
    data_row_riesgo_cluster('Grupo 1', riesgo_cluster_0, 'Porcentaje Total'),
    data_row_riesgo_cluster('Grupo 2', riesgo_cluster_1, 'Porcentaje Total'),
    data_row_riesgo_cluster('Grupo 3', riesgo_cluster_2, 'Porcentaje Total'),
    data_row_riesgo_cluster('Grupo 4', riesgo_cluster_3, 'Porcentaje Total')
]

data_riesgo_fc_cluster = [
    data_row_riesgo_cluster('Grupo 1', riesgo_fc_cluster_0, 'Frecuencia Cardiaca'),
    data_row_riesgo_cluster('Grupo 2', riesgo_fc_cluster_1, 'Frecuencia Cardiaca'),
    data_row_riesgo_cluster('Grupo 3', riesgo_fc_cluster_2, 'Frecuencia Cardiaca'),
    data_row_riesgo_cluster('Grupo 4', riesgo_fc_cluster_3, 'Frecuencia Cardiaca')
]

data_riesgo_sis_cluster = [
    data_row_riesgo_cluster('Grupo 1', riesgo_sis_cluster_0, 'Presión Sistólica'),
    data_row_riesgo_cluster('Grupo 2', riesgo_sis_cluster_1, 'Presión Sistólica'),
    data_row_riesgo_cluster('Grupo 3', riesgo_sis_cluster_2, 'Presión Sistólica'),
    data_row_riesgo_cluster('Grupo 4', riesgo_sis_cluster_3, 'Presión Sistólica')
]

data_riesgo_dis_cluster = [
    data_row_riesgo_cluster('Grupo 1', riesgo_dis_cluster_0, 'Presión Diastólica'),
    data_row_riesgo_cluster('Grupo 2', riesgo_dis_cluster_1, 'Presión Diastólica'),
    data_row_riesgo_cluster('Grupo 3', riesgo_dis_cluster_2, 'Presión Diastólica'),
    data_row_riesgo_cluster('Grupo 4', riesgo_dis_cluster_3, 'Presión Diastólica')
]

# Define los rangos de edades
rangos_edades = [(20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90)]
# Agrupa los datos por los rangos de edades
def conteo_por_rango_edades(cluster_seleccionado):
    conteo_por_rango = []
    for rango in rangos_edades:
        conteo_por_rango.append(((cluster_seleccionado['Edad'] >= rango[0]) & (cluster_seleccionado['Edad'] < rango[1])).sum())
    return conteo_por_rango

max_value_age_custer_0 = max(conteo_por_rango_edades(cluster_0))
max_index_age_custer_0 = conteo_por_rango_edades(cluster_0).index(max_value_age_custer_0)
rangos_edades_cluster_0 = rangos_edades[max_index_age_custer_0]

max_value_age_custer_1 = max(conteo_por_rango_edades(cluster_1))
max_index_age_custer_1 = conteo_por_rango_edades(cluster_1).index(max_value_age_custer_1)
rangos_edades_cluster_1 = rangos_edades[max_index_age_custer_1]

max_value_age_custer_2 = max(conteo_por_rango_edades(cluster_2))
max_index_age_custer_2 = conteo_por_rango_edades(cluster_2).index(max_value_age_custer_2)
rangos_edades_cluster_2 = rangos_edades[max_index_age_custer_2]

max_value_age_custer_3 = max(conteo_por_rango_edades(cluster_3))
max_index_age_custer_3 = conteo_por_rango_edades(cluster_3).index(max_value_age_custer_3)
rangos_edades_cluster_3 = rangos_edades[max_index_age_custer_3]

def rangos_edades_string(rango):
    if rango == (20, 30):
        return '20-30'
    elif rango == (30, 40):
        return '30-40'
    elif rango == (40, 50):
        return '40-50'
    elif rango == (50, 60):
        return '50-60'
    elif rango == (60, 70):
        return '60-70'
    elif rango == (70, 80):
        return '70-80'
    elif rango == (80, 90):
        return '80-90'
    else:
        return '0'

def data_row_caracteristica_cluster(grupo, edades, genero, estado_civil, imc):
    return {
        "Grupo de Pacientes": grupo,
        "Rango de edades de la Mayoría de pacientes": edades,
        "Género de la Mayoría de pacientes": genero,
        "Estado Civil de la Mayoría de pacientes": estado_civil,
        "Categría de IMC de la Mayoría de pacientes": imc
    }

def genero(cluster):
    # Calcula los conteos de cada categoría de género
    conteos_genero = cluster['sexo'].value_counts()
    
    # Encuentra el nombre de la variable con el máximo conteo
    genero_mas_comun = conteos_genero.idxmax()

    if genero_mas_comun == 'F':
        genero_mas_comun = 'Femenino'
    elif genero_mas_comun == 'M':
        genero_mas_comun = 'Masculino'
    
    return genero_mas_comun
    

def estado_civil(cluster):
    # Calcula los conteos de cada categoría de género
    conteos_estado_civil = cluster['estado_civil'].value_counts()

    # Encuentra el nombre de la variable con el máximo conteo
    estado_civil_mas_comun = conteos_estado_civil.idxmax()

    if estado_civil_mas_comun == 'M':
        estado_civil_mas_comun = 'Casados'
    elif estado_civil_mas_comun == 'S':
        estado_civil_mas_comun = 'Solteros'
    elif estado_civil_mas_comun == 'W':
        estado_civil_mas_comun = 'Viudos'
    elif estado_civil_mas_comun == 'D':
        estado_civil_mas_comun = 'Divorciados'

    return estado_civil_mas_comun  


genero_cluster_1 = max(cluster_1['sexo'].value_counts())
genero_cluster_2 = max(cluster_2['sexo'].value_counts())
genero_cluster_3 = max(cluster_3['sexo'].value_counts())

estado_civil_cluster_0 = max(cluster_0['estado_civil'].value_counts())
estado_civil_cluster_1 = max(cluster_1['estado_civil'].value_counts())
estado_civil_cluster_2 = max(cluster_2['estado_civil'].value_counts())
estado_civil_cluster_3 = max(cluster_3['estado_civil'].value_counts())


# Categoriza los datos de IMC en las categorías deseadas

def imc(cluster):
    sobre_peso = cluster[cluster['IMC'] > 25]
    peso_normal = cluster[(cluster['IMC'] >= 18.5) & (cluster['IMC'] <= 25)]
    obesidad = cluster[cluster['IMC'] > 30]
    bajo_peso = cluster[cluster['IMC'] < 18.5]

    # Calcula el conteo de valores en cada categoría
    conteo_sobre_peso = sobre_peso['IMC'].count()
    conteo_peso_normal = peso_normal['IMC'].count()
    conteo_obesidad = obesidad['IMC'].count()
    conteo_bajo_peso = bajo_peso['IMC'].count()
    # Obtener el valor máximo
    max_value = max(conteo_sobre_peso, conteo_peso_normal, conteo_obesidad, conteo_bajo_peso)
    imc_max = ''
    # Comparar el valor máximo con cada variable para determinar cuál tiene el mayor valor
    if max_value == conteo_sobre_peso:
        imc_max = 'Sobrepeso'
    elif max_value == conteo_peso_normal:
        imc_max = 'Saludable'
    elif max_value == conteo_obesidad:
        imc_max = 'Obesidad'
    elif max_value == conteo_bajo_peso:
        imc_max = 'Bajo de Peso'

    return imc_max

data_caracteristicas_cluster = [
    data_row_caracteristica_cluster('Grupo 1', rangos_edades_string(rangos_edades_cluster_0), genero(cluster_0), estado_civil(cluster_0), imc(cluster_0)),
    data_row_caracteristica_cluster('Grupo 2', rangos_edades_string(rangos_edades_cluster_1), genero(cluster_1), estado_civil(cluster_1), imc(cluster_1)),
    data_row_caracteristica_cluster('Grupo 3', rangos_edades_string(rangos_edades_cluster_2), genero(cluster_2), estado_civil(cluster_2), imc(cluster_2)),
    data_row_caracteristica_cluster('Grupo 4', rangos_edades_string(rangos_edades_cluster_3), genero(cluster_3), estado_civil(cluster_3), imc(cluster_3))
]

alert_colors =  {
    'normal': '#81c784',
    'alto': '#ff00008c',
    'medio': '#ffa50085',
    'no_data': '#b5b5b5'
}

# Define los colores y su significado
color_info = [
    {'color': alert_colors['alto'], 'text': 'Grupo con Riesgo más Alto'},
    {'color': alert_colors['medio'], 'text': 'Grupo con Riesgo Medio'},
    {'color': alert_colors['normal'], 'text': 'Grupo con Menos Riesgo'}
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

data_conditional_riesgo_total = [
    row_color('Grupo 1', 'medio'),
    cell_color('Grupo 1'),
    row_color('Grupo 2', 'normal'),
    cell_color('Grupo 2'),
    row_color('Grupo 3', 'alto'),
    cell_color('Grupo 3'),
    row_color('Grupo 4', 'medio'),
    cell_color('Grupo 4')
]

data_conditional_riesgo_fc = [
    row_color('Grupo 1', 'medio'),
    cell_color('Grupo 1'),
    row_color('Grupo 2', 'medio'),
    cell_color('Grupo 2'),
    row_color('Grupo 3', 'medio'),
    cell_color('Grupo 3'),
    row_color('Grupo 4', 'medio'),
    cell_color('Grupo 4')
]

data_conditional_riesgo_sis = [
    row_color('Grupo 1', 'normal'),
    cell_color('Grupo 1'),
    row_color('Grupo 2', 'normal'),
    cell_color('Grupo 2'),
    row_color('Grupo 3', 'alto'),
    cell_color('Grupo 3'),
    row_color('Grupo 4', 'medio'),
    cell_color('Grupo 4')
]

data_conditional_riesgo_dis = [
    row_color('Grupo 1', 'medio'),
    cell_color('Grupo 1'),
    row_color('Grupo 2', 'normal'),
    cell_color('Grupo 2'),
    row_color('Grupo 3', 'alto'),
    cell_color('Grupo 3'),
    row_color('Grupo 4', 'normal'),
    cell_color('Grupo 4')
]

data_conditional_caracteristicas = [
    cell_color('Grupo 1'),
    cell_color('Grupo 2'),
    cell_color('Grupo 3'),
    cell_color('Grupo 4'),
]

def cell_color_table(column_id, risk_type, risk_grade):
    risk_grade_color = ('normal' if risk_grade == 'Saludable' 
        else 'medio' if risk_grade == 'Sobrepeso' 
        else 'alto' if risk_grade == 'Obesidad' 
        else str(risk_grade).lower())
    return {
        'if': {
            'column_id': column_id,
            'filter_query': '{'+risk_type+'} contains "'+risk_grade+'"'
        },
        'backgroundColor': alert_colors[risk_grade_color], 
        'color': 'black' 
    }

def cell_botton_table(column_id):
    return {
        'if': {
            'column_id': column_id
        },
        'color': 'blue',  # Color del enlace
        'textDecoration': 'underline',  # Subrayar el texto
        'cursor': 'pointer'  # Cambiar el cursor al pasar el ratón
    }

data_conditional_table = [
        cell_color_table('frecuencia_cardiaca', 'n_frec','no_data'),
        cell_color_table('frecuencia_cardiaca', 'n_frec', 'normal'),
        cell_color_table('frecuencia_cardiaca', 'n_frec', 'medio'),
        cell_color_table('frecuencia_cardiaca', 'n_frec', 'alto'),
        cell_color_table('t_a_sistolica', 'n_sis', 'normal'),
        cell_color_table('t_a_sistolica', 'n_sis', 'medio'),
        cell_color_table('t_a_sistolica', 'n_sis', 'alto'),
        cell_color_table('t_a_diastolica', 'n_dis', 'normal'),
        cell_color_table('t_a_diastolica', 'n_dis', 'medio'),
        cell_color_table('t_a_diastolica', 'n_dis', 'alto'),
        cell_color_table('riesgo', 'riesgo', 'normal'),
        cell_color_table('riesgo', 'riesgo', 'medio'),
        cell_color_table('riesgo', 'riesgo', 'alto'),
        cell_botton_table('Action')
        #cell_color('Estado de IMC', 'Estado de IMC', 'Saludable'),
        #cell_color('Estado de IMC', 'Estado de IMC', 'Sobrepeso'),
        #cell_color('Estado de IMC', 'Estado de IMC', 'Obesidad'),
        #cell_color('IMC', 'Estado de IMC', 'Saludable'),
        #cell_color('IMC', 'Estado de IMC', 'Sobrepeso'),
        #cell_color('IMC', 'Estado de IMC', 'Obesidad')
    ]


# Define las opciones del Dropdown
options = [
    {'label': 'Grupo de Pacientes 1', 'value': 0},
    {'label': 'Grupo de Pacientes 2', 'value': 1},
    {'label': 'Grupo de Pacientes 3', 'value': 2},
    {'label': 'Grupo de Pacientes 4', 'value': 3}
]


def tabla_pacientes(cluster):
    return Row(
        Col([
            dcc.Loading(
                id="loading-1",
                type="default",
                children=[
                    dash_table.DataTable(
                        id='datatable_pacientes',
                        data=cluster.to_dict('records'),
                        page_size=5,
                        columns=[
                            {'name': 'Nombre de Paciente', 'id': 'nombre'},
                            {'name': 'Identificación', 'id': 'identificacion'},
                            {'name': 'Edad', 'id': 'Edad'},
                            {'name': 'Género', 'id': 'sexo'},
                            {'name': 'Peso (kg)', 'id': 'peso'},
                            {'name': 'Talla (cm)', 'id': 'talla'},
                            {'name': 'IMC', 'id': 'IMC'},
                            {'name': 'Estado de IMC', 'id': 'Estado IMC'},  
                            {'name': 'Frecuencia Cardiaca BPM', 'id': 'frecuencia_cardiaca'},
                            {'name': 'Presión Sistólica mm[Hg]', 'id': 't_a_sistolica'},
                            {'name': 'Presión Diastólica mm[Hg]', 'id': 't_a_diastolica'},
                            {'name': 'Riesgo', 'id': 'riesgo'},
                            {'name': 'Detalle', 'id': 'Action'}],
                       
                        # style_data_conditional=data_conditional,
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
                        style_data_conditional=data_conditional_table
                    ),
                ]
            )],width=12, style={'margin': '30px 10px'} # Centrar la tabla y asignarle un ancho
        )
    )

# Función para calcular la prioridad
def calcular_prioridad(row):
    count_alto = sum(row[['n_frec', 'n_sis', 'n_dis']].str.contains('alto'))
    count_medio = sum(row[['n_frec', 'n_sis', 'n_dis']].str.contains('medio'))
    count_normal = sum(row[['n_frec', 'n_sis', 'n_dis']].str.contains('normal'))
   
    if count_alto == 3:
        return 1
    elif count_alto == 2:
        if count_medio == 1:
            return 2  # Dos "alto" y uno "medio"
        elif count_normal == 1:
            return 3  # Dos "alto" y un normal
        else:
            return 4
    elif count_alto == 1:
        if count_medio == 2:
            return 5  # Un "alto" y dos "medio"
        elif count_medio == 1:
            return 6  # Un "alto" y un "medio"
        elif count_normal == 2:
            return 7  # Un "alto" y un "medio"
        else:
            return 8  # Un "alto" y cero "medio"
    elif count_medio == 3:
        return 9
    elif count_medio == 2:
        if count_normal == 1:
            return 10  # Dos "alto" y uno "medio"
        else:
            return 11
    elif count_medio == 1:
        return 12
    else:
        return 13

def etiqueta_estado_civil(dato):
    if dato == 'M':
        return 'Casados'
    elif dato == 'S':
        return 'Solteros'
    elif dato == 'W':
        return 'Viudos'
    elif dato == 'D':
        return 'Divorciados'
    else:
        return ''

def etiqueta_genero(dato):
    if dato == 'M':
        return 'Hombres'
    elif dato == 'F':
        return 'Mujeres'
    else:
        return 'Solteros'

def update_graphs(selected_cluster):
    addRiesgoCluster()
    # Filtrar el dataframe según el cluster seleccionado
    filtered_cluster = cluster_0
    nombre_grupo = ''
    if selected_cluster == 0:
        filtered_cluster = cluster_0
        nombre_grupo = 'Grupo de Pacientes 1'
    elif selected_cluster == 1:
        filtered_cluster = cluster_1
        nombre_grupo = 'Grupo de Pacientes 2'
    elif selected_cluster == 2:
        filtered_cluster = cluster_2
        nombre_grupo = 'Grupo de Pacientes 3'
    elif selected_cluster == 3:
        filtered_cluster = cluster_3
        nombre_grupo = 'Grupo de Pacientes 4'
    
    # Calcula el conteo de riesgo
    risgo_counts = filtered_cluster['riesgo'].value_counts()
    fig_riesgo_total = go.Figure(data=[go.Pie(labels=risgo_counts.index, values=risgo_counts.values)])
    fig_riesgo_total.update_traces(marker=dict(colors=[alert_colors[risgo] for risgo in risgo_counts.index]))
    # Establece el título
    
    fig_riesgo_total.update_layout(title='<b style="color:black">Riesgo General</b>')

    # Calcula el conteo de riesgo de fc
    riesgo_fc_counts = filtered_cluster['n_frec'].value_counts()
    fig_riesgo_fc = go.Figure(data=[go.Pie(labels=riesgo_fc_counts.index, values=riesgo_fc_counts.values)])
    fig_riesgo_fc.update_traces(marker=dict(colors=[alert_colors[risgo] for risgo in riesgo_fc_counts.index]))
    # Establece el título
    fig_riesgo_fc.update_layout(title='<b style="color:black">Riesgo Frecuencia Cardiaca</b>')

    # Calcula el conteo de riesgo de sistólica
    riesgo_sis_counts = filtered_cluster['n_sis'].value_counts()
    fig_riesgo_sis = go.Figure(data=[go.Pie(labels=riesgo_sis_counts.index, values=riesgo_sis_counts.values)])
    fig_riesgo_sis.update_traces(marker=dict(colors=[alert_colors[risgo] for risgo in riesgo_sis_counts.index]))
    # Establece el título
    fig_riesgo_sis.update_layout(title='<b style="color:black">Riesgo Presión Sistólica</b>')

    # Calcula el conteo de riesgo de diastólica
    riesgo_dis_counts = filtered_cluster['n_dis'].value_counts()
    fig_riesgo_dis = go.Figure(data=[go.Pie(labels=riesgo_dis_counts.index, values=riesgo_dis_counts.values)])
    fig_riesgo_dis.update_traces(marker=dict(colors=[alert_colors[risgo] for risgo in riesgo_dis_counts.index]))
    # Establece el título
    fig_riesgo_dis.update_layout(title='<b style="color:black">Riesgo Presión Diastólica</b>')


    # Calcula el conteo de género
    genero_counts = filtered_cluster['sexo'].value_counts()
   
    dato_0_genero = genero_counts.index[0]
    dato_1_genero= genero_counts.index[1]

    etiquetas_genero = [
        etiqueta_genero(dato_0_genero), 
        etiqueta_genero(dato_1_genero)
    ]
    fig_genero = go.Figure(data=[go.Pie(labels=etiquetas_genero, values=genero_counts.values)])
    fig_genero.update_layout(title='<b style="color:black">Género</b>')

    # Calcula el conteo de estado civil
    estado_civil_counts = filtered_cluster['estado_civil'].value_counts()
    # Accede a los datos en la posición 0 y 1 del índice
    dato_0_estado_civil = estado_civil_counts.index[0]
    dato_1_estado_civil = estado_civil_counts.index[1]
    dato_2_estado_civil = estado_civil_counts.index[2]
    dato_3_estado_civil = estado_civil_counts.index[3]

    # Define las etiquetas personalizadas para el estado civil
    etiquetas_estado_civil = [
        etiqueta_estado_civil(dato_0_estado_civil), 
        etiqueta_estado_civil(dato_1_estado_civil), 
        etiqueta_estado_civil(dato_2_estado_civil), 
        etiqueta_estado_civil(dato_3_estado_civil)
    ]

    fig_estado_civil = go.Figure(data=[go.Pie(labels=etiquetas_estado_civil, values=estado_civil_counts.values)])
    fig_estado_civil.update_layout(title='<b style="color:black">Estado Civil</b>')

    sobre_peso = filtered_cluster[filtered_cluster['IMC'] > 25]
    peso_normal = filtered_cluster[(filtered_cluster['IMC'] >= 18.5) & (filtered_cluster['IMC'] <= 25)]
    obesidad = filtered_cluster[filtered_cluster['IMC'] > 30]
    bajo_peso = filtered_cluster[filtered_cluster['IMC'] < 18.5]

    # Calcula el conteo de valores en cada categoría
    conteo_sobre_peso = sobre_peso['IMC'].count()
    conteo_peso_normal = peso_normal['IMC'].count()
    conteo_obesidad = obesidad['IMC'].count()
    conteo_bajo_peso = bajo_peso['IMC'].count()

    # Define los límites de los rangos para cada estado de IMC
    rangos = [float('-inf'), 18.5, 25, 30, float('inf')]

    # Define las etiquetas correspondientes a cada estado de IMC
    etiquetas = ['Bajo peso', 'Saludable', 'Sobrepeso', 'Obesidad']

    # Agrega una nueva columna 'Estado IMC' al DataFrame con los valores correspondientes
    filtered_cluster['Estado IMC'] = np.where(filtered_cluster['IMC'] > 25, 'Sobrepeso',
                                     np.where((filtered_cluster['IMC'] >= 18.5) & (filtered_cluster['IMC'] <= 25),
                                     'Saludable',
                                     np.where(filtered_cluster['IMC'] > 30, 'Obesidad',
                                     np.where(filtered_cluster['IMC'] < 18.5, 'Bajo Peso', 'Saludable'))))


    # Define los nombres de las categorías
    categorias = ['Sobrepeso', 'Peso normal', 'Obesidad', 'Bajo peso']

    # Define los conteos de cada categoría
    conteos = [conteo_sobre_peso, conteo_peso_normal, conteo_obesidad, conteo_bajo_peso]

    # Define los colores para cada categoría
    color_map = {
        'Sobrepeso': 'orange',
        'Peso normal': 'green',
        'Obesidad': 'red',
        'Bajo peso': 'red'
    }

    # Crea un DataFrame con los nombres de las categorías y los conteos
    data = {'Categoría': categorias, 'Conteo': conteos}

    # Crea el gráfico de torta
    fig_imc = px.pie(data, names='Categoría', values='Conteo', title='<b style="color:black">Distribución de IMC</b>',
                color_discrete_map=color_map)


    # Calcula los conteos de cada rango de edades
    conteo_por_rango = conteo_por_rango_edades(filtered_cluster)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[f'{rango[0]}-{rango[1]}' for rango in rangos_edades],
        y=conteo_por_rango,
        marker_color='steelblue',  # Color de las barras
        opacity=0.8,  # Opacidad de las barras
    ))
    
    # Personaliza el diseño del gráfico
    fig.update_layout(
        title='<b style="color:black">Distribución de Edades</b>',
        xaxis_title='Rango de Edades',
        yaxis_title='Número de Pacientes',
        template='plotly_white'  # Estilo del gráfico
    )


    # REVISAR: https://community.plotly.com/t/button-inside-a-dash-table/51460
    # Modificar la columna 'Action_text' para incluir el valor de 'id_cia' como texto del botón
    filtered_cluster['Action'] = 'Ver Detalles'
   
    filtered_cluster['Prioridad'] = filtered_cluster.apply(calcular_prioridad, axis=1)

    # Ordenar por la columna de prioridad
    filtered_cluster.sort_values(by='Prioridad', inplace=True)

    # Eliminar la columna de prioridad
    filtered_cluster.drop(columns=['Prioridad'], inplace=True)

    # Devuelve los gráficos como elementos HTML
    return [
         Row([
            html.H4(nombre_grupo, style={"margin": "30px 0", "fontWeight": "800"}) 
        ]),
        dcc.Loading(
                id="loading-1",
                type="default",
                children=[
                     Row([
                        Col([
                            dcc.Graph(figure=fig_riesgo_total)
                        ]),
                        Col([
                            dcc.Graph(figure=fig_riesgo_fc),
                        ])
                    ]),
                    Row([
                        Col([
                            dcc.Graph(figure=fig_riesgo_sis)
                        ]),
                        Col([
                            dcc.Graph(figure=fig_riesgo_dis),
                        ])
                    ]),
                    Row([
                        Col([
                            dcc.Graph(figure=fig_genero)
                        ]),
                        Col([
                            dcc.Graph(figure=fig_estado_civil)
                        ])
                    ]),
                    Row([
                        Col([
                            dcc.Graph(figure=fig_imc)
                        ]),
                        Col([
                            dcc.Graph(figure=fig)
                        ])
                    ]),
                    Row([
                        html.H5('Información de Cada Paciente', style={"margin": "10px", "fontWeight": "800"}) 
                    ]),

                ]),
        tabla_pacientes(filtered_cluster)
    ]

def layout_table(data, data_conditional, id):
    return Row(
        Col([
            dcc.Loading(
                id="loading-1",
                type="default",
                children=[
                    dash_table.DataTable(
                        id=id,
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
                            'height': '50px',  # Alto máximo de la celda
                            'whiteSpace': 'normal',  # Permitir saltos de línea
                        },
                        style_table={'overflowX': 'auto', 'width': '100%'},
                        style_data_conditional=data_conditional
                    ),
                ]
            )],width=12, style={'margin': '10px auto'} # Centrar la tabla y asignarle un ancho
        )
    )

def layout_analytics():
    return html.Div([
    html.H3('Analítica de Pacientes', style={"margin": "30px"}),
    html.P('En este Dashboard se encuentran 4 grupos de pacientes que han sido clasificados de acuerdo a los patrones entre ellos', style={"margin": "30px"}),
   
    Row([
        html.H4('Riesgo en Grupos de Pacientes'),
        html.Div(id="output"),
        Col([
            layout_table(data_riesgo_cluster, data_conditional_riesgo_total, 'datatable_riesgo_total'),
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
        ]  
        ),
        Col([
            layout_table(data_riesgo_fc_cluster, data_conditional_riesgo_fc, 'datatable_riesgo_fc'),
            layout_table(data_riesgo_sis_cluster, data_conditional_riesgo_sis, 'datatable_riesgo_sis'),
            layout_table(data_riesgo_dis_cluster, data_conditional_riesgo_dis, 'datatable_riesgo_dis')
        ]
        )
    ], style={'border': '1px solid black', 'padding': '20px 12px', 'margin': '30px'}
    ),
     Row([
        html.H4('Caraterísticas de Grupos de Pacientes'),
        Col([
            layout_table(data_caracteristicas_cluster, data_conditional_caracteristicas, 'datatable_caracteristicas'),
        ]
        )
    ], style={'border': '1px solid black', 'padding': '20px 12px', 'margin': '30px'}
    ),
     Row([
        html.H4('Caraterísticas en cada uno de los Grupos de Pacientes', style={'marginBottom': '20px'}),
        dcc.Dropdown(
            id='cluster-dropdown',
            options=options,
            value=0 # Valor predeterminado
        ),
        html.Div(id='cluster-graphs')
    ], style={'border': '1px solid black', 'padding': '20px 12px', 'margin': '30px'}
    )
])