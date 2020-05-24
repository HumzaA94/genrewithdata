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
########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='GenreWithData'
########### Set up the layout


dict_columns = ['TACTICS','PASS', 'CARRY', 'UNDER_PRESSURE', 'BALL_RECEIPT', 'COUNTERPRESS',
                'INTERCEPTION', 'DRIBBLE', 'GOALKEEPER', 'SHOT', 'OUT', 'DUEL', 'BALL_RECOVERY',
                'CLEARANCE', 'OFF_CAMERA', 'FOUL_WON', 'FOUL_COMMITTED', 'SUBSTITUTION',
                'INJURY_STOPPAGE', 'MISCONTROL', '50_50', 'BAD_BEHAVIOUR', 'BLOCK', 'PLAYER_OFF',
                'HOME_COUNTRY', 'AWAY_COUNTRY', 'STADIUM_COUNTRY', 'REFEREE_COUNTRY']
button_dict={
    'button_1':'statsbomb.competition_information',
    'button_2':'statsbomb.match_information',
    'button_3':'nba_reference.player_overall_seasons',
    'button_4':'nba_reference.player_stats_by_game'
    }

def generate_banner(title):
    return html.Label(children=title)


app.layout = html.Div([
    generate_banner('Improve the banner style, want to keep the get info here?'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Tab One', value='tab-1-example'),
        dcc.Tab(label='Query Tab', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
])
########### Run the app
if __name__ == '__main__':
    server.run(debug=True, port=8080)
