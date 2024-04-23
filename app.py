# Import packages
from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from sqlalchemy import create_engine
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

""""
# Crear un objeto cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Ejecutar una consulta SQL
sql_query = "SELECT * FROM pacientes_vit"
cursor.execute(sql_query)

# Obtener los resultados de la consulta como una lista de diccionarios
results = cursor.fetchall()

# Crear un DataFrame a partir de los resultados
df = pd.DataFrame(results)

# Cerrar el cursor y la conexión
cursor.close()
conn.close()

# Mostrar el DataFrame
# print(df)

"""
##------------------------------------------------------------------##
# Inicializar un DataFrame vacío
df_empty = pd.DataFrame()

# Initialize the app
app = Dash(__name__)

# Lista global para almacenar los nombres de los pacientes
search_names = []

# Callback para cargar los nombres de los pacientes en la barra de búsqueda
@app.callback(
    Output('search-input', 'options'),
    [Input('search-input', 'search_value')]
)
def update_search_options(search_value):
    global search_names

    # Si la lista de nombres ya está cargada, no es necesario volver a cargarla
    if search_names:
        return search_names

    # Realizar una consulta SQL para obtener todos los nombres de los pacientes
    try:
        cursor = conn.cursor()
        sql_query_names = ("SELECT DISTINCT nombre FROM pacientes.pacientes_vit")
        cursor.execute(sql_query_names)
        names = cursor.fetchall()
        # Cerrar la conexión
        conn.close()
        cursor.close()
        search_names = [{'label': name['nombre'], 'value': name['nombre']} for name in names]
        return search_names

    except pymysql.Error as e:
        print('Error de MySQL:', e)
        return []

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data'),
     dcc.Dropdown(
        id='search-input',
        options=[],
        multi=False,
        placeholder="Buscar por nombre de paciente..."
    ),
    html.Button('Buscar', id='search-button', n_clicks=0),
    dash_table.DataTable(
        id='datatable',
        data=df_empty.to_dict('records') ,
        page_size=5
    )
])


# Callback para actualizar los datos de la tabla basados en la búsqueda
@app.callback(
    Output('datatable', 'data'),
    [Input('search-button', 'n_clicks')],
    [State('search-input', 'value')]
)
def update_table(n_clicks, search_value):
    if n_clicks > 0 and search_value:
        # Tu lógica de búsqueda aquí
        # Si el botón se ha clicado y hay un valor de búsqueda, realiza la búsqueda
        # Crear un objeto cursor para ejecutar consultas SQL
    
        print(search_value)

        try:
            # Ejecutar una consulta SQL
            cursor = conn.cursor()
            sql_query_search = ("SELECT fecha, identificacion, nombre, fec_nacimiento, sexo, peso, talla, (peso * 10000) / (talla*talla) AS IMC, " +
                "CASE " +
                "WHEN (peso * 10000) / (talla*talla) >= 30 THEN 'Obesidad' " +
                "WHEN (peso * 10000) / (talla*talla) >= 25 THEN 'Sobrepeso' " +
                "ELSE 'Saludable' " +
                "END AS 'Estado de IMC' " +
                "FROM pacientes.pacientes_vit " +
                "WHERE nombre LIKE '%"+search_value+"%'" +
                "ORDER BY fecha DESC")
                
            print(sql_query_search)
            cursor.execute(sql_query_search)

            # Obtener los resultados de la consulta como una lista de diccionarios
            results = cursor.fetchall()
            print(results)
            # Cerrar la conexión
            conn.close()
            cursor.close()

            # Crear un DataFrame a partir de los resultados
            df_search = pd.DataFrame(results)
            print(df_search)
            #Devolver los datos del DataFrame de búsqueda

            if not results:
                print("No se encontraron resultados para la búsqueda:", search_value)
                return []

            return df_search.to_dict('records')
        
        except pymysql.Error as e:
            print('Error de MySQL: ', e)
            return df_empty.to_dict('records')  

    else:
        # Si no se ha hecho clic en el botón o no hay un valor de búsqueda, devuelve datos vacíos o lo que sea apropiado
        # Si no hay valor de búsqueda, retornar un DataFrame vacío
        return df_empty.to_dict('records')  
    

    

"""""
def update_table(search_value):
    if search_value:
        # Filtrar los datos en función del valor de búsqueda
        filtered_data = df[df.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]
        return filtered_data.to_dict('records')
    else:
        # Si no hay valor de búsqueda, retornar un DataFrame vacío
        return df_empty.to_dict('records')   
"""""
    
    
# Run the app
if __name__ == '__main__':
    app.run(debug=True)