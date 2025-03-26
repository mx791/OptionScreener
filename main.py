from dash import Dash, html, dcc, Input, Output, callback, State, dash_table
import dash_bootstrap_components as dbc
import yfinance as yf
import plotly.express as px
import pandas as pd
import plotly.io as pio
from datetime import datetime, timedelta
import numpy as np
from layout import layout
from callbacks import *


pio.templates.default = "plotly_white"
app = Dash(external_stylesheets=[dbc.themes.LUX])



app.layout = layout



if __name__ == '__main__':
    app.run(debug=True)
