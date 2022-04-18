import dash

from ast import Div
import dash_bootstrap_components as dbc
from dash import Input, Output,dcc,html
import os

# Connect to main app.py file
from app import app
from app import server


from pages import Homepage,node_link1,node_link2,animation,juxtaposed

app_name = os.getenv("DASH_APP_PATH", "/Homepage")

nav = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home Page", href="/Homepage")),
        dbc.NavItem(dbc.NavLink("Node Link 1", href="/node_link1")),
        dbc.NavItem(dbc.NavLink("Node Link 2", href="/node_link2")),
        dbc.NavItem(dbc.NavLink("Animation", href="/animation")),
        dbc.NavItem(dbc.NavLink("Juxtaposed", href="/juxtaposed")),
    ],
    brand_href="#",
    dark= True,
    color="primary",
    links_left= True,
    fluid=True,
    expand="xl",
)

app.layout = dbc.Container(
    [
        html.H2("Visualisation of temporal networks"),
        dcc.Location(id='url', refresh=False),
        nav,
        html.Div(id='page-content', children=[]),
    ],
    fluid= True,
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/Homepage":
        return Homepage.layout
    elif pathname == '/node_link1':
        return node_link1.layout
    elif pathname == '/node_link2':
        return node_link2.layout
    elif pathname == '/animation':
        return animation.layout
    elif pathname == '/juxtaposed':
        return juxtaposed.layout
    else:
        return Homepage.layout
    
if __name__=='__main__':
    app.run_server(debug=False)