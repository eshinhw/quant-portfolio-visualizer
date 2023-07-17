from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
import plotly.express as px
from factor import get_pbr_cummulative_returns
from factor import pbr_factor_stat

app = Dash(__name__)

BUTTON_STYLE = {"color": "white", "background-color": "black", "padding": "12px 18px", "cursor": "pointer", "border": "none"}

app.layout = html.Div(
    [
        # html.Div([        html.H1(
        #     children="Factor Portfolio Visualizer",
        #     style={"textAlign": "center"},
        # ),
        # html.Div([
        #   html.Button("Value", id='value-button', style=BUTTON_STYLE),    
        #   html.Button("Momentum", id='momentum-button', style=BUTTON_STYLE),    
        #   html.Button("Quality", id='quality-button', style=BUTTON_STYLE),    
        #   html.Button("Low Vol", id='low-vol-button', style=BUTTON_STYLE),    
        # ], style={"display": "flex", "gap": "50px", "justify-content": "center", "align-items": "center", "margin-bottom": "50px", "margin-top": "30px"})], style={"display": "flex", "gap": "20px", "justify-content": "center", "align-items": "center"}),
        html.H1(
            children="Factor Portfolio Visualizer",
            style={"textAlign": "center"},
        ),
        html.Div([
          html.Button("Value", id='value-button', style=BUTTON_STYLE),    
          html.Button("Momentum", id='momentum-button', style=BUTTON_STYLE),    
          html.Button("Quality", id='quality-button', style=BUTTON_STYLE),    
          html.Button("Low Vol", id='low-vol-button', style=BUTTON_STYLE),    
        ], style={"display": "flex", "gap": "50px", "justify-content": "center", "align-items": "center", "margin-bottom": "30px", "margin-top": "5px"}),        
        dcc.RadioItems(
            ["Bottom-Mid-High", "Quintiles", "Deciles"],
            "Bottom-Mid-High",
            id="radioitems-selection",
            inline=True,
            style={"display": "flex", "gap": "20px", "justify-content": "center", "align-items": "center"}
        ),
        # html.Div([dcc.Graph(id="graph-content"), html.Div([html.H2(children="Value Factor Portfolio Statistics", style={"textAlign": "center"}, id="factor-statistics"),html.Div([])], 
        #          style={"display": "flex", "gap": "20px", "justify-content": "center", "align-items": "center"}),
        dcc.Graph(id="graph-content"),
        html.H2(children="Value Factor Portfolio Statistics", style={"textAlign": "center"}, id="factor-statistics"),
        html.Div([dash_table.DataTable(id="table-content")], style={'margin': "50px 50px"})
        
        
    ]
)

# @callback(Output(component_id="factor-statistics", component_property="children"), Input(component_id="value-button", component_property='value'))
# def updateHeading(value):
#     print(value)
#     print("Hello?")
#     print(ctx.triggered_id)
#     if "Value" == ctx.triggered_id:
#         value = "Value"
#         return f"{value} Factor Statistics"
    

@callback(
    Output(component_id="table-content", component_property="data"),
    Input(component_id="radioitems-selection", component_property="value"),
)
def update_table(value):
    if value == "Bottom-Mid-High":
        return pbr_factor_stat(value).to_dict("records")
    if value == "Quintiles":
        return pbr_factor_stat(value).to_dict("records")
    if value == "Deciles":
        return pbr_factor_stat(value).to_dict("records")


@callback(Output("graph-content", "figure"), Input("radioitems-selection", "value"))
def update_graph(value):
    if value == "Bottom-Mid-High":
        df = get_pbr_cummulative_returns(value)
        return px.line(
            df,
            x="Date",
            y=["Lo 30", "Med 40", "Hi 30"],
        )
    if value == "Quintiles":
        df = get_pbr_cummulative_returns(value)

        return px.line(
            df,
            x="Date",
            y=["Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"],
        )
    if value == "Deciles":
        df = get_pbr_cummulative_returns(value)
        return px.line(
            df,
            x="Date",
            y=[
                "Lo 10",
                "Dec 2",
                "Dec 3",
                "Dec 4",
                "Dec 5",
                "Dec 6",
                "Dec 7",
                "Dec 8",
                "Dec 9",
                "Hi 10",
            ],
        )
    


if __name__ == "__main__":
    app.run(debug=True)
