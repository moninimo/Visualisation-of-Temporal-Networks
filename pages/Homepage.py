from pydoc import classname
import dash
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import pathlib

from app import app
from dash import Input, Output, dcc, html

PATH = pathlib.Path(__file__).parent

layout = dbc.Container([
    html.H3('This is the home page'),
    ])
