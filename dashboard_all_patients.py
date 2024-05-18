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

def cell_color(column_id, risk_type, risk_grade):
    print('risk_grade: ', risk_grade)
    risk_grade_color = ('normal' if risk_grade == 'Saludable' 
        else 'medio' if risk_grade == 'Sobrepeso' 
        else 'alto' if risk_grade == 'Obesidad' 
        else str(risk_grade).lower())
    print('risk_grade_after: ', risk_grade)
    print('risk_type: ', risk_type)
    print('risk_grade_color: ', risk_grade_color)
    print('color grade: ', alert_colors[risk_grade_color])
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

data_conditional = [
        cell_color('Frecuencia Cardiaca BPM', 'Riesgo FC', 'no_data'),
        cell_color('Frecuencia Cardiaca BPM', 'Riesgo FC', 'normal'),
        cell_color('Frecuencia Cardiaca BPM', 'Riesgo FC', 'medio'),
        cell_color('Frecuencia Cardiaca BPM', 'Riesgo FC', 'alto'),
        cell_color('Presión Sistólica mm[Hg]', 'Riesgo Sis', 'normal'),
        cell_color('Presión Sistólica mm[Hg]', 'Riesgo Sis', 'medio'),
        cell_color('Presión Sistólica mm[Hg]', 'Riesgo Sis', 'alto'),
        cell_color('Presión Diastólica mm[Hg]', 'Riesgo Dis', 'normal'),
        cell_color('Presión Diastólica mm[Hg]', 'Riesgo Dis', 'medio'),
        cell_color('Presión Diastólica mm[Hg]', 'Riesgo Dis', 'alto'),
        cell_color('Riesgo', 'Riesgo', 'Normal'),
        cell_color('Riesgo', 'Riesgo', 'Medio'),
        cell_color('Riesgo', 'Riesgo', 'Alto'),
        cell_botton_table('Action')
        #cell_color('Estado de IMC', 'Estado de IMC', 'Saludable'),
        #cell_color('Estado de IMC', 'Estado de IMC', 'Sobrepeso'),
        #cell_color('Estado de IMC', 'Estado de IMC', 'Obesidad'),
        #cell_color('IMC', 'Estado de IMC', 'Saludable'),
        #cell_color('IMC', 'Estado de IMC', 'Sobrepeso'),
        #cell_color('IMC', 'Estado de IMC', 'Obesidad')
    ]

# Función para calcular la prioridad
def calcular_prioridad(row):
    count_alto = sum(row[['Riesgo FC', 'Riesgo Dis', 'Riesgo Sis']].str.contains('alto'))
    count_medio = sum(row[['Riesgo FC', 'Riesgo Dis', 'Riesgo Sis']].str.contains('riesgo medio'))
    count_normal = sum(row[['Riesgo FC', 'Riesgo Dis', 'Riesgo Sis']].str.contains('normal'))
   
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


