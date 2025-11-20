# Aufgabe 3
set.seed(100)
library(boot)
x <- readRDS("semester-5/gstat/quiz/kaffetassen.rds")
estimator <- function(data, ind) mean(data[ind])
boot.erg <- boot(data = x, statistic = estimator, R = 100000)
boot.erg$t0 # Original Schätzung
head(boot.erg$t) # Bootstap-Schätzungen
boot.ci(boot.erg, conf = 0.99, type = c("perc"))

# Aufgabe 4
load("semester-5/gstat/quiz/schraubenlaengen.rda")
schraubenlaengen
library(BSDA)
t.test(schraubenlaengen, conf.level = 0.95)$conf.int

mean(schraubenlaengen)
sd(schraubenlaengen)

# Aufgabe 6
## A
alpha <- 0.01
n <- 45
value <- (1.6 / sqrt(n)) * qnorm(1 - alpha / 2)
round(38.5 - value, 3)
round(38.5 + value, 3)

## B
width <- 2 * value
value_new <- (2 * 1.6 * qnorm(1 - alpha / 2) / value)^2

## C
alpha <- 0.02
n <- 45
value <- (1.6 / sqrt(n)) * qnorm(1 - alpha / 2)
round(38.5 - value, 3)
round(38.5 + value, 3)

# Aufgabe 7
1 / 10 + (0)^2
exp(-10) + (3)^2
1 / 15 + (0)^2

# Aufgabe 9
load("semester-5/gstat/quiz/mikrowellen.rda")
mikrowellen

# maximize Weibull likelihood (shape fixed at 12.7) by optimizing log-scale for positivity
loglik <- function(logbeta) {
  beta <- exp(logbeta)
  prod(dweibull(mikrowellen, shape = 12.7, scale = beta, log = TRUE))
}
# optim minimizes, so minimize negative log-likelihood
negloglik <- function(logbeta) -loglik(logbeta)

res <- optim(par = log(1), fn = negloglik, method = "BFGS", control = list(reltol = 1e-12))
mle_beta <- exp(res$par)

res
cat("MLE scale (beta) =", mle_beta, "\n")
cat("Max log-likelihood =", -res$value, "\n")

# Aufgabe 10
nsim <- 10000

result <- matrix(NA, nrow = nsim, ncol = 2)
n <- 5

for (i in 1:nsim) {
  x <- rlnorm(n, meanlog = 3, sdlog = 2)
  s_1 <- mean(log(x))
  s_2 <- log(mean(x))
  result[i, ] <- c(s_1, s_2)
}

colnames(result) <- c("s_1", "s_2")

## A
mean(result[, "s_1"])
mean(result[, "s_2"])

## B
var(result[, "s_1"])
var(result[, "s_2"])
