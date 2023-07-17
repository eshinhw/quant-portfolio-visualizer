from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
import pandas_datareader.data as web
from pandas_datareader.famafrench import get_available_datasets

data = web.DataReader("Portfolios_Formed_on_BE-ME", "famafrench", start="1900-01-01")
df_pbr = data[0]

df_pbr_cum = np.log(1 + df_pbr / 100).cumsum()
df_pbr_cum.reset_index(inplace=True)
df_pbr_cum["Date"] = df_pbr_cum["Date"].astype(str)

# print(df_pbr_cum)


def factor_stat(df):
    n = len(df)

    ret_ari = (df / 100).mean(axis=0) * 12
    ret_geo = (1 + df / 100).prod() ** (12 / n) - 1
    vol = (df / 100).std(axis=0) * np.sqrt(12)
    sharp = ret_ari / vol

    stat = pd.DataFrame(
        [ret_ari, ret_geo, vol, sharp],
        index=[
            "Arithmetic Mean",
            "Geometric Mean",
            "Annualized Volatility",
            "Sharpe Ratio",
        ],
    ).round(4)

    return stat


app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            children="Historical Performance of Value Factor",
            style={"textAlign": "center"},
        ),
        dcc.Dropdown(
            ["Quantile", "Decimal", "Low-Med-High"],
            "Quantile",
            id="dropdown-selection",
        ),
        dcc.Graph(id="graph-content"),
        html.H1(children="Factor Stats", style={"textAlign": "center"}),
        dash_table.DataTable(id="table-content"),
    ]
)


@callback(
    Output(component_id="table-content", component_property="data"),
    Input(component_id="dropdown-selection", component_property="value"),
)
def update_table(value):
    if value == "Quantile":
        return factor_stat(
            df_pbr.loc[:, ["Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"]]
        ).to_dict("records")


@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    if value == "Quantile":
        df = df_pbr_cum.loc[:, ["Date", "Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"]]
        print(df)

        return px.line(
            df,
            x="Date",
            y=["Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"],
        )
    if value == "Decimal":
        df = df_pbr_cum.loc[
            :,
            [
                "Date",
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
        ]
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
    if value == "Low-Med-High":
        df = df_pbr_cum.loc[:, ["Date", "Lo 30", "Med 40", "Hi 30"]]
        return px.line(
            df,
            x="Date",
            y=["Lo 30", "Med 40", "Hi 30"],
        )


if __name__ == "__main__":
    app.run(debug=True)
