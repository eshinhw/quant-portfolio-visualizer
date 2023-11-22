import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Market Beta", href="/beta"),
                dbc.DropdownMenuItem("Value", href="/value"),
                dbc.DropdownMenuItem("Momentum", href="/momentum"),
            ],
            nav=True,
            in_navbar=True,
            label="Fama-French",
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Classic 60/40", href="/classic"),
                dbc.DropdownMenuItem("Permanent", href="#"),
                dbc.DropdownMenuItem("All Season", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Fixed Portfolios",
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Dynamic Asset Allocations",
        ),
    ],
    brand="Quant Portfolio Visualizer",
    brand_href="/",
    color="primary",
    dark=True,
)
