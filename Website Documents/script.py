import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import os
cwd = os.getcwd()
import numpy as np

app = Dash(__name__)
server = app.server
# df = pd.read_csv(r"C:\Users\siddh\Projects\Stock Market Manipulation\project_base.csv")
df = pd.read_csv(f'{cwd}/project_base.csv')
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(children = [

    html.H1("Detection of Stock Market Manipulation using Market Structure", style={'text-align': 'center'}),
    dcc.Dropdown(id="slct_co",
                 options=[
                     {"label":x, "value":x} for x in df.sort_values('Company')['Company'].unique()],
                 multi=False,
                 value="Reliance Industries Ltd",
                 style={'width': "35%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='my_map', figure={})
])
# # ------------------------------------------------------------------------------
# # Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_map', component_property='figure')],
    [Input(component_id='slct_co', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Analysis of number of shares of {}.".format(option_slctd)
    # Plotly Express
    dff = df.copy()
    dff = dff[(dff['Company'] == option_slctd)]
    dff['ld'] = dff['No.of Shares'].apply(lambda x:str(x)[0])
    dfff = dff['ld'].value_counts(normalize = True).to_frame().mul(100).round(1)
    dfff['index'] = dff['ld'].value_counts(normalize = True).index
    dffff = dfff.sort_values(by=['index'])
    fig = px.bar(dffff,x = 'index',y = 'ld',labels={
                     "index": "Leading digit of Number of shares",
                     "ld": "Percentage Occurence"
                 },text = 'ld')
    fig.update_traces(hovertemplate='Occurence: %{y:.2f%}')
    # pio.write_html(fig, file=r"C:\Users\siddh\Desktop\stock_market\index.html", auto_open=True)
    return container, fig
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
    
