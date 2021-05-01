# Py OANDA Forex Trader

## Introduction

Deleveop a trading bot deployed in forex & CFD markets to capitalize trading opportunities in systematic and algorithmic ways, using various historically proven trading strategies.

## Disclaimer & Limitation of FX & CFD Trading

FX & CFD trading looks attractive for beginners who are interested in trading the markets. They can start trading with small amount of capital and many forex brokers provide instant access to the markets without much restrictions. However, there are downsides of it when you want to seriously manage large amount of money. The main limitation is you are most likely trading against your broker with the quotes provided by them. Therefore, there is information disadvantages between you and your brokers as your broker knows everything about your open trades, transactions and account activities. They can always use those information against you for their own benefits when market conditions go wild.

My advice is that if you really want to trade the markets seriously, you should consider trading futures or other derivatives which are traded in centralized and regulated exchanges. For example, trading futures involves real market participation through centralized exchanges, and you have access to real market order flows which are transparant and no hidden stuff. 

In summary, forex and cfd are good instruments for you to test your algorithms with small amount of capital, but I don't recommend using them for large accounts due to the reasons above. 

## Trend Following Strategy (Original Turtle Traders)

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

## Reversal Strategy (Turtle Soup by Linda Bradford-Raschke)

<p align="center">
  <img width="500" height="500" src="https://user-images.githubusercontent.com/41933169/116794213-4ccaa800-aa99-11eb-9405-0766a6a5999c.png">
</p>

#### Strategy Overview

Since original turtle trading system has about 30% of breakout success rate at key highs and lows, that means 70% of the time markets fail to break out key levels. We can reverse-engineer to bet against original turtles to capitalize 70% of false breakouts. 'Turtle Soup' strategy goes long at previous lows and goes short at previous highs, expecting the markets to reverse.

<p align="center">
  <img width="900" height="450" src="https://user-images.githubusercontent.com/41933169/116794365-7df7a800-aa9a-11eb-9d3d-ad6392b33f10.png">
</p>

#### Pros

- Testing the key levels doesn't require large stops which means risk reward ratio can be improved if the market moves in favour of our positions.


#### Cons

- The markets might move choppy around the key levels and we have no quantifiable information about how much the market actually behaves and reacts around the key levels. 
