# %%
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

# %% [markdown]
# ## Import Portfolio Classes

# %%
from vaa import VAA
from fixed_allocations import FixedAllocation

vaa = VAA()
spy = FixedAllocation('SPY',['SPY'],np.array([1]))
sf = FixedAllocation("60% Stocks & 40% Bonds",['BND', 'SPY'],np.array([0.4, 0.6]))
fs = FixedAllocation("Four Seasons",['VTI', 'TLT', 'IEF', 'GLD', 'DBC'],np.array([0.3, 0.4, 0.15, 0.075, 0.075]))
aw = FixedAllocation("All Weather",['VT', 'LTPZ', 'EDV', 'VCLT', 'EMLC', 'IAU', 'BCI'],np.array([0.35, 0.2, 0.2, 0.075, 0.075, 0.05, 0.05]))
pm = FixedAllocation("Permanent",['VTI', 'IEF', 'TLT', 'GLD'],np.array([0.25, 0.25, 0.25, 0.25]))

portfolios = [vaa, spy, sf, fs, aw, pm]

# %% [markdown]
# ## CAGR and MDD Comparison

# %%
strategies = {}

for p in portfolios:
    strategies[str(p)] = {}
    strategies[str(p)]['CAGR'] = p.cagr()
    strategies[str(p)]['MDD'] = p.mdd()
    strategies[str(p)]['CAGR/MDD'] = p.cagr() / -p.mdd()

summary = pd.DataFrame(strategies)
summary.transpose()

# %% [markdown]
# ## Cummulative Returns of Portfolios

# %%
cummulative_returns = {}

for p in portfolios:
    cummulative_returns[str(p)] = p.port_cum_returns

# %%
cum_returns_df = pd.DataFrame(cummulative_returns)
cum_returns_df.dropna(inplace=True)

for port in cum_returns_df.columns:
    cum_returns_df[port] = cum_returns_df[port] / cum_returns_df.loc[cum_returns_df.index[0],port]

# %%
type(cum_returns_df.index[0])
cum_returns_df.index = pd.to_datetime(cum_returns_df.index)
type(cum_returns_df.index[0])

# %% [markdown]
# ## SPY Performance Summary

# %% [markdown]
# ## 60% Stocks + 40% Bond

# %%
sf.report()

# %% [markdown]
# ## Four Seasons

# %%
fs.report()

# %% [markdown]
# ## Performance Visualization

# %%
### Backtesting Performance Comparison (All Portfolios)
plt.figure(figsize=(15,10))
plt.plot(cum_returns_df)
plt.legend(cum_returns_df.columns)
plt.xlabel('Date')
plt.ylabel('Returns')
plt.title('Historical Cummulative Returns of Portfolios')
### Backtesting Performance Comparison (Original VAA, 60/40, SPY)
# sub_df = combined_df[['VAA/Original', '60/40', 'SPY']]
# plt.figure(figsize=(15,10))
# plt.plot(sub_df)
# plt.legend(sub_df.columns)
# plt.xlabel('Date')
# plt.ylabel('Returns')
# plt.title('Portfolio Performance Comparison')

# %%



