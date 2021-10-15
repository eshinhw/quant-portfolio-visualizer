# pyTrader

Deleveop a trading bot deployed in forex & CFD markets to capitalize trading opportunities in systematic and algorithmic ways, using various historically proven trading strategies.

## Data Sources

- [Financial Modelling Prep API](https://financialmodelingprep.com/developer/docs/)
- [OANDA API](https://developer.oanda.com/)

## Trading Instruments

- FX/CFD
- Cryptocurrencies

## Turtle Trend Following Strategy

Long term trend following strategy with wide stop and target. **A breakout signal of previous highs or lows is considered as the beginning of new trend.** Stops are determined by Average True Range of previous days. By original turtle trading, system 1 uses shorter periods to catch short trend and system 2 uses longer periods to catch long term trend. You can learn more about turtle trading [here](https://bigpicture.typepad.com/comments/files/turtlerules.pdf).

In this repo, only system 2 will be implemented.

#### Trading Logics

- **Entry**: Breakout Long @ previous 55 days high or Breakout Short @ previous 55 days low
- **Stop Loss**: 2 x ATR
- **Take Profit (Modified)**: either 2 x ATR or 20 days low for long and 20 days high for short (whichever is close to current price)

## Against Turtle Reversal Strategy

It's known that original turtle trading system has about 30% of breakout success rate at key highs and lows. Then, about 70% of the time, markets fail to break out pre-determined key levels. Based on this statistical edge, We can create a simple reversal strategy which bets against original turtles to capitalize 70% of false breakouts. The reversal strategy takes long at previous key lows and takes short at previous key highs, expecting the markets to reverse. This strategy is known as 'Turtle Soup' by Linda Bradford-Raschke, and you can learn more about this strategy and many more short term trading strategies [here](https://www.amazon.ca/Street-Smarts-Probability-Trading-Strategies/dp/0965046109).

#### Trading Logics

- **Entry**: Long @ previous X days low or Short @ previous X days high
- **Stop Loss**: Trailing stop to limit the downside risk
- **Take Profit (Modified)**: Until the initial trailing stop is hit.

## Volatility Breakout Strategy
