import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Market Beta", href="/beta"),
                dbc.DropdownMenuItem("Size", href="/size"),
                dbc.DropdownMenuItem("Value", href="/value"),
                dbc.DropdownMenuItem("Momentum", href="/momentum"),
            ],
            nav=True,
            in_navbar=True,
            label="Fama-French Factors",
        ),
        dbc.NavItem(dbc.NavLink("Fixed Portfolios", href="/fixed")),
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("Page 1", href="#"),
        #         dbc.DropdownMenuItem("Page 2", href="#"),
        #         dbc.DropdownMenuItem("Page 3", href="#"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="Momentum Portfolios",
        # ),
    ],
    brand="Quant Portfolio Visualizer",
    brand_href="/home",
    color="primary",
    dark=True,
)
