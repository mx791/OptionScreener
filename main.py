from dash import Dash, html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import yfinance as yf
import plotly.express as px
import pandas as pd

app = Dash(external_stylesheets=[dbc.themes.JOURNAL])


app.layout = html.Div([
    dcc.Store(id='ticker_data'),
    html.H1("Option Screener"),
    html.Div("Symbol:"),
    dcc.Input(id="symbol_name", type="text"),
    html.Button("Fetch data", id="validate_symbol"),
    html.Br(),
    html.Br(),
    dcc.Dropdown(id="expiry_list"),
    dcc.Graph(id="prices_charts"),
    dcc.Graph(id="iv_charts"),
], className="container")


@callback(
    Output("expiry_list", "options"),
    Input("validate_symbol", "n_clicks"),
    State("symbol_name", "value"),
    
)
def fetch_symbol(n_click, symbol):
    if n_click == 0 or symbol is None:
        return []
    ticker = yf.Ticker(symbol)
    return ticker.options


@callback(
    [Output("prices_charts", "figure"), Output("iv_charts", "figure")],
    Input("expiry_list", "value"),
    State("symbol_name", "value"),
    prevent_initial_call=True
)
def show_options(expiry, ticker):
    if expiry is None or expiry == "":
        return None, None
    
    ticker = yf.Ticker(ticker)
    options = ticker.option_chain(expiry)
    calls = options.calls
    puts = options.puts

    calls["cp"] = "Call"
    puts["cp"] = "Put"

    data = pd.concat([calls, puts])
    return px.scatter(data, x="strike", y="lastPrice", color="cp"), px.scatter(data, x="strike", y="impliedVolatility", color="cp")



if __name__ == '__main__':
    app.run(debug=True)
