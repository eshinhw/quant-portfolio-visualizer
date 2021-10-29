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

### 2. Historical Momentum (Emphasis on Recent Momentum)

### 3. Entry Rule: Moving Averages Crossover

- Long @ 60MA golden cross 252MA
- Short @ 60MA dead cross 252MA

### 4. Position Sizing

- 1~5% per trade

### 5. Stop Loss for Risk Management

- Trailing Stop @ ATR_MULTIPLIER * ATR(252)



<!-- ## Turtle Trend Following Strategy (Depreciated)

Long term trend following strategy with wide stop and target. **A breakout signal of previous highs or lows is considered as the beginning of new trend.** Stops are determined by Average True Range of previous days. By original turtle trading, system 1 uses shorter periods to catch short trend and system 2 uses longer periods to catch long term trend. You can learn more about turtle trading [here](https://bigpicture.typepad.com/comments/files/turtlerules.pdf).

In this repo, only system 2 will be implemented.

#### Trading Logics

- **Entry**: Breakout Long @ previous 55 days high or Breakout Short @ previous 55 days low
- **Stop Loss**: 2 x ATR
- **Take Profit (Modified)**: either 2 x ATR or 20 days low for long and 20 days high for short (whichever is close to current price)
-->
