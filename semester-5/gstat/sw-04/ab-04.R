# Aufgabe 1

## A
dbinom(34, size = 100, prob = c(0, 1:6 / 6))
# 2/6 ist der beste Maximum-Likelihood-Schätzer

## B
n <- 100
lambda <- 1 / 5

stichprobe <- rexp(n, rate = lambda)

log_likelihood <- function(x) {
  sum(log(dexp(stichprobe, rate = x)))
}

opt <- optimize(log_likelihood, interval = c(0.01, 1), maximum = TRUE)
opt$maximum

# Aufgabe 2

###
### Funktion loglik(mu, sigma, dat) muss definiert sein !!!
###
xs <- c(-0.033, -0.76, 2.02, 1.13, 0.65, 0.49, 0.76, 0.40, 0.10, 0.61)
# install.packages("manipulate", dependencies = TRUE)
library(manipulate)

loglik <- function(mu, sigma) {
  sum(dnorm(xs, mean = mu, sd = sigma, log = TRUE))
}

manipulate(
  {
    lik <- loglik(mu = muEst, sigma = sigmaEst, dat = xs)
    # W'keitdichte einzeichnen für Werte von -5 bis 5
    xvals <- seq(-5, 5, 0.05)
    plot(xvals, dnorm(xvals, mean = muEst, sd = sigmaEst),
      type = "l", xlab = "Daten", ylab = "", pch = "|",
      main = paste0("loglikelihood = ", round(lik, digits = 3)), xlim = c(0.95 * min(xs), 1.05 * max(xs))
    )
    # Stichprobenwerte auf der x-Achse einzeichnen
    rug(x = xs, lwd = 3, col = "blue")
    # Legende
    legend(
      x = "topright",
      legend = c("Datenpunkte", "W'keitdichte"), lwd = c(2, 1), col = c("blue", "black"), bty = "n"
    )
  },
  # Slider für den Parameter mu
  muEst = slider(-5, 5, initial = 0.1, step = 0.01),
  # Slider für en Parameter sigma
  sigmaEst = slider(0, 5, initial = 0.1, step = 0.01)
)

## C
expand.grid(mu = seq(-5, 5, by = 0.1), sigma = seq(0.1, 5, by = 0.1)) -> params
params$loglik <- apply(params, 1, function(x) loglik(mu = x[1], sigma = x[2]))
which.max(params$loglik)
params[which.max(params$loglik), ]
# mu = 0.5, sigma = 0.7
