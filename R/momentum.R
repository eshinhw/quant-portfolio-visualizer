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

ret <- Return.calculate(adj_prices) %>% xts::last(252)

ret_12m = ret %>% sapply(., function(x) {
  prod(1+x) - 1
})


ret_12m[rank(-ret_12m) <= 15]

invest_mom = rank(-ret_12m) <= 15
invest_mom

mom_stocks <- fin[invest_mom,] %>% select(symbol) %>% mutate('12M_return' = round(ret_12m[invest_mom], 4))

glimpse(mom_stocks)

mom_stocks

