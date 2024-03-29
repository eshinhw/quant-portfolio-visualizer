import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", title="Quant Portfolio Visualizer")


layout = dbc.Container(
    [
        html.Div(
            [
                html.H5("Fama-French Factor Analysis"),
                html.Ul(
                    [
                        html.Li(dcc.Link("Market Beta", href="/beta")),
                        html.Li(dcc.Link("Size", href="/size")),
                        html.Li(dcc.Link("Value", href="/value")),
                        html.Li(dcc.Link("Momentum", href="/momentum")),
                    ]
                ),
                html.H5("Fixed Weights Portfolios"),
                html.Ul(
                    [
                        html.Li(dcc.Link("Classic 60/40 Portfolio", href="/fixed")),
                        html.Li(dcc.Link("All Weather Portfolio", href="/fixed")),
                        html.Li(dcc.Link("Permanent Portfolio", href="/fixed")),
                    ]
                ),
                html.H5("Momentum Portfolios"),
                html.Ul(
                    [
                        html.Li(
                            dcc.Link("Global Equities Momentum (GEM)", href="/gem")
                        ),
                        html.Li(
                            dcc.Link("Global Balanced Momentum (GBM)", href="/gbm")
                        ),
                    ]
                ),
            ],
        ),
    ],
    fluid="md",
    className="content-container",
)
