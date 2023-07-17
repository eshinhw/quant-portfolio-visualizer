from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
import plotly.express as px
from factor import get_pbr_cummulative_returns, get_momentum_cummulative_returns, pbr_factor_stat, mom_factor_stat

app = Dash(__name__)

BUTTON_STYLE = {"color": "white", "background-color": "black", "padding": "12px 18px", "cursor": "pointer", "border": "none"}
FACTORS = ['Value', 'Momentum']

app.layout = html.Div(
    [
        html.Div([html.H1(
            children="Factor Portfolio Visualizer",
            style={"textAlign": "center", "fontSize": "35px"},
        ),
        html.Div([dcc.Dropdown(FACTORS, 'Value', id='dropdown-selection', clearable=False),], style={"width": "500px"})],style={"display": "flex", "gap": "20px", "justify-content": "space-between", "align-items": "center"}),
        
        # html.Div([
        #   html.Button("Value", id='value-button', style=BUTTON_STYLE),    
        #   html.Button("Momentum", id='momentum-button', style=BUTTON_STYLE),    
        #   html.Button("Quality", id='quality-button', style=BUTTON_STYLE),    
        #   html.Button("Low Vol", id='low-vol-button', style=BUTTON_STYLE),    
        # ], style={"display": "flex", "gap": "50px", "justify-content": "center", "align-items": "center", "margin-bottom": "30px", "margin-top": "5px"}),        
        
        # html.Div([dcc.Graph(id="graph-content"), html.Div([html.H2(children="Value Factor Portfolio Statistics", style={"textAlign": "center"}, id="factor-statistics"),html.Div([])], 
        #          style={"display": "flex", "gap": "20px", "justify-content": "center", "align-items": "center"}),
        dcc.Graph(id="graph-content"),
        html.Div(id="factor-stat-header"),
        html.Div([dash_table.DataTable(id="table-content")], style={'margin': "50px 50px"})
    ]
)

# @callback(Output("breakpoint", "children"), Input("dropdown-selection", "value"))
# def updateBreakpoints(factor):
#     if factor == "Value":
#         return dcc.RadioItems(
#             ["Bottom-Mid-High", "Quintiles", "Deciles"],
#             "Bottom-Mid-High",
#             id="radioitems-selection",
#             inline=True,
#             style={"display": "flex", "gap": "20px", "justify-content": "start", "margin-left": "75px", "align-items": "center"}
#         ),
    

@callback(Output(component_id="factor-stat-header", component_property="children"), [Input(component_id="dropdown-selection", component_property='value')])
def update_heading(factor):
    if factor == "Value":
      df = get_pbr_cummulative_returns()
      startDate = df['Date'].iloc[0].replace("-",".")
      endDate = df['Date'].iloc[-1].replace("-",".")
      return html.H2(children=f"{factor} Portfolio Statistics ({startDate} - {endDate})", style={'textAlign': "center", "fontSize": "30px"})
    
    if factor == "Momentum":
        df = get_momentum_cummulative_returns()
        startDate = df['Date'].iloc[0].replace("-",".")
        endDate = df['Date'].iloc[-1].replace("-",".")
        
        return html.H2(children=f"{factor} Portfolio Statistics ({startDate} - {endDate})", style={'textAlign': "center", "fontSize": "30px"})
    
    if factor == "Quality":
        return html.H2(children=f"{factor} Portfolio Statistics", style={'textAlign': "center", "fontSize": "30px"})
    
    if factor == "Low Volatility":
        return html.H2(children=f"{factor} Portfolio Statistics", style={'textAlign': "center", "fontSize": "30px"})
    

@callback(
    Output(component_id="table-content", component_property="data"),
    Input(component_id="dropdown-selection", component_property="value"),
)
def update_table(factor):
    if factor == "Value":
      return pbr_factor_stat().to_dict("records")
    if factor == "Momentum":
      return mom_factor_stat().to_dict("records")


@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(factor):
    if factor == "Value":
        df = get_pbr_cummulative_returns()
        return px.line(
            df,
            x="Date",
            y=[col for col in df.columns if col != 'Date']
        )
    if factor == "Momentum":
       df = get_momentum_cummulative_returns()
       return px.line(
            df,
            x="Date",
            y=[col for col in df.columns if col != 'Date'],
        )
    

        



if __name__ == "__main__":
    app.run(debug=True)
