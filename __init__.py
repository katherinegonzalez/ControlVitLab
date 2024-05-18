import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dashboard_all_patients import layout_dashboard1
from dashboard_patient import layout_dashboard_patient, update_table, update_gauge_heart_rate, update_gauge_diastolic, update_gauge_sistolic, update_search_options, showOrHideFigures, update_time_series_plot_frecuencia_cardiaca, update_time_series_plot_sistolica, update_time_series_plot_diastolica, get_available_dates
from dashboard_analytics import layout_analytics, update_graphs
from bd_conf import conn
import pandas as pd
import sys
from urllib.parse import parse_qs, urlparse

print(sys.executable)

# Utilizando Bootstrap para obtener estilos predefinidos
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, 'tableStyles.css'])

# Layout de la página
app.layout = html.Div([
    # Componente dcc.Location para detectar cambios en la URL
    dcc.Location(id='url', refresh=False),
    # Barra de navegación
    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.NavbarBrand("ControlVit Lab", className="navbar-text"),  # Nombre de la aplicación
                href="#"
            )
        ]),
        color="primary",
        dark=True
    ),
    # Contenedor principal
    html.Div([       
        # Contenedor para mostrar el contenido del dashboard seleccionado
        html.Div(id='page-content')
    ])
])

# Definir callbacks si es necesario

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.Div([
            html.Div([
                html.H1("¡Bienvenidos a ControlVit Lab!", style={'margin-bottom': '30px'}),
                html.H4("En esta plataforma, podrás acceder a tableros con información detallada sobre los pacientes."),
                html.H4("Elige una de las siguientes opciones para comenzar:"),
            ], style={'textAlign': 'center', 'margin': '50px'}),
            # Botones para los dashboards
            dbc.Row([
                dbc.Col([
                    dbc.Button("Búsqueda por Paciente", color="primary", href="/dashboard-paciente", style={'marginBottom': '20px'}),
                    html.P("Encuentra información específica sobre un paciente.")
                ]),
                dbc.Col([
                    dbc.Button("Ver Pacientes y Alertas", color="primary", href="/dashboard-alertas", style={'marginBottom': '20px'}),
                    html.P("Revisa el estado y las alertas de todos los pacientes.")
                ]),
                dbc.Col([
                    dbc.Button("Análisis de Datos de Pacientes", color="primary", href="/dashboard-analitica", style={'marginBottom': '20px'}),
                    html.P("Explora y analiza los datos de los pacientes para obtener información valiosa.")
                ])
            ], style={'margin': 'auto', 'width': '50%', 'textAlign': 'center', 'marginTop': '50px'}),
        ])
    if pathname == '/dashboard-alertas':
        return layout_dashboard1()
    elif pathname == '/dashboard-paciente':
        return layout_dashboard_patient()
    elif '/dashboard-paciente' in pathname:
        return layout_dashboard_patient()
    elif pathname == '/dashboard-analitica':
        return layout_analytics()
    else:
        return '404 Página no encontrada'
    
#--------------------------------------------

try:
    # Callback para cargar los nombres e identificaciones de los pacientes en el dropdown
    @app.callback(
        Output('search-input', 'options'),
        [Input('search-input', 'search_value')],
    )
    def update_search_options_callback(search_value):
        return update_search_options()
    
    @app.callback(
        Output('search-input', 'value'),
        [Input('url', 'pathname'),
        Input('url', 'search')]
    )
    def update_dropdown_value(pathname, search):
        if search:
            # Parse the URL query parameters
            query_params = parse_qs(urlparse(search).query)
            patient_id = query_params.get('patient', [None])[0]
            if patient_id:
                return patient_id
        elif 'patient' in pathname:
            patient_id = pathname.split('patient=')[1]
            if patient_id:
                return patient_id

        return dash.no_update
    
    @app.callback(
        Output('search-button', 'n_clicks'),
        [Input('url', 'pathname'),
        Input('url', 'search')]
    )
    def simular_clic(pathname, search):
        if search:
            # Parse the URL query parameters
            query_params = parse_qs(urlparse(search).query)
            patient_id = query_params.get('patient', [None])[0]
            if patient_id:
                return 1
        elif 'patient' in pathname:
            patient_id = pathname.split('patient=')[1]
            if patient_id:
                return 1
        return 0
 
    # Callback para actualizar los datos de la tabla basados en la búsqueda
    @app.callback(
        Output('datatable', 'data'),
        [Input('search-button', 'n_clicks')],
        [State('search-input', 'value')],
    )
    def update_table_callback(n_clicks, search_value):
        return update_table(n_clicks, search_value)
    
     # Callback para mostrar 
    @app.callback(
        Output('container', 'style'),
        [Input('datatable', 'data')]
    )
    def show_callback(table_data):
        return showOrHideFigures(table_data)

    # Callback para actualizar el gráfico de Gauge con la frecuencia cardíaca
    @app.callback(
        Output('gauge-graph-heart-rate', 'figure'),
        [Input('datatable', 'data')]
    )
    def update_gauge_heart_rate_callback(table_data):
        return update_gauge_heart_rate()

    # Callback para actualizar el gráfico de Gauge con presión diastólica
    @app.callback(
        Output('gauge-graph-diastolic', 'figure'),
        [Input('datatable', 'data')]
    )
    def update_gauge_diastolic_callback(table_data):
        return update_gauge_diastolic()

    # Callback para actualizar el gráfico de Gauge con presión sistólica
    @app.callback(
        Output('gauge-graph-sistolic', 'figure'),
        [Input('datatable', 'data')]
    )
    def update_gauge_sistolic_callback(table_data):
        return update_gauge_sistolic()
    
    # Callback para el gráfico de tiempo de la frecuencia cardiaca
    @app.callback(
        Output('time-series-plot-frecuencia-cardiaca', 'figure'),
        [Input('time-series-button', 'n_clicks')],
        [State('radio-buttons', 'value')],
        [State('date-picker-range', 'start_date')],
        [State('date-picker-range', 'end_date')],
        [State('search-input', 'value')]
    )
    def update_time_series_plot_frecuencia_cardiaca_callback(n_clicks, type_value, start_date, end_date, search_value):
        return update_time_series_plot_frecuencia_cardiaca(n_clicks, type_value, start_date, end_date, search_value)
    # Callback para el gráfico de tiempo de la presión sistólica
    
    @app.callback(
        Output('time-series-plot-sistolica', 'figure'),
        [Input('time-series-button', 'n_clicks')],
        [Input('time-series-plot-frecuencia-cardiaca', 'figure')],
        [State('radio-buttons', 'value')],
        [State('date-picker-range', 'start_date')],
        [State('date-picker-range', 'end_date')],
        [State('search-input', 'value')]
    )
    def update_time_series_plot_sistolica_callback(n_clicks, figure, type_value, start_date, end_date, search_value):
        return update_time_series_plot_sistolica(n_clicks, type_value, start_date, end_date, search_value)
    
    # Callback para el gráfico de tiempo de la presión diastólica
    @app.callback(
        Output('time-series-plot-diastolica', 'figure'),
        [Input('time-series-button', 'n_clicks')],
        [Input('time-series-plot-sistolica', 'figure')],
        [State('radio-buttons', 'value')],
        [State('date-picker-range', 'start_date')],
        [State('date-picker-range', 'end_date')],
        [State('search-input', 'value')]
    )
    def update_time_series_plot_diastolica_callback(n_clicks, figure, type_value, start_date, end_date, search_value):
        return update_time_series_plot_diastolica(n_clicks, type_value, start_date, end_date, search_value)
    
    # Callback para mostrar u ocultar el gráfico de Gauge
    @app.callback(
        Output('gauge-graph-diastolic', 'style'),
        [Input('datatable', 'data')]
    )
    def toggle_gauge_visibility_callback(table_data):
        return showOrHideFigures(table_data)
        
    @app.callback(
        Output('gauge-graph-sistolic', 'style'),
        [Input('datatable', 'data')]
    )
    def toggle_gauge_visibility_callback(table_data):
        return showOrHideFigures(table_data)

    @app.callback(
        Output('gauge-graph-heart-rate', 'style'),
        [Input('datatable', 'data')]
    )
    def toggle_gauge_visibility_callback(table_data):
        return showOrHideFigures(table_data)

    @app.callback(
        Output('date-picker-range', 'dates'),
        [Input('datatable', 'data')],
        [State('search-input', 'value')],
    )
    def update_date_picker(data_table, search_value):
        return get_available_dates(data_table,search_value)
        
    # Callback para mostrar u ocultar los graficos de series
    @app.callback(
        Output('time-series-plot-frecuencia-cardiaca', 'style'),
        [Input('datatable', 'data')]
    )
    def toggle_time_series_visibility_callback(table_data):
        return showOrHideFigures(table_data)

    @app.callback(
        Output('time-series-plot-sistolica', 'style'),
        [Input('datatable', 'data')]
    )
    def toggle_time_series_visibility_callback(table_data):
        return showOrHideFigures(table_data)
        
    @app.callback(
        Output('time-series-plot-diastolica', 'style'),
        [Input('datatable', 'data')]
    )
    def toggle_time_series_visibility_callback(table_data):
        return showOrHideFigures(table_data)
    
    # Condicional para Layaout:


    # Callback para actualizar los gráficos según la selección del usuario
    @app.callback(
        Output('cluster-graphs', 'children'),
        [Input('cluster-dropdown', 'value')],
        [Input('datatable_riesgo_total', 'data')]
    )
    def update_graphs_callback(selected_cluster, table_data):
        return update_graphs(selected_cluster)
    
    @app.callback(
        Output("url", "pathname"),
        Input("datatable_pacientes", "active_cell"),
        State("datatable_pacientes", "derived_viewport_data"),
    )
    def cell_clicked(cell, data):
        print('cell', cell)
        if cell:
            print('data', data[cell["row"]])
            selected = data[cell["row"]][cell["column_id"]]
            print('selected: ', selected)
            id= data [cell["row"]]['id_cia']
            print(id)

            return f"/dashboard-paciente?patient={id}"
            
        else:
           return dash.no_update
        

except Exception as e:
        print('Error: ', e)



if __name__ == '__main__':
    app.run_server(debug=False)