from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash

from tabs import tab_functions as tf
import pandas as pd

table_names=sorted(tf.button_dict.values(),reverse=False)

tab_1_layout = html.Div(
    id="app-container",
    children=[
        html.Br(),
        html.Div(id='table-selection-container',
        children=[
            tf.single_value_dropdown("table-dropdown","Choosing Your Data",table_names,"Select a table from the following..."),
            html.Div(id='table-story'),]),
        # tf.multi_value_dropdown('multi-dropdown',"Continent selections",table_names),
        html.Div(id="table-filtering-container")])
