import base64
from importlib.resources import contents
import io

import pathlib

from app import app
import pandas as pd
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html, dash_table, callback


PATH = pathlib.Path(__file__).parent

sidebar = html.Div(
    [
        html.Label('Pleas upload the data :'),
        dcc.Upload(html.Button('Upload File'),id='upload-data-jutaposed',
            multiple=False),
    ],
)


fig = go.Figure()

layout = dbc.Container(
    [
        html.Hr(),
        dcc.Store(id='store-data-jutaposed',data=[]),
        dbc.Row([
        dbc.Col(sidebar,md=2),
        dbc.Col([
            dcc.Graph(id='juxtaposed-graph',figure= fig)],md=10),
        ])
    ],
    fluid=True,
)

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df

@callback(Output('store-data-jutaposed', 'data'),
            Input('upload-data-jutaposed', 'contents'),
            Input('upload-data-jutaposed', 'filename'))
def generateGraph(contents,filename):  
    df = parse_data(contents,filename)   
    return df.to_dict('records')


@callback(
    Output('juxtaposed-graph','figure'),
    Input('store-data-jutaposed', 'data'))
def update_graph(data):
    df = pd.DataFrame(data)
    header = df.columns.values
    fig = go.Figure()
    for index, row in df.iterrows():
        source, target = row[header[1]], row[header[2]]
        tstart,tend = row[header[3]], row[header[4]]
        nodes = []
        edges = []
        line_name = source + ' to ' + target
        
        for i in range(tstart,tend):
            nodes.extend((i,i,i))
            edges.extend((source,target,None))
    
        fig.add_trace(go.Scatter( 
        x = nodes,
        y = edges,
        name = line_name,
        connectgaps= False))
    return fig