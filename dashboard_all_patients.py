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
dt_clf_fc = joblib.load('modelosClasificacion/modelo_frecuencia_cardiaca.pkl')
dt_clf_sis = joblib.load('modelosClasificacion/modelo_presion_sistolica.pkl')
dt_clf_dis = joblib.load('modelosClasificacion/modelo_presion_diastolica.pkl')



# Define los colores y su significado
color_info = [
    {'color': '#ff00008c', 'text': 'Riesgo Alto'},
    {'color': '#ffa50085', 'text': 'Riesgo Medio'}
]

data_conditional = [
        {
            'if': {'column_id': 'Estado de IMC', 'filter_query': '{Estado de IMC} = "Saludable"'},
            'color': 'green'  # Color verde para estado saludable
        },
        {
            'if': {'column_id': 'Estado de IMC', 'filter_query': '{Estado de IMC} = "Sobrepeso"'},
            'color': 'orange'  # Color naranja para sobrepeso
        },
        {
            'if': {'column_id': 'Estado de IMC', 'filter_query': '{Estado de IMC} = "Obesidad"'},
            'color': 'red'  # Color rojo para obesidad
        },
        {
            'if': {
                'column_id': 'Frecuencia Cardiaca BPM',
                'filter_query': '{Riesgo FC} contains "riesgo alto"'
            },
            'backgroundColor': '#ff00008c',  # Color de fondo rojo
            'color': 'black'  # Texto blanco
        },
        {
            'if': {
                'column_id': 'Frecuencia Cardiaca BPM',
                'filter_query': '{Riesgo FC} contains "riesgo medio"'
            },
            'backgroundColor': '#ffa50085',  # Color de fondo rojo
            'color': 'black'  # Texto blanco
        },
        {
            'if': {
                'column_id': 'Presión Sistólica mm[Hg]',
                'filter_query': '{Riesgo Sis} contains "riesgo alto"'
            },
            'backgroundColor': '#ff00008c',  # Color de fondo rojo
            'color': 'black'  # Texto blanco
        },
        {
            'if': {
                'column_id': 'Presión Sistólica mm[Hg]',
                'filter_query': '{Riesgo Sis} contains "riesgo medio"'
            },
            'backgroundColor': '#ffa50085',  # Color de fondo rojo
            'color': 'black'  # Texto blanco
        },
        {
            'if': {
                'column_id': 'Presión Diastólica mm[Hg]',
                'filter_query': '{Riesgo Dis} contains "riesgo alto"'
            },
            'backgroundColor': '#ff00008c',  # Color de fondo rojo
            'color': 'black'  # Texto blanco
        },
        {
            'if': {
                'column_id': 'Presión Diastólica mm[Hg]',
                'filter_query': '{Riesgo Dis} contains "riesgo medio"'
            },
            'backgroundColor': '#ffa50085',  # Color de fondo rojo
            'color': 'black'  # Texto blanco
        },
        ]
    

def get_patients_risk(resultados_sql):

    # Para cada fila de los resultados
    for indice, fila in resultados_sql.iterrows():

        # Verificar si alguno de los valores es NaN
        if pd.isna(fila['Frecuencia Cardiaca BPM']) or pd.isna(fila['Presión Sistólica mm[Hg]']) or pd.isna(fila['Presión Diastólica mm[Hg]']):
            print(f"Los datos de la fila {indice} contienen NaN, no se realizará ninguna predicción.")
            continue
    
        data_to_predict = {
            'frecuencia_cardiaca': [fila['Frecuencia Cardiaca BPM']],
            't_a_sistolica': [fila['Presión Sistólica mm[Hg]']],
            't_a_diastolica': [fila['Presión Diastólica mm[Hg]']]
        }

        # Convertir el diccionario data_to_predict en una matriz bidimensional
        X_to_predict = pd.DataFrame(data_to_predict, columns=['frecuencia_cardiaca', 't_a_sistolica', 't_a_diastolica'])
       
        # Aplica los modelos de árbol de decisión para predecir la etiqueta
        try: 
            prediccion_fc = dt_clf_fc.predict(X_to_predict)  # Reemplaza 'frecuencia_cardiaca' con la columna correspondiente en tus resultados
            prediccion_sis = dt_clf_sis.predict(X_to_predict)  # Reemplaza 't_a_sistolica' con la columna correspondiente en tus resultados
            prediccion_dis = dt_clf_dis.predict(X_to_predict)  # Reemplaza 't_a_diastolica' con la columna correspondiente en tus resultados
        
            # Añadir las predicciones como columnas nuevas a la fila actual
            resultados_sql.at[indice, 'Riesgo FC'] = prediccion_fc[0]
            resultados_sql.at[indice, 'Riesgo Sis'] = prediccion_sis[0]
            resultados_sql.at[indice, 'Riesgo Dis'] = prediccion_dis[0]

        except Exception as e:
            print('Error en prediccion: ', e)
        
    return resultados_sql

