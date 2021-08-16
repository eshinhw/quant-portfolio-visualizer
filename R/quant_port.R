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

# Filter stocks with positive DivYield, Rev_Growth, DPS_Growth, ROE and EPS_Growth

pos_fin <- fin %>% filter(!is.na(DivYield)) %>% filter(Revenue_Growth > 0 & DPS_Growth > 0 & ROE > 0 & EPS_Growth > 0)

high_quality <- pos_fin %>% select(symbol, name)

tickers <- high_quality$symbol

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



# div <- div %>% mutate(DPSGrowth_rank = rank(DPS_Growth)) %>% arrange(desc(DPSGrowth_rank))

# median <- boxplot(div$DPS_Growth)$stat[3,1]

# div <- div %>% filter(div$DPS_Growth > median)

GetMySymbols <- function(x) {
  getSymbols(x, src='yahoo', from='2018-01-01', to=Sys.Date(), auto.assign=FALSE)
}

tickers <- div$symbol

print(tickers)

adj_prices <- map(tickers, GetMySymbols) %>% map(Ad) %>% reduce(merge.xts)

# ret_3m <- Return.calculate(adj_prices) %>% xts::last(60) %>% 
#   sapply(., function(x) {prod(1+x) - 1})
# 
# ret_6m <- Return.calculate(adj_prices) %>% xts::last(120) %>% 
#   sapply(., function(x) {prod(1+x) - 1})

ret_12m <- Return.calculate(adj_prices) %>% xts::last(252) %>% 
  sapply(., function(x) {prod(1+x) - 1})

def_ret_12m <- ret_12m %>% data.frame()

df <- cbind(symbol = rownames(def_ret_12m), def_ret_12m)
rownames(df) <- 1:nrow(df)


df$symbol <- sub(".Adjusted", "", df$symbol)

df <- rename(df, ret_12m = .)

combined <- left_join(df,div, by='symbol')

col_order <- c('symbol', 'name', 'DPS_Growth', 'ret_12m', 'DPSGrowth_rank')

combined <- combined[, col_order]

combined_data <- combined %>% mutate(mom_rank = rank(ret_12m)) %>% mutate(total_rank = DPSGrowth_rank + mom_rank) %>% arrange(desc(total_rank))



factor_mom %>% 
  data.frame() %>%
  ggplot(aes(x = `.`)) +
  geom_histogram()