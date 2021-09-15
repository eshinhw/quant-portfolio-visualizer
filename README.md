# FX Trading Bot

## Introduction

Deleveop a trading bot deployed in forex & CFD markets to capitalize trading opportunities in systematic and algorithmic ways, using various historically proven trading strategies.

## Trend Following Strategy (Original Turtle Traders)

#### Strategy Overview

Long term trend following strategy with wide stop and target. A breakout signal of previous highs or lows is considered as the beginning of new trend. Stops are determined by Average True Range of previous days. System 1 uses shorter periods to catch short trend and System 2 uses longer periods to catch long term trend.

In this demonstration, only System 2 is implemented.

#### System 2 Trading Rules

- **Entry**: Breakout Long @ previous 55 days high / Breakout Short @ previous 55 days low
- **Stop Loss**: 2 x ATR
- **Take Profit (Modified)**: either 2 x ATR or 20 days low for long and 20 days high for short (whichever is close to current price)

#### Source Resource

- The Original Turtle Rules: https://bigpicture.typepad.com/comments/files/turtlerules.pdf

## Reversal Strategy (Turtle Soup by Linda Bradford-Raschke)

#### Strategy Overview

If original turtle trading system has about 30% of breakout success rate at key highs and lows, then 70% of the time, markets fail to break out pre-determined key levels. We can reverse-engineer to bet against original turtles to capitalize 70% of false breakouts. 'Turtle Soup' strategy goes long at previous lows and goes short at previous highs, expecting the markets to reverse.

#### Trading Rules

- **Entry**: Long @ previous X days low and Short @ previous X days high
- **Stop Loss**: Trailing stop to limit the downside risk
- **Take Profit (Modified)**: Until the initial trailing stop is hit.
