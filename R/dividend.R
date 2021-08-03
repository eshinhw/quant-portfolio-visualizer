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

div <- high_quality %>% select(symbol, name, DPS_Growth)

div <- div %>% mutate(DPSGrowth_rank = rank(desc(DPS_Growth)))

GetMySymbols <- function(x) {
  getSymbols(x, src='yahoo', from='2018-01-01', to=Sys.Date(), auto.assign=FALSE)
}

tickers <- high_quality$symbol

adj_prices <- map(tickers, GetMySymbols) %>% map(Ad) %>% reduce(merge.xts)

# ret_3m <- Return.calculate(adj_prices) %>% xts::last(60) %>% 
#   sapply(., function(x) {prod(1+x) - 1})
# 
# ret_6m <- Return.calculate(adj_prices) %>% xts::last(120) %>% 
#   sapply(., function(x) {prod(1+x) - 1})

ret_12m <- Return.calculate(adj_prices) %>% xts::last(252) %>% 
  sapply(., function(x) {prod(1+x) - 1})

ret_12m <- ret_12m %>% mutate(rank = rank(.)) %>% arrange(desc(rank))

# ret_bind <- cbind(ret_3m, ret_6m, ret_12m) %>% data.frame()



# factor_mom <- ret_bind %>%
#   mutate_all(list(~min_rank(desc(.)))) %>%
#   mutate_all(list(~scale(.))) %>% 
#   rowSums()
# 
# factor_mom <- factor_mom %>%  data.frame()



factor_mom %>% 
  data.frame() %>%
  ggplot(aes(x = `.`)) +
  geom_histogram()