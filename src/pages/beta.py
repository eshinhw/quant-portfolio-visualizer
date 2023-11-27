import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
from factors.beta import get_beta_cummulative_returns, beta_factor_stat
import plotly.express as px
import dash_bootstrap_components as dbc
import utils


dash.register_page(__name__, title="Quant Portfolio Visualizer")

layout = dbc.Container(
    [
        utils.update_heading("Market Beta", get_beta_cummulative_returns()),
        dcc.Graph(
            id="graph-content",
            figure=utils.update_graph(get_beta_cummulative_returns()),
        ),
        dbc.Container(
            [
                dash_table.DataTable(
                    id="table-content",
                    sort_action="native",
                    data=utils.update_table(beta_factor_stat()),
                    style_table={"overflowX": "auto"},
                ),
            ],
            fluid=True,
        ),
    ],
    fluid="md",
    className="content-container",
)
