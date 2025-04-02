from dash import Dash, html, dcc, Input, Output, callback, State, dash_table
import dash_bootstrap_components as dbc
from utils import colors


layout = html.Div([
    dcc.Store(id='ticker_data'),
    html.H1("Option Screener"),
    html.Div("Symbol:"),
    dcc.Input(id="symbol_name", type="text", className="form-control"),
    html.Br(),
    html.Center(dbc.Button("Fetch data", id="validate_symbol", color="info", className="me-1", style={"background-color": colors[0]})),
    html.Br(),
    html.Div("Error fetching data", id="error_message", style={"display": "none"}, className="alert alert-warning"),
    html.Br(),
    dcc.Graph(id="underlying_price",),
    html.Div("Expiry:"),
    dcc.Dropdown(id="expiry_list"),
    html.Div([], id="days_to_expiry"),
    html.Div([
        dcc.Graph(id="prices_charts", className="col-sm-6"),
        dcc.Graph(id="iv_charts", className="col-sm-6"),
    ], className="row"),
    dcc.Tabs(id="call_puts_tabs", value='call', children=[
        dcc.Tab(label='Call', value='call'),
        dcc.Tab(label='Put', value='put'),
    ]),
    html.Div([
        dash_table.DataTable(id="option_table_calls", page_size=12),
    ], id="tab_container_call"),
    html.Div([
        dash_table.DataTable(id="option_table_puts", page_size=12),
    ], id="tab_container_puts"),
    dcc.Graph(id="historical_returns",),
], className="container")