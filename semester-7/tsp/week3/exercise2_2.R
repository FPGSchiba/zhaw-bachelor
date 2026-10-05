## 1

## 2

## 3
interval_forecast <- function(x, h, q) {
  len <- length(x)
  # Estimation of parameters
  ma_obj <- arima(x, order = c(0, 0, q))
  # Forecast multi-step ahead
  xhat <- predict(ma_obj, h)
  # Compute the forecast intervals
  x_lower <- xhat$pred - 2 * xhat$se
  x_upper <- xhat$pred + 2 * xhat$se
  return(list(x_lower = x_lower, x_upper = x_upper))
}


set.seed(12)
sigma <- sqrt(2)
q <- 2
b_1 <- -1.7
b_2 <- 0.8
len <- 50
mu <- 0
# Number simulations
anzsim <- 1000
sigma_vec <- 1:anzsim
# Forecast horizon
h <- 10
emp_sig <- rep(0, h)

wh <- rep(0, anzsim)

# We compute anzsim replications of length len+h of the MA(2)
for (j in 1:anzsim) # j<-1
{
  # Simulate process
  x <- mu + arima.sim(n = len + h, list(ma = c(b_1, b_2)), sd = sigma)
  # The first len observations are fed to interval_forecast
  z <- x[1:len]
  int_obj <- interval_forecast(z, h, q)

  # we verify that x[101:(100+h)] are in the forecast intervals
  # If not (miss) the empirical significance level emp_sig is incremented by 1
  for (i in 1:h) # i<-1
  {
    if (x[len + i] < int_obj$x_lower[i] | x[len + i] > int_obj$x_upper[i]) {
      emp_sig[i] <- emp_sig[i] + 1
      if (i == 1) {
        wh[j] <- 1
      }
    }
  }
}
# The empirical significance level should be close to 5%
# For shorter series (len=50) the empirical significance level is above 5%: too optimistic; bands too narrow (overfitting)
#   and point forecast biased
# For longer series the effect vanishes: empirical significance levels are closer to theoretical one
emp_sig / anzsim


# Slightly more complex model: MA(4)

set.seed(12)
sigma <- sqrt(2)
q <- 4
b_1 <- -1.7
b_2 <- 0.8
b_3 <- 1.2
b_4 <- -0.9
mu <- 0
# Number simulations
anzsim <- 1000
sigma_vec <- 1:anzsim
# Forecast horizon
h <- 10
emp_sig <- rep(0, h)

wh <- rep(0, anzsim)

# We compute anzsim replications of length len+h of the MA(2)
for (j in 1:anzsim) # j<-1
{
  # Simulate process
  x <- mu + arima.sim(n = len + h, list(ma = c(b_1, b_2, b_3, b_4)), sd = sigma)
  # The first len observations are fed to interval_forecast
  z <- x[1:len]
  int_obj <- interval_forecast(z, h, q)

  # we verify that x[101:(100+h)] are in the forecast intervals
  # If not (miss) the empirical significance level emp_sig is incremented by 1
  for (i in 1:h) # i<-1
  {
    if (x[len + i] < int_obj$x_lower[i] | x[len + i] > int_obj$x_upper[i]) {
      emp_sig[i] <- emp_sig[i] + 1
      if (i == 1) {
        wh[j] <- 1
      }
    }
  }
}
# The empirical significance level should be close to 5%
# For shorter series (len=50) the empirical significance level is above 5%: too optimistic; bands too narrow (overfitting)
#   and point forecast biased
# For longer series the effect vanishes: empirical significance levels are closer to theoretical one
emp_sig / anzsim
