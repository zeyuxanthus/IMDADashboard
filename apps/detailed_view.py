import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash import callback_context
import dash_bootstrap_components as dbc

import apps.backend as be
from app import app


layout = html.Div([
    html.Div([
        html.Div([
        html.Img(src=app.get_asset_url('luxoft.PNG'), 
                     id = 'corona-image',
                     style={'height': '100px',
                            'width': 'auto',
                            'text-align': 'center'})
        ], className='one-third column'),
        html.Div([
            html.P('Select Region: ', style = {'color': 'White', 'fontSize':40, 'text-align': 'center'}),
            dcc.Dropdown(["Singapore"],  id='region-dropdown')
        ], className='one-third column')
    ], id = 'header', className= 'row flex-display', style={'margin-bottom': '25px', 'margin-left':'50px'}),
    html.Div(id = 'body'),
    html.Div(id = 'info') 
], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

def getStudent(df):
    studentList = be.getStudent(df)
    return html.Div([
        html.Div([
            dcc.Dropdown(options = studentList, id = 'Student')
        ], className='one-third column'),
        html.Div(id ='student-id', className='one-half column', style = {"outline-style": "solid", "outline-color":"white"})
    ], className= 'row flex-display', style={'margin-top': '50px'})

def getModule(df):
    return html.Div([
        html.P(['Module'], style = {'color': 'White', 'fontSize':40, 'text-align': 'center'})
    ])

@app.callback(
    Output('student-id', 'children'),
    Input('Student', 'value'),
    Input('region-dropdown', 'value')
)
def student_id(value, region):
    if value is None:
        return dash.no_update 
    else:
        df = be.getDF(region)
        df = be.getStudentInfo(df, value)
        results = be.scores(df)
        project = be.project(df)
        return dbc.Card(
                [
                    dbc.CardImg(src=app.get_asset_url(f'{value}.PNG'), style = {'height': '200px','width': 'auto'}),
                    dbc.CardBody(
                        [
                            html.H4(f'Name: {value}', className="card-title", style = {'color': 'White'}),
                            html.P('Scores: ', style = {'color': 'White'}),
                            html.P(results, style = {'white-space': 'pre', 'color': 'White'}),
                            html.P(project, style = {'color': 'White'})
                        ]
                    ),
                ],
                style={"maxWidth": "540px"}
            )

@app.callback(
    Output('body', 'children'),
    Input('region-dropdown', 'value')
)
def update_output(value):
    if value is None:
        return dash.no_update 
    else:
        df = be.getDF(value)
        total, title, completed, t = be.getCount(df)
        return html.Div([
            html.P(f'{title}', style = {'color': 'White', 'fontSize':30, 'text-align': 'center'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.P('Total Canditates:', style = {'color': 'White', 'fontSize':20, 'text-align': 'center'}),
                        html.P(f'{total}', style = {'color': 'White', 'fontSize':30, 'text-align': 'center'}),
                        html.Div([
                            html.Button('View', id='submit-c', style = {'background-color': '#e7e7e7', 'color': 'black'})
                        ],style = {'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}, n_clicks=0)
                    ])
                ], className='one-half column'),
                html.Div([
                    html.Div([
                        html.P('Modules Completed:', style = {'color': 'White', 'fontSize':20, 'text-align': 'center'}),
                        html.P(f'{completed}/{t}', style = {'color': 'White', 'fontSize':30, 'text-align': 'center'}),
                        html.Div([
                            html.Button('View', id='submit-m', style = {'background-color': '#e7e7e7', 'color': 'black'})
                        ],style = {'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}, n_clicks=0)
                    ])
                ], className='one-half column')
                
            ], className= 'row flex-display', style={'margin-bottom': '25px'})
        ])

@app.callback(
    Output('info', 'children'),
    Input('region-dropdown', 'value'),
    Input('submit-c', 'n_clicks'),
    Input('submit-m', 'n_clicks')
)
def submit_update(region, c, m):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    df = be.getDF(region)

    if 'submit-c' in changed_id:
        children = getStudent(df)
    elif 'submit-m' in changed_id:
        children = getModule(df)
    return children