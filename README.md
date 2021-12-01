<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/139356204-1253068f-b11c-4507-a921-6e77112b7a55.png">
</p>

# pyTrader

Deleveop an automated trading bot to capitalize trading opportunities in FX markets.

<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/141128813-6cf66bd2-84e2-41f4-b9d4-93206c3b9276.png">
</p>

## External Resources

- Market Data: [OANDA API](https://developer.oanda.com/)
- Trading Automation: [Google Cloud Platform (GCP) Virtual Machine](https://cloud.google.com/)


## Account Verification

- Account Performance Verification: [Myfxbook - Trending MA Crossover](https://www.myfxbook.com/members/EddieShin/tf-ma/9190213)

## Trend Following + MA Crossover Strategy

I learned the base of this trading system from [Leveraged Trading](https://www.amazon.com/Leveraged-Trading-professional-approach-trading/dp/0857197215/ref=sr_1_1?crid=21M6UR528CUFU&keywords=Leveraged+Trading%3A+A+professional+approach+to+trading+FX%2C+stocks+on+margin%2C+CFDs%2C+spread+bets+and+futures+for+all+traders&qid=1636410285&sprefix=leveraged+trading+a+professional+approach+to+trading+fx%2C+stocks+on+margin%2C+cfds%2C+spread+bets+and+futures+for+all+traders%2Caps%2C309&sr=8-1) written by [Rob Carver](https://qoppac.blogspot.com/).

### 1. Determine Investment Universe

- Global FX Pairs

### 2. Entry Rule: Moving Averages Crossover

- Long @ Bullish Crossover D 120MA X D 480MA
- Short @ Bearish Crossover D 120MA X D 480MA

### 3. Position Sizing & Stop Loss

- 2% of total capital / trade
- Stop Loss for Long Trade: Entry - 2.5%
- Stop Loss for Short Trade: Entry + 2.5% 

### 4. Exit Rule: Counter Moving Averages Crossover (Continuous Trading)

- If currently in long trade and bearish crossover occurs, exit the long trade and enter the short trade.
- If currently in short trade and bullish crossover occurs, exit the short trade and enter the long trade.

## Overall Comments

I've tried other short-term strategies like **Volatility Breakout** and **Reversal** but none of them really worked well in FX markets. I decided to focus on longer term trading systems which are simple and intuitive.

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
