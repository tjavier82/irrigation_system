
# Reads information from sqlite and creates graphs with plot.ly

import pandas as pd
from sqlalchemy import create_engine # database connection
import datetime as dt

import plotly.plotly as py # interactive graphing
import plotly.graph_objs as go

import configparser
import argparse
import logging

DEFAULT_CONFIG_FILE = "config.ini"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file. If not provided, " + DEFAULT_CONFIG_FILE + " will be used.",
                        default=DEFAULT_CONFIG_FILE)
    parser.add_argument("-v", "--verbose", help="increase verbosity", action="store_true")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    try:
        config.read(args.config)

    except:
        print('Error reading config file')
        exit()

    logger = logging.getLogger(config['Logging']['LoggerName'])
    disk_engine = create_engine('sqlite:///' + config['Database']['FilePath'])

    df_1 = pd.read_sql_query('SELECT date, moisture '
                             'FROM moistureRead '
                             'WHERE plant = 1 '
                             'ORDER BY date', disk_engine)

    # normalize
    moistureMaxLevel = int(config['Graph']['MoistureMaxLevel'])
    moistureMinLevel = int(config['Graph']['MoistureMinLevel'])

    #Note that the higher moisture level, the dryer and the lower, soil is more wet
    df_1['moisture'] = 100 - (
            (df_1["moisture"] - moistureMaxLevel) / (moistureMinLevel - moistureMaxLevel)) * 100

    df_2 = pd.read_sql_query('SELECT date, waterAmount '
                             'FROM watering '
                             'WHERE plant = 1 '
                             'ORDER BY date', disk_engine)



    trace_1 = go.Scatter(
        x=df_1['date'],
        y=df_1['moisture'],
        name='Soil Moisture',
        mode='lines',
        line=dict(color='rgb(205, 12, 24)', width=2),
        connectgaps=True,
    )

    trace_2 = go.Scatter(
        x=df_2['date'],
        y=df_2['waterAmount'],
        name='Watering',
        yaxis='y2',
        mode='markers',
        marker=dict(
            size=10,
            color='rgb(49, 130, 189)',
        ),
    )

    layout = go.Layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickcolor='rgb(204, 204, 204)',
            tickwidth=2,
            ticklen=5,
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            title='Soil Moisture',
            showgrid=False,
            zeroline=True,
            showline=True,
            showticklabels=True,
            type='linear',
            range=[1, 100],
            dtick=20,
            ticksuffix='%'
        ),
        yaxis2=dict(
            title='Watering',
            titlefont=dict(
                color='rgb(49, 130, 189)'
            ),
            tickfont=dict(
                color='rgb(49, 130, 189)'
            ),
            overlaying='y',
            side='right',
            range=[0, 0.2],
            dtick=0.05,
        )
    )

    fig = go.Figure(data=[trace_1, trace_2], layout=layout)
    py.plot(fig, filename='Soil moisture evolution')
