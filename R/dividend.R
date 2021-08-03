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
