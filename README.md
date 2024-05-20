# ControlVit Lab 👩‍⚕️

ControlVit Lab es una aplicación para el monitoreo de pacientes con Insuficiencia Cardíaca, permite visualizar dashboards con datos y alertas de los pacientes, para permitr tomar decisiones informadas.

Este proyecto ha sido implementado como proyecto de grado de la maestría en Ingeniería de Sistemas y Computación de la Pontificia Universidad Javeriana. Si deseas ver el dcumento académico del proyecto haz cick en el siguiente link:
[Artículo: Desarrollo de una aplicación Web para la detección temprana de tizón en cultivos de papa](https://livejaverianaedu-my.sharepoint.com/:b:/g/personal/lorenamora_javeriana_edu_co/EWRiNSZrOrhOuHjOvNxHt8QBVyWLa_gstnHQ9tu2szDjkw)

Dentro de este repositorio se encuentran la aplicación Web implementada en DashPlotly con Python.

# Estructura de Carpetas 📂

Las carpetas se estructuran de la siguiente manera:
- **/**: En la raíz del proyecto se encuentra el código de Dashplotly de la Aplicación Web.
- **/modeloClustering**: Contiene los datos agrupados de los pacientes resultantes del modelo de analítica K means.
- **/modelosClasificación**: Contienen los modelos de clasficacón de árbol de decisión previamente entrenados para clasificar los datos de los acientes.
- **/bd_config**: En este archivo se encuentran los datos de configuración para realizar la conexión con la base de datos del Proyecto.  

## Librerias 📋

* [Dashplotly](https://dash.plotly.com/): Esta librería fue usada para la implementación de toda la apicación web.
* [PyMysql](https://pypi.org/project/pymysql/): Esta librería fue usada para la conexión y el manejo de peticiones a la base de datos.
* [Scikit-learn](https://scikit-learn.org/stable/): Esta librería se usó para realizar la predcción de datos de los pacientes con los modelos entrenados.
* [Joblib](https://joblib.readthedocs.io/en/stable/): Esta librerá se usó para carcgar los modelos de clasificación previamente entrenados.
* [Pandas](https://pandas.pydata.org/): Esta librería se usó para el manejo de los datos del pryecto.
* [Numpy](hhttps://numpy.org/): Esta librería se usó para el manejo de los datos del pryecto.
* [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/): Esta librería se usó para manejar los estilos y el diseño de la aplicación.

## Instalación 💻 

Para instalar y configurar el proyecto en tu ambiente local, sigue los siguientes pasos:

1. Clona el repositorio: `git clone https://github.com/katherinegonzalez/ControlVitLab.git`
3. Instala las siguientes dependencias: 

    * `pip3 install dash`
    * `pip3 install pandas`
    * `pip3 install numpy`
    * `pip3 install dash-bootstrap-components`
    * `pip3 install pymysql`
    * `pip install joblib`
    * `pip3 install -U scikit-learn`

##  Ejecución del Proyecto 💻 

Para ejecutar el proyecto en tu ambiente local:

1. Ve al archivo bd_conf.py
2. Modifca todos los datos de conexón a la base de datos para que la aplicacón se conecte a la tuya:

project_id = ''
instance_connection_name = ''
database_name = 'pacientes'
db_user = ''
db_password = ''

instance_ip = ''
instance_port = '3306'

2. Ve al terminal, en la raíz del proyecto.
2. Ejecuta el comando `python3 __init__.py`, de esta manera se ejecuta el servidor en nuestro ambiente local, generalmente en el puerto `8050` - `http://127.0.0.1:8050/`

## Notebooks Google Colab

[Procesamiento y Preparación de Datos](https://colab.research.google.com/drive/1uybCczm1rgscE6-nKgsTDxsk7ej8LrlT?usp=sharing)

[Modelo de Clasificación](https://colab.research.google.com/drive/1uybCczm1rgscE6-nKgsTDxsk7ej8LrlT?usp=sharing)

[Modelo de Clustering](https://colab.research.google.com/drive/1GJ2jNuapbhR6rumOdeU8XhfQGRjD-iVC?usp=sharing)

## Github repository 📦

[GithubPapApp](https://github.com/katherinegonzalez/ClasificadorTizonTemprano)

## Autora 😊

Katherine Xiomar González Santacruz  
