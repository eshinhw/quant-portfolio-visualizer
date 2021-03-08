from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import expected_returns
from pypfopt import risk_models

import pandas_datareader.data as web
import datetime as dt

import pandas as pd


from pypfopt import plotting
from pypfopt import cla


#-------------------------------------------------
# TICKER INPUTS & PRICE DATAFRAME
#-------------------------------------------------

symbols = ['FB', 'JNJ', 'DIS', 'T', 'O', 'PG']

START_DATE = dt.datetime(1970,1,1)
END_DATE = dt.datetime.today()

df = web.DataReader(symbols, 'yahoo', START_DATE, END_DATE)['Adj Close']

performance = pd.DataFrame(columns=['Portfolio', 'Expected Return', 'Annual Volatility', 'Sharpe Ratio'])

print(performance)

#-------------------------------------------------
# STATISTICAL INPUTS FOR PORTFOLIO OPTIMIZATION
#-------------------------------------------------

mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

plotting.plot_covariance(S)

#-------------------------------------------------
# MAX SHARPE PORTFOLIO
#-------------------------------------------------
maxSharpe = EfficientFrontier(mu, S)

maxSharpe.max_sharpe()

maxSharpe_weights = maxSharpe.clean_weights()

maxSharpe_result = maxSharpe.portfolio_performance(verbose=True)

data = {'Portfolio': 'Max Sharpe', 'Expected Return': maxSharpe_result[0], 'Annual Volatility': maxSharpe_result[1], 'Sharpe Ratio': maxSharpe_result[2]}

performance = performance.append(data, ignore_index=True)

plotting.plot_weights(maxSharpe_weights)

#-------------------------------------------------
# MIN VOLATILITY PORTFOLIO
#-------------------------------------------------

minVol = EfficientFrontier(mu,S)

minVol.min_volatility()

minVol_weights = minVol.clean_weights()

minVol_result = minVol.portfolio_performance(verbose=True)

data = {'Portfolio': 'Min Volatility', 'Expected Return': minVol_result[0], 'Annual Volatility': minVol_result[1], 'Sharpe Ratio': minVol_result[2]}

performance = performance.append(data, ignore_index=True)

#-------------------------------------------------
# MAX QUADRATIC UTILITY PORTFOLIO
#-------------------------------------------------

maxQuadraticUtility = EfficientFrontier(mu,S)

maxQuadraticUtility.max_quadratic_utility()

maxQuadraticUtility_weights = maxQuadraticUtility.clean_weights()

maxQuadraticUtility_result = maxQuadraticUtility.portfolio_performance(verbose=True)

data = {'Portfolio': 'Max Quadratic Utility', 'Expected Return': maxQuadraticUtility_result[0], 'Annual Volatility': maxQuadraticUtility_result[1], 'Sharpe Ratio': maxQuadraticUtility_result[2]}

performance = performance.append(data, ignore_index=True)

#-------------------------------------------------
# OPTIMIZED PORTFOLIO IN CLA OBJECT FOR PLOTTING
#-------------------------------------------------

# Efficient Frontier for Maximum Sharpe Portfolio
maxSharpeCLA = cla.CLA(mu,S)
maxSharpeCLA.max_sharpe()
plotting.plot_efficient_frontier(maxSharpeCLA, show_assets=True)

# Efficient Frontier for Minimum Volatility Portfolio
minVolCLA = cla.CLA(mu,S)
minVolCLA.min_volatility()
plotting.plot_efficient_frontier(minVolCLA, show_assets=True)

