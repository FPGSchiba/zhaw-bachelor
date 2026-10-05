path <- "semester-7/tsp/data/"

## 1

## 2
ma50 <- read.table(paste(path, "ma50.txt", sep = ""), header = FALSE)
ma50

ts.plot(ma50, lty = 1:4, main = "MA(50) Time Series")

acf(ma50$V1, main = "ACF of MA(50) V1")
pacf(ma50$V1, main = "PACF of MA(50) V1")
# Lag 1 is significant, but not lag 2, so it is MA(1)
x_obj <- arima(ma50$V1, order = c(0, 0, 1))

tsdiag(x_obj, gof.lag = 20)
# Diagnostics look good. No significant ACF for residuals and no significant Ljung-Box test p-values.

acf(ma50$V2, main = "ACF of MA(50) V2")
acf(ma50$V3, main = "ACF of MA(50) V3")
acf(ma50$V4, main = "ACF of MA(50) V4")

## 3
ma300 <- read.table(paste(path, "ma300.txt", sep = ""), header = FALSE)
ma300
