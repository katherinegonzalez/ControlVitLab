# Import packages
from dash import Dash, html, dash_table, dcc, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objs as go
# Importar el controlador pymysql en lugar de MySQLdb
import pymysql

# Caagar datos en csv
# df = pd.read_csv('patients_complete.csv')

##----------------------------Conexión con BD------------------------------------------##

# Definir la conexión a la base de datos
project_id = 'vernal-day-418920'
instance_connection_name = 'vernal-day-418920:us-central1:tesismsyc'
database_name = 'pacientes'
db_user = 'katherine'
db_password = 'mysql123*'

instance_ip = '34.172.195.129'
instance_port = '3306'

# Establecer la conexión a la base de datos
conn = pymysql.connect(
    host=instance_ip,
    port=3306,  # Puerto predeterminado de MySQL
    user=db_user,
    password=db_password,
    database=database_name,
    charset='utf8mb4',  # Codificación de caracteres
    cursorclass=pymysql.cursors.DictCursor  # Cursor que devuelve los resultados como diccionarios
)

# Crear un cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Variable de bandera para controlar si se cerró la conexión
connection_closed = False

##------------------------------------------------------------------##
# Inicializar un DataFrame vacío
df_empty = pd.DataFrame()

# Initialize the app
app = Dash(__name__)

# Lista global para almacenar los nombres e identificaciones de los pacientes
search_options = []

# Callback para cargar los nombres e identificaciones de los pacientes en el dropdown
@app.callback(
    Output('search-input', 'options'),
    [Input('search-input', 'search_value')]
)
def update_search_options(search_value):
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

# App layout
app.layout = html.Div([
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
            dcc.Graph(id='gauge-graph-heart-rate')
        ]
    ),
    dcc.Loading(
        id="loading-3",
        type="default",
        children=[
            dcc.Graph(id='gauge-graph-diastolic'),
            dcc.Graph(id='gauge-graph-sistolic')
        ]
    )
])

# Variable global para almacenar la frecuencia cardíaca
heart_rate = None
p_sistolic = None
p_diastolic = None

# Callback para actualizar los datos de la tabla basados en la búsqueda
@app.callback(
    Output('datatable', 'data'),
    [Input('search-button', 'n_clicks')],
    [State('search-input', 'value')],
)
def update_table(n_clicks, search_value):
    global heart_rate
    global p_sistolic
    global p_diastolic
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


def gauge_figure(value): 
    figure = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': "Frecuencia Cardíaca"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100]},
            'steps' : [
                {'range': [0, 60], 'color': "lightgray"},
                {'range': [60, 100], 'color': "gray"}
            ],
            'threshold' : {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80}
            }
    ))

    return figure  # Devolver la figura del gráfico de Gauge
 
# Callback para actualizar el gráfico de Gauge con la frecuencia cardíaca
@app.callback(
    Output('gauge-graph-heart-rate', 'figure'),
    [Input('datatable', 'data')]
)
def update_gauge_heart_rate(table_data):
    try:
        # Solo ejecutar si se hizo clic en el botón
        if heart_rate:
            print(heart_rate)
             # Crear el objeto de figura para el gráfico de Gauge
            return gauge_figure(heart_rate)

    except Exception as e:
        print('Error en Frecuencia Cardiaca: ', e)
        return dash.no_update

    else:
        # Si no se ha hecho clic en el botón, no actualizar el gráfico
        return dash.no_update


# Callback para actualizar el gráfico de Gauge con la frecuencia cardíaca
@app.callback(
    Output('gauge-graph-diastolic', 'figure'),
    [Input('datatable', 'data')]
)
def update_gauge_diastolic(table_data):
    try:
        # Solo ejecutar si se hizo clic en el botón
        if p_diastolic:
            print(p_diastolic)
             # Crear el objeto de figura para el gráfico de Gauge
            return gauge_figure(p_diastolic)

    except Exception as e:
        print('Error en Presión Diastólca: ', e)
        return dash.no_update

    else:
        # Si no se ha hecho clic en el botón, no actualizar el gráfico
        return dash.no_update

# Callback para actualizar el gráfico de Gauge con la frecuencia cardíaca
@app.callback(
    Output('gauge-graph-sistolic', 'figure'),
    [Input('datatable', 'data')]
)
def update_gauge_sistolic(table_data):
    try:
        # Solo ejecutar si se hizo clic en el botón
        if p_sistolic:
            print(p_sistolic)
             # Crear el objeto de figura para el gráfico de Gauge
            return gauge_figure(p_sistolic)

    except Exception as e:
        print('Error en Presión Sistólica: ', e)
        return dash.no_update

    else:
        # Si no se ha hecho clic en el botón, no actualizar el gráfico
        return dash.no_update


# REVISAR COMO Y DONDE CERRAR LA CONEXIÓN
#cursor.close()
#conn.close()


# Run the app
if __name__ == '__main__':
    app.run(debug=True)