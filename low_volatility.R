library(xts)
library(dplyr)
library(purrr)
library(stringr)
library(ggplot2)
library(magrittr)
library(quantmod)
library(PerformanceAnalytics)



financials <- read.csv('./data/financials.csv')



threshold <- nrow(financials) * 0.05
threshold

invest_roe <- rank(-financials$ROE) <= threshold
invest_roe

high_roe <- financials[invest_roe, ] %>% 
  select('symbol') %>% 
  glimpse(.)

high_roe


symbols <- financials$symbol



symbols
tryCatch(
  
  expr = {
    prices <- map(symbols, function(x) Ad(get(x)))
    prices <- reduce(prices,merge)
    colnames(prices) <- symbols
  },
  error = function(e) {
    print(e)
  }
    
    
    
  )



tail(prices)

ret <- Return.calculate(prices)
ret

std_12m_daily <- xts::last(ret, 252) %>% 
  apply(., 2, sd) %>%
  multiply_by(sqrt(252))

std_12m_daily

std_12m_daily %>% 
  data.frame() %>%
  ggplot(aes(x = (`.`))) +
  geom_histogram(binwidth = 0.01) +
  annotate("rect", xmin = -0.02, xmax = 0.02,
           ymin = 0,
           ymax = sum(std_12m_daily == 0, na.rm = TRUE) * 1.1,
           alpha=0.3, fill="red") +
  xlab(NULL)

std_12m_daily[std_12m_daily == 0] = NA