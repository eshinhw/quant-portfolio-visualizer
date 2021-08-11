# Quantitative Investing in Python and R

## Introduction

Questrade is one of the investing brokers in Canada, and I have an investing account with them that I want to keep track of regularly. A jupyter notebook called 'Questrade Portfolio Manager' retrieves account information using Questrade API wrapper called 'qtrade' and summarizes up-to-date information such as monthly account activities, position changes and dividend income that I earn every month. Whenever I want to know how my investing account is doing, all I need to do is just run this notebook from time to time. In terms of security, qtrade wrapper automatically refreshes a security token, so I don't have to log in to the website to get a new token everytime I run the notebook. Below are some of the sample visualizations from the notebook.

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

## Quantitative Stock Selection Model 

### Model Assumptions

I've developed a quantitative model which finds a list of stocks from S&P 500 which have **high historical dividend growth rate** and **strong historical price momentum** at the same time. I believe that these two factors are useful fundamental measures for long term dividend investors who are looking to achieve dividend growth and capital appreciation simultaneously. 

<p align="center">
  <img width="700" height="400" src="https://user-images.githubusercontent.com/41933169/117091006-f030ec80-ad27-11eb-8fe5-0919d4cdbccf.png">
</p>

Some of the matured companies such as AT&T have high dividend yield of 6.50% which is attractive but in terms of capital growth, it's not attractive at all. AT&T's price chart above shows that the stock price has been in the range of $20 and $60 almost over the last 30 years. Investors who have been investing in AT&T may have collected some dividends, but there is a possibility that their unrealized capital loss might be bigger than the total dividends collected.

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

### MySQL Database for Historical Financial Data

The main source of financial data for the model is Financial Modeling Prep API (https://financialmodelingprep.com/developer/docs/). They have well-organized financial data which I can directly request through API calls. The data that I collect from the API are sorted and stored in local MySQL database. I've written basic SQL scripts to handle the data. Regularly, the data in the database is updated to stay updated and most of analysis work start from loading the data from the database as well. 

All types of automated tasks are run through raspberry pi with **crontab** which allows us to execute python scripts at scheduled times. 

### Daily Stock Update Email Alert

<p align="center">
  <img width="1000" height="500" src="https://user-images.githubusercontent.com/41933169/121985878-94fd0b80-cd63-11eb-944f-248f8d69e4a4.png">
</p>

Every weekday at 5:30pm after the market closes, the list of stocks is sent through email into my inbox. The stocks in the list are considered cheap as their stock prices have fallen more than certain predetermined discount threshold. Looking through the list, I can make purchases if I think current prices relative previous highs are attractive.

The automated email alert system eliminates the manual process of checking the stock prices every day to decide whether they are traded at discount or not. 

### Financial Data Analysis in R

I've recently found coding resources for financial data analysis and quantitative investing in R. There are many useful libraries in R which help perform financial data analysis.
