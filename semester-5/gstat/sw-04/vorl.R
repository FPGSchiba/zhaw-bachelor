# Gamma Verteilung Maximum Likelihood Schätzung
n <- 100
alpha <- 7
beta <- 2
stichprobe <- rgamma(n, shape = alpha, scale = beta)
log_likelihood <- function(x) {
  sum(log(dgamma(stichprobe, shape = x[1], scale = x[2])))
}
opt <- optim(c(1, 1), function(x) -log_likelihood(x),
  method = "L-BFGS-B",
  lower = c(0.01, 0.01)
)
opt$par
# alpha = 7, beta = 2
