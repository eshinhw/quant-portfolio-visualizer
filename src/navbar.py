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
        #         dbc.DropdownMenuItem("Absolute Momentum", href="/absolute_momentum"),
        #         dbc.DropdownMenuItem("Relative Momentum", href="/relative_momentum"),
        #         dbc.DropdownMenuItem("Dual Momentum", href="/dual_momentum"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="Momentum Portfolios",
        # ),
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("Vigilant Asset Allocation (VAA)", href="/vaa"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="Keller Portfolios",
        # ),
    ],
    brand="Quant Portfolio Visualizer",
    brand_href="/",
    color="#03459C",
    dark=True,
)
