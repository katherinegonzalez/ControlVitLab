# Importar el controlador pymysql en lugar de MySQLdb
import pymysql
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

