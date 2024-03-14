import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

#List some template for graphs to use : we use dark
plotly_built_in_templates = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
#CSS for the website
external_stylesheets = [dbc.themes.DARKLY]
#Create app with Dash and define name and stylesheet
app = Dash(name="IOT Visualisation App - JSS", external_stylesheets=external_stylesheets)
#Configure the html layout:
app.layout = html.Div(
    html.Div([
        html.H2('IOT Visualisation JSS'), #Title of html page
        html.Br(), #retour à la ligne
        dcc.Graph(id='live-update-graph-temp'), #graphique temp
        html.Br(),
        dcc.Graph(id='live-update-graph-hum'),
        html.Br(),
        dcc.Graph(id='live-update-graph-lum'),
        html.Br(),
        dcc.Graph(id='live-update-graph-vib'),
        dcc.Interval( #Configure interval of update graphs
            id='interval-component',
            interval=1*60000,  # in milliseconds : per one minute
            n_intervals=0
        )
    ])
)


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph-temp', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live_temp(n):

    # Collect some data
    #df = pd.read_csv('IOTdata.csv')
    dfarduino = pd.read_csv('IOTArduinoData.csv')
    dfnucleo = pd.read_csv('IOTNucleoData.csv')
    if len(dfnucleo) < len(dfarduino):
        dfarduino = dfarduino.head(len(dfnucleo))
    else:
        dfnucleo = dfnucleo.head(len(dfarduino))
    # Create the graph
    #df['Timestamp'] = df[['Time', 'Date']].apply(' '.join, axis=1)
    dfarduino['Timestamp'] = dfarduino[['Time', 'Date']].apply(' '.join, axis=1)
    # Convert the 'timestamp' column to datetime type
    #dfarduino['Timestamp'] = pd.to_datetime(dfarduino['Timestamp'])
    #              color='Device name', template=plotly_built_in_templates[2])
    fig = px.line(dfarduino, x='Timestamp', y=['Temperature (°C)', dfnucleo['Temperature (°C)']], title='Temperature',
                  template=plotly_built_in_templates[2])
    # Keep user settings (zoom, pan, etc.) for graph and
    # change axis labels depending on number of ticks recorded
    fig.update_layout(uirevision="Don't change",  xaxis_tickformatstops=[
        dict(dtickrange=[None, 1000], value="%H:%M ms"),
        dict(dtickrange=[1000, 60000], value="%H:%M s"),
        dict(dtickrange=[60000, 3600000], value="%H:%M m"),  # One month of recordings = 43 200
        dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
        dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
        dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
        dict(dtickrange=["M1", "M12"], value="%b '%y M"),
        dict(dtickrange=["M12", None], value="%Y Y")
    ], xaxis_title='Timestamp', yaxis_title='Temperature (°C)')
    newnames = {'Temperature (°C)': 'Arduino', 'wide_variable_1': 'Nucleo'}
    fig.for_each_trace(lambda t: t.update(name=newnames[t.name], legendgroup=newnames[t.name],
                                          hovertemplate=t.hovertemplate.replace(t.name, newnames[t.name])))
    fig.update_traces(mode='markers+lines')
    # Return fig
    return fig