def get_patients_risk(resultados_sql):

    # Para manejar los valores NaN y reemplazarlos con "Sin dato"
    resultados_sql.fillna(value="Sin datos", inplace=True)

    # Para cada fila de los resultados
    for indice, fila in resultados_sql.iterrows():
         
        frec_cardiaca_to_pred = [fila['Frecuencia Cardiaca BPM']]
        sistolica_to_pred = [fila['Presión Sistólica mm[Hg]']]
        diastolica_to_pred = [fila['Presión Diastólica mm[Hg]']]

        # Verificar si alguno de los valores es NaN
        if pd.isna(fila['Frecuencia Cardiaca BPM']) and pd.isna(fila['Presión Sistólica mm[Hg]']) and pd.isna(fila['Presión Diastólica mm[Hg]']):
            print(f"Los datos de la fila {indice} contienen NaN, no se realizará ninguna predicción.")
            continue
        elif fila['Frecuencia Cardiaca BPM'] == 'Sin datos':
            frec_cardiaca_to_pred = 0
        elif pd.isna(fila['Presión Sistólica mm[Hg]']):
            sistolica_to_pred = 0
        elif pd.isna(fila['Presión Diastólica mm[Hg]']):
            diastolica_to_pred = 0
    
        data_to_predict = {
            'frecuencia_cardiaca': frec_cardiaca_to_pred,
            't_a_sistolica': sistolica_to_pred,
            't_a_diastolica': diastolica_to_pred
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

            if fila['Frecuencia Cardiaca BPM'] == 'Sin datos':
                resultados_sql.at[indice, 'Riesgo FC'] = 'no_data'
            elif fila['Presión Sistólica mm[Hg]'] == 'Sin datos':
                resultados_sql.at[indice, 'Riesgo Sis'] = 'no_data'
            elif fila['Presión Diastólica mm[Hg]'] == 'Sin datos':
                resultados_sql.at[indice, 'Riesgo FC'] = 'no_data'

            riesgo_total = 'Normal'
            if 'alto' in prediccion_fc[0] or 'alto' in prediccion_sis[0] or 'alto' in prediccion_dis[0]:
                riesgo_total = 'Alto'
            elif 'medio' in prediccion_fc[0] or 'medio' in prediccion_sis[0] or 'medio' in prediccion_dis[0]:
                riesgo_total = 'Medio'
            else: 
                riesgo_total = 'Normal'

            resultados_sql.at[indice, 'Riesgo'] = riesgo_total

        except Exception as e:
            print('Error en prediccion: ', e)

    resultados_sql['Action'] = 'Ver Detalles'
    # Para reorganizar el DataFrame según los niveles de riesgo
    # Crear la columna de prioridad
    resultados_sql['Prioridad'] = resultados_sql.apply(calcular_prioridad, axis=1)

    # Ordenar por la columna de prioridad
    resultados_sql.sort_values(by='Prioridad', inplace=True)
    print(resultados_sql['Prioridad'])

    # Eliminar la columna de prioridad
    resultados_sql.drop(columns=['Prioridad'], inplace=True)

    return resultados_sql

# Utiliza resultados_con_color para crear la tabla en Dash con celdas coloreadas según la etiqueta predicha

def get_all_patients_last_report():
    try:
        # Ejecutar una consulta SQL
        cursor = conn.cursor()
        sql_query_search = ("""
            SELECT 
                pv.id_cia,            
                DATE_FORMAT(pv.fecha, '%Y-%m-%d') AS 'Fecha de Diagnóstico', 
                pv.nombre AS 'Nombre de Paciente', 
                pv.identificacion AS 'Identificación', 
                TIMESTAMPDIFF(YEAR, pv.fec_nacimiento, CURDATE()) AS 'Edad',
                pv.sexo AS 'Género', 
                pv.peso AS 'Peso',     
                pv.talla AS 'Talla', 
                pv.frecuencia_cardiaca AS 'Frecuencia Cardiaca BPM', 
                pv.t_a_sistolica AS 'Presión Sistólica mm[Hg]', 
                pv.t_a_diastolica AS 'Presión Diastólica mm[Hg]',
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
    html.H3('Reporte de Pacientes y Alertas Destacadas', style={"margin": "30px 10px"}),
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
    Row(
        Col([
            dcc.Loading(
                id="loading-1",
                type="default",
                children=[
                    dash_table.DataTable(
                        id='datatable_pacientes',
                        data=get_all_patients_last_report(),
                        page_size=20,
                        columns=[
                            {'name': 'Fecha de Diagnóstico', 'id': 'Fecha de Diagnóstico'},
                            {'name': 'Nombre de Paciente', 'id': 'Nombre de Paciente'},
                            {'name': 'Identificación', 'id': 'Identificación'},
                            {'name': 'Edad', 'id': 'Edad'},
                            {'name': 'Género', 'id': 'Género'},
                            {'name': 'Peso (kg)', 'id': 'Peso'},
                            {'name': 'Talla (cm)', 'id': 'Talla'},
                            {'name': 'IMC', 'id': 'IMC'},
                            {'name': 'Estado de IMC', 'id': 'Estado de IMC'},  
                            {'name': 'Frecuencia Cardiaca BPM', 'id': 'Frecuencia Cardiaca BPM'},
                            {'name': 'Presión Sistólica mm[Hg]', 'id': 'Presión Sistólica mm[Hg]'},
                            {'name': 'Presión Diastólica mm[Hg]', 'id': 'Presión Diastólica mm[Hg]'},
                            {'name': 'Riesgo', 'id': 'Riesgo'},
                            {'name': 'Detalle', 'id': 'Action'}        
                        ],
                        style_data_conditional=data_conditional,
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
                        style_table={'overflowX': 'auto', 'width': '100%'}
                    ),
                ]
            )],width=12, style={'margin': '30px 10px'} # Centrar la tabla y asignarle un ancho
        )
    )
])