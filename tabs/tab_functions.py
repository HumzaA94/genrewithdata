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

import os




try:
    engine = sqlalchemy.create_engine(os.environ.get('AWS_DATABASE_URL'))
except:
    print("Unable to connect to db")

def read_sql(string, engine=engine):
    try:
        df = pd.read_sql(string, con=engine)
        return df

    except sqlalchemy.exc.ProgrammingError as e:
        msg=str(e)
        return msg

def create_table(div_id,df,page_no):
    return (dash_table.DataTable(
        id=div_id,
        columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= page_no,
        export_format='csv',
        style_table={'overflowX': 'scroll'},
        style_cell = {
                'text_align': 'center'}))

def generate_banner(title):
    return html.Label(children=title)

def generate_button(val,btn_id,outline=True):
    return dbc.Button(val, id=btn_id, outline=outline,className="buttons",n_clicks=0)

def generate_range_slider(div_id,min,max,marks):
    return dcc.RangeSlider(
        id=div_id,
        min=min,
        max=max,
        step=1,
        marks=marks,
        value=[min, max])

def single_value_dropdown(div_id,label_name,list1,text):
    return html.Div(
    children = [      #if more than 1 container will have the exact feature, a classname might be more convenient
    html.H5(children=label_name),
    html.Br(),
    dcc.Dropdown(
            id= div_id, #container_id used to design the container of the dropdown in css,
            options=[{'label': l, 'value': l} for l in list1],
            placeholder=text,
            style={'display':'inline-block','width':'400px','height':'30px'})])

def multi_value_dropdown(div_id,label_name,list1):
    return html.Div(
    children = [
    html.Label(children=label_name),
    html.Br(),
    dcc.Dropdown(
    id= div_id,
    options=[{'label': l, 'value': l} for l in list1],
    value=list1,
    style={'display':'inline-block','width':'500px','height':'150px'},
    multi=True
    ),],
    )
