library(xts)
library(dplyr)
library(purrr)
library(stringr)
library(ggplot2)
library(magrittr)
library(quantmod)
library(tidyquant)
library(PerformanceAnalytics)

fin <- read.csv('./data/dow_financials.csv')

# Dividend Stock + Remove negative revenue and dividend growth stocks

high_quality <- fin %>% filter(!is.na(DivYield)) %>% filter(Revenue_Growth > 0 & DPS_Growth > 0 & ROE > 0 & EPS_Growth > 0)

GetMySymbols <- function(x) {
  getSymbols(x, src='yahoo', from='2018-01-01', to=Sys.Date(), auto.assign=FALSE)
}

tickers <- high_quality$symbol

adj_prices <- map(tickers, GetMySymbols) %>% map(Ad) %>% reduce(merge.xts)

ret_3m <- Return.calculate(adj_prices) %>% xts::last(60) %>% 
  sapply(., function(x) {prod(1+x) - 1})

ret_12m = ret 