import dash_bootstrap_components as dbc
import pandas as pd
from dash import  dcc, Input, Output, html,ctx
import dash
import plotly.express as px
import plotly.graph_objects as go

logo_path= 'assets/gai'
output = pd.read_csv('output.csv')
dates= pd.to_datetime(output['Timestamp'])
options =output['Company_Name'].unique()


layout = dbc.Container([
    html.Div([
            html.H2("Company:",style={'text-align':'left','width':'88%','display':'inline-block','color':'white'}),
            html.H4("SDG DASHBOARD",style={'textAlign':'right','display':'inline-block','color':'white'}),
            dcc.Dropdown(id='dropdown',options = options,placeholder="Select a Company",style={'verticalAlign':'top','width':'40%','display':'inline-block'}),
        html.Div([html.Img(src="assets/GAI logo-8.jpg",style={'verticalAlign':'top'})],style={'text-align':'right'})
    ]),
    html.Div(html.H2("COMPANY NAME", id='company_name', style={'margin-left': '5%', 'color': '#008fb3'})),
    html.Div([
        html.H3("Sector",style={'color':'white'}),
        html.H3(id="sector",style={'color':'#008fb3'})
    ],style={'display':'inline-block','margin-left':'2%'}),
    html.Div([
        html.H3("Ticker",style={'color':'white'}),
        html.H3(id="ticker",style={'color':'#008fb3'})
    ],style={'display':'inline-block','margin-left':'15%'}),
    html.Div([
        html.H3("ISIN",style={'color':'white'}),
        html.H3(id="isin",style={'color':'#008fb3'})
    ],style={'display':'inline-block','margin-left':'15%'}),
    html.Div(html.Button("Update Graphs",id='updatebutton',n_clicks=0,style={"border":"2px black solid",'color':'white','background':'grey','width':'8%','height':'4vh'})),
    html.Center(html.H3("COMPANY Statistics",id="company_stats",style={'color':'#008fb3'})),
    html.Center(html.H3("Todays Date",id="date",style={'color':'#008fb3','margin-top':'-1%'})),
    html.Div([
        html.H6("SDG Short-Term Score",style={'color':'white'}),
        html.H6("SDG Short-Term Score",style={'color':'#008fb3'})],style={'display':'inline-block','margin-left':'10%'}),
    html.Div([
        html.H6("SDG Long-Term Score", style={'color': 'white'}),
        html.H6("SDG Long-Term Score", style={'color': '#008fb3'})],style={'display':'inline-block','margin-left':'7%'}),
    html.Div([
        html.H6("Industry Percentile(STS_Mean)", style={'color': 'white'}),
        html.H6("Industry Percentile(STS_Mean)", style={'color': '#008fb3'})],style={'display':'inline-block','margin-left':'7%'}),
    html.Div([
        html.H6("Industry Percentile(LTS_Mean)", style={'color': 'white'}),
        html.H6("Industry Percentile(LTS_Mean)", style={'color': '#008fb3'})],style={'display':'inline-block','margin-left':'7%'}),
    html.Div([
        html.H6("Momentum 1-Week", style={'color': 'white'}),
        html.H6("Momentum 1-Week", style={'color': '#008fb3'})],style={'display':'inline-block','margin-left':'7%'}),
    html.Div([
        html.H6("Momentum 30-Day", style={'color': 'white'}),
        html.H6("Momentum 30-Day", style={'color': '#008fb3'})],style={'display':'inline-block','margin-left':'7%'}),
    html.Div([
        dcc.Graph(id='spydergram', style={'height': '30%', 'width': '33%', 'display': 'inline-block','background':'black'}),
        dcc.Graph(id='speedometer', style={'height': '30%', 'width': '34%', 'display': 'inline-block','background':'black'}),
        dcc.Graph(id='hist', style={'height': '30%', 'width': '33%', 'display': 'inline-block','background':'black'}),
    ],style={'background': 'Black'}),
    html.Div(dcc.DatePickerRange(id='datepicker',min_date_allowed=dates.min(),max_date_allowed=dates.max(),initial_visible_month=dates.min(),end_date=dates.max()),style={'border-color':'black','background-color':'black'}),
    dcc.Dropdown(id='dropdown2',options=['SDG_Mean','SDG_1', 'SDG_2', 'SDG_3','SDG_4', 'SDG_5', 'SDG_6','SDG_7', 'SDG_8', 'SDG_9','SDG_10', 'SDG_11', 'SDG_12','SDG_13', 'SDG_14', 'SDG_15','SDG_16', 'SDG_17'], multi=True,style={'width':'35vh'}),
    html.Div([
        dcc.Graph(id='stsfig',style={'height': '30%', 'width': '50%','display': 'inline-block','background':'black'}),
        dcc.Graph(id='ltsfig', style={'height': '30%', 'width': '50%','display': 'inline-block','background':'black'}),
    ],style={'background': 'Black'}),
    ],style={'background':'black','border':'black','margin':'0'})

