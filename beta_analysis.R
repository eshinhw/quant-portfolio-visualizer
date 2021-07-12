library(dplyr)
library(quantmod)
library(magrittr)
library(PerformanceAnalytics)

# data = read.csv("financials.csv")

symbols = c("AAPL", "SPY")
symbols

getSymbols(symbols)


prices = do.call(cbind,
                 lapply(symbols, function(x)Cl(get(x))))

ret = Return.calculate(prices)

ret = ret['2020-01::2020-12']
tail(ret)

rm = ret[, 2]
ri = ret[, 1]

reg = lm(ri ~ rm)
summary(reg)

plot(as.numeric(rm), as.numeric(ri), pch = 4, cex = 0.3, 
     xlab = "SPY BENCHMARK", ylab = "AAPL",
     xlim = c(-0.02, 0.02), ylim = c(-0.02, 0.02))
abline(a = 0, b = 1, lty = 2)
abline(reg, col = 'red')