@app.callback(Output('live-update-graph-hum', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live_hum(n):

    # Collect some data
    #df = pd.read_csv('IOTdata.csv')
    dfarduino = pd.read_csv('IOTArduinoData.csv')
    dfnucleo = pd.read_csv('IOTNucleoData.csv')
    if len(dfnucleo) < len(dfarduino):
        dfarduino = dfarduino.head(len(dfnucleo))
    else:
        dfnucleo = dfnucleo.head(len(dfarduino))
    dfarduino['Timestamp'] = dfarduino[['Time', 'Date']].agg(' '.join, axis=1)
    #dfarduino['Timestamp'] = pd.to_datetime(dfarduino['Timestamp'])
    # Clip all values with extremely large resistance values to 0% RH
    dfarduino.loc[(dfarduino['Humidity (%RH)'] > 100), 'Humidity (%RH)'] = 0
    # Create the graph
    #fig = px.line(df, x=df['Timestamp'], y=df['Humidity (%RH)'], title='Humidity levels',
    #              color='Device name', template=plotly_built_in_templates[2])
    fig = px.line(dfarduino, x='Timestamp', y=['Humidity (%RH)', dfnucleo['Humidity (%RH)']], title='Humidity levels',
                  template=plotly_built_in_templates[2])
    fig.update_layout(uirevision="Don't change",  xaxis_tickformatstops=[
        dict(dtickrange=[None, 1000], value="%H:%M ms"),
        dict(dtickrange=[1000, 60000], value="%H:%M s"),
        dict(dtickrange=[60000, 3600000], value="%H:%M m"),  # One month of recordings = 43 200
        dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
        dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
        dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
        dict(dtickrange=["M1", "M12"], value="%b '%y M"),
        dict(dtickrange=["M12", None], value="%Y Y")
    ], xaxis_title='Timestamp', yaxis_title='Humidity (%RH)')
    newnames = {'Humidity (%RH)': 'Arduino', 'wide_variable_1': 'Nucleo'}
    fig.for_each_trace(lambda t: t.update(name=newnames[t.name], legendgroup=newnames[t.name],
                                          hovertemplate=t.hovertemplate.replace(t.name, newnames[t.name])))
    fig.update_traces(mode='markers+lines')
    return fig


@app.callback(Output('live-update-graph-vib', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live_vib(n):

    # Collect some data
    #df = pd.read_csv('IOTdata.csv')
    dfarduino = pd.read_csv('IOTArduinoData.csv')
    dfnucleo = pd.read_csv('IOTNucleoData.csv')
    if len(dfnucleo) < len(dfarduino):
        dfarduino = dfarduino.head(len(dfnucleo))
    else:
        dfnucleo = dfnucleo.head(len(dfarduino))
    dfarduino['Timestamp'] = dfarduino[['Time', 'Date']].agg(' '.join, axis=1)
    #dfarduino['Timestamp'] = pd.to_datetime(dfarduino['Timestamp'])
    # Create the graph
    fig = px.line(dfarduino, x='Timestamp', y=['Vibration', dfnucleo['Vibration']], title='Device vibration detection',
                  template=plotly_built_in_templates[2])
    fig.update_layout(uirevision="Don't change",  xaxis_tickformatstops=[
        dict(dtickrange=[60000, 3600000], value="%H:%M m"),  # One month of recordings = 43 200
        dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
        dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
        dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
        dict(dtickrange=["M1", "M12"], value="%b '%y M"),
        dict(dtickrange=["M12", None], value="%Y Y")
    ], xaxis_title='Timestamp', yaxis_title='Vibration State')
    newnames = {'Vibration': 'Arduino', 'wide_variable_1': 'Nucleo'}
    fig.for_each_trace(lambda t: t.update(name=newnames[t.name], legendgroup=newnames[t.name],
                                          hovertemplate=t.hovertemplate.replace(t.name, newnames[t.name])))
    fig.update_traces(mode='markers+lines')
    return fig


@app.callback(Output('live-update-graph-lum', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live_lum(n):

    # Collect some data
    #df = pd.read_csv('IOTdata.csv')
    dfarduino = pd.read_csv('IOTArduinoData.csv')
    dfnucleo = pd.read_csv('IOTNucleoData.csv')
    if len(dfnucleo) < len(dfarduino):
        dfarduino = dfarduino.head(len(dfnucleo))
    else:
        dfnucleo = dfnucleo.head(len(dfarduino))
    dfarduino['Timestamp'] = dfarduino[['Time', 'Date']].agg(' '.join, axis=1)
    #dfarduino['Timestamp'] = pd.to_datetime(dfarduino['Timestamp'])
    # Clip all values with extremely large resistance values to 0% RH
    # Create the graph
    fig = px.line(dfarduino, x='Timestamp', y=['Luminosity (%)', dfnucleo['Luminosity (%)']], title='Device Luminosity (%)',
                  template=plotly_built_in_templates[2])
    fig.update_layout(uirevision="Don't change",  xaxis_tickformatstops=[
        dict(dtickrange=[60000, 3600000], value="%H:%M m"),  # One month of recordings = 43 200
        dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
        dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
        dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
        dict(dtickrange=["M1", "M12"], value="%b '%y M"),
        dict(dtickrange=["M12", None], value="%Y Y")
    ], xaxis_title='Timestamp', yaxis_title='Luminosity (%)')
    newnames = {'Luminosity (%)': 'Arduino', 'wide_variable_1': 'Nucleo'}
    fig.for_each_trace(lambda t: t.update(name=newnames[t.name], legendgroup=newnames[t.name],
                                          hovertemplate=t.hovertemplate.replace(t.name, newnames[t.name])))
    fig.update_traces(mode='markers+lines')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)  # Run Dash app


