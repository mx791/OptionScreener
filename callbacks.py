from dash import Dash, html, dcc, Input, Output, callback, State, dash_table
import yfinance as yf
import plotly.express as px
import pandas as pd
import plotly.io as pio
from datetime import datetime, timedelta
import numpy as np


colors = ["#1a5276", "#0e6655", "#7b241c"]


@callback(
    [
        Output("expiry_list", "options"), Output("underlying_price", "figure"),
        Output("select_a_symbol_message", "style"), Output("select_expiry_block", "style"),
    ],
    Input("validate_symbol", "n_clicks"),
    State("symbol_name", "value"),
)
def fetch_symbol(n_click, symbol):
    if n_click == 0 or symbol is None:
        return [], None, {"display": "block"}, {"display": "none"}
    
    ticker = yf.Ticker(symbol)

    stock_price_chart = px.line(
        ticker.history("3Y"), y="Close", title=f"{ticker.info['shortName']}",
    ).update_traces(line_color=colors[0])

    return ticker.options, stock_price_chart, {"display": "none"}, {"display": "block"}



@callback(
    [
        Output("prices_charts", "figure"), Output("iv_charts", "figure"),
        Output("option_table_calls", 'data'), Output("option_table_puts", 'data'),
        Output("days_to_expiry", 'children'), Output("historical_returns", "figure"),
        Output("options_shows_block", "style")
    ],
    Input("expiry_list", "value"),
    State("symbol_name", "value"),
    prevent_initial_call=True
)
def show_options(expiry, ticker):
    if expiry is None or expiry == "":
        return None, None, None, None, {"display": "none"}
    
    target_date = datetime.strptime(expiry, "%Y-%m-%d").date()
    today_date = datetime(2025, 3, 25).date()
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
    returns = (historical["Close"].values[working_days:] / historical["Close"].values[:-working_days] - 1) * 100

    price_strike_scatter = px.scatter(
        data, x="strike", y="lastPrice", color="cp",
        title="Prices vs strike", size="volume",
    )

    iv_strike_scatter = px.scatter(
        data, x="strike", y="impliedVolatility", size="volume",
        color="cp", title="Implied volatility vs strike"
    )


    returns_hist = px.histogram(
        returns, title=f"Historical underlying % returns over a {working_days} days period"
    ).update_traces(marker_color=colors[0])


    return price_strike_scatter, iv_strike_scatter, calls[columns].to_dict('records'), puts[columns].to_dict('records'), f"""
{total_days} days till expiry, {working_days} market days""", returns_hist, {"display": "block"}



@callback([
        Output('tab_container_call', 'style'),
        Output('tab_container_puts', 'style'),
    ],
    Input('call_puts_tabs', 'value'))
def call_put_tabs(tab_name):
    if tab_name == "put":
        return {"display": "none"}, {"display": "block"}
    return {"display": "block"}, {"display": "none"}
