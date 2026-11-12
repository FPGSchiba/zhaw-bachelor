load(file = paste(getwd(), "/semester-7/tsp/mid-term/data.Rdata", sep = ""))

x_mat

tail(x_mat)

ts.plot(x_mat)

5 + 1.3 * 19 - 0.5 * 19
5 + 2 * 2 * sqrt(1 + 1.3^2)
5 - 2 * 2 * sqrt(1 + 1.3^2)

plot_predict_func <- function(y, h, y_obj) {
  ymin <- min(min(predict(y_obj, n.ahead = h)$pred - 2 * predict(y_obj, n.ahead = h)$se), y)
  ymax <- max(max(predict(y_obj, n.ahead = h)$pred + 2 * predict(y_obj, n.ahead = h)$se), y)
  ts.plot(c(y, rep(NA, h)),
    xlab = "", ylab = "", main = "Multi steps ahead interval forecast",
    ylim = c(ymin, ymax)
  )
  lines(c(rep(NA, length(y)), predict(y_obj, n.ahead = h)$pred), col = "blue")
  lines(c(rep(NA, length(y)), predict(y_obj, n.ahead = h)$pred - 2 * predict(y_obj, n.ahead = h)$se),
    col = "blue", lty = 2
  )
  lines(c(rep(NA, length(y)), predict(y_obj, n.ahead = h)$pred + 2 * predict(y_obj, n.ahead = h)$se),
    col = "blue", lty = 2
  )
}

series_1 <- x_mat[, 1]
series_2 <- x_mat[, 2]
series_3 <- x_mat[, 3]
series_4 <- x_mat[, 4]

ts.plot(series_1)

library(sarima)

pacf(series_1, lag.max = 12)
acf(series_1, lag.max = 12)

y_obj <- arima(series_1, order = c(2, 2, 1), seasonal = list(order = c(0, 1, 1), period = 12))
tsdiag(y_obj, gof.lag = 24)
h <- 48
plot_predict_func(series_1, h, y_obj)


ts.plot(series_2)

pacf(series_2)
acf(series_2)

y_obj <- arima(series_2, order = c(2, 1, 1))
tsdiag(y_obj, gof.lag = 24)
plot_predict_func(series_2, h, y_obj)

ts.plot(series_3)

acf(series_3)
pacf(series_3)

y_obj <- arima(series_3, order = c(4, 0, 0), seasonal = list(order = c(0, 1, 1), period = 12))
tsdiag(y_obj, gof.lag = 24)
plot_predict_func(series_3, h, y_obj)

ts.plot(series_4)

acf(series_4)
pacf(series_4)

y_obj <- arima(series_4, order = c(0, 0, 2)) # , seasonal = list(order = c(0, 0, 0), period = 12))
tsdiag(y_obj, gof.lag = 24)
plot_predict_func(series_4, h, y_obj)
