from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash

from tabs import tab_functions as tf

tab_2_layout= html.Div([
    html.Div(id="information_container",
             children=[
                 html.Div(id="sql_container",
                          children=[
                              dcc.Textarea(id="sql_script",placeholder='You can write your SQL query here.\nNot sure how the data looks like or the column names? \nClick on one of the tables to find out.',
                                           style={'width': '80%', 'height': 300},),
                              dbc.Button('Submit',id="button_21",className="buttons",n_clicks=0)],
                          className='containers'),
                 html.Div( id="table_list_container",
                          children=[
                              html.H4('List of Tables Available'),
                              tf.generate_button(tf.button_dict['button_1'],"button_1"),
                              tf.generate_button(tf.button_dict['button_2'],"button_2"),
                              tf.generate_button(tf.button_dict['button_3'],"button_3"),
                              tf.generate_button(tf.button_dict['button_4'],"button_4")],
                          className='containers')]),
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Br(),
    html.Div(id="output-container",className='containers'),
    ])
