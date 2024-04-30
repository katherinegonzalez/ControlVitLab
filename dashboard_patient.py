from dash import html
from bd_conf import conn
import pymysql
from dash import Dash, html, dash_table, dcc, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash
import plotly.graph_objs as go
import pandas as pd
from dash_bootstrap_components import Row, Col, Button, Card, CardBody

# Crear un cursor para ejecutar consultas SQL
# cursor = conn.cursor()
# Inicializar un DataFrame vacío
df_empty = pd.DataFrame()

search_options = []
# Variable global para almacenar la frecuencia cardíaca
heart_rate = None
p_sistolic = None
p_diastolic = None

# heart_rate_series = pd.DataFrame()
# p_sistolic_series = pd.DataFrame()
p_diastolic_series = pd.DataFrame()

available_dates = []

options = [
    {'label': 'Anual', 'value': 'anual'},
    {'label': 'Diario', 'value': 'diario'},
    {'label': 'Mensual', 'value': 'mensual'}
]

# util functions

def showOrHideFigures(data):
    # Si hay datos disponibles, mostrar el gráfico
    if data:
        return {'display': 'block'}
    else:
        # Si no hay datos disponibles, ocultar el gráfico
        return {'display': 'none'}

def heart_rate_color(value):
    color = '#45c212'
    if value >= 60 and value <=79:
        #'frecuencia cardiaca normal'
        color = '#45c212'
    elif value >= 50 and value <=59:
        #'frecuencia cardiaca riesgo medio por debajo del promedio'
        color = '#ff8d33'
    elif value >= 80 and value <=99:
        #'frecuencia cardiaca riesgo medio por encima del promedio'
        color = '#ff8d33'
    elif value <=49:
        #'frecuencia cardiaca riesgo alto por debajo del promedio'
        color = '#ff3933'
    elif value >=100:
        #'frecuencia cardiaca riesgo alto por encima del promedio'
        color = '#ff3933'
    return color

def sistolic_color(value):
    color = '#45c212'
    if value >= 90 and value <=129:
        #'presión sistólica normal'
        color = '#45c212'
    elif value >= 80 and value <=89:
        #'presión sistólica  riesgo medio por debajo del promedio'
        color = '#ff8d33'
    elif value >= 130 and value <=139:
        #'presión sistólica riesgo medio por encima del promedio'
        color = '#ff8d33'
    elif value <=79:
        #'presión sistólica riesgo alto por debajo del promedio'
        color = '#ff3933'
    elif value >=140:
        #'presión sistólica riesgo alto por encima del promedio'
        color = '#ff3933'
    return color

def diastolic_color(value):
    color = '#45c212'
    if value >= 60 and value <=79:
        #'presión sistólica normal'
        color = '#45c212'
    elif value >= 50 and value <=59:
        #'presión sistólica  riesgo medio por debajo del promedio'
        color = '#ff8d33'
    elif value >= 80 and value <=89:
        #'presión sistólica riesgo medio por encima del promedio'
        color = '#ff8d33'
    elif value <=49:
        #'presión sistólica riesgo alto por debajo del promedio'
        color = '#ff3933'
    elif value >=90:
        #'presión sistólica riesgo alto por encima del promedio'
        color = '#ff3933'
    return color


# Configurar el margen con un diccionario
margin_dict = {'t': 60, 'b': 0, 'l': 30, 'r': 30}  # Establece 10 píxeles para todos los márgenes
layout = {'margin': margin_dict, 'height': 350} #cambiar este heght de acuerd al responsive - por defecto es 450
def gauge_figure(value, title, rangoAltoDebajo, rangoMedioDebajo, rangoNormal, rangoMedioEncima, rangoAltoEncima, range, color): 
    figure = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title},
        domain = {'x': [0, 1], 'y': [0.3, 1]},
        # domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': range, 'dtick': 10},
            'steps' : [
                {'range': rangoAltoDebajo, 'color': "#ff3933"},
                {'range': rangoMedioDebajo, 'color': "#ff8d33"},
                {'range': rangoNormal, 'color': "#45c212"},
                {'range': rangoMedioEncima, 'color': "#ff8d33"},
                {'range': rangoAltoEncima, 'color': "#ff3933"}
            ],
            'threshold' : {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.8,
                'value': value},
            'bar' : {
                'color': color,
                'thickness': 0.7, # Ajusta el grosor de la barra
                'line': {'color': 'black', 'width': 0.6}  # Color y ancho del borde
                },

            },
        number = {'font': { 'color': color}},         
    ), layout=layout)

    figure.layout.autosize = True

    return figure  # Devolver la figura del gráfico de Gauge
  
