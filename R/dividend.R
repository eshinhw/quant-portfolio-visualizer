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
print(fin)


# Dividend Stocks in Dow Jones

dividend <- fin %>% filter(!is.na(DivYield))
print(dividend)

# Remove negative revenue and dividend growth stocks

positive_revGrowth <- dividend %>% filter(Revenue_Growth > 0 | DPS_Growth > 0)
