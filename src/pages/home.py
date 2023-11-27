import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx

import plotly.express as px


dash.register_page(__name__, path="/", title="Quant Portfolio Visualizer")


layout = html.Div(
    [
        html.Div(
            [
                html.H5("Fama-French Factor Analysis"),
                html.Ul(
                    [
                        html.Li("Market Beta"),
                        html.Li("Size"),
                        html.Li("Value"),
                        html.Li("Momentum"),
                    ]
                ),
                html.H5("Fixed Portfolios"),
                html.Ul(
                    [
                        html.Li("Classic 60/40 Portfolio"),
                        html.Li("All Weather Portfolio"),
                        html.Li("Permanent Portfolio"),
                    ]
                ),
                html.H5("Momentum Portfolios"),
            ],
            style={
                "margin-left": "60px",
                "padding-left": "12px",
                "margin-top": "20px",
                "max-width": "1320px",
            },
        ),
    ],
)
