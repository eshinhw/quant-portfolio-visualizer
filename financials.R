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

# remove outliers for dividend yield
boxplot(fin$DivYield)$stats
fin$DivYield <- ifelse(fin$DivYield < boxplot(fin$DivYield)$stats[1,1] 
                       | fin$DivYield > boxplot(fin$DivYield)$stats[5,1], NA, fin$DivYield)
fin <- fin %>% filter(!is.na(fin$DivYield))

# remove outliers for revenue growth
boxplot(fin$Revenue_Growth)$stats
fin$Revenue_Growth <- ifelse(fin$Revenue_Growth < boxplot(fin$Revenue_Growth)$stats[2,1], NA, fin$Revenue_Growth)
fin <- fin %>% filter(!is.na(fin$Revenue_Growth))
boxplot(fin$Revenue_Growth)

# remove outliers for DPS growth
boxplot(fin$DPS_Growth)$stats
fin$DPS_Growth <- ifelse(fin$DPS_Growth < boxplot(fin$DPS_Growth)$stats[2,1] | fin$DPS_Growth > boxplot(fin$DPS_Growth)$stats[5,1], NA, fin$DPS_Growth)
fin <- fin %>% filter(!is.na(fin$DPS_Growth))

# remove outliers for EPS growth
boxplot(fin$EPS_Growth)$stats
fin$EPS_Growth <- ifelse(fin$EPS_Growth < boxplot(fin$EPS_Growth)$stats[3,1] | fin$EPS_Growth > boxplot(fin$EPS_Growth)$stats[5,1], NA, fin$EPS_Growth)
fin <- fin %>% filter(!is.na(fin$EPS_Growth))

# remove outliers for ROE
boxplot(fin$ROE)$stats
fin$ROE <- ifelse(fin$ROE < boxplot(fin$ROE)$stats[3,1], NA, fin$ROE)
fin <- fin %>% filter(!is.na(fin$ROE))

# remove outliers for Gross Profit Margin
boxplot(fin$GPMargin)$stats
fin$GPMargin <- ifelse(fin$GPMargin < boxplot(fin$GPMargin)$stats[2,1], NA, fin$GPMargin)
fin <- fin %>% filter(!is.na(fin$GPMargin))

# rank financial factors

glimpse(fin)
summary(fin)

