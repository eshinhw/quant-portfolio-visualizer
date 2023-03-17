# %% [markdown]
# # Global Equities Momentum (GEM) and Global Balanced Momentum (GBM)

# %%
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# %% [markdown]
# ## Define asset allocation

# %%
portfolios = {'GEM': ['SPY', 'VEU', 'BND'],
              'GBM': ['SPY', 'VEU', 'BND'],
              'benchmark': ['SPY'],
              'sixtyForty': ['SPY', 'BND'],
              'Permanent': ['VTI', 'BIL', 'TLT', 'GLD']}
momentum = ['GEM', 'GBM']
fixed_portfolio = ['sixtyForty']

# %% [markdown]
# ## Retrieve historical monthly prices

# %%
combined_assets = []

for portfolio in portfolios.keys():
    combined_assets = combined_assets + portfolios[portfolio]

combined_assets = list(set(combined_assets))
combined_assets

# %%
prices = pd.DataFrame()
for asset in combined_assets:
    prices[asset] = fmp.get_monthly_prices(asset)[asset]

prices

# %% [markdown]
# ## Global Equities Momentum Portfolio

# %%
gem_prices = pd.DataFrame()
for col in prices.columns:
    if col in portfolios['GEM']:
        gem_prices[col] = prices[col]

monthly_momentum = gem_prices.copy()
monthly_momentum = monthly_momentum.apply(
    lambda x: x.shift(1)/x.shift(12) - 1, axis=0)
monthly_momentum.dropna(inplace=True)

rank_df = monthly_momentum.rank(axis=1, ascending=False)
for col in rank_df.columns:
    rank_df[col] = np.where(rank_df[col] == 1, 1, 0)

monthly_gem_returns = gem_prices.pct_change()
monthly_gem_returns.dropna(inplace=True)
monthly_gem_returns = monthly_gem_returns[rank_df.index[0]:].shift(-1)

port = np.multiply(rank_df, monthly_gem_returns)
port_returns = port.sum(axis=1)
port_cum_returns = np.exp(np.log1p(port_returns).cumsum())[:-1]
port_cum_returns

# %% [markdown]
# ## Global Balanced Momentum Portfolio

# %%
gbm_prices = pd.DataFrame()
for col in prices.columns:
    if col in portfolios['GBM']:
        gbm_prices[col] = prices[col]

gbm_momentum = gbm_prices.copy()
gbm_momentum = gbm_momentum.apply(lambda x: x.shift(1)/x.shift(12) - 1, axis=0)
gbm_momentum.dropna(inplace=True)

gbm_rank = gbm_momentum.rank(axis=1)
for col in gbm_rank.columns:
    gbm_rank[col] = np.where(gbm_rank[col] > 2, 1, 0)

monthly_gbm_returns = gbm_prices.pct_change()
monthly_gbm_returns.dropna(inplace=True)
monthly_gbm_returns = monthly_gbm_returns[gbm_rank.index[0]:]

gbm_sixty = np.multiply(gbm_rank, monthly_gbm_returns)
gbm_sixty_returns = gbm_sixty.sum(axis=1)

gbm_port = pd.DataFrame()
gbm_port['GBM_sixty'] = gbm_sixty_returns
gbm_port['GBM_forty'] = monthly_gbm_returns['BND']
weight = np.array([0.6, 0.4])
gbm_port['port_return'] = gbm_port.dot(weight)
gbm_cum_returns = (1 + gbm_port['port_return']).cumprod()
gbm_cum_returns

# %% [markdown]
# ## 60/40 Portfolio

# %%
sixtyForty = pd.DataFrame()

for col in prices.columns:
    if col in portfolios['sixtyForty']:
        sixtyForty[col] = prices[col]

sixtyForty_returns = sixtyForty.pct_change()
sixtyForty_returns = sixtyForty_returns[rank_df.index[0]:]
sixtyForty_weights = np.array([0.4, 0.6])
sixtyForty_returns['port'] = sixtyForty_returns.dot(sixtyForty_weights)
sixtyForty_cum_returns = np.exp(np.log1p(sixtyForty_returns['port']).cumsum())
sixtyForty_cum_returns

# %% [markdown]
# ## SPY (S&P 500 Index)

# %%
benchmark_prices = prices['SPY']
benchmark_returns = benchmark_prices.pct_change()
benchmark_returns = benchmark_returns[rank_df.index[0]:]
benchmark_cum_returns = np.exp(np.log1p(benchmark_returns).cumsum())
benchmark_cum_returns

# %% [markdown]
# ## Portfolio Performance Comparison

# %%
combined_df = pd.DataFrame()
combined_df['GEM'] = port_cum_returns
combined_df['GBM'] = gbm_cum_returns
combined_df['Sixty Forty'] = sixtyForty_cum_returns
combined_df['benchmark'] = benchmark_cum_returns
combined_df.iloc[0] = 1
combined_df.index = pd.to_datetime(combined_df.index)

stats_summary = pd.DataFrame(
    columns=['Portfolio', 'CAGR (%)', 'MDD (%)', 'CAGR/MDD'])

beginning_month = combined_df.index[0].year

for col in combined_df.columns:
    # compute CAGR
    first_value = combined_df[col][0]
    last_value = combined_df[col][-1]
    years = len(combined_df[col].index)/12
    cagr = (last_value/first_value)**(1/years) - 1

    # compute MDD
    cumulative_returns = combined_df[col]
    previous_peaks = cumulative_returns.cummax()
    drawdown = (cumulative_returns - previous_peaks) / previous_peaks
    portfolio_mdd = drawdown.min()

    # save CAGR and MDD for each portfolio

    stats_summary = stats_summary.append({'Portfolio': col,
                                         'CAGR (%)': cagr * 100,
                                          'MDD (%)': portfolio_mdd * 100,
                                          'CAGR/MDD': abs(cagr / portfolio_mdd).round(2)}, ignore_index=True)

stats_summary.set_index('Portfolio', inplace=True)
stats_summary.sort_values('CAGR/MDD', ascending=False, inplace=True)
stats_summary

# %% [markdown]
# ## Performance Visualization

# %%
plt.figure(figsize=(15, 10))
plt.plot(combined_df)
plt.legend(combined_df.columns)
plt.xlabel('Date')
plt.ylabel('Returns')
plt.title('Portfolio Performance Comparison')

# %%
