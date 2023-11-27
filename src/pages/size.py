import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
from factors.size import get_size_cummulative_returns, size_factor_stat
import plotly.express as px
import dash_bootstrap_components as dbc
import utils


dash.register_page(__name__, title="Quant Portfolio Visualizer")


def update_graph():
    df = get_size_cummulative_returns()
    fig = px.line(df, x="Date", y=[col for col in df.columns if col != "Date"])
    return fig


def update_table():
    return size_factor_stat().to_dict("records")


def update_heading():
    df = get_size_cummulative_returns()

    startDate = df["Date"].iloc[0].replace("-", ".")
    endDate = df["Date"].iloc[-1].replace("-", ".")
    return html.H3(
        f"Size Factor ({startDate} ~ {endDate})", className="text-center m-2"
    )


layout = dbc.Container(
    [
        utils.update_heading("Size", get_size_cummulative_returns()),
        dcc.Graph(
            id="graph-content",
            figure=utils.update_graph(get_size_cummulative_returns()),
        ),
        dash_table.DataTable(
            id="table-content",
            sort_action="native",
            data=utils.update_table(size_factor_stat()),
            style_table={"overflowX": "auto"},
        ),
    ],
    fluid="md",
    className="content-container",
)
