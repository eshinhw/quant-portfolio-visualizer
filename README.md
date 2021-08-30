# Quantitative Stock Investing in Python

## Data Sources

- Financial Modelling Prep API (https://financialmodelingprep.com/developer/docs/)
- Questrade API (https://www.questrade.com/api)

## Data-Driven Stock Selection

### Key Considerations

- Good Dividend History
- High Dividend Growth Rate
- Strong Historical Momentum (Historical Price Movement)

##### Good Stock Example: Johnson&Johnson (JNJ)

<p align="center">
  <img width="700" height="400" src="https://user-images.githubusercontent.com/41933169/117091817-7d754080-ad2a-11eb-8f87-c2bf3afc0bb4.png">
</p>

<p align="center">
  <img width="800" height="400" src="https://user-images.githubusercontent.com/41933169/115498299-53f0eb00-a23b-11eb-95f3-2f69c4439350.png">
</p>

##### Bad Stock Example: AT&T (T)

Even with high dividend yield, we can't expect high price appreciation.

<p align="center">
  <img width="700" height="400" src="https://user-images.githubusercontent.com/41933169/117091006-f030ec80-ad27-11eb-8fe5-0919d4cdbccf.png">
</p>

### Financial Factors

- Market Cap (B)
- Revenue Growth
- Return on Equity (ROE)
- Gross Profit Margin
- EPS Growth
- Dividend Yield
- DPS
- DPS Growth

I've developed a quantitative model which finds a list of stocks from S&P 500 which have **high historical dividend growth rate** and **strong historical price momentum** at the same time. I believe that these two factors are useful fundamental measures for long term dividend investors who are looking to achieve dividend growth and capital appreciation simultaneously.



Some of the matured companies such as AT&T have high dividend yield of 6.50% which is attractive but in terms of capital growth, it's not attractive at all. AT&T's price chart above shows that the stock price has been in the range of $20 and $60 almost over the last 30 years. Investors who have been investing in AT&T may have collected some dividends, but there is a possibility that their unrealized capital loss might be bigger than the total dividends collected.



### Factors to be Considered

- Minimum Market Cap
- No Dividend Cut History
- Minimum Dividend Growth Rate
- Long Term Trend Analysis based on Historical Momentum

Out of 500 stocks in the S&P 500 index, the model sorts out the companies which satisfy minimum market cap size and have paid dividends consecutively over a certain periods of years. The next step is to calculate historical dividend growth rate and historical long term momentum to select the companies which have high dividend growth rate and historical uptrend price movements. The model assumes that these companies are reliable companies we can buy as a dividend growth investor who looks for both dividend growth and capital appreciation at the same time.


## Visualizations on Account Activities

<p align="center">
  <img width="600" height="600" src="https://user-images.githubusercontent.com/41933169/112911987-84be8400-90c4-11eb-94cf-b3c9836887f5.png">
</p>

<p align="center">
Breakdown of Holdings
</p>

<p align="center">
  <img width="800" height="500" src="https://user-images.githubusercontent.com/41933169/112912007-90aa4600-90c4-11eb-9868-7e1939e89af2.png">
</p>

<p align="center">
Monthly Dividend Income
</p>

<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/112912042-a15abc00-90c4-11eb-8098-4c1e84b4b433.png">
</p>

<p align="center">
Holding Positions Summary
</p>

