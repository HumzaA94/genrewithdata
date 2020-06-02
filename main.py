from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash

import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import sqlalchemy
import psycopg2
import time
import re

from tabs import dropdown_tab, query_tab, tab_functions as tf, variables as var

########### Initiate the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title='GenreWithData'

competitions=tf.read_sql('SELECT DISTINCT "COMPETITION_NAME" as "Competitions", "COMPETITION_ID" from statsbomb.competition_information order by 1;')
seasons=tf.read_sql('SELECT DISTINCT "SEASON_NAME" as "Seasons", "SEASON_ID" from statsbomb.competition_information order by 1;')
comp_dict=dict(zip(competitions['Competitions'],competitions['COMPETITION_ID']))
season_dict=dict(zip(seasons['Seasons'],seasons['SEASON_ID']))

app.layout = html.Div([
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Filtering Option', value='tab-1-example'),
        dcc.Tab(label='SQL Interaction', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example'),
    dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab =='tab-1-example':
        return dropdown_tab.tab_1_layout
    elif tab == 'tab-2-example':
        return query_tab.tab_2_layout


#callbacks for dropdown_tab
@app.callback(Output('table-story','children'),
              [Input('table-dropdown','value')])
def get_data_background(val):
    if val is None:
        return html.Div(style={'display': 'none'})
    else:
        val1='''
        #### Background of Data

        {}'''.format(var.intro_dict[val])

        return dcc.Markdown(val1)

@app.callback(Output('table-filtering-container','children'),
              [Input('table-dropdown','value')])
def selecting_filtering_option(val):
    time.sleep(3)
    if val is None:
        return html.Div(style={'display': 'none'})
    elif 'nba' in val:
        marks= dict(zip(var.nba_year_keys, var.nba_year_values))
        return (
            html.Div(id='nba-filtering-options',
                     className='containers',
                     children=[
                         html.Div(id='filtering-story'),
                         dcc.Graph(id='nba-graph'),
                         html.Br(),
                         html.Div(id='explaining-filter'),
                         tf.generate_range_slider('nba-player-range',1992,2020,marks)]),
            html.Div(id='nba-datatable',className='containers'))
    else:
        return (
            html.Div(id='soccer-filtering-options',className='containers',
                     children=[
                         html.Div(id='filtering-story'),
                         dcc.Graph(id='soccer-graph'),
                         html.Br(),
                         html.Div(id='soccer-dropdown-options',
                                  children=[
                                      tf.multi_value_dropdown('comp_dropdown', 'Filter through the Comptitions',competitions['Competitions']),
                                      tf.multi_value_dropdown('season_dropdown', 'Filter through the Seasons',seasons['Seasons'])])]),
            html.Div(id='soccer-datatable',className='containers'))

@app.callback(Output('filtering-story','children'),
              [Input('table-dropdown','value')])
def create_content(tab_val):
    if tab_val is None:
        return html.Div(style={'display': 'none'})
    elif 'nba' in tab_val:
        string_val=var.filtering_string_dict['nba'][0]
        return dcc.Markdown(string_val)
    elif 'statsbomb' in tab_val:
        string_val=var.filtering_string_dict['statsbomb'][0]
        return dcc.Markdown(string_val)

@app.callback(Output('explaining-filter','children'),
              [Input('table-dropdown','value')])
def create_content(tab_val):
    if tab_val is None:
        return html.Div(style={'display': 'none'})
    elif 'nba' in tab_val:
        string_val=var.filtering_string_dict['nba'][1]
        return dcc.Markdown(string_val)
    elif 'statsbomb' in tab_val:
        string_val=var.filtering_string_dict['statsbomb'][1]
        return dcc.Markdown(string_val)


@app.callback(Output('nba-graph','figure'),
              [Input('table-dropdown','value'),
               Input('nba-player-range','value')])
def create_graph(tab_val,val2):
    try:
        min_val=val2[0]
        max_val=val2[1]
        string='''select distinct ("SEASON"),COUNT(distinct ("PLAYER NAME" )) as  "Number of Players in Season" from {}
        where ("SEASON" >= '{}') and ("SEASON" <='{}')  group by 1 order by 1 ;'''.format(tab_val,min_val,max_val)
        df=tf.read_sql(string)
        df.to_csv('test.csv')
        fig=go.Figure()
        fig.add_trace(go.Bar(
            x=[i for i in np.arange(min_val+1,max_val+1)],
            y=df['Number of Players in Season'],
            marker_color='rgb(55, 83, 109)',
                ))
        fig.update_layout(
            title={
                'text':"Number of Players Involved per Season between {} - {}".format(min_val+1,max_val),
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis=dict(tickmode = 'linear',
                       tick0=int(min_val),
                       dtick=1))
        return fig
    except ValueError as e:
        return None

@app.callback(Output('nba-datatable', 'children'),
              [Input('table-dropdown','value'),
               Input('nba-player-range','value')])
def displayClick(tab_val,val2):
    try:
        min_val=val2[0]
        max_val=val2[1]
        string='''select * from {} where ("SEASON" >= '{}') and ("SEASON" <='{}');'''.format(tab_val,min_val,max_val)
        df=tf.read_sql(string)
        return html.Div(children=
                        [dcc.Markdown(var.table_string),
                         tf.create_table('nba_query_table',df,20)])
    except AttributeError as e:
        return html.Div(style={'display':'none'})

@app.callback(Output('soccer-graph','figure'),
              [Input('table-dropdown','value'),
               Input('comp_dropdown','value'),
               Input('season_dropdown','value')])
def create_graph(val1,val2,val3):
    try:
        comp_val=[comp_dict[i] for i in val2]
        comp_val=tuple(comp_val)
        season_val=[season_dict[i] for i in val3]
        season_val=tuple(season_val)
        val1='statsbomb.competition_information'
        val='{} {} {}'.format(val1,comp_val,season_val)
        string='''
        select "COMPETITION_NAME" as "Competitions","SEASON_NAME" as "Seasons", count(distinct "MATCH_ID" ) as "Number of Games" from {}
        where ("COMPETITION_ID" in {}) and ("SEASON_ID" in {})
        group by 1,2
        order by 1 DESC,2 ASC;'''.format(val1,comp_val,season_val)
        df=tf.read_sql(string)
        fig = px.bar(df, x='Competitions', y='Number of Games',color='Seasons',barmode='group')
        fig.update_layout(
            title={
                'text':"Number of Games per Season by Competition",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
                showlegend=False)
        return fig
    except:
        return None

@app.callback(Output('soccer-datatable', 'children'),
              [Input('table-dropdown','value'),
               Input('comp_dropdown','value'),
               Input('season_dropdown','value')])
def displayClick(tab_val,val2,val3):
    comp_val=[comp_dict[i] for i in val2]
    comp_val=tuple(comp_val)
    season_val=[season_dict[i] for i in val3]
    season_val=tuple(season_val)
    tab_val='statsbomb.competition_information'
    string='''select * from {} where ("COMPETITION_ID" in {}) and ("SEASON_ID" in {});'''.format(tab_val,comp_val,season_val)
    df=tf.read_sql(string)
    for c in df.columns:
        if c in var.dict_columns:
            df[c]=df[c].astype(str)
    return html.Div(children=
                    [dcc.Markdown(var.table_string),
                     tf.create_table('soccer_query_table',df,20)])


#callbacks for query_tab
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
            val1='SELECT * FROM {} LIMIT 10;'.format(var.button_dict[button_val])
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
                if c in var.dict_columns:
                    df[c]=df[c].astype(str)
            return html.Div(tf.create_table('query_table',df,10))


########### Run the app
if __name__ == '__main__':
    server.run(debug=True, port=8080)
