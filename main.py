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
import re

from tabs import dropdown_tab, query_tab, tab_functions as tf

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='GenreWithData'
########### Set up the layout

app.layout = html.Div([
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
# #callbacks for query_tab
@app.callback(Output('intermediate-value','children'),
              [Input('button_1', 'n_clicks'),
               Input('button_2', 'n_clicks'),
               Input('button_3','n_clicks'),
               Input('button_4','n_clicks'),
               Input('button_21','n_clicks')],
              [State('sql_script','value')])
def update_query(btn1,btn2,btn3,btn4,btn21,val):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    try:
        button_val=re.split("\.",changed_id)[0]
        if button_val=='button_21':
            return val
        else:
            val1='SELECT * FROM {} LIMIT 10;'.format(tf.button_dict[button_val])
            return  val1
    except KeyError as e:
        return None

@app.callback(Output('output-container', 'children'),
              [Input('intermediate-value', 'children')])
def displayClick(val):
    if val is None:
        return html.Div(style={'display': 'none'})
    else:
        df=tf.read_sql(val)
        if isinstance(df,str):
            return html.Div(children=[df])
        else:
            for c in df.columns:
                if c in tf.dict_columns:
                    df[c]=df[c].astype(str)
            return html.Div(tf.create_table('query_table',df,10))
########### Run the app
if __name__ == '__main__':
    server.run(debug=True, port=8080)
