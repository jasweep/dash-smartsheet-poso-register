import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import createEntry

# token layout?
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[html.H1('Index Page')])
])


# handle routes
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
         return createEntry.layout
    else:
        return '404'

# run the server
if __name__ == '__main__':
    app.run_server(debug=True)
