from dash import html
from dash import Dash, html, dash_table, dcc
from bd_conf import conn
import pandas as pd
import pymysql
from dash_bootstrap_components import Row, Col, Button, Card, CardBody, Container
from joblib import load
import joblib

import numpy as np

def layout_analytics():
    return html.Div([
        html.H3('Reporte de Registro Actual de Pacientes', style={"margin": "30px 10px"})
    ])