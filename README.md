<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/139356204-1253068f-b11c-4507-a921-6e77112b7a55.png">
</p>

# pyTrader

Deleveop a trading bot to capitalize short term and swing trading opportunities in FX markets.

## Data Sources

- [OANDA API](https://developer.oanda.com/)

## Trading Automation 

- [Google Cloud Platform (GCP) Virtual Machine](https://cloud.google.com/)

## Trend Following + MA Crossover Strategy (Rob Carver)

### 1. Determine Investment Universe

- Major FX Pairs: USD, JPY, EUR, AUD, NZD, CAD

### 2. Entry Rule: Moving Averages Crossover

- Long @ H1 120MA X H1 720MA
- Short @ H1 120MA X H1 720MA

### 3. Position Sizing

- 1~5% per trade

### 4. Stop Loss for Risk Management

- Trailing Stop with Average True Range (ATR)
- Structural Stop Loss Management based on Previous Support/Resistance

## Volatility Breakout Strategy (Larry Williams)

The trading bot uses Volatility Breakout strategy developed by Larry Williams. You can find lots of free resources online. 

In addition to technical components of the strategy, it also utilizies time-series data prediction model called **Prophet** developed by Facebook. Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. You can learn more about this [here](https://facebook.github.io/prophet/).
