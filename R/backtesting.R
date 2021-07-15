library(quantmod)
library(PerformanceAnalytics)
library(magrittr)

ticker = c('SPY', 'TLT')
getSymbols(ticker)

prices = do.call(cbind,
                 lapply(ticker, function(x) Ad(get(x))))

tail(prices)

rets = Return.calculate(prices) %>% na.omit()

rets


cor(rets)


portfolio = Return.portfolio(R = rets,
                             weights = c(0.6, 0.4),
                             rebalance_on = 'years',
                             verbose = TRUE)

portfolios = cbind(rets, portfolio$returns) %>%
  setNames(c('주식', '채권', '60대 40'))

charts.PerformanceSummary(portfolios,
                          main = '60대 40 포트폴리오')