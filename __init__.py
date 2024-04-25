import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dashboard_all_patients import layout_dashboard1
from dashboard_patient import layout_dashboard2, callbacks_dashboard2
import sys
print(sys.executable)

# Utilizando Bootstrap para obtener estilos predefinidos
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                html.H1("Bienvenido a ControlVit Lab", style={'margin-bottom': '20px'}),
                html.H4("Aquí podrás visualizar tableros para los pacientes."),
                html.H4("Selecciona cualquiera de las dos opciones."),
            ], style={'textAlign': 'center', 'margin': '50px'}),
            # Botones para los dashboards
            dbc.Row([
                dbc.Col(dbc.Button("Búsqueda por Paciente", color="primary", href="/dashboard1")),
                dbc.Col(dbc.Button("Ver Todos los Pacientes", color="primary", href="/dashboard2")),
            ], style={'margin': 'auto', 'width': '50%', 'textAlign': 'center', 'marginTop': '50px'}),
        ])
    if pathname == '/dashboard1':
        return layout_dashboard1()
    elif pathname == '/dashboard2':
        return layout_dashboard2()
    else:
        return '404 Página no encontrada'
    
callbacks_dashboard2(app)

if __name__ == '__main__':
    app.run_server(debug=True)