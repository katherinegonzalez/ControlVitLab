from dash import dcc

import dash
from dash import Dash, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dashboard_all_patients import layout_dashboard1
from dashboard_patient import layout_dashboard2

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Página inicial'),
    dcc.Link('Ir al Dashboard 1', href='/dashboard1'),
    dcc.Link('Ir al Dashboard 2', href='/dashboard2')
])

app.layout = html.Div([
    html.H1('Página inicial'),
    dcc.Link('Ir al Dashboard 1', href='/dashboard1'),
    dcc.Link('Ir al Dashboard 2', href='/dashboard2'),
    html.Div(id='page-content')
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboard1':
        return layout_dashboard1()
    elif pathname == '/dashboard2':
        return layout_dashboard2()
    else:
        return '404 Página no encontrada'

if __name__ == '__main__':
    app.run_server(debug=True)