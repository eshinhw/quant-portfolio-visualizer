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
  getSymbols(x, src='yahoo', from='2015-01-01', to=Sys.Date(), auto.assign=FALSE)
}

tickers <- fin$symbol

adj_prices <- map(tickers, GetMySymbols) %>% map(Ad) %>% reduce(merge.xts)

ret_6m = Return.calculate(adj_prices) %>% xts::last(126) %>% sapply(., function(x) {
  prod(1+x) - 1
})

ret_12m = Return.calculate(adj_prices) %>% xts::last(252) %>% sapply(., function(x) {
  prod(1+x) - 1
})

ret_24m = Return.calculate(adj_prices) %>% xts::last(378) %>% sapply(., function(x) {
  prod(1+x) - 1
})

m24 <- rank(-ret_24m)



ret_12m[rank(-ret_12m) <= 15]

invest_mom = rank(-ret_12m) <= 15
invest_mom

mom_stocks <- processed_fin[invest_mom,] %>% select(symbol) %>% mutate('Ymom' = round(ret_12m[invest_mom], 4)) 
class(mom_stocks)
mom_stocks %>% arrange(desc(Ymom))

glimpse(mom_stocks)

mom_stocks

