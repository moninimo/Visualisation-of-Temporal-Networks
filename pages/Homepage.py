from pydoc import classname

import dash
import dash_bootstrap_components as dbc
import pathlib

from app import app
import pandas as pd
from dash import dcc, html

PATH = pathlib.Path(__file__).parent

df = pd.DataFrame(
    {
        "Num (int)": [0,1,2,3,4],
        "node1 (str)": ["A", "B", "B", "C","D"],
        "node2 (str)": ["B", "C", "D","E","F"],
        "start (int)": [1,2,3,4,5],
        "end (int)": [2,3,4,5,6],
    }
)


layout = dbc.Container([
    html.Br(),
    
    html.H3('♬ A website to visualizing temproal network '),
    html.P('This website provides four methods to visulazing temporal network.'),
    
    dbc.CardGroup([
        dbc.Card(
                [
                    dbc.CardHeader("♫ Node Link 1 :"),
                    dbc.CardBody(
                        html.P("A series node-link diagrams on a timeline with constant node positions, and edges change over times.", className="card-text")
                    ),
                    dbc.CardLink("Link", href="/node_link1"),
                ],
            ),
        dbc.Card(
                [
                    dbc.CardHeader("♫ Node Link 2 :"),
                    dbc.CardBody(
                        html.P("A time-stamp decorated, aggregated graph. The labels of the edges denotes the contacts between the nodes.", className="card-text"),
                    ),
                    dbc.CardLink("Link", href="/node_link2"),
                ],
            ),
        dbc.Card(
                [
                    dbc.CardHeader("♫ Juxtaposed :"),
                    dbc.CardBody(
                        html.P("A node-centric time line, where a vertical line represents a contact between two connected individual at the time given by the x-axis.", className="card-text")
                    ),
                    dbc.CardLink("Link", href="/juxtaposed"),
                ],
            ),
        dbc.Card(
                [
                    dbc.CardHeader("♫ Animation :"),
                    dbc.CardBody(
                        html.P("A mapping of timestamps assigned to a sequence of graphs to visualization time results in an animated representation.", className="card-text")
                    ),
                    dbc.CardLink("Link", href="/animation"),
                ],
            )
            
    ]), 
    
    html.Br(),
    html.P('You can upload your own data to perform the visualization and get instant react graphs. ' ),
    dbc.Alert('Please note: the data format must be as follwing ', color="light"),
    dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
    html.P('Some example datasets are also aviable on Github, if needed.'), 
    
    html.Br(),
    html.Br(),
    html.P('The source code are aviable on :'), 
    dcc.Link(href='https://github.com/moninimo/Visualisation-of-Temporal-Networks'),
    ])
