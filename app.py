import dash
import smartsheet
import pandas as pd

# SS helper functions
def getCellVal(register, row, col):
    return register['rows'][row - 1]['cells'][col - 1]['value']

def getColIndexes(register):
    colDict = {}
    for col in register['columns']:
        ID = col['title']
        colDict[ID] = col['index']
    return colDict

def getContractors(register):
    msaCols = getColIndexes(register)
    contractorIdx = msaCols['Contractor']
    contractorArr = []
    for row in register['rows']:
        contractorArr.append(row['cells'][contractorIdx]['value'])
    return contractorArr

def getDataFrame(register):
    colData = [col['title'] for col in register['columns']]
    rowData = []
    for row in register['rows']:
        rowTuple = ()
        for cell in row['cells']:
            try:
                rowTuple += (cell['value'],)
            except KeyError:
                rowTuple += ('',)
        rowData.append(rowTuple)
    return pd.DataFrame.from_records(rowData, columns=colData)

# ESTABLISH SMARTSHEET CONNECTION AND COLLECT DATA
ss_client = smartsheet.Smartsheet('7zfex45sf0mcijlu9pk4wutr7t')
ss_client.errors_as_exceptions(True)

posoReg = ss_client.Sheets.get_sheet(4125811084158852, include=[
    'attachments',
    'crossSheetReferences',
    'discussions',
    'format'
]).to_dict()
posoDF = getDataFrame(posoReg)

msaReg = ss_client.Sheets.get_sheet(8038705605699460, include=[
    'attachments',
    'crossSheetReferences',
    'discussions',
    'format'
]).to_dict()
msaDF = getDataFrame(msaReg)

# get list of contractors from MSA Sheet data
contractors = getContractors(msaReg)


# Setup Dash App
app = dash.Dash()
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})
server = app.server
app.config.suppress_callback_exceptions = True
