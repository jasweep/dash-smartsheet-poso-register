# import modules
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt

from app import app, msaReg, getCellVal, getColIndexes, posoDF, msaDF


# MODEL (actual python logic for SS interaction)

'''This should handle all the relationships between the relevant sheets.

Best option would be to use Pandas dataframe queries to perform DB like
relational queries

Should also be method heavy so that the callback functions can modify data
without having to re-build the model'''

contractors = msaDF['Contractor'].tolist()
contractorOptions = [{'label': entry, 'value': entry} for entry in contractors]

services = msaDF['Services'].unique().tolist()
serviceOptions = [{'label': entry, 'value': entry} for entry in services]

# VIEW (layout) -- CREATION PAGE LOOK
layout = html.Div(className='fluid-container', children=[
    html.H1('CREATE ENTRY PAGE'),
    html.Div(className='contractorDiv', children=[
        html.H4('Contractor'),
        dcc.Dropdown(
            options=contractorOptions
        )
    ]),

    html.Div(className='serviceDiv', children=[
        html.H4('Service'),
        dcc.Dropdown(
            options=serviceOptions,
        )
    ]),

    html.Div(className='startDateDiv', children=[
        html.H4('Start Date'),
        dcc.DatePickerSingle(
            id='startDatePicker',
            date=dt(2018, 6, 25)
        )
    ]),

    html.Div(className='transportDiv', children=[
        html.H4('Transportation'),
        dcc.Dropdown(
            options=[
                {'label': "Tri-Star providing", 'value': 'DRL'},
                {'label': "Contractor providing", 'value': 'CMT'},
                {'label': "What transport?", 'value': 'WRL'}
            ],
            value=''
        )
    ]),

    html.Div(className='keyPersDiv', children=[
        html.H4('Key Personnel'),
        dcc.Textarea(
            placeholder='Please enter key personnel on a new line each...',
            value='',
            style={'width': '100%', 'height': '100%'}
        )
    ]),

    html.Div(className='submitDiv', children=[
        html.Button('Submit', id='submitButton')
    ])

])


# CONTROLLER (callbacks)
