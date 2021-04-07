# Py Trading Bot

## Introduction

Deleveop a trading bot deployed in forex & CFD markets to capitalize trading opportunities in systematic and algorithmic ways, using various historically proven trading strategies.

## Trend Following by Turtle Traders

<p align="center">
  <img width="400" height="300" src="https://user-images.githubusercontent.com/41933169/113924806-3f7f0e00-97b8-11eb-918a-b2b2cd8e8e0b.png">
</p>

#### Strategy Overview

- Long term trend following strategy with wide stop and target.
- A breakout signal of previous highs or lows is considered as the beginning of new trend.
- Stops are determined by Average True Range of previous days.
- System 1 uses shorter periods to catch short trend and System 2 uses longer periods to catch long term trend.

#### Trading Rules (System 2)

- **Entry**: Breakout Long @ previous 55 days high / Breakout Short @ previous 55 days low
- **Stop Loss**: 2 x ATR
- **Take Profit (Modified)**: either 2 x ATR or 20 days low for long and 20 days high for short (whichever is close to current price)

#### Pros

- Easy to understand and simple rules.
- Less frequent trades.

#### Cons

- Possibly lots of small losing trades, and it must catch big trends to cover previous losses.
- Long term view might not be best for FX markets with lots of noise and consolidation phases.

#### Resources

- The Original Turtle Rules: https://bigpicture.typepad.com/comments/files/turtlerules.pdf

## Volatility Breakout Strategy by Larry Williams

- Coming up soon...


