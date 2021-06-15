# Automated Quantitative Investing with Financial Modeling Prep API and Questrade API

## Introduction

Questrade is one of the investing brokers in Canada, and I have an investing account with them that I want to keep track of regularly. A jupyter notebook called 'Questrade Portfolio Manager' retrieves account information using Questrade API called 'qtrade' and summarizes some useful information such as monthly account activities, position changes and dividend income that I earned every month. Whenever I want to know how my investing account is doing, all I need to do is just run this notebook from time to time. In terms of security, qtrade wrapper automatically refreshes a security token, so I don't have to log in to the website to get a new token everytime I run the notebook. Below are a sample dataframe and visualizations I can create from the notebook.

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

## Quantitative Model for Stock Selection

### Model Assumptions

I've developed a quantitative model which finds a list of stocks from S&P 500 which have high historical dividend growth rate and strong historical price momentum at the same time. I believe that these two factors can be useful fundamental factors for long term dividend investors who are looking to achieve dividend growth and capital appreciation simultaneously. 

<p align="center">
  <img width="700" height="400" src="https://user-images.githubusercontent.com/41933169/117091006-f030ec80-ad27-11eb-8fe5-0919d4cdbccf.png">
</p>

Some of the matured companies such as AT&T have high dividend yield of 6.50% which is attractive but in terms of capital growth, it's not quite attractive at all. AT&T's price chart above shows that the stock price has been in the range of $20 and $60 almost over the last 30 years. Investors who have been investing in AT&T may have collected much dividends, but there is a possibility that their unrealized capital loss might be bigger than the total dividends collected.

<p align="center">
  <img width="700" height="400" src="https://user-images.githubusercontent.com/41933169/117091817-7d754080-ad2a-11eb-8f87-c2bf3afc0bb4.png">
</p>

In comparison, Johnson&Johnson is a company which has been paying dividends consecutively many decades, but more attractively, its price has been growing steadly over the long period. This is the company we want to invest in. 

<p align="center">
  <img width="800" height="400" src="https://user-images.githubusercontent.com/41933169/115498299-53f0eb00-a23b-11eb-95f3-2f69c4439350.png">
</p>

The dividend history for Johnson&Johnson looks very stable and steady as well.

### Factors to be Considered

- Minimum Market Cap
- No Dividend Cut History
- Minimum Dividend Growth Rate
- Long Term Trend Analysis based on Historical Momentum

Out of 500 stocks in the S&P 500 index, the model sorts out the companies which satisfy minimum market cap size and have paid dividends consecutively over a certain periods of years. The next step is to calculate historical dividend growth rate and historical long term momentum to select the companies which have high dividend growth rate and historical uptrend price movements. The model assumes that these companies are reliable companies we can buy as a dividend growth investor who looks for both dividend growth and capital appreciation at the same time.

### Stock Price Email Alert

<p align="center">
  <img width="1000" height="500" src="https://user-images.githubusercontent.com/41933169/117089862-bf02ed00-ad24-11eb-8398-58be02b00342.png">
</p

Once we have a list of companies from S&P 500 which satisfy dividend growth and momentum criteria, we don't go straight to buy them. The key idea here is that we wait for the stocks to fall below certain price levels before we consider buying them. We don't want to buy them all time highs but rather wait for the market to correct and buy them when they are relatively cheap. In summary, we want to buy fundamentally strong companies which have had high dividend growth rate and been in uptrend for a long time when they are relatively cheap and discounted. 

In order to buy them when they are cheap, do we have to sit in front of the charts and look at the prices every day? This is very unproductive thing to do and my email alert script can help with this. I use raspberry pi to run the alert script 24/7 which updates current prices of the stocks in dataframe, compare them with drop prices and send an email alert whenever current price of any stock falls below any of drop prices.

### Set Up My Own Database Server in Raspberry Pi (For Practice)

I practice using SQL database to store price and dividend data collected from yahoo finance into remote database server in raspberry pi which runs 24/7. Working with SQL database is not perfectly done and there are many more improvements that can be made here in terms of database design such as collecting data from API calls, querying data from the database and updating values in the database.

<p align="center">
  <img width="800" height="400" src="https://user-images.githubusercontent.com/41933169/115794877-d0e7a600-a39c-11eb-83aa-192d74b15222.png">
</p>

<p align="center">
Dividend History
</p>

<p align="center">
  <img width="800" height="400" src="https://user-images.githubusercontent.com/41933169/115794919-e9f05700-a39c-11eb-8e6d-7ea7bcf22cb4.png">
</p>

<p align="center">
Historical Prices
</p>

<p align="center">
  <img width="400" height="800" src="https://user-images.githubusercontent.com/41933169/115794960-01c7db00-a39d-11eb-955a-9689c4a4f1de.png">
</p>

<p align="center">
Financial Ratios
</p>
