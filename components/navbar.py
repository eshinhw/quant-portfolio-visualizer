import dash_bootstrap_components as dbc


navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Classic", href="#"),
                dbc.DropdownMenuItem("Permanent", href="#"),
                dbc.DropdownMenuItem("All Weather", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Fixed",
        ),
        dbc.NavItem(dbc.NavLink("GTAA", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("DM", href="#"),
                dbc.DropdownMenuItem("CDM", href="#"),
                dbc.DropdownMenuItem("ADM", href="#"),
                dbc.DropdownMenuItem("MDM", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Momentum",
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("VAA", href="#"),
                dbc.DropdownMenuItem("DAA", href="#"),
                dbc.DropdownMenuItem("PAA", href="#"),
                dbc.DropdownMenuItem("BAA", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Keller",
        ),
    ],
    brand="Dynamic Portfolio Allocator",
    brand_href="/",
    color="primary",
    dark=True,
)
