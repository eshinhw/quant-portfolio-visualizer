import dash
from dash import html
from dash import Dash, html, dcc, callback, Output, Input, dash_table, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import bt

# dash.register_page(__name__, title="Quant Portfolio Visualizer")

SECTOR_ETFS = [
    "xlb",
    "xlc",
    "xly",
    "xlp",
    "xle",
    "xlf",
    "xlv",
    "xli",
    "xlk",
    "xlu",
    "xlre",
]

# download data
data = bt.get(
    ",".join(SECTOR_ETFS),
    start="2010-01-01",
)

# a rolling mean is a moving average, right?
sma = data.rolling(50).mean()


class SelectWhere(bt.Algo):

    """
    Selects securities based on an indicator DataFrame.

    Selects securities where the value is True on the current date (target.now).

    Args:
        * signal (DataFrame): DataFrame containing the signal (boolean DataFrame)

    Sets:
        * selected

    """

    def __init__(self, signal):
        self.signal = signal

    def __call__(self, target):
        # get signal on target.now
        if target.now in self.signal.index:
            sig = self.signal.loc[target.now]

            # get indices where true as list
            selected = list(sig.index[sig])

            # save in temp - this will be used by the weighing algo
            target.temp["selected"] = selected

        # return True because we want to keep on moving down the stack
        return True


# first we create the Strategy
s = bt.Strategy(
    "above50sma",
    [SelectWhere(data > sma), bt.algos.WeighEqually(), bt.algos.Rebalance()],
)

# now we create the Backtest
t = bt.Backtest(s, data)

# and let's run it!
res = bt.run(t)


if __name__ == "__main__":
    print(list(res.display()))
