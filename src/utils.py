import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
import plotly.express as px


def monthly_prices(assets):
    monthly_prices = pd.DataFrame()
    for asset in assets:
        monthly_prices[asset] = yf.download(
            asset,
            start=dt.datetime(2018, 1, 1),
            end=dt.datetime.today(),
            interval="1mo",
            progress=False,
        )["Adj Close"]
    monthly_prices.dropna(inplace=True)
    return monthly_prices


def monthly_returns(assets):
    monthly_returns = monthly_prices(assets).pct_change()
    monthly_returns.dropna(inplace=True)
    return monthly_returns


def update_graph(df):
    fig = px.line(df, x="Date", y=[col for col in df.columns if col != "Date"])
    return fig


def update_table(stat):
    return stat.to_dict("records")


def update_heading(title, df):
    startDate = df["Date"].iloc[0].replace("-", ".")
    endDate = df["Date"].iloc[-1].replace("-", ".")

    return html.H3(
        f"{title} Factor ({startDate} ~ {endDate})",
        className="text-center m-2",
    )
