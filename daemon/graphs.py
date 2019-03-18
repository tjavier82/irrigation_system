
# Reads information from sqlite and creates graphs with plot.ly

import pandas as pd
from sqlalchemy import create_engine # database connection
import datetime as dt

import plotly.plotly as py # interactive graphing
import plotly.graph_objs as go

import configparser
import argparse

if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file. If not provided, " + DEFAULT_CONFIG_FILE + " will be used.",
                        default=DEFAULT_CONFIG_FILE)
    parser.add_argument("-v", "--verbose", help="increase verbosity", action="store_true")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    try:
        config.read (args.config)

    except:
        print('Error reading config file')
        exit()

    disk_engine = create_engine('sqlite://' + config['Database']['FilePath'])

    df = pd.read_sql_query('SELECT date, moisture'
                           'FROM moistureRead '
                           'WHERE plant = 1 '
                           'ORDER BY date asc', disk_engine)

    py.iplot({
        'data': [go.Scatter(x=df['date'], y=df['moisture'])],
        'layout': {
            'margin': {'b': 150},  # Make the bottom margin a bit bigger to handle the long text
            'xaxis': {'tickangle': 40}}  # Angle the labels a bit
    }, filename='Soil moisture evolution')
