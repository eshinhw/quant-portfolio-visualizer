import pandas as pd
import numpy as np
import pandas_datareader.data as web

QUINTILES = ["Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"]


def get_beta_cummulative_returns():
    monthly_ret = web.DataReader(
        "Portfolios_Formed_on_BETA", "famafrench", start="1900-01-01"
    )[0]
    monthly_ret_cum = np.log(1 + monthly_ret / 100).cumsum()
    monthly_ret_cum.reset_index(inplace=True)
    monthly_ret_cum["Date"] = monthly_ret_cum["Date"].astype(str)
    monthly_ret_cum.rename(
        columns={"Lo 20": "Low Beta", "Hi 20": "High Beta"}, inplace=True
    )
    # print(monthly_ret_cum)
    return monthly_ret_cum[["Date", "Low Beta", "High Beta"]]


def beta_factor_stat():
    data = {}

    monthly_ret = web.DataReader(
        "Portfolios_Formed_on_BETA", "famafrench", start="1900-01-01"
    )[0][QUINTILES]
    n = len(monthly_ret)
    ret_ari = (monthly_ret / 100).mean(axis=0) * 12
    ret_geo = (1 + monthly_ret / 100).prod() ** (12 / n) - 1
    vol = (monthly_ret / 100).std(axis=0) * np.sqrt(12)
    sharpe = ret_ari / vol

    data["Quintiles"] = QUINTILES
    data["Arithmetic Mean"] = list(ret_ari.values)
    data["Geometric Mean"] = list(ret_geo.values)
    data["Annualized Volatility"] = list(vol)
    data["Sharpe Ratio"] = list(sharpe)

    stat = pd.DataFrame(data).round(3)

    return stat


if __name__ == "__main__":
    get_beta_cummulative_returns()
