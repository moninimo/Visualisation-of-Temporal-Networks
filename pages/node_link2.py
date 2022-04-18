import io
import base64
import pathlib
import pandas as pd
from app import app

import dash_cytoscape as cyto
cyto.load_extra_layouts()

import dash_bootstrap_components as dbc
from xml.dom.minidom import Element
from dash import Input, Output, State, dcc, html, dash_table, callback


PATH = pathlib.Path(__file__).parent

sidebar = html.Div(
    [
        html.Label('Pleas upload the data :'),
        dcc.Upload(html.Button('Upload File'),id='upload-data-nodelink2',
            multiple=False),
        html.Label('Pleas choose a graph layout :'),
        dcc.Dropdown(
            id='dropdown-update-layout',
            value='spread',
            clearable=False,
            options=[
                {'label': name.capitalize(), 'value': name}
                for name in ['spread','grid', 'random', 'circle', 'cose', 'concentric','klay',
                             'dagre','euler','cola']
            ]
        ),
    ],
)

edges = []
nodes = []

layout = html.Div(
    [
        html.Hr(),
        dcc.Store(id='store-data-nodelink2',data=[]),
        dbc.Row([
        dbc.Col(sidebar,md=2),
        dbc.Col([
            cyto.Cytoscape(
                id='graph-nodelink2',
                elements = edges+nodes ,
                layout = {'name': 'spread'},
                style={'height': '70vh'},
                stylesheet = [
                    {
                    'selector': 'node',
                    'style':{ 
                        'background-color': '#BFD7B5',
                        'content': 'data(label)'} 
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'line-color': '#A3C4BC',
                            'curve-style': 'bezier',
                            'source-arrow-shape': 'triangle',
                            'label': 'data(label)'                            
                        }
                    },
                ],
            )], md=10),
        ])
    ]
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

def getelements(df):  
    cy_edges = []
    cy_nodes = []
    nodes = set()
    header = df.columns.values

    for index, row in df.iterrows():
        source, target = row[header[1]], row[header[2]]
        tstart,tend = row[header[3]], row[header[4]]
        label =list(range(tstart,tend+1))

        if source not in nodes:
            nodes.add(source)
            cy_nodes.append({"data": {"id": source, "label": source}})
        if target not in nodes:
            nodes.add(target)
            cy_nodes.append({"data": {"id": target, "label": target}})
        cy_edges.append({
                        'data': {
                            'source': source,
                            'target': target,
                            'label' : str(label),
                        }
                    })
    return cy_nodes+cy_edges



@callback(Output('store-data-nodelink2', 'data'),
            Input('upload-data-nodelink2', 'contents'),
            Input('upload-data-nodelink2', 'filename'))
def generateGraph(contents,filename):  
    df = parse_data(contents,filename)   
    return df.to_dict('records')


@callback( 
    Output('graph-nodelink2', 'elements'),
    Input('store-data-nodelink2', 'data'))
def update_figure(data):
    df = pd.DataFrame(data)
    elements = getelements(df)    
    return elements


@app.callback(Output('graph-nodelink2', 'layout'),
              Input('dropdown-update-layout', 'value'))
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }