#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dataSrc
import utilities
import pandas as pd


# In[2]:


# Retrieve symbols and financials

sp500_tickers = dataSrc.sp500_symbols()
dow_tickers = dataSrc.dow_symbols()
# sp500_financials = dataSrc.financials(sp500_tickers)


df = dataSrc.financials(dow_tickers)



# df = pd.read_csv('./R/data/dow_financials.csv')
# df = df.drop(['Unnamed: 0'], axis=1)
# df = df.dropna()



conditions = (df['Revenue_Growth'] > 0) &             (df['GPMargin'] > 0)&             (df['EPS_Growth'] > 0)&             (df['ROE'] > 0) &             (df['DPS_Growth'] > 0) &             (df['DivYield'] > 0)
df = df[conditions]




# Compute historical momentum
# Average momentum of prev 6M, 12M and 24M

mom_list = []
for symbol in df['symbol']:
    print(symbol)
    m12_momentum = utilities.calculate_hist_momentum(symbol, 252)
    m24_momentum = utilities.calculate_hist_momentum(symbol, 504)
    m36_momentum = utilities.calculate_hist_momentum(symbol, 756)
    avg_momentum = (m12_momentum + m24_momentum + m36_momentum) / 3
    mom_list.append(avg_momentum)

df['momentum'] = mom_list
df


# In[17]:


df['mom_rank'] = df['momentum'].rank()
df = df.sort_values(by=['mom_rank'], ascending=False)
# numRows = df.shape[0]
# numCols = df.shape[1]
# top10 = df.copy()
df = df[df['momentum'] > 0]


# In[18]:


watchlist = df[['symbol','name']].copy()
watchlist


# In[19]:


# Update current prices, 52W High and Discount %

currentPrices = []
highs = []
discounts = []

for symbol in watchlist['symbol']:
    print(symbol)
    currentPrice = utilities.get_current_price(symbol)
    high = utilities.calculate_prev_max_high(symbol, 252)
    discount_pct = (currentPrice - high) / high

    currentPrices.append(currentPrice)
    highs.append(high)
    discounts.append(discount_pct)


watchlist['CurrentPrice'] = currentPrices
watchlist['52W_High'] = highs
watchlist['Discount%'] = discounts



# In[20]:


watchlist = watchlist.sort_values(by='Discount%')


# In[21]:


watchlist


# In[ ]:





# In[ ]:




