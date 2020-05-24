from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash

import plotly.graph_objs as go
import pandas as pd
import sqlalchemy
import psycopg2

from tabs import dropdown_tab, query_tab, tab_functions as tf

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='GenreWithData'
########### Set up the layout

app.layout = html.Div([
    tf.generate_banner('Improve the banner style, want to keep the get info here?'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Tab One', value='tab-1-example'),
        dcc.Tab(label='Query Tab', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab =='tab-1-example':
        return dropdown_tab.tab_1_layout
    elif tab == 'tab-2-example':
        return query_tab.tab_2_layout

########### Run the app
if __name__ == '__main__':
    server.run(debug=True, port=8080)
