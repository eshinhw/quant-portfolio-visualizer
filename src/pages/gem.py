import dash
from dash import html

from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

dash.register_page(__name__, title="Quant Portfolio Visualizer")

GEM = ["SPY", "VEU", "BND"]


def get_gem_port_rets():
    gem_prices = pd.DataFrame()
    for ticker in GEM:
        gem_prices[ticker] = yf.Ticker(ticker).history(period="max", interval="1d")[
            "Close"
        ]

    monthly_momentum = gem_prices.copy()
    monthly_momentum = monthly_momentum.apply(
        lambda x: x.shift(1) / x.shift(12) - 1, axis=0
    )
    monthly_momentum.dropna(inplace=True)

    rank_df = monthly_momentum.rank(axis=1, ascending=False)
    for col in rank_df.columns:
        rank_df[col] = np.where(rank_df[col] == 1, 1, 0)

    monthly_gem_returns = gem_prices.pct_change()
    monthly_gem_returns.dropna(inplace=True)
    monthly_gem_returns = monthly_gem_returns[rank_df.index[0] :].shift(-1)

    monthly_gem_returns["port_ret"] = np.multiply(rank_df, monthly_gem_returns).sum(
        axis=1
    )
    monthly_gem_returns["GEM"] = np.exp(
        np.log1p(monthly_gem_returns["port_ret"]).cumsum()
    )[:-1]
    monthly_gem_returns["spy_cum"] = np.exp(
        np.log1p(monthly_gem_returns["SPY"]).cumsum()
    )[:-1]
    monthly_gem_returns.dropna(inplace=True)
    monthly_gem_returns.reset_index(inplace=True)
    return monthly_gem_returns


def create_cum_ret_graph():
    gem_port = get_gem_port_rets()
    return px.line(gem_port, x="Date", y=["GEM"])


def create_table():
    gem_port = get_gem_port_rets()

    stats = {"Portfolio": ["Global Equities Momentum"], "CAGR": [], "MDD": []}
    # compute CAGR
    first_value = gem_port.iloc[0, -2]
    last_value = gem_port.iloc[-1, -2]

    years = gem_port.shape[0] / 12
    cagr = (last_value / first_value) ** (1 / years) - 1

    # compute MDD
    cumulative_returns = gem_port["GEM"]
    previous_peaks = cumulative_returns.cummax()
    drawdown = (cumulative_returns - previous_peaks) / previous_peaks
    portfolio_mdd = drawdown.min()

    stats["CAGR"].append(cagr)
    stats["MDD"].append(portfolio_mdd)

    df = pd.DataFrame(stats)

    return df.to_dict("records")


def create_mdd_graph():
    gem_port = get_gem_port_rets()
    # compute MDD
    cumulative_returns = gem_port["GEM"]
    previous_peaks = cumulative_returns.cummax()
    drawdown = (cumulative_returns - previous_peaks) / previous_peaks
    return px.line(drawdown)


layout = dbc.Container(
    [
        html.Div(
            [
                html.H5("Portfolio Statistics", style={"margin-bottom": "20px"}),
                dash_table.DataTable(
                    create_table(),
                    style_cell={"textAlign": "center"},
                    sort_action="native",
                    style_table={"overflowX": "auto"},
                ),
            ]
        ),
        html.Div(
            [
                html.H5("Historical Cummulative Returns", style={"margin-top": "20px"}),
                dcc.Graph(
                    figure=create_cum_ret_graph(),
                    responsive=True,
                ),
            ]
        ),
        html.Div(
            [
                html.H5("Historical Drawdowns", style={"margin-top": "20px"}),
                dcc.Graph(
                    figure=create_mdd_graph(),
                    responsive=True,
                ),
            ]
        ),
    ],
    className="content-container",
)
