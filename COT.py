import cot_reports as cot
import pandas as pd
from matplotlib import pyplot as plt
import plotly.graph_objects as go 
import numpy as np

import matplotlib.pyplot as plt

from dash import dcc,html ,Dash,Output,Input,State


# from dash.dependencies import Output,Input,State
import plotly.graph_objects as go


import plotly.express as px

# from jupyter_dash import JupyterDash



import dash_bootstrap_components as dbc
import yfinance as yf
from datetime import datetime as dt

pd.set_option('display.max_columns', None)
yahoo_tk_fut={
    "ES=F": "E-Mini S&P 500",
    "YM=F": "Mini Dow Jones Indus",
    "NQ=F": "Nasdaq 100 Mar",
    "RTY=F": "E-mini Russell 2000 Index",
    "ZB=F": "U.S. Treasury Bond Futures",
    "ZN=F": "10-Year T-Note Futures",
    "ZF=F": "Five-Year US Treasury Note Futu",
    "ZT=F": "2-Year T-Note Futures",
    "GC=F": "Gold",
    "MGC=F": "Micro Gold Futures",
    "SI=F": "Silver",
    "SIL=F": "Micro Silver Futures",
    "PL=F": "Platinum",
    "HG=F": "Copper",
    "PA=F": "Palladium",
    "CL=F": "Crude Oil",
    "HO=F": "Heating Oil",
    "NG=F": "Natural Gas",
    "RB=F": "RBOB Gasoline",
    "BZ=F": "Brent Crude Oil Last Day Finan",
    "B0=F": "Mont Belvieu LDH Propane (OPIS)",
    "ZC=F": "Corn Futures",
    "ZO=F": "Oat Futures",
    "KE=F": "KC HRW Wheat Futures",
    "ZR=F": "Rough Rice Futures",
    "ZM=F": "Soybean Meal Futures",
    "ZL=F": "Soybean Oil Futures",
    "ZS=F": "Soybean Futures",
    "GF=F": "Feeder Cattle Futures",
    "HE=F": "Lean Hogs Futures",
    "LE=F": "Live Cattle Futures",
    "CC=F": "Cocoa",
    "KC=F": "Coffee",
    "CT=F": "Cotton",
    "LBS=F": "Lumber",
    "OJ=F": "Orange Juice",
    "SB=F": "Sugar"

}


year_now=dt.now().year
df=pd.DataFrame()
years_back=3

for x in range(years_back):
    new_data=cot.cot_year(year = year_now-x, cot_report_type = 'legacy_fut')
    df=pd.concat([df,new_data],axis=0)

# Define the title for the app
mytitle = dcc.Markdown(children='# App that analyzes COT')

## Define the graph
graph1 = dcc.Graph(id='graph1', figure={})
graph2 = dcc.Graph(id='graph2', figure={})

## Define components to use in the app
dropdown1 = dcc.Dropdown(id='graph2-dropdown1',options=df['Market and Exchange Names'].unique(),clearable=False)
dropdown2 = dcc.Dropdown(id='graph2-dropdown2',options=yahoo_tk_fut,clearable=False)

## Define components to use in the app

## Customize your layout
app = Dash(external_stylesheets=[dbc.themes.CYBORG])
app.layout = dbc.Container([
        mytitle,
        dbc.Row(
            [dropdown1,
            dbc.Col(dcc.Markdown('## COT position'), width=12),
            dbc.Col(graph1, width=12),
            ]
        ),
        dbc.Row(
            [dropdown2,
            dbc.Col(dcc.Markdown('## markets datas'), width=12),
            dbc.Col(graph2, width=12)
            ]
        ),
        ],fluid=True)

## Callback allows components to interact
@app.callback(
    Output(graph1, component_property='figure'),
    Input(dropdown1, component_property='value')
)
def update_graph(user_input):  # Function arguments come from the component property of the input
    df_select=df[df['Market and Exchange Names']==user_input].copy()
    df_select.set_index("As of Date in Form YYYY-MM-DD",inplace=True)
    df_select=df_select.iloc[:,7:9]
    print(df_select)

    
    df_select["net long"]=df_select.iloc[:,0]-df_select.iloc[:,1]
    df_select.sort_index(inplace=True)
    fig=px.line(df_select)
    fig.update_layout(title=f'{user_input}',legend={'orientation': 'h', 'y':0, 'yanchor': 'bottom', 'x': 0.5, 'xanchor': 'center'})
    return fig

# Callback to update the second graph
@app.callback(
    Output(graph2, 'figure'),
    Input(dropdown2,'value')
)

def update_graph2(user_input):
    df_select = yf.download(user_input ,interval ="1d", period=f'{years_back}y')[["Close"]]
    fig.update_layout(title=f'{user_input}', legend={'orientation': 'h', 'y': 0, 'yanchor': 'bottom', 'x': 0.5, 'xanchor': 'center'})
    return fig
if __name__ == '__main__':
   app.run_server( port=8000)