# pyQuant

Welcome to pyQuant! :)

## Table of Contents
* [Data Sources](#data-sources)
* [Prerequisites: Basics of Quant Investing](#prerequisites)
* [Questrade Portfolio Manager](#questrade-portfolio-manager)
* [Fixed Asset Allocation Portfolios](#fixed-asset-allocations)
* [Tactical Asset Allocation Portfolios](#tactical-asset-allocations)
  * [Dual Momentum](#dual-momentum)
  * [Vigilant Asset Allocation (VAA)](#vigilant-asset-allocation)
  * [Defensive Asset Allocation (DAA)](#defensive-asset-allocation)
* [Individual Stock Investing](#individual-stock-investing)

## Data Sources <a name="data-sources"></a>

- [Financial Modelling Prep API](https://financialmodelingprep.com/developer/docs/)
- [Questrade API](https://www.questrade.com/api)

## Prerequisites: Basics of Quant Investing <a name="prerequisites"></a>

Below is a collection of jupyter notebooks which touch upon the basics of quantitative investing and data analysis in Python Pandas.

- Working with Pandas DataFrame Notebook
- Returns, Volatility and Sharpe Ratio of Stocks Notebook
- Maximum Drawdown (MDD) Notebook
- Portfolio Statistics and Optimizaion with PyPortfolioOpt Notebook
- Performance Against Benchmark Notebook

## Questrade Portfolio Manager <a name="questrade-portfolio-manager"></a>

### Portfolio Holdings

<p align="center">
  <img width="600" height="600" src="https://user-images.githubusercontent.com/41933169/112911987-84be8400-90c4-11eb-94cf-b3c9836887f5.png">
</p>

<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/112912042-a15abc00-90c4-11eb-8098-4c1e84b4b433.png">
</p>

### Monthly Dividend Income

<p align="center">
  <img width="800" height="500" src="https://user-images.githubusercontent.com/41933169/112912007-90aa4600-90c4-11eb-9868-7e1939e89af2.png">
</p>

## Fixed Asset Allocation Portfolios <a name="fixed-asset-allocations"></a>

- Traditonal 60/40 Portfolio
- Four Seasons Portfolio
- All Weather Portfolio
- Permanent Portfolio

<p align="center">
  <img width="800" height="500" src="https://user-images.githubusercontent.com/41933169/134737654-68260fef-7996-443e-89cf-1ed0a8510052.png">
</p>

## Tactical Asset Allocation Portfolios <a name="tactical-asset-allocations"></a>

### Dual Momentum <a name="dual-momentum"></a>

<p align="center">
  <img width="800" height="500" src="https://user-images.githubusercontent.com/41933169/134734529-a66b258b-bc31-433a-95be-d72cd367fb93.png">
</p>

### Vigilant Asset Allocation (VAA) <a name="vigilant-asset-allocation"></a>

<p align="center">
  <img width="800" height="500" src="https://user-images.githubusercontent.com/41933169/134711294-cf8d6242-df12-436d-b8ca-736a06a80083.png">
</p>

<p align="center">
  <img width="600" height="400" src="https://user-images.githubusercontent.com/41933169/134708641-5b99eeb7-c6cc-497c-84a8-9f82ef10489e.png">
</p>

<p align="center">
  <img width="800" height="500" src="https://user-images.githubusercontent.com/41933169/134711636-525a29bf-1b1d-48dd-8fcf-ae14b8001486.png">
</p>

### Defensive Asset Allocation (DAA) <a name="defensive-asset-allocations"></a>

## Individual Stock Investing <a name="individual-stock-investing"></a>

Below is a collection of jupyter notebooks for individual stock investing.

- Quantitative Stock Selection Notebook
- Historical Dividend Payout Notebook

### Investment Goals

- Good Dividend History
- High Dividend Growth Rate
- Strong Historical Momentum (Historical Price Movement)

### Financial Ratios Considered

- Market Cap (B)
- Revenue Growth
- Return on Equity (ROE)
- Gross Profit Margin
- EPS Growth
- Dividend Yield
- DPS
- DPS Growth





# pyTrader

## Introduction

Deleveop a trading bot deployed in forex & CFD markets to capitalize trading opportunities in systematic and algorithmic ways, using various historically proven trading strategies.

## Trading Platform & Data Source

- [OANDA API](https://developer.oanda.com/)

## Trend Following Strategy

### Strategy Overview

Long term trend following strategy with wide stop and target. **A breakout signal of previous highs or lows is considered as the beginning of new trend.** Stops are determined by Average True Range of previous days. By original turtle trading, system 1 uses shorter periods to catch short trend and system 2 uses longer periods to catch long term trend. You can learn more about turtle trading [here](https://bigpicture.typepad.com/comments/files/turtlerules.pdf).

In this repo, only system 2 will be implemented.

### System 2 Trading Logics

- **Entry**: Breakout Long @ previous 55 days high or Breakout Short @ previous 55 days low
- **Stop Loss**: 2 x ATR
- **Take Profit (Modified)**: either 2 x ATR or 20 days low for long and 20 days high for short (whichever is close to current price)

## Reversal Strategy

### Strategy Overview

It's known that original turtle trading system has about 30% of breakout success rate at key highs and lows. Then, about 70% of the time, markets fail to break out pre-determined key levels. Based on this statistical edge, We can create a simple reversal strategy which bets against original turtles to capitalize 70% of false breakouts. The reversal strategy takes long at previous key lows and takes short at previous key highs, expecting the markets to reverse. This strategy is known as 'Turtle Soup' by Linda Bradford-Raschke, and you can learn more about this strategy and many more short term trading strategies [here](https://www.amazon.ca/Street-Smarts-Probability-Trading-Strategies/dp/0965046109).

### Trading Logics

- **Entry**: Long @ previous X days low or Short @ previous X days high
- **Stop Loss**: Trailing stop to limit the downside risk
- **Take Profit (Modified)**: Until the initial trailing stop is hit.
