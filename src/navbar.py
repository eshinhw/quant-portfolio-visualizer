import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Fixed Portfolios", href="/fixed")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("GEM (Global Equities Momentum)", href="/gem"),
                dbc.DropdownMenuItem("GBM (Global Balanced Momentum)", href="/gbm"),
            ],
            nav=True,
            in_navbar=True,
            label="Momentum Portfolios",
        ),
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
