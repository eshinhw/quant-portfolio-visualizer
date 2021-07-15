library(xts)
library(dplyr)
library(purrr)
library(stringr)
library(ggplot2)
library(magrittr)
library(quantmod)
library(PerformanceAnalytics)

fin <- read.csv('./data/financials.csv')

# get historical prices

GetMySymbols <- function(x) {
  getSymbols(x, src='yahoo', from='2018-01-01', to=Sys.Date(), auto.assign=FALSE)
}

tickers <- fin$symbol

adj_prices <- map(tickers, GetMySymbols) %>% map(Ad) %>% reduce(merge.xts)

ret <- Return.calculate(adj_prices)
std_12m_daily <- xts::last(ret,252) %>% apply(.,2,sd) %>% multiply_by(sqrt(252))

std_12m_daily %>% 
  data.frame() %>%
  ggplot(aes(x = (`.`))) +
  geom_histogram(binwidth = 0.01) +
  annotate("rect", xmin = -0.02, xmax = 0.02,
           ymin = 0,
           ymax = sum(std_12m_daily == 0, na.rm = TRUE) * 1.1,
           alpha=0.3, fill="red") +
  xlab(NULL)


std_12m_daily[rank(std_12m_daily) <= 15]

std_12m_daily[rank(std_12m_daily) <= 15] %>%
  data.frame() %>%
  ggplot(aes(x = rep(1:15), y = `.`)) +
  geom_col() +
  xlab(NULL)

# top 15 low volatility stocks based on DAILY return

invest_lowvol <- rank(std_12m_daily) <= 15

fin[invest_lowvol,] %>% 
  select(symbol) %>% 
  mutate(volatility=round(std_12m_daily[invest_lowvol], 4))

# top 15 low volatility stocks based on WEEKLY return

std_12m_weekly = xts::last(ret, 252) %>%
  apply.weekly(Return.cumulative) %>%
  apply(., 2, sd) %>% multiply_by(sqrt(52))

std_12m_weekly[rank(std_12m_weekly) <= 15]

invest_lowvol_weekly <- rank(std_12m_weekly) <= 15

fin[invest_lowvol_weekly,] %>% 
  select(symbol) %>% 
  mutate(volatility=round(std_12m_weekly[invest_lowvol_weekly], 4))

# low vol stocks in both daily and weekly volatility

intersect(fin[invest_lowvol, "symbol"], fin[invest_lowvol_weekly, 'symbol'])
