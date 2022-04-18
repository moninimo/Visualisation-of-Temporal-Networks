import io

import base64
import pathlib
import pandas as pd
from app import app
import dash_cytoscape as cyto
cyto.load_extra_layouts()

import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html,callback


PATH = pathlib.Path(__file__).parent

sidebar = html.Div(
    [
        html.Label('Pleas upload the data :'),
        dcc.Upload(html.Button('Upload File'),id='upload-data-animation',
            multiple=False),
        html.Label('Pleas choose a graph layout :'),
        dcc.Dropdown(
            id='dropdown-update-layout',
            value='circle',
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
        dcc.Store(id='store-data-animation',data=[]),
        dbc.Row([
        dbc.Col(sidebar,md=2),
        dbc.Col([
            dcc.Interval(id="animate", disabled=True),
            html.Label('Click play to start:'),
            dbc.Row(
            html.Div(
                [
                dbc.Button("Play",id="play", outline=True, color="primary", className="me-1"),
                dcc.Slider(id='timeSlider-animation',min=0,max=0,value=0),
                ],
                style={"display": "grid", "grid-template-columns": "5% 95%"}
            )),
            dbc.Row(
            cyto.Cytoscape(
                id='graph-animation',
                elements = edges+nodes ,
                layout = {'name': 'grid'},
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
                        }
                    },
                ],
            ))
        ], md=10),
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

def getelements(df,num):  
    cy_edges = []
    cy_nodes = []
    nodes = set()
    header = df.columns.values

    for index, row in df.iterrows():
        source, target = row[header[1]], row[header[2]]
        tstart,tend = row[header[3]], row[header[4]]

        if source not in nodes:
            nodes.add(source)
            cy_nodes.append({"data": {"id": source, "label": source}})
        if target not in nodes:
            nodes.add(target)
            cy_nodes.append({"data": {"id": target, "label": target}})
        if tstart<=num and num<=tend:
            cy_edges.append({
                'data': {
                    'source': source,
                    'target': target
                }
            })
    return cy_nodes+cy_edges


#Store the data
@callback(Output('store-data-animation', 'data'),
            Input('upload-data-animation', 'contents'),
            Input('upload-data-animation', 'filename'))
def generateGraph(contents,filename):  
    df = parse_data(contents,filename)   
    return df.to_dict('records')



@callback(
            Output('timeSlider-animation', 'min'),
            Output('timeSlider-animation', 'max'),
            Input('store-data-animation', 'data'))
def generateGraph(data): 
    df = pd.DataFrame(data)
    return df.iloc[:,3].min(), df.iloc[:,4].max()


@app.callback(
    Output("graph-animation", "elements"),
    Output("timeSlider-animation", "value"),
    Input("animate", "n_intervals"),
    State("timeSlider-animation", "min"),
    State("timeSlider-animation", "max"),
    State('store-data-animation', 'data'),
    State("timeSlider-animation", "value"),
    prevent_initial_call=True,
)
def update_figure(n, min,max,data,value):
    if value == 0:
        value = min    
    index = value
    index = (index + 1) % max
    df = pd.DataFrame(data)
    return getelements(df,index),index

@app.callback(
    Output("animate", "disabled"),
    Input("play", "n_clicks"),
    State("animate", "disabled"),
)
def toggle(n, playing):
    if n:
        return not playing
    return playing

@app.callback(Output('graph-animation', 'layout'),
              Input('dropdown-update-layout', 'value'))
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }