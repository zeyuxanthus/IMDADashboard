import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash

from app import app
from app import server

from apps import overview,detailed_view

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Link('Overview',href='/apps/overview')
        ], className = 'column'),
        html.Div([
            dcc.Link('Detailed view',href='/apps/detailed_view')
        ], className = "column", style = {"margin-bottom":"50px"})
    ], className="row"),
    dcc.Location(id='url',refresh=False),
    html.Div(id='page-content',children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/overview':
        return overview.layout
    if pathname == '/apps/detailed_view':
        return detailed_view.layout
    else:
        return dash.no_update 


if __name__ == '__main__':
    app.run_server(debug=False)

