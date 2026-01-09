# Aufgabe 1

## A
llh <- function(theta, x) {
  sum(log(2 * theta^2 * x * exp(-(theta * x)^2)))
}

d <- c(5, 4, 3, 2, 5, 4, 2, 6, 2, 1, 1)
theta <- 0.2
llh(theta, d)

## B
min_llh <- function(theta, x) {
  -llh(theta, x)
}
result <- optim(par = theta, fn = min_llh, method = "BFGS", x = d)
result$par

# Aufgabe 3
without <- c(120, 130, 150, 90, 100, 140)
with <- c(180, 130, 120, 190, 220, 120)

# B
library(car)
qqPlot(x = with, distribution = "norm", mean = 0, sd = 1)
qqPlot(x = without, distribution = "norm", mean = 0, sd = 1)

# C
t.test(
  x = with,
  y = without,
  var.equal = TRUE,
  alternative = "greater"
)

# Aufgabe 4
# A
tab <- rbind(
  c(95, 300, 160, 250, 320),
  c(75, 200, 100, 230, 270)
)
chisq.test(
  x = tab,
)

# B
beben <- c(55, 72, 64, 73, 57)
poisson.test(
  x = sum(beben),
  T = 5,
  conf.level = 0.90
)$conf.int

# C
alpha <- 0.01
z <- qnorm(1 - alpha / 2)
sd <- 2.06
n <- 40
mean <- 12.73
c(mean - z * (sd / sqrt(n)), mean + z * (sd / sqrt(n)))

# Aufgabe 5
set.seed(20200123)
x <- rlnorm(20, meanlog = 1, sdlog = sqrt(log(2)))
#  A
T <- sqrt((1 / length(x)) * sum((x - mean(x))^2)) / mean(x)
T

# B
library(boot)
estimator <- function(data, ind) {
  sqrt((1 / length(data[ind])) * sum((data[ind] - mean(data[ind]))^2)) / mean(data[ind])
}
boot.erg <- boot(data = x, statistic = estimator, R = 6999)
boot.erg$t0 # Original Schätzung
head(boot.erg$t) # Bootstap-Schätzungen
boot.ci(boot.erg, conf = 0.9, type = "all")
