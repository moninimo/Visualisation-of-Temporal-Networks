
from cProfile import label
import dash
import pandas as pd
from dash import Dash, html,Input,Output,dcc,State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash.exceptions import PreventUpdate
# Load extra layouts
cyto.load_extra_layouts()

app = Dash(__name__)
df = pd.read_csv('datasets\\test.csv')

df = df.head(10)
nodes = set()

def getelements(df):  
    cy_nodes = []
    cy_edges = []
    nodes = set()
    header = df.columns.values

    for index, row in df.iterrows():
        source, target = row[header[1]], row[header[2]]
        tstart,tend = row[header[3]], row[header[4]]
        label =list(range(tstart,tend))

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
    return cy_nodes



def getnodes(df): 
    nodes = []
    header = df.columns.values

    for index, row in df.iterrows():
        source, target = row[header[1]], row[header[2]]
        if source not in nodes:
            nodes.append(source)
        if target not in nodes:
            nodes.append(target)
    return nodes

# def getedges(nodes,x):
#     cy_edges = [] 
#     header = df.columns.values
#     for index, row in df.iterrows():
#         source, target = row[header[1]], row[header[2]]
#         tstart,tend = row[header[3]], row[header[4]]
#         label =list(range(tstart,tend))
        
        
#         cy_edges.append({
#                         'data': {
#                             'source': source,
#                             'target': target,
#                             'label' : label,
#                         }
#                     })
#     return cy_nodes

app.layout = html.Div([
cyto.Cytoscape(
                id='graph-nodelink2',
                elements = getelements(df) ,
                layout = {'name': 'spread'},
                style={'height': '70vh'},
                stylesheet = [
                    {
                    'selector': 'node',
                    'style':{ 
                        'background-color': '#BFD7B5',
                        'content': 'data(label)',
                        'label': 'data(label)'},
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
            )
])


x = []
y = []
for i in range(df['tstart'][1],df['tend'][1]):
    x.extend((i,i))
    y.extend((df['node1'][1],df['node2'][1]))
    
    
print(y[1]+' to '+y[2])

# if __name__ == '__main__':
#     app.run_server(debug=True)