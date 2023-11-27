import dash
from factors.momentum import (
    get_momentum_cummulative_returns,
    mom_factor_stat,
)
from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
import plotly.express as px
import dash_bootstrap_components as dbc
import utils

dash.register_page(__name__, title="Quant Portfolio Visualizer")


layout = dbc.Container(
    [
        utils.update_heading("Momentum", get_momentum_cummulative_returns()),
        dcc.Graph(
            id="graph-content",
            figure=utils.update_graph(get_momentum_cummulative_returns()),
        ),
        dash_table.DataTable(
            id="table-content",
            sort_action="native",
            data=utils.update_table(mom_factor_stat()),
            style_table={"overflowX": "auto"},
        ),
    ],
    fluid="md",
)
