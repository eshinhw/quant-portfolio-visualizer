import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import dash
from dash import html

from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__, title="Quant Portfolio Visualizer")

GBM = ["SPY", "VEU", "BND"]


def get_port_returns():
    gbm_prices = pd.DataFrame()
    for ticker in GBM:
        gbm_prices[ticker] = yf.Ticker(ticker).history(period="max", interval="1d")[
            "Close"
        ]

    gbm_momentum = gbm_prices.copy().apply(
        lambda x: x.shift(1) / x.shift(12) - 1, axis=0
    )
    gbm_momentum.dropna(inplace=True)

    gbm_rank = gbm_momentum.rank(axis=1)

    for col in gbm_rank.columns:
        gbm_rank[col] = np.where(gbm_rank[col] > 2, 1, 0)

    monthly_gbm_returns = gbm_prices.pct_change()
    monthly_gbm_returns.dropna(inplace=True)
    monthly_gbm_returns = monthly_gbm_returns[gbm_rank.index[0] :]

    gbm_sixty = np.multiply(gbm_rank, monthly_gbm_returns)
    gbm_sixty_returns = gbm_sixty.sum(axis=1)

    gbm_port = pd.DataFrame()
    gbm_port["GBM_sixty"] = gbm_sixty_returns
    gbm_port["GBM_forty"] = monthly_gbm_returns["BND"]
    weight = np.array([0.6, 0.4])
    gbm_port["port_return"] = gbm_port.dot(weight)
    gbm_port["GBM"] = (1 + gbm_port["port_return"]).cumprod()
    gbm_port.reset_index(inplace=True)
    return gbm_port


def create_cum_returns_graph():
    gbm_port = get_port_returns()
    return px.line(gbm_port, x="Date", y=["GBM"])


def create_table():
    gbm_port = get_port_returns()
    print(gbm_port)
    stats = {"Portfolio": ["Global Balanced Momentum"], "CAGR": [], "MDD": []}
    # compute CAGR
    first_value = gbm_port.iloc[0, -1]
    last_value = gbm_port.iloc[-1, -1]
    print(first_value, last_value)
    years = gbm_port.shape[0] / 12
    cagr = (last_value / first_value) ** (1 / years) - 1

    # compute MDD
    cumulative_returns = gbm_port["GBM"]
    previous_peaks = cumulative_returns.cummax()
    drawdown = (cumulative_returns - previous_peaks) / previous_peaks
    portfolio_mdd = drawdown.min()

    stats["CAGR"].append(cagr)
    stats["MDD"].append(portfolio_mdd)

    df = pd.DataFrame(stats)

    return df.to_dict("records")


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
                    figure=create_cum_returns_graph(),
                    responsive=True,
                ),
            ]
        ),
    ],
    className="content-container",
)