app = dash.Dash(__name__)
server = app.server
app.layout=layout

@app.callback(Output('company_name', 'children'),
              [Input('dropdown', 'value')])
def update_company_name(input_value):
    return f'{input_value.upper()}'

@app.callback(Output('sector', 'children'),
              [Input('dropdown', 'value')])
def update_sector(input_value):
    sector = output[output["Company_Name"].isin([input_value])]['GICS Sector'].unique()
    return sector

@app.callback(Output('ticker', 'children'),
              [Input('dropdown', 'value')])
def update_ticker(input_value):
    ticker = output[output["Company_Name"].isin([input_value])]['Ticker'].unique()
    return ticker

@app.callback(Output('isin', 'children'),
              [Input('dropdown', 'value')])
def update_isin(input_value):
    isin = output[output["Company_Name"].isin([input_value])]['ISIN'].unique()
    return isin

@app.callback(Output('company_stats', 'children'),
              [Input('dropdown', 'value')])
def update_isin(input_value):
    return f'{input_value.upper()} Statistics'

@app.callback(Output('date', 'children'),
              [Input('dropdown', 'value')])
def update_isin(input_value):
    return output.tail(1)["Timestamp"]


@app.callback(Output('spydergram', 'figure'),
              [Input('dropdown', 'value'),
               Input('updatebutton', 'n_clicks')])
def update_sts(input_value,updatebutton):
    if "updatebutton" == ctx.triggered_id:
        attempt = output.set_index("Timestamp")
        attempt = attempt[attempt["Company_Name"].isin([input_value])]
        attempt = attempt.tail(1)[
            ["STS_1", "STS_2", 'STS_3', 'STS_4', 'STS_5', 'STS_6', 'STS_7', 'STS_8', 'STS_9', 'STS_10', 'STS_11',
             'STS_12', 'STS_13', 'STS_14', 'STS_15', 'STS_16', 'STS_17']].T
        attempt2 = attempt.squeeze()
        fig = px.line_polar(attempt2, r=attempt2, theta=attempt2.index, line_close=True)
        fig.update_layout(title_text=f"{input_value} STS_SDG", title_x=0.5)
        fig.update_polars(bgcolor="black")
        fig.layout.paper_bgcolor = 'black'
        fig.layout.plot_bgcolor = 'black'
    else:
        fig = go.Figure()
    return fig


@app.callback(Output('speedometer', 'figure'),
              [Input('dropdown', 'value'),
               Input('updatebutton', 'n_clicks')])
def update_sts_dates(dropdown,updatebutton):
    if "updatebutton" == ctx.triggered_id:
        attempt=output[output["Company_Name"].isin([dropdown])].max()
        fig = go.Figure(go.Indicator(mode="gauge+number", value=float(attempt['STS_Mean']), domain={'x': [0, 1], 'y': [0, 1]}))
        fig.update_layout(title_text=f"STS SDG Score", title_x=0.5)
        fig.layout.paper_bgcolor = 'black'
        fig.layout.plot_bgcolor = 'black'
    else:
        fig = go.Figure()
    return fig

