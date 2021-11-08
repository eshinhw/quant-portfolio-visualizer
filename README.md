<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/139356204-1253068f-b11c-4507-a921-6e77112b7a55.png">
</p>

# pyTrader

Deleveop an automated trading bot to capitalize short term trading opportunities in FX markets. With the scripts in pyTrader, I can manage lots of orders and trades at once.

<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/140251156-0dadf0d7-ff8d-4a40-a598-95bb8ecc9c1d.png">
</p>

<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/140251232-6cec6486-fc71-4225-982c-c000e0a8c981.png">
</p>

## External Resources

- Market Data: [OANDA API](https://developer.oanda.com/)
- Trading Automation: [Google Cloud Platform (GCP) Virtual Machine](https://cloud.google.com/)
- Account Performance Verification: [Trending MA Crossover](https://www.myfxbook.com/members/EddieShin/trending-ma-crossover/9170659)

## Trend Following + MA Crossover Strategy (Rob Carver)

### 1. Determine Investment Universe

- Global FX Pairs

### 2. Entry Rule: Moving Averages Crossover

- Long @ Bullish Crossover D 120MA X D 480MA
- Short @ Bearish Crossover D 120MA X D 480MA

### 3. Position Sizing & Stop Loss

- 2% of total capital / trade
- Stop Loss for Long Trade: Entry - 2.5%
- Stop Loss for Short Trade: Entry + 2.5% 

### 4. Exit Rule: Counter Moving Averages Crossover

- If currently in long trade and bearish crossover occurs, exit the long trade.
- If currently in short trade and bullish crossover occurs, exit the short trade.

<!-- ## Monthly Support/Resistance Reversal Strategy

### 1. Determine Investment Universe

- Global FX Pairs

### 2. Entry Rule

- Determine monthly lows and highs.
- Place two types of orders at the same time: limit order for reversal and stop order for breakout

### 3. Position Sizing

- 0.01% per trade

### 4. Stop Loss for Risk Management

- Entry +/- Average True Range (ATR)
- Close at the end of day (24 hours time cut)

In addition to technical components of the strategy, it also utilizies time-series data prediction model called **Prophet** developed by Facebook. Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. You can learn more about this [here](https://facebook.github.io/prophet/). -->
