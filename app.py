from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
import plotly.express as px
from factor import get_pbr_cummulative_returns
from factor import pbr_factor_stat

app = Dash(__name__)

BUTTON_STYLE = {"color": "white", "background-color": "black", "padding": "12px 18px", "cursor": "pointer", "border": "none"}
FACTORS = ['Value', 'Momentum', 'Quality', 'Low Volatility']

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
        html.Div([html.H1(
            children="Factor Portfolio Visualizer",
            style={"textAlign": "center", "fontSize": "35px"},
        ),
        html.Div([dcc.Dropdown(FACTORS, 'Value', id='dropdown-selection'),], style={"width": "500px"})], style={"display": "flex", "gap": "20px", "justify-content": "space-between", "align-items": "center"}),
        
        # html.Div([
        #   html.Button("Value", id='value-button', style=BUTTON_STYLE),    
        #   html.Button("Momentum", id='momentum-button', style=BUTTON_STYLE),    
        #   html.Button("Quality", id='quality-button', style=BUTTON_STYLE),    
        #   html.Button("Low Vol", id='low-vol-button', style=BUTTON_STYLE),    
        # ], style={"display": "flex", "gap": "50px", "justify-content": "center", "align-items": "center", "margin-bottom": "30px", "margin-top": "5px"}),        
        
        # html.Div([dcc.Graph(id="graph-content"), html.Div([html.H2(children="Value Factor Portfolio Statistics", style={"textAlign": "center"}, id="factor-statistics"),html.Div([])], 
        #          style={"display": "flex", "gap": "20px", "justify-content": "center", "align-items": "center"}),
        dcc.Graph(id="graph-content"),
        dcc.RadioItems(
            ["Bottom-Mid-High", "Quintiles", "Deciles"],
            "Bottom-Mid-High",
            id="radioitems-selection",
            inline=True,
            style={"display": "flex", "gap": "20px", "justify-content": "start", "margin-left": "75px", "align-items": "center"}
        ),
        html.Div(id="factor-stat"),
        html.Div([dash_table.DataTable(id="table-content")], style={'margin': "50px 50px"})
    ]
)

@callback(Output(component_id="factor-stat", component_property="children"), [Input(component_id="dropdown-selection", component_property='value'), Input("radioitems-selection", "value")])
def updateHeading(factor, bp):
    if factor == "Value":
      df = get_pbr_cummulative_returns(bp)
      startDate = df['Date'].iloc[0].replace("-",".")
      endDate = df['Date'].iloc[-1].replace("-",".")
      return html.H2(children=f"{factor} Portfolio Statistics ({startDate} - {endDate})", style={'textAlign': "center", "fontSize": "30px"})
    

@callback(
    Output(component_id="table-content", component_property="data"),
    Input(component_id="radioitems-selection", component_property="value"),
)
def update_table(bp):
    if bp == "Bottom-Mid-High":
        return pbr_factor_stat(bp).to_dict("records")
    if bp == "Quintiles":
        return pbr_factor_stat(bp).to_dict("records")
    if bp == "Deciles":
        return pbr_factor_stat(bp).to_dict("records")


@callback(Output("graph-content", "figure"), Input("radioitems-selection", "value"))
def update_graph(bp):
    if bp == "Bottom-Mid-High":
        df = get_pbr_cummulative_returns(bp)
        return px.line(
            df,
            x="Date",
            y=["Lo 30", "Med 40", "Hi 30"],
        )
    if bp == "Quintiles":
        df = get_pbr_cummulative_returns(bp)

        return px.line(
            df,
            x="Date",
            y=["Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"],
        )
    if bp == "Deciles":
        df = get_pbr_cummulative_returns(bp)
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
