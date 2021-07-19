library(stringr)
library(xts)
library(PerformanceAnalytics)
library(magrittr)
library(dplyr)
library(purrr)
library(quantmod)


fin <- read.csv('./data/financials.csv')

# get historical prices

GetMySymbols <- function(x) {
  getSymbols(x, src='yahoo', from='2018-01-01', to=Sys.Date(), auto.assign=FALSE)
}

tickers <- fin$symbol

adj_prices <- map(tickers, GetMySymbols) %>% map(Ad) %>% reduce(merge.xts)

ret <- Return.calculate(adj_prices)

ret_12m <- ret %>% xts::last(252)
ret_12m