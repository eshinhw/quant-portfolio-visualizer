import dash
from dash import html
from strategies.BasePortfolio import BasePortfolio
from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
import plotly.express as px
import pandas as pd

dash.register_page(__name__, title="Quant Portfolio Visualizer")

cp = BasePortfolio("Classic 60/40 Portfolio", ["SPY", "IEF"], [0.6, 0.4])

pp = BasePortfolio(
    "Permanent Portfolio", ["VTI", "BIL", "TLT", "GLD"], [0.25, 0.25, 0.25, 0.25]
)
allSeason = BasePortfolio(
    "All Season Portfolio",
    ["SPY", "TLT", "IEF", "DBC", "GLD"],
    [0.3, 0.4, 0.15, 0.075, 0.075],
)


def update_table():
    data = {
        "Allocation": [str(cp), str(pp), str(allSeason)],
        "CAGR": [cp.cagr(), pp.cagr(), allSeason.cagr()],
        "MDD": [cp.mdd(), pp.mdd(), allSeason.mdd()],
    }
    df = pd.DataFrame(data)

    return df.to_dict("records")


def update_returns_graph():
    df = pd.DataFrame()

    df[str(cp)] = cp.port_cum_returns()
    df[str(pp)] = pp.port_cum_returns()
    df[str(allSeason)] = allSeason.port_cum_returns()
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    return px.line(
        df,
        x="Date",
        y=[col for col in df.columns if col != "Date"],
        title="Historical Returns",
    )


def update_drawdown_graph():
    df = pd.DataFrame()

    df[str(cp)] = cp.drawdown()
    df[str(pp)] = pp.drawdown()
    df[str(allSeason)] = allSeason.drawdown()
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    return px.line(
        df,
        x="Date",
        y=[col for col in df.columns if col != "Date"],
        title="Historical Drawdowns",
    )


layout = html.Div(
    [
        html.Div(
            [
                dcc.Graph(figure=update_returns_graph(), id="total-perf-graph"),
                dcc.Graph(figure=update_drawdown_graph(), id="total-drawdown-graph"),
                html.Div(
                    [
                        dash_table.DataTable(
                            update_table(),
                            id="total-perf-table",
                            style_cell={"textAlign": "center"},
                        )
                    ]
                ),
            ],
            style={"margin": "0px 35px 0px 35px"},
        ),
    ],
)
