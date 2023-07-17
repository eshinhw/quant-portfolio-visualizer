from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            children="Factor Portfolio Visualizer",
            style={"textAlign": "center"},
        ),
        html.Div([
          html.Button("Value"),    
          html.Button("Momentum"),    
          html.Button("Quality"),    
          html.Button("Low Vol"),    
        ], style={"display": "flex", "gap": "50px", "justify-content": "center", "align-items": "center", "margin-bottom": "50px", "margin-top": "30px"}),        
        dcc.RadioItems(
            ["Quantile", "Decimal", "Low-Med-High"],
            "Quantile",
            id="radioitems-selection",
            inline=True,
            style={"display": "flex", "gap": "20px", "justify-content": "center", "align-items": "center"}
        ),
        dcc.Graph(id="graph-content"),
        html.H2(children="Factor Statistics", style={"textAlign": "center"}),
        # dash_table.DataTable(id="table-content"),
    ]
)


# @callback(
#     Output(component_id="table-content", component_property="data"),
#     Input(component_id="dropdown-selection", component_property="value"),
# )
# def update_table(value):
#     if value == "Quantile":
#         return factor_stat(
#             df_pbr.loc[:, ["Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"]]
#         ).to_dict("records")


# @callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
# def update_graph(value):
    # if value == "Quantile":
    #     df = df_pbr_cum.loc[:, ["Date", "Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"]]
    #     print(df)

    #     return px.line(
    #         df,
    #         x="Date",
    #         y=["Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"],
    #     )
    # if value == "Decimal":
    #     df = df_pbr_cum.loc[
    #         :,
    #         [
    #             "Date",
    #             "Lo 10",
    #             "Dec 2",
    #             "Dec 3",
    #             "Dec 4",
    #             "Dec 5",
    #             "Dec 6",
    #             "Dec 7",
    #             "Dec 8",
    #             "Dec 9",
    #             "Hi 10",
    #         ],
    #     ]
    #     return px.line(
    #         df,
    #         x="Date",
    #         y=[
    #             "Lo 10",
    #             "Dec 2",
    #             "Dec 3",
    #             "Dec 4",
    #             "Dec 5",
    #             "Dec 6",
    #             "Dec 7",
    #             "Dec 8",
    #             "Dec 9",
    #             "Hi 10",
    #         ],
    #     )
    # if value == "Low-Med-High":
    #     df = df_pbr_cum.loc[:, ["Date", "Lo 30", "Med 40", "Hi 30"]]
    #     return px.line(
    #         df,
    #         x="Date",
    #         y=["Lo 30", "Med 40", "Hi 30"],
    #     )


if __name__ == "__main__":
    app.run(debug=True)
