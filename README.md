# Questrade Portfolio Manager

## Introduction

Questrade is one of the investing brokers in Canada, and I have an investing account with them that I want to keep track of regularly. A jupyter notebook called 'Questrade Portfolio Manager' retrieves account information using Questrade API called 'qtrade' and summarizes some useful information such as monthly account activities, position changes and dividend income that I earned every month. Whenever I want to know how my investing account is doing, all I need to do is just run this notebook from time to time. In terms of security, qtrade wrapper automatically refreshes a security token, so I don't have to log in to the website to get a new token everytime I run the notebook. Below are a sample dataframe and visualizations I can create from the notebook.

## Breakdown of Holdings

<p align="center">
  <img width="600" height="600" src="https://user-images.githubusercontent.com/41933169/112911987-84be8400-90c4-11eb-94cf-b3c9836887f5.png">
</p>

## Monthly Dividend Income

<p align="center">
  <img width="800" height="500" src="https://user-images.githubusercontent.com/41933169/112912007-90aa4600-90c4-11eb-9868-7e1939e89af2.png">
</p>

## Holding Positions Summary

<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/112912042-a15abc00-90c4-11eb-8098-4c1e84b4b433.png">
</p>

# Quantitative Investing in Python

<p align="center">
  <img width="800" height="400" src="https://user-images.githubusercontent.com/41933169/115498299-53f0eb00-a23b-11eb-95f3-2f69c4439350.png">
</p>

On top of retrieving account data using Questrade API, another jupyter notebook called 'US Stock Data Analysis' uses quantitative ways of analyzing and filtering out stocks which satisfy certain quantified factor conditions. I believe that applying factor analysis to sort out individual stocks helps improve the overall performance and outperforms against the benchmark, S&P 500. 

## Considering Factors

- 100 Billions Market Cap
- Dividiend Payout History
- Dividend Growth
- Historical Momentum
- 12M Momentum

My investing model only analyzes S&P 500, but only selects stocks which have more than 100 Billions market cap and have paid out dividends from the past. Some high growth stocks which have not paid dividends at all in the past are removed. I can manually add mid or small cap stocks if I wish, but the model only looks for large-cap stocks with dividend history.

Next, it calculates average dividend growth rate of certain periods (10 years by default) to sort out companies which have increased their dividend payments over time. 

Lastly, it calculates long term momentum with the average of ranges from 3 months to 10 years to analyze historical long term trend of stocks. Also, 12M momentum might be useful for rebalancing.

Certainly, more equity factors and financial ratios can be added further like earnings or balance sheet ratios to further sort out companies.

## Trading Strategy with Email Alert

<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/116454295-d1b18980-a82d-11eb-8073-bab4b32551e5.png">
</p>

How do we determine when to buy stocks? The model uses a simple logic to determine market timing. Since all the stocks selected above have positive long term trend which means they may continue to go up in the future. All we want to do is buy those stocks when they are traded at discount. It uses 52 Weeks High as a pivot to calculate 15% drop, 30% drop and 50% drop from the high. By applying this rule, it prevents chasing the market moves at new highs but wait for retracement to buy them at better prices. The percentage drops can be customized, and whenever current prices falls below those drop prices, it sends email alerts so I don't have to watch the market every time.

## Establishing My Own Database Server in Raspberry Pi

I practice using SQL database to store price and dividend data collected from yahoo finance into remote database server in raspberry pi which runs 24/7.

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
