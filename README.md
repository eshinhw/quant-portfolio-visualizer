# Py Trader

## Introduction

Deleveop a trading bot deployed in forex & CFD markets to capitalize trading opportunities in systematic and algorithmic ways, using various historically proven trading strategies.

## Limitations of FX & CFD Trading with Brokers (Before We Begin)

FX & CFD trading looks attractive for beginners who are interested in trading the markets, as they only need small amount of capital to start trading and it's very easy to access the markets from Forex brokers. However, there are downsides of it when you want to seriously manage large amount of money in this platform. Compared to stock markets and futures markets, you are not trading against real players in centralized and regulated exchanges, but trading against the brokers that you are registered with. Therefore, there is information disadvantages between you and your brokers as your broker knows everything about your open trades, transactions and account activities. They can always use those information against you for their own benefits.

My advice is that if you really want to go into trading seriously, you should look into futures instead of FX & CFD. Trading futures involves real market participation through centralized exchanges, and you have access to real market order flows which are transparant and no hidden stuff.

In summary, it's a good practice to test trading algorithms through these FX brokers, but be aware of hidden truth about them as well. 

## Trend Following by Original Turtle Traders

<p align="center">
  <img width="400" height="300" src="https://user-images.githubusercontent.com/41933169/113924806-3f7f0e00-97b8-11eb-918a-b2b2cd8e8e0b.png">
</p>

#### Strategy Overview

Long term trend following strategy with wide stop and target. A breakout signal of previous highs or lows is considered as the beginning of new trend. Stops are determined by Average True Range of previous days. System 1 uses shorter periods to catch short trend and System 2 uses longer periods to catch long term trend.

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
- Out-dated strategy with today's advanced markets.

#### Resources

- The Original Turtle Rules: https://bigpicture.typepad.com/comments/files/turtlerules.pdf

## Turtle Soup by Linda Bradford-Raschke

<p align="center">
  <img width="700" height="500" src="https://user-images.githubusercontent.com/41933169/114284407-a7825e00-9a1d-11eb-8a42-38906125221b.png">
</p>

#### Strategy Overview

Since original turtle trading system has about 30% of breakout success rate at key highs and lows, that means 70% of the time markets fail to break out key levels. We can reverse-engineer to bet against original turtles to capitalize 70% of false breakouts. 'Turtle Soup' strategy goes long at previous lows and goes short at previous highs, entering trades against original turtles.

'Turtle Soup Plus One' can further improve the success rate by wating for one day at key ares until the daily candle completes to determine whether previous highs or lows are right places to enter. If the daily candle indicates that the highs or lows are not going to hold, it doesn't enter a trade. However, if the daily candle shows some sort of rejections at the level, we can enter a trade. 

## Volatility Breakout Strategy by Larry Williams (Still In Development)

<p align="center">
  <img width="700" height="500" src="https://user-images.githubusercontent.com/41933169/114284586-e4028980-9a1e-11eb-893b-e2df34434285.png">
</p>

#### Strategy Overview

- Follow daily breakout momentum.
- Entry determined by previous day's range * K (0 <= K <= 1, usually K = 0.5 ~ 0.6)
- Trailing stop to maximize return and minimize risk

#### Issues

- Price data misalignment issue from weekend since fx markets don't have official open and close time like stock markets.
- Need to filter out specified time periods like from London Open to NY Close.
