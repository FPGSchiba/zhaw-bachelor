# Aufgabe 1

## A
mat <- matrix(replicate(10000, rnorm(30, mean = 50, sd = 10)), ncol = 10000, nrow = 30) # nolint

## B
# install.packages("BSDA", dependencies = TRUE) nolint
library(BSDA)
kis <- matrix(NA, ncol = ncol(mat), nrow = 2) # nolint
for (i in seq_len(ncol(mat))) {
  kis[, i] <- z.test(x = mat[, i], sigma.x = 10, alternative = "two.sided", conf.level = 0.95)$conf.int # nolint
}

## C
results <- kis[1, ] <= 50 & kis[2, ] >= 50
sum(results) / ncol(mat)

# Aufgabe 2
## A
6.048 + qnorm(c(0.05, 0.95)) * 0.02 / sqrt(1219)

qnorm(c(0.05, 0.95), mean = 6.048, sd = 0.02 / sqrt(1219))

## B
pnorm(q = 6.0, mean = 6.048, sd = 0.02)

## C
(2 * 0.02 / 0.001 * qnorm(0.95))^2

# Aufgabe 3
## A
mu <- 42
n <- 3
sigma <- 4
sim <- 10000

t_n <- function(x) (mean(x) - mu) / (sigma / sqrt(length(x)))

t_values <- replicate(sim, {
  x <- rnorm(n, mean = mu, sd = sigma)
  t_n(x)
})

par(mfrow = c(1, 2))

hist(t_values, breaks = 50, freq = FALSE, main = "Verteilung der t_n Werte", xlab = "t_n Werte")
curve(dnorm(x), add = TRUE, col = "blue", lwd = 2) # Standardnormaldichte überlagern

qqnorm(t_values, main = "QQ-Plot der t_n Werte vs N(0,1)")
qqline(t_values, col = "red")

## B
mu <- 42
n <- 3
sigma <- 4
sim <- 10000

s_x <- function(x) (sum((x - mean(x))^2)) / (length(x) - 1)
t_n <- function(x) (mean(x) - mu) / (s_x(x) / sqrt(length(x)))

t_values <- replicate(sim, {
  x <- rnorm(n, mean = mu, sd = sigma)
  t_n(x)
})

par(mfrow = c(1, 2))

hist(t_values, breaks = 50, freq = FALSE, main = "Verteilung der t_n Werte", xlab = "t_n Werte")
curve(dnorm(x), add = TRUE, col = "blue", lwd = 2) # Standardnormaldichte überlagern

qqnorm(t_values, main = "QQ-Plot der t_n Werte vs N(0,1)")
qqline(t_values, col = "red")

# Aufgabe 4
mu <- 0
sigma <- 1
n <- c(5, 10, 100)
results <- lapply(n, function(n_i) {
  sims <- 10000

  # 1) sigma known (use true sigma)
  ci_known <- replicate(sims, {
    x <- rnorm(n_i, mean = mu, sd = sigma)
    m <- mean(x)
    h <- qnorm(0.975) * sigma / sqrt(n_i)
    c(m - h, m + h)
  })

  # 2) sigma "known" but cheating (use sample sd as if it were true)
  ci_cheat <- replicate(sims, {
    x <- rnorm(n_i, mean = mu, sd = sigma)
    m <- mean(x)
    s <- sd(x)
    h <- qnorm(0.975) * s / sqrt(n_i)
    c(m - h, m + h)
  })

  # 3) sigma unknown (use t-based CI)
  ci_t <- replicate(sims, {
    x <- rnorm(n_i, mean = mu, sd = sigma)
    t.test(x, mu = mu)$conf.int
  })

  in_known <- ci_known[1, ] <= mu & ci_known[2, ] >= mu
  in_cheat <- ci_cheat[1, ] <= mu & ci_cheat[2, ] >= mu
  in_t <- ci_t[1, ] <= mu & ci_t[2, ] >= mu

  cov_known <- mean(in_known)
  cov_cheat <- mean(in_cheat)
  cov_t <- mean(in_t)

  count_known <- sum(in_known)
  count_cheat <- sum(in_cheat)
  count_t <- sum(in_t)

  width_known <- mean(ci_known[2, ] - ci_known[1, ])
  width_cheat <- mean(ci_cheat[2, ] - ci_cheat[1, ])
  width_t <- mean(ci_t[2, ] - ci_t[1, ])

  data.frame(
    n = n_i,
    sims = sims,
    coverage_known = cov_known,
    count_known = count_known,
    coverage_cheat = cov_cheat,
    count_cheat = count_cheat,
    coverage_t = cov_t,
    count_t = count_t,
    width_known = width_known,
    width_cheat = width_cheat,
    width_t = width_t
  )
})

do.call(rbind, results)

# Aufgabe 5
x <- c(104, 103, 107, 105, 102, 109, 105, 104, 106)
t.test(x, mu = 100, alternative = "two.sided", conf.level = 0.95)
