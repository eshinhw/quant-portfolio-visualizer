from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from strategies.BasePortfolio import BasePortfolio

from components.navbar import navbar

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

cp = BasePortfolio("Classic 60/40 Portfolio", ["SPY", "IEF"], [0.6, 0.4])
pp = BasePortfolio("Permanent Portfolio", ["VTI", "BIL", "TLT", "GLD"], [0.25, 0.25, 0.25, 0.25])
allSeason = BasePortfolio("All Season Portfolio", ["SPY", "TLT", "IEF", "DBC", "GLD"], [0.3, 0.4, 0.15, 0.075, 0.075])


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
    return px.line(df, x="Date", y=[col for col in df.columns if col != "Date"], title="Historical Returns")


def update_drawdown_graph():
    df = pd.DataFrame()

    df[str(cp)] = cp.drawdown()
    df[str(pp)] = pp.drawdown()
    df[str(allSeason)] = allSeason.drawdown()
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    return px.line(df, x="Date", y=[col for col in df.columns if col != "Date"], title="Historical Drawdowns")


app.layout = html.Div(
    [
        navbar,
        html.Div(
            [
                dcc.Graph(figure=update_returns_graph(), id="total-perf-graph"),
                dcc.Graph(figure=update_drawdown_graph(), id="total-drawdown-graph"),
                html.Div(
                    [dash_table.DataTable(update_table(), id="total-perf-table", style_cell={"textAlign": "center"})]
                ),
            ],
            style={"margin": "0px 35px 0px 35px"},
        ),
    ],
)


if __name__ == "__main__":
    app.run(debug=True)
