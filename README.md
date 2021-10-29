# pyTrader

Deleveop a trading bot deployed in Forex, CFD and Cryptocurrency markets to capitalize short term or swing trading opportunities in systematic ways.
## Data Sources

- [OANDA API](https://developer.oanda.com/)
- [Financial Modelling Prep API](https://financialmodelingprep.com/developer/docs/)

## Volatility Breakout Strategy (Larry Williams)

The trading bot uses Volatility Breakout strategy developed by Larry Williams. You can find lots of free resources online. 

In addition to technical components of the strategy, it also utilizies time-series data prediction model called **Prophet** developed by Facebook. Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. You can learn more about this [here](https://facebook.github.io/prophet/).

## Trend Following + Momentum Strategy (Rob Carver)

### 1. Determine Investment Universe
- FX Pairs

### 2. Entry Rule: Moving Averages Crossover

- Long @ 60MA golden cross 252MA
- Short @ 60MA dead cross 252MA

### 3. Position Sizing

- 1~5% per trade

### 4. Stop Loss for Risk Management

- Trailing Stop @ ATR_MULTIPLIER * ATR(252)