def time_series_graph(
        dataFrame, 
        tipo, 
        title, 
        riesgoAltoDebajo, 
        riesgoMedioDebajo, 
        riesgoNormal, 
        riesgoMedioEncima, 
        riesgoAltoEncima,
        period,
        bottomRange,
        topRange,
        ejeYtitle
        ):
    print(tipo, dataFrame.empty)
    print('dataFrame: ', dataFrame)
    if not dataFrame.empty:
        print(tipo)
        # Crea el gráfico de series temporales
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dataFrame['fecha'], y=dataFrame[tipo], mode='lines', name='Time Series'))
        fig.update_layout(
            title= {
                'text': title,
                'font': {
                    'color': 'black',  # Color del texto
                    'size': 22,        # Tamaño del texto
                    'family': 'Arial', # Fuente del texto
                }
            },
            xaxis_title='Fecha', 
            yaxis_title=ejeYtitle)
    
        fig.update_layout(yaxis_range=[bottomRange, topRange])
        # Agrega dos líneas horizontales (umbrales)
        fig.add_hline(y=riesgoMedioEncima, line_dash='dash', line_color='red', annotation_text='Rieso Alto', annotation_position='top right')
        fig.add_hline(y=riesgoMedioEncima, line_dash='dash', line_color='red', annotation_text='Rieso Medio', annotation_position='bottom right')
        fig.add_hline(y=riesgoNormal, line_dash='dash', line_color='green', annotation_text='Normal', annotation_position='bottom right')
        fig.add_hline(y=riesgoMedioDebajo, line_dash='dash', line_color='orange', annotation_text='Rieso Medio', annotation_position='bottom right')
        fig.add_hline(y=riesgoAltoDebajo, line_dash='dash', line_color='red', annotation_text='Rieso Alto', annotation_position='bottom right')
        
        # Agrega un color de fondo entre las líneas
        # fig.add_hrect(y0=0, y1=riesgoAltoDebajo, fillcolor='red', opacity=0.5)
        # fig.add_hrect(y0=riesgoAltoDebajo, y1=riesgoMedioDebajo, fillcolor='orange', opacity=0.3)
        # fig.add_hrect(y0=riesgoMedioDebajo, y1=riesgoNormal, fillcolor='green', opacity=0.5)
        # fig.add_hrect(y0=riesgoNormal, y1=riesgoMedioEncima, fillcolor='orange', opacity=0.5)
        # fig.add_hrect(y0=riesgoMedioEncima, y1=riesgoAltoEncima, fillcolor='red', opacity=0.5)

        if period == 'anual':
            fig.update_xaxes(
                dtick='M12',
                tickangle=90  # Rotar las etiquetas del eje x
            )
        elif period == 'mensual':
            fig.update_xaxes(
                dtick='M1',
                tickangle=90  # Rotar las etiquetas del eje x
            )
        elif period == 'diario':
            fig.update_xaxes(
                tickmode= 'array',
                tickvals= dataFrame['fecha'],
                tickangle=90,  # Rotar las etiquetas del eje x
            )

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
        cursor = conn.cursor()
        sql_query_names = ("SELECT DISTINCT nombre, identificacion, id_cia FROM pacientes.pacientes_vit")
        cursor.execute(sql_query_names)
        names_and_ids = cursor.fetchall()
        search_options = [{'label': f"{item['nombre']} ({item['identificacion']})", 'value': item['id_cia']} for item in names_and_ids]
        return search_options

    except pymysql.Error as e:
        print('Error de MySQL:', e)
        return []
    finally:
        cursor.close()

def update_table(n_clicks, search_value, dates_limit):
    global heart_rate
    global p_sistolic
    global p_diastolic

    # global heart_rate_series
    # global p_sistolic_series
    # global p_diastolic_series

    global available_dates
    
    print('entra a tabla: ',  n_clicks)
    if n_clicks > 0 and search_value:
        # Si el botón se ha clicado y hay un valor de búsqueda, realiza la búsqueda
        try:
            # Ejecutar una consulta SQL
            cursor = conn.cursor()
            sql_query_search = ("""
                SELECT 
                    fecha AS 'Fecha', 
                    frecuencia_cardiaca, t_a_sistolica, t_a_diastolica, 
                    identificacion AS 'Identificación', 
                    nombre AS 'Nombre', 
                    fec_nacimiento AS 'Fecha de Nacimiento', 
                    TIMESTAMPDIFF(YEAR, fec_nacimiento, CURDATE()) AS 'Edad',
                    sexo, peso, talla, 
                    ROUND((peso * 10000) / (talla*talla), 2) AS IMC,
                CASE 
                    WHEN (peso * 10000) / (talla*talla) >= 30 THEN 'Obesidad' 
                    WHEN (peso * 10000) / (talla*talla) >= 25 THEN 'Sobrepeso' 
                    ELSE 'Saludable' 
                END AS 'Estado de IMC'
                FROM pacientes.pacientes_vit 
                WHERE id_cia = %s
                ORDER BY fecha DESC
                LIMIT %s
            """)
            cursor.execute(sql_query_search, (search_value, dates_limit))

            # Obtener los resultados de la consulta como una lista de diccionarios
            results = cursor.fetchall()

            if not results:
                print("No se encontraron resultados para la búsqueda:", search_value)
                return []

            # Crear un DataFrame a partir de los resultados
            df_search = pd.DataFrame(results)

            # available_dates = df_search['fecha'].iloc[0]

            # Guardar la frecuencia cardíaca en la variable global
            heart_rate = df_search['frecuencia_cardiaca'].iloc[0]
            p_sistolic = df_search['t_a_sistolica'].iloc[0]
            p_diastolic = df_search['t_a_diastolica'].iloc[0]

            # Excluir la columna de frecuencia cardíaca de los datos de la tabla
            df_search = df_search.drop(columns=['frecuencia_cardiaca', 't_a_sistolica', 't_a_diastolica'])

            df_search = df_search.iloc[[0]].copy()

            # Devolver los datos del DataFrame de búsqueda
            return df_search.to_dict('records') # Tomar solo el primer registro con iloc
        
        except pymysql.Error as e:
            print('Error de MySQL en tabla: ', e)
            return df_empty.to_dict('records') 
        finally:
            cursor.close() 
        
    else:
        # Si no se ha hecho clic en el botón o no hay un valor de búsqueda, devuelve datos vacíos o lo que sea apropiado
        # Si no hay valor de búsqueda, retornar un DataFrame vacío
        return df_empty.to_dict('records')  


# Obtener fechas disponibles en la base de datos
def get_available_dates(data_table, search_value):
    print('search value en date picker: ', search_value)
    if data_table:
        try:
            cursor = conn.cursor()
            sql_query_dates = ("""
                SELECT DISTINCT fecha
                FROM pacientes.pacientes_vit 
                WHERE id_cia = %s
                ORDER BY fecha DESC
                """)
            cursor.execute(sql_query_dates, search_value)

            # Obtener los resultados de la consulta como una lista de diccionarios
            results = cursor.fetchall()
            

            available_dates = [date['fecha'] for date in results]
            print('available_dates: ', available_dates)


             # Determinar la fecha mínima y máxima
            min_date = min(available_dates)
            max_date = max(available_dates)
            return min_date, max_date

        except pymysql.Error as e:
            print('Error de MySQL en dates: ', e)
            return dash.no_update, dash.no_update
        finally:
            cursor.close() 
    else:
        return dash.no_update, dash.no_update
    

def update_gauge_heart_rate():
    try:
        # Solo ejecutar si se hizo clic en el botón
        if heart_rate:
            print(heart_rate)
            return gauge_figure(
                heart_rate, 
                'BPM', 
                [0, 50],
                [50, 60],
                [60, 80],
                [80, 100],
                [100, 120],
                [40, 120],
                heart_rate_color(heart_rate)
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
                'Diastólica', 
                [0, 50],
                [50, 60],
                [60, 80],
                [80, 90],
                [90, 120],
                [40, 120],
                diastolic_color(p_diastolic)
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
                'Sistólica', 
                [0, 80],
                [80, 90],
                [90, 130],
                [130, 140],
                [140, 160],
                [60, 160],
                sistolic_color(p_sistolic)
            )

    except Exception as e:
        print('Error en Presión Sistólica: ', e)
        return dash.no_update

    else:
        # Si no se ha hecho clic en el botón, no actualizar el gráfico
        return dash.no_update
 

