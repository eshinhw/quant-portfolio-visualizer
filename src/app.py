from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
from navbar import navbar
import dash
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    title="Quant Portfolio Visualizer",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    pages_folder="pages",
    use_pages=True,
    assets_folder="../assets",
    update_title=None,
)

server = app.server

app.layout = html.Div(
    [
        navbar,
        dash.page_container,
    ],
)


if __name__ == "__main__":
    app.run(debug=True)
