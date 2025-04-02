from dash import Dash, html, dcc, Input, Output, callback, State, dash_table
import dash_bootstrap_components as dbc
import yfinance as yf
import plotly.express as px
import pandas as pd
import plotly.io as pio
from datetime import datetime
import numpy as np


pio.templates.default = "plotly_white"
app = Dash(external_stylesheets=[dbc.themes.LUX])

colors = ["#1a5276", "#0e6655", "#7b241c"]


app.layout = html.Div([
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


@callback(
    [Output("expiry_list", "options"), Output("underlying_price", "figure"), Output("error_message", "style")],
    Input("validate_symbol", "n_clicks"),
    State("symbol_name", "value"),
    
)
def fetch_symbol(n_click, symbol):
    if n_click == 0 or symbol is None:
        return [], None, {"display": "none"}
    
    try:
        ticker = yf.Ticker(symbol)
        return ticker.options, px.line(
            ticker.history("3Y"), y="Close", title=f"{ticker.info['shortName']}",
        ).update_traces(line_color=colors[0]), {"display": "none"}

    except Exception:
        return [], None, {"display": "block"}

@callback(
    [
        Output("prices_charts", "figure"), Output("iv_charts", "figure"),
        Output("option_table_calls", 'data'), Output("option_table_puts", 'data'),
        Output("days_to_expiry", 'children'), Output("historical_returns", "figure")
    ],
    Input("expiry_list", "value"),
    State("symbol_name", "value"),
    prevent_initial_call=True
)
def show_options(expiry, ticker):
    if expiry is None or expiry == "":
        return None, None, None, None, None, None
    

    target_date = datetime.strptime(expiry, "%Y-%m-%d").date()
    today_date = datetime.today().date()
    total_days = abs((target_date - today_date).days)
    working_days = np.busday_count(today_date, target_date)
    
    ticker = yf.Ticker(ticker)
    options = ticker.option_chain(expiry)
    calls = options.calls
    puts = options.puts

    calls["cp"] = "Call"
    puts["cp"] = "Put"

    data = pd.concat([calls, puts])
    data["volume"] = data["volume"].fillna(1.0)

    columns = ["lastTradeDate", "strike", "lastPrice", "volume", "impliedVolatility"]
    historical = ticker.history("3Y")
    working_days = max(working_days, 1)
    returns = (historical["Close"].values[working_days:] / historical["Close"].values[:-working_days] - 1) * 100

    return px.scatter(
        data, x="strike", y="lastPrice", color="cp",
        title="Prices vs strike", size="volume",
    ), px.scatter(
        data, x="strike", y="impliedVolatility", size="volume",
        color="cp", title="Implied volatility vs strike"
    ), calls[columns].to_dict('records'), puts[columns].to_dict('records'), f"""
{total_days} days till expiry, {working_days} market days""", px.histogram(
    returns, title=f"Historical underlying % returns over a {working_days} days period"
    ).update_traces(marker_color=colors[0])



@callback([
        Output('tab_container_call', 'style'),
        Output('tab_container_puts', 'style'),
    ],
    Input('call_puts_tabs', 'value'))
def call_put_tabs(tab_name):
    if tab_name == "put":
        return {"display": "none"}, {"display": "block"}
    return {"display": "block"}, {"display": "none"}



if __name__ == '__main__':
    app.run(debug=True)