def get_heart_rate_data(start_date, end_date, search_value):
    try:
        cursor = conn.cursor()
        sql_query_heart_rate_data = ("""
            SELECT DISTINCT fecha, frecuencia_cardiaca 
            FROM pacientes.pacientes_vit 
            WHERE id_cia = %s
            AND fecha >= %s
            AND fecha <= %s
            ORDER BY fecha DESC
            """)
        cursor.execute(sql_query_heart_rate_data, (search_value, start_date, end_date))

        # Obtener los resultados de la consulta como una lista de diccionarios
        results = cursor.fetchall()
        heart_rate_series = pd.DataFrame(results)

        if not heart_rate_series.empty:
            print('heart_rate_series: ', heart_rate_series)
            heart_rate_series.loc[:, 'fecha'] = pd.to_datetime(heart_rate_series['fecha'])
        
        return heart_rate_series

    except pymysql.Error as e:
        print('Error de MySQL en get data: ', e)
        return pd.DataFrame()
    finally:
        cursor.close() 

def get_sistolic_data(start_date, end_date, search_value):
    try:
        cursor = conn.cursor()
        sql_query_heart_rate_data = ("""
            SELECT DISTINCT fecha, t_a_sistolica 
            FROM pacientes.pacientes_vit 
            WHERE id_cia = %s
            AND fecha >= %s
            AND fecha <= %s
            ORDER BY fecha DESC
            """)
        cursor.execute(sql_query_heart_rate_data, (search_value, start_date, end_date))

        # Obtener los resultados de la consulta como una lista de diccionarios
        results = cursor.fetchall()
        sistolic_series = pd.DataFrame(results)

        if not sistolic_series.empty:
            print('sistolic_series: ', sistolic_series)
            sistolic_series.loc[:, 'fecha'] = pd.to_datetime(sistolic_series['fecha'])
        
        return sistolic_series

    except pymysql.Error as e:
        print('Error de MySQL en get data sistolic: ', e)
        return pd.DataFrame()
    finally:
        cursor.close()  

def get_diastolic_data(start_date, end_date, search_value):
    try:
        cursor = conn.cursor()
        sql_query_heart_rate_data = ("""
            SELECT DISTINCT fecha, t_a_diastolica 
            FROM pacientes.pacientes_vit 
            WHERE id_cia = %s
            AND fecha >= %s
            AND fecha <= %s
            ORDER BY fecha DESC
            """)
        cursor.execute(sql_query_heart_rate_data, (search_value, start_date, end_date))

        # Obtener los resultados de la consulta como una lista de diccionarios
        results = cursor.fetchall()
        diastolic_series = pd.DataFrame(results)

        if not diastolic_series.empty:
            print('diastolic_series: ', diastolic_series)
            diastolic_series.loc[:, 'fecha'] = pd.to_datetime(diastolic_series['fecha'])
        
        return diastolic_series

    except pymysql.Error as e:
        print('Error de MySQL en get data sistolic: ', e)
        return pd.DataFrame()
    finally:
        cursor.close()  


def update_time_series_plot_frecuencia_cardiaca(n_clicks, type_value, start_date, end_date, search_value):
    
    if n_clicks > 0 and start_date and end_date and type_value:

        heart_rate_series = get_heart_rate_data(start_date, end_date, search_value)

        return time_series_graph(
            heart_rate_series, 
            'frecuencia_cardiaca', 
            'Frecuencia Cardíaca', 
            50, 
            60,
            80, 
            100,  
            120,
            type_value,
            40,
            120,
            'BPM')
    else:
        return dash.no_update
  
def update_time_series_plot_sistolica(n_clicks, type_value, start_date, end_date, search_value):

    if n_clicks > 0 and start_date and end_date and type_value:
        p_sistolic_series = get_sistolic_data(start_date, end_date, search_value)
 
        return time_series_graph(
            p_sistolic_series, 
            't_a_sistolica', 
            'Presión Sistólica', 
            80, 
            90,
            130, 
            140,  
            140,
            type_value,
            60,
            160,
            'mm[Hg]')
    else:
        return dash.no_update
         
