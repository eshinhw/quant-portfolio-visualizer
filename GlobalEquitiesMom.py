
import pandas as pd
import datetime as dt
import yfinance as yf

EQUITIES_ETF = ['SPY', 'QQQ', 'VXUS']

def equal_weighted_momentum(prices):
    '''equal weighted momentum'''
    m1 = prices / prices.shift(1) - 1
    m3 = prices / prices.shift(3) - 1
    m6 = prices / prices.shift(6) - 1
    m9 = prices / prices.shift(9) - 1
    m12 = prices / prices.shift(12) - 1
    return m1 + m3 + m6 + m9 + m12


def keller_momentum(x):
    """
    momentum_periods = [1,3,6,12]
    momentum_weights = np.array([12,4,2,1])
    """
    m1 = x / x.shift(1) - 1
    m3 = x / x.shift(3) - 1
    m6 = x / x.shift(6) - 1
    m12 = x / x.shift(12) - 1
    return 12 * m1 + 4 * m3 + 2 * m6 + 1 * m12

def monthly_prices(assets):
    monthly_prices = pd.DataFrame()
    for asset in assets:
        monthly_prices[asset] = yf.download(asset, start= dt.datetime(2018,1,1), end = dt.datetime.today(),interval='1mo', progress=False)['Adj Close']
    monthly_prices.dropna(inplace=True)
    return monthly_prices

def momentum_score(prices):
    # calcuate weighted momentum scores at each month
    # ew_mom_score = prices.copy().apply(equal_weighted_momentum,axis=0)
    keller_mom_score = prices.copy().apply(keller_momentum,axis=0)
    keller_mom_score.dropna(inplace=True)
    return keller_mom_score

if __name__ == "__main__":
    prices_df = monthly_prices(EQUITIES_ETF)
    # print(equal_weighted_momentum(prices_df))
    print(keller_momentum(prices_df))
    print(momentum_score(prices_df))