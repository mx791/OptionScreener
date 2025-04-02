from dash import Dash, html, dcc, Input, Output, callback, State, dash_table
import dash_bootstrap_components as dbc


layout = html.Div([

    dcc.Store(id='ticker_data'),

    html.Br(),
    
    html.H1("Option Screener"),
    dbc.Form(dbc.Row([
        dbc.Label("Symbol:", width="auto"),
        dbc.Col(dbc.Input(id="symbol_name", type="text", className="me-3")),
        dbc.Col(
            dbc.Button("Fetch data", id="validate_symbol",),
            width="auto",
        ),
    ])),
    html.Br(),

    html.Div([
        html.Br(),
        html.Br(),
        html.Center(html.H3("Please select a symbol...")),
    ], id="select_a_symbol_message"),

    html.Div([
        dcc.Graph(id="underlying_price",),
        html.Div("Expiry:"),
        dcc.Dropdown(id="expiry_list"),
    ], id="select_expiry_block", style={"display": "none"}),

    html.Div([
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

    ], id="options_shows_block", style={"display": "none"}),

], className="container")