def update_time_series_plot_diastolica(n_clicks, type_value, start_date, end_date, search_value):
    if n_clicks > 0 and start_date and end_date and type_value:
        p_diastolic_series = get_diastolic_data(start_date, end_date, search_value)
 
        return time_series_graph(
            p_diastolic_series, 
            't_a_diastolica', 
            'Presión Diastólica', 
            50, 
            60,
            80, 
            90,  
            90,
            type_value,
            40,
            120,
            'mm[Hg]')
    else:
        return dash.no_update

def layout_dashboard_patient(): 

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
        }]

    return html.Div([
        # Barra de búsqueda y botón
        Row([
            Col([
                dcc.Dropdown(
                    id='search-input',
                    options=[],
                    multi=False,
                    placeholder="Buscar por nombre o identificación de paciente..."
                ),
            ], width=10),
            Col([
                Button('Buscar', id='search-button', n_clicks=0, className="btn btn-primary btn-block", style={"width": "100%"}),
            ], width=2),
        ], className="mb-3", style={"margin-top": "30px", "margin-bottom": "30px"} ),
        # Tabla
        dcc.Loading(
            id="loading-1",
            type="default",
            children=[
                dash_table.DataTable(
                    id='datatable',
                    data=df_empty.to_dict('records'),
                    page_size=5,
                    style_data_conditional=data_conditional,
                    style_header = {
                    'textAlign': 'left',  # Alinear texto a la derecha
                    'backgroundColor': '#0d6efd99',  # Fondo de la cabecera
                    'fontFamily': 'Arial, sans-serif',  
                    'fontWeight': '600'
                    },
                    style_cell= {
                    'textAlign': 'left',
                    }
                ),
            ]
        ),
        # Gráficos de Gauge  de frecuencia y panel de presión
        Row([
            Col([
                html.H4(children='Frecuencia Cardiaca', className="mb-3", style={'text-align': 'center'}), 
                dcc.Loading(
                    id="loading-2",
                    type="default",
                    children=[
                        dcc.Graph(id='gauge-graph-heart-rate', style={'display': 'none'}, config={'responsive': True})
                    ]
                ),
            ], width=4, style={'border': '1px solid black', 'padding': '20px 12px'}),
            Col([
                html.H4(children='Presión mm[Hg]', className="mb-3", style={'text-align': 'center'}), 
                Row([
                    Col([
                        dcc.Loading(
                            id="loading-3",
                            type="default",
                            children=[
                                dcc.Graph(id='gauge-graph-diastolic', style={'display': 'none'}),
                            ]
                        ),
                    ], width=6),
                    Col([
                        dcc.Loading(
                            id="loading-4",
                            type="default",
                            children=[
                                dcc.Graph(id='gauge-graph-sistolic', style={'display': 'none'}),
                            ]
                        ),
                    ], width=6),
                ]),
            ], width=8, style={'border': '1px solid black', 'padding': '20px 12px'}),
        ], className="mb-3", style={"margin": "30px 10px"}),

        # Date Picker y Radio Button
        Row([
            html.H4(children='Seguimiento Continuo de los datos', className="mb-3"), 
            html.P(children='A continuación, seleccione el rango de fecha y la agrupación de datos (Anual, Diario o Mensual) que desea observar:', className="mb-3"), 
            Col([
                dcc.DatePickerRange(
                id='date-picker-range',
                start_date_placeholder_text="Fecha de inicio",
                end_date_placeholder_text="Fecha de fin",
                display_format='MM/DD/YYYY', 
                style={'display': 'none'}
                )
            ], width=4),
            Col([
                dcc.RadioItems(
                id='radio-buttons',
                options=options,
                value='anual'  # Valor por defecto seleccionado
                )
            ], width=2),
            Col([
                Button('Ver Datos en el Tiempo', id='heart-rate-button', n_clicks=0, className="btn btn-primary btn-block", style={"width": "100%"}),
            ], width=4),
            Col([], width=2),
        ], className="mb-3", style={"margin": "30px 10px"}),
        # Gráficos de tiempo
        Row([
            Col([
                dcc.Loading(
                    id="loading-5",
                    type="default",
                    children=[
                        dcc.Graph(id='time-series-plot-frecuencia-cardiaca', style={'display': 'none'}),
                        dcc.Graph(id='time-series-plot-sistolica', style={'display': 'none'}),
                        dcc.Graph(id='time-series-plot-diastolica', style={'display': 'none'})
                    ]
                )
            ], width=12),
        ]),
    # html.Button('Ver Frecuencia Cardiaca', id='heart-rate-button', n_clicks=0)
    ], className="container-fluid")