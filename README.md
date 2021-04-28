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
On top of retrieving account data using Questrade API, another jupyter notebook called 'US Stock Data Analysis' uses quantitative ways of analyzing and filtering out stocks which satisfy certain quantified factor conditions. I believe that applying factor analysis to sort out individual stocks helps improve the overall performance and outperforms against the benchmark, S&P 500. 

## Considering Factors
- 100 Billions Market Cap
- Dividiend Payout History
- Dividend Growth
- Historical Momentum
- 12M Momentum

My investing model only analyzes S&P 500, but only selects stocks which have more than 100 Billions market cap and have paid out dividends from the past. Some high growth stocks which have not paid dividends at all in the past are removed.


## Dividend Investing?

<p align="center">
  <img width="800" height="400" src="https://user-images.githubusercontent.com/41933169/115498299-53f0eb00-a23b-11eb-95f3-2f69c4439350.png">
</p>

In the U.S. stock market, many healthy and mature companies pay cash to its shareholders as dividend every certain period. Periods can be monthly, quarterly or every 6 months or every year. The good thing is investors who own shares of those companies don't have to do anything to collect periodic dividends. Cash payments just deposit directly to shareholders' accounts. All shareholders have to do to collect dividends is just buy and hold the shares of the company which pay out dividends. As shareholders, we can do whatever we want with the dividends. we can pay monthly expenses like phone bills or rents, go shopping to buy whatever we want or buy more shares to collect more dividends later.

Dividend is one of the equity factors which generate extra alpha returns, and investing in the stocks which pay dividends to their shareholders can collect extra returns.

## Considering Factors
- **Dividend Factors**: Dividend Yield, Dividend Growth
- **Fundamental Factors**: Earnings, ROE, Balance Sheet Ratios
- **Momentum Factor**: used to determine current market direction (negative momentum -> downtrend, positive momentum -> uptrend)

## Establishing My Own Database Server in Raspberry Pi

Financial ratios, price and dividend data is automatically collected from yahoo finance and financial modelling prep into a remote database server set up in rapsberry pi. Raspberry pi runs 24/7 to update numbers in the database, and main laptop accesses the database remotely to retrieve data from it.

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
