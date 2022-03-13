<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/139356204-1253068f-b11c-4507-a921-6e77112b7a55.png">
</p>

# pyTrader

Deleveop an automated trading bot to capitalize trading opportunities in FX markets.

## External Resources

- Market Data: [OANDA API](https://developer.oanda.com/)
- Trading Automation: [Google Cloud Platform (GCP) Virtual Machine](https://cloud.google.com/)

## Account Verification

- Account Performance Verification: [Myfxbook - Trending MA Crossover](https://www.myfxbook.com/members/EddieShin/tf-ma/9190213)

## Moving Averages Crossover Strategy

I learned the base of this trading system from [Leveraged Trading](https://www.amazon.com/Leveraged-Trading-professional-approach-trading/dp/0857197215/ref=sr_1_1?crid=21M6UR528CUFU&keywords=Leveraged+Trading%3A+A+professional+approach+to+trading+FX%2C+stocks+on+margin%2C+CFDs%2C+spread+bets+and+futures+for+all+traders&qid=1636410285&sprefix=leveraged+trading+a+professional+approach+to+trading+fx%2C+stocks+on+margin%2C+cfds%2C+spread+bets+and+futures+for+all+traders%2Caps%2C309&sr=8-1) written by [Rob Carver](https://qoppac.blogspot.com/).

### Trading Instrument

- EUR/USD

### Entry Rule

- Long @ Bullish Crossover D 120MA X D 480MA
- Short @ Bearish Crossover D 120MA X D 480MA

### Position Sizing

- 2% of total capital / trade
- Stop Loss for Long Trade: Entry - 2.5%
- Stop Loss for Short Trade: Entry + 2.5% 

### Exit Rule

- Trailing Stop automatically adjusts as the market moves in favor of position.

## Volatility Breakout Strategy

### Trading Instrument

- EUR/USD

### Entry Rule

- If the current market price breaks above previous high + (previous range * K), buy at the breakout.
- If the current market price falls below previous low - (previous range * K), sell at the breakout.

### Position Sizing

- 1% / trade

### Exit Rule

- Close all trades at the end of the day.

