library(xts)
library(dplyr)
library(purrr)
library(stringr)
library(ggplot2)
library(magrittr)
library(quantmod)
library(tidyquant)
library(PerformanceAnalytics)

fin <- read.csv('./data/financials.csv')

glimpse(fin)

remove_lower_outliers <- function(factor) {
  boxplot(factor)$stats
  Q1 <- boxplot(factor)$stats[2,1]
  factor <- ifelse(factor < Q1, NA, factor)
  fin <- fin %>% filter(!is.na(factor))
  return(fin)
}

# remove outliers for dividend yield
processed_fin <- remove_lower_outliers(fin$DivYield)
processed_fin <- remove_lower_outliers(fin$Revenue_Growth)
processed_fin <- remove_lower_outliers(fin$DPS_Growth)
processed_fin <- remove_lower_outliers(fin$ROE)
processed_fin <- remove_lower_outliers(fin$GPMargin)

glimpse(processed_fin)
summary(processed_fin)