# Utiliza resultados_con_color para crear la tabla en Dash con celdas coloreadas según la etiqueta predicha

def get_all_patients_last_report():
    try:
        # Ejecutar una consulta SQL
        cursor = conn.cursor()
        sql_query_search = ("""
            SELECT 
                pv.fecha AS 'Fecha de Diagnóstico', 
                pv.nombre AS 'Nombre de Paciente', 
                pv.identificacion AS 'Identificación', 
                TIMESTAMPDIFF(YEAR, pv.fec_nacimiento, CURDATE()) AS 'Edad',
                pv.sexo AS 'Género', 
                pv.peso AS 'Peso',          
                pv.frecuencia_cardiaca AS 'Frecuencia Cardiaca BPM', 
                pv.t_a_sistolica AS 'Presión Sistólica mm[Hg]', 
                pv.t_a_diastolica AS 'Presión Diastólica mm[Hg]', 
                pv.talla AS 'Talla', 
                ROUND((pv.peso * 10000) / (pv.talla * pv.talla), 2) AS IMC,
                CASE 
                    WHEN (pv.peso * 10000) / (pv.talla * pv.talla) >= 30 THEN 'Obesidad' 
                    WHEN (pv.peso * 10000) / (pv.talla * pv.talla) >= 25 THEN 'Sobrepeso' 
                    ELSE 'Saludable' 
                END AS 'Estado de IMC'
                 
            FROM pacientes.pacientes_vit pv
            INNER JOIN (
                SELECT id_cia, MAX(fecha) AS max_fecha
                FROM pacientes.pacientes_vit
                GROUP BY id_cia
            ) max_dates
            ON pv.id_cia = max_dates.id_cia AND pv.fecha = max_dates.max_fecha
            LIMIT 100;
        """)
        cursor.execute(sql_query_search)

        # Obtener los resultados de la consulta como una lista de diccionarios
        results = cursor.fetchall()

        if not results:
            print("No se encontraron pacientes")
            return df_empty.to_dict('records') 
        
        # Crear un DataFrame a partir de los resultados
        df_search = get_patients_risk(pd.DataFrame(results))

        # Devolver los datos del DataFrame de búsqueda
        return df_search.to_dict('records')
    
    except pymysql.Error as e:
        print('Error de MySQL en tabla: ', e)
        return df_empty.to_dict('records') 
    finally:
        cursor.close() 

def layout_dashboard1():
    return html.Div([
    html.H3('Reporte de Registro Actual de Pacientes', style={"margin": "30px 10px"}),
    Row([
        Col([
            Row([
                Col([
                    html.Div(style={'background-color': color['color'], 'height': '20px', 'width': '20px'})
                ], width=2),
                Col([
                    html.Div(color['text'])
                ], width=10),
            ]) for color in color_info
            
        ], width=4, style={'border': '1px solid black', 'padding': '20px 12px'})
    ], className="mb-3", style={"margin": "30px 10px"}),
    Row(
        Col([
            dcc.Loading(
                id="loading-1",
                type="default",
                children=[
                    dash_table.DataTable(
                        id='datatable',
                        # Aquí obtienes los datos de la función get_all_patients_last_report()
                        data=get_all_patients_last_report(),
                        page_size=20,
                        style_data_conditional=data_conditional,
                        style_header={
                            'textAlign': 'left',  # Alinear texto a la izquierda
                            'backgroundColor': '#0d6efd99',  # Fondo de la cabecera
                            'fontFamily': 'Arial, sans-serif',
                            'fontWeight': '600'
                        },
                        style_cell={
                            'textAlign': 'left',
                        },
                        style_table={'overflowX': 'auto', 'width': '100%'}
                    ),
                ]
            )],width=12, style={'margin': '30px 10px'} # Centrar la tabla y asignarle un ancho
        )
    )
])