@app.callback(Output('hist', 'figure'),
              [Input('dropdown', 'value'),
               Input('updatebutton', 'n_clicks')])
def update_sts(input_value,updatebutton):
    if "updatebutton" == ctx.triggered_id:
        attempt = output[output['Company_Name'] == input_value].set_index('Ticker').sort_values('Timestamp')[
            ['STS_1', 'STS_2', 'STS_3', 'STS_4', 'STS_5', 'STS_6', 'STS_7', 'STS_8', 'STS_9', 'STS_10', 'STS_11',
             'STS_12', 'STS_13', 'STS_14', 'STS_15', 'STS_16', 'STS_17']].mean()
        fig = px.histogram(x=attempt.index, y=attempt).update_layout(yaxis_title='')
        fig.update_layout(title_text=f"{input_value} STS_SDG", title_x=0.5)
        fig.update_layout(xaxis_title='')
        fig.layout.paper_bgcolor = 'black'
        fig.layout.plot_bgcolor = 'black'
    else:
        fig=go.Figure()
    return fig

@app.callback(Output('stsfig', 'figure'),
              [Input('dropdown', 'value'),
               Input('updatebutton', 'n_clicks'),
               Input('datepicker','start_date'),
               Input('datepicker','end_date'),
               Input('dropdown2','value')])
def update_stsfig(dropdown,updatebutton,start_date,end_date,dropdown2):
    if "updatebutton" == ctx.triggered_id:
        if dropdown2 is not None:
            dropdown2.append('STS_Mean')
            sdata =output[output["Company_Name"].isin([dropdown])].set_index('Timestamp')
            sdata=sdata.T.loc[dropdown2].T
        else:
            sdata = output[output["Company_Name"].isin([dropdown])].set_index('Timestamp')['STS_Mean']
        if start_date and end_date is None:
            fig = px.line(sdata)
        if start_date is None and end_date is not None:
            sdata = sdata.loc[:end_date]
            fig = px.line(sdata)
        if start_date is not None and end_date is None:
            sdata = sdata.loc[start_date:]
            fig = px.line(sdata)
        if start_date and end_date is not None:
            sdata = sdata.loc[start_date:end_date]
            fig = px.line(sdata)
        fig.update_layout(title_text=f"STS Data over time", title_x=0.5)
        fig.layout.paper_bgcolor = 'black'
        fig.layout.plot_bgcolor = 'black'
    else:
        fig=go.Figure()
    return fig

@app.callback(Output('ltsfig', 'figure'),
              [Input('dropdown', 'value'),
               Input('updatebutton', 'n_clicks'),
               Input('datepicker','start_date'),
               Input('datepicker','end_date'),
               Input('dropdown2','value')])
def update_stsfig(dropdown,updatebutton,start_date,end_date,dropdown2):
    if "updatebutton" == ctx.triggered_id:
        if dropdown2 is not None:
            dropdown2.append('LTS_Mean')
            sdata =output[output["Company_Name"].isin([dropdown])].set_index('Timestamp')
            sdata=sdata.T.loc[dropdown2].T
        else:
            sdata = output[output["Company_Name"].isin([dropdown])].set_index('Timestamp')['LTS_Mean']
        if start_date and end_date is None:
            fig = px.line(sdata)
        if start_date is None and end_date is not None:
            sdata = sdata.loc[:end_date]
            fig = px.line(sdata)
        if start_date is not None and end_date is None:
            sdata = sdata.loc[start_date:]
            fig = px.line(sdata)
        if start_date and end_date is not None:
            sdata = sdata.loc[start_date:end_date]
            fig = px.line(sdata)
        fig.update_layout(title_text=f"LTS Data over time", title_x=0.5)
        fig.layout.paper_bgcolor = 'black'
        fig.layout.plot_bgcolor = 'black'
    else:
        fig=go.Figure()
    return fig


if __name__ == '__main__':
    app.run_server()