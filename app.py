from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
from navbar import navbar
import dash
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    pages_folder="pages",
    use_pages=True,
)

app.layout = html.Div(
    [
        navbar,
        # html.Div(
        #     [
        #         html.H3("Fama-French Factor Analysis"),
        #         html.Ul(
        #             [
        #                 html.Li("Market Beta"),
        #                 html.Li("Size"),
        #                 html.Li("Value"),
        #                 html.Li("Momentum"),
        #             ]
        #         ),
        #         html.H3("Fixed Portfolios"),
        #         html.H3("Dynamic Portfolios"),
        #     ],
        #     style={"margin-left": "10px", "margin-right": "10px"},
        # ),
        dash.page_container,
    ],
)


if __name__ == "__main__":
    app.run(debug=True)
