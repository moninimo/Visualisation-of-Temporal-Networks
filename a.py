import dash
import io
import base64
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html,Input,Output,dcc,State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash.exceptions import PreventUpdate
# Load extra layouts
cyto.load_extra_layouts()

app = Dash(__name__)

df = pd.read_csv('datasets\\test.csv')
df = df.head(10)


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


fig = go.Figure()

x1 = []
y1 = []
for i in range(df['tstart'][1],df['tend'][1]):
    x1.extend((i,i,i))
    y1.extend((df['node1'][1],df['node2'][1],None))
    

fig.add_trace(go.Scatter( 
        x = x1,
        y = y1,
        name = 'Test 1',
        connectgaps= False
    ))

x2 = []
y2 = []
for i in range(df['tstart'][2],df['tend'][2]):
    x2.extend((i,i,i))
    y2.extend((df['node1'][2],df['node2'][2],None))
    
fig.add_trace(go.Scatter( 
        x = x2,
        y = y2,
        name = 'Test 2',
        connectgaps= False
    ))



app.layout = html.Div([    
    dcc.Upload(html.Button('Upload File'),id='upload-data-jutaposed',
            multiple=False),
    dcc.Store(id='store-data-jutaposed',data=[]),
    html.Div(id='output_data', style={'font-size':36}),
    dcc.Graph(id='juxtaposed-graph',figure= fig)
    
])

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

@app.callback(Output('store-data-jutaposed', 'data'),
            Input('upload-data-jutaposed', 'contents'),
            Input('upload-data-jutaposed', 'filename'))
def generateGraph(contents,filename):  
    df = parse_data(contents,filename)   
    return df.to_dict('records')

@app.callback(
    Output('juxtaposed-graph','figure'),
    Input('store-data-jutaposed', 'data'))
def update_graph(data):
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
    

if __name__ == '__main__':
    app.run_server(debug=True)
