from dash import html
from bd_conf import conn
import pymysql
from dash import Dash, html, dash_table, dcc, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash
import plotly.graph_objs as go
import pandas as pd

# Crear un cursor para ejecutar consultas SQL
cursor = conn.cursor()
# Inicializar un DataFrame vacío
df_empty = pd.DataFrame()

search_options = []
# Variable global para almacenar la frecuencia cardíaca
heart_rate = None
p_sistolic = None
p_diastolic = None

heart_rate_series = pd.DataFrame()
p_sistolic_series = pd.DataFrame()
p_diastolic_series = pd.DataFrame()

# util functions

def showOrHideFigures(data):
    # Si hay datos disponibles, mostrar el gráfico
    if data:
        return {'display': 'block'}
    else:
        # Si no hay datos disponibles, ocultar el gráfico
        return {'display': 'none'}

def gauge_figure(value, title, rangoAltoDebajo, rangoMedioDebajo, rangoNormal, rangoMedioEncima, rangoAltoEncima, threshold): 
    figure = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 200]},
            'steps' : [
                {'range': rangoAltoDebajo, 'color': "#ff3933"},
                {'range': rangoMedioDebajo, 'color': "#ff8d33"},
                {'range': rangoNormal, 'color': "#45c212"},
                {'range': rangoMedioEncima, 'color': "#ff8d33"},
                {'range': rangoAltoEncima, 'color': "#ff3933"}
            ],
            'threshold' : {
                'line': {'color': "yellow", 'width': 4},
                'thickness': 0.75,
                'value': threshold},
            'bar' : {
                'color': "blue",
                'thickness': 0.2
                }
            },
            
    ))

    return figure  # Devolver la figura del gráfico de Gauge
  
def time_series_graph(dataFrame, tipo, title, riesgoAltoDebajo, riesgoMedioDebajo, riesgoNormal, riesgoMedioEncima, riesgoAltoEncima):
    print(tipo, dataFrame.empty)
    if not dataFrame.empty:
        print(tipo)
        # Crea el gráfico de series temporales
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dataFrame['fecha'], y=dataFrame[tipo], mode='lines', name='Time Series'))
        fig.update_layout(title=title, xaxis_title='Fecha', yaxis_title='Valor')
    
        # Agrega dos líneas horizontales (umbrales)
        fig.add_hline(y=riesgoAltoEncima, line_dash='dash', line_color='red', annotation_text='Rieso Alto Por Encima del Promedio', annotation_position='top right')
        fig.add_hline(y=riesgoMedioEncima, line_dash='dash', line_color='orange', annotation_text='Rieso Medio Por Encima del Promedio', annotation_position='top right')
        fig.add_hline(y=riesgoNormal, line_dash='dash', line_color='green', annotation_text='Normal', annotation_position='top right')
        fig.add_hline(y=riesgoMedioDebajo, line_dash='dash', line_color='orange', annotation_text='Rieso Medio Por Debajo del Promedio', annotation_position='top right')
        fig.add_hline(y=riesgoAltoDebajo, line_dash='dash', line_color='red', annotation_text='Rieso Alto Por Debajo del Promedio', annotation_position='top right')
        
        return fig
        
    else:
        return dash.no_update
    


#Callbacks

def update_search_options():
    global search_options

    # Si la lista de opciones ya está cargada, no es necesario volver a cargarla
    if search_options:
        return search_options

    # Realizar una consulta SQL para obtener todos los nombres e identificaciones de los pacientes
    try:
        sql_query_names = ("SELECT DISTINCT nombre, identificacion, id_cia FROM pacientes.pacientes_vit")
        cursor.execute(sql_query_names)
        names_and_ids = cursor.fetchall()
        search_options = [{'label': f"{item['nombre']} ({item['identificacion']})", 'value': item['id_cia']} for item in names_and_ids]
        return search_options

    except pymysql.Error as e:
        print('Error de MySQL:', e)
        return []

def update_table(n_clicks, search_value):
    global heart_rate
    global p_sistolic
    global p_diastolic

    global heart_rate_series
    global p_sistolic_series
    global p_diastolic_series
    
    print('entra a tabla: ',  n_clicks)
    if n_clicks > 0 and search_value:
        # Si el botón se ha clicado y hay un valor de búsqueda, realiza la búsqueda
        try:
            # Ejecutar una consulta SQL
            # cursor = conn.cursor()
            sql_query_search = ("""
                SELECT fecha, frecuencia_cardiaca, t_a_sistolica, t_a_diastolica, identificacion, nombre, fec_nacimiento, sexo, peso, talla, (peso * 10000) / (talla*talla) AS IMC, 
                CASE 
                    WHEN (peso * 10000) / (talla*talla) >= 30 THEN 'Obesidad' 
                    WHEN (peso * 10000) / (talla*talla) >= 25 THEN 'Sobrepeso' 
                    ELSE 'Saludable' 
                END AS 'Estado de IMC' 
                FROM pacientes.pacientes_vit 
                WHERE id_cia = %s
                ORDER BY fecha DESC
            """)
            cursor.execute(sql_query_search, search_value)

            # Obtener los resultados de la consulta como una lista de diccionarios
            results = cursor.fetchall()

            if not results:
                print("No se encontraron resultados para la búsqueda:", search_value)
                return []

            # Crear un DataFrame a partir de los resultados
            df_search = pd.DataFrame(results)

            # Guardar la frecuencia cardíaca en la variable global
            heart_rate = df_search['frecuencia_cardiaca'].iloc[0]
            p_sistolic = df_search['t_a_sistolica'].iloc[0]
            p_diastolic = df_search['t_a_diastolica'].iloc[0]

            heart_rate_series = df_search[['frecuencia_cardiaca', 'fecha']].copy()
            heart_rate_series.loc[:, 'fecha'] = pd.to_datetime(heart_rate_series['fecha'])

            print(heart_rate_series)

            p_diastolic_series = df_search[['t_a_diastolica', 'fecha']].copy()
            p_diastolic_series.loc[:, 'fecha'] = pd.to_datetime(p_diastolic_series['fecha'])

            print(p_diastolic_series)

            p_sistolic_series = df_search[['t_a_sistolica', 'fecha']].copy()
            p_sistolic_series.loc[:, 'fecha'] = pd.to_datetime(p_sistolic_series['fecha'])

            print(p_sistolic_series)

            # Excluir la columna de frecuencia cardíaca de los datos de la tabla
            df_search = df_search.drop(columns=['frecuencia_cardiaca', 't_a_sistolica', 't_a_diastolica'])

            # Devolver los datos del DataFrame de búsqueda
            return df_search.to_dict('records')
        
        except pymysql.Error as e:
            print('Error de MySQL: ', e)
            return df_empty.to_dict('records')  
        
    else:
        # Si no se ha hecho clic en el botón o no hay un valor de búsqueda, devuelve datos vacíos o lo que sea apropiado
        # Si no hay valor de búsqueda, retornar un DataFrame vacío
        return df_empty.to_dict('records')  

def update_gauge_heart_rate():
    try:
        # Solo ejecutar si se hizo clic en el botón
        if heart_rate:
            print(heart_rate)
            return gauge_figure(
                heart_rate, 
                'Frecuencia Cardíaca', 
                [0, 50],
                [50, 60],
                [60, 80],
                [80, 100],
                [100, 200],
                80
            )

    except Exception as e:
        print('Error en Frecuencia Cardiaca: ', e)
        return dash.no_update

    else:
        # Si no se ha hecho clic en el botón, no actualizar el gráfico
        return dash.no_update

def update_gauge_diastolic():
    try:
        # Solo ejecutar si se hizo clic en el botón
        if p_diastolic:
            print(p_diastolic)
             # Crear el objeto de figura para el gráfico de Gauge
            return gauge_figure(
                p_diastolic, 
                'Presión Diastólica', 
                [0, 50],
                [50, 60],
                [60, 80],
                [80, 90],
                [90, 200],
                80
            )
        

    except Exception as e:
        print('Error en Presión Diastólca: ', e)
        return dash.no_update

    else:
        # Si no se ha hecho clic en el botón, no actualizar el gráfico
        return dash.no_update

def update_gauge_sistolic():
    try:
        # Solo ejecutar si se hizo clic en el botón
        if p_sistolic:
            print(p_sistolic)
             # Crear el objeto de figura para el gráfico de Gauge
            return gauge_figure(
                p_sistolic, 
                'Presión Sistólica', 
                [0, 80],
                [80, 90],
                [90, 130],
                [130, 140],
                [140, 200],
                130
            )

    except Exception as e:
        print('Error en Presión Sistólica: ', e)
        return dash.no_update

    else:
        # Si no se ha hecho clic en el botón, no actualizar el gráfico
        return dash.no_update
 
def update_time_series_plot_frecuencia_cardiaca():
    print('p_sistolic_series', p_sistolic_series.empty)
    print('p_diastolic_series', p_diastolic_series.empty)
    return time_series_graph(
        heart_rate_series, 
        'frecuencia_cardiaca', 
        'Gráfico de Frecuencia Cardiaca en el tiempo', 
        20, 
        50,
        60, 
        80,  
        100)
  
def update_time_series_plot_sistolica():
    print('entra a callback para sistolica: ', p_sistolic_series)
    return time_series_graph(
        p_sistolic_series, 
        't_a_sistolica', 
        'Gráfico de Presión Sistólica en el tiempo', 
        20, 
        80,
        90, 
        130,  
        140)
         
def update_time_series_plot_diastolica():
    return time_series_graph(
        p_diastolic_series, 
        't_a_diastolica', 
        'Gráfico de Presión Diastólica en el tiempo', 
        10, 
        50,
        60, 
        80,  
        90)

def layout_dashboard_patient():
    return html.Div([
        html.Div(children='ControlVit Lab'),
        dcc.Dropdown(
            id='search-input',
            options=[],
            multi=False,
            placeholder="Buscar por nombre o identificación de paciente..."
        ),
        html.Button('Buscar', id='search-button', n_clicks=0),
        # Figura 1: Un gráfico que se renderiza inmediatamente
        dcc.Loading(
            id="loading-1",
            type="default",
            children=[
                dash_table.DataTable(
                id='datatable',
                data=df_empty.to_dict('records') ,
                page_size=5
            ),
            ]
        ),
        dcc.Input(id='frecuencia-cardiaca', type='text', value='', style={'display': 'none'}),
        # Figura 2: Un gráfico que se renderiza después de un retraso simulado
        dcc.Loading(
            id="loading-2",
            type="default",
            children=[
                dcc.Graph(id='gauge-graph-heart-rate', style={'display': 'none'})
            ]
        ),
        dcc.Loading(
            id="loading-3",
            type="default",
            children=[
                dcc.Graph(id='gauge-graph-diastolic', style={'display': 'none'}),
                dcc.Graph(id='gauge-graph-sistolic', style={'display': 'none'})
            ]
        ),
        dcc.Loading(
            id="loading-4",
            type="default",
            children=[
                dcc.Graph(id='time-series-plot-frecuencia-cardiaca', style={'display': 'none'}),
                dcc.Graph(id='time-series-plot-sistolica', style={'display': 'none'}),
                dcc.Graph(id='time-series-plot-diastolica', style={'display': 'none'})
            ]
        )
    ])
