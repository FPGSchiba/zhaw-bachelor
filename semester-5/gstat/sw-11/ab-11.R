# Aufgabe 2
## A

nsim <- 10000
n_upper <- 20
n_lower <- 3

x <- matrix(NA, nrow = nsim, ncol = n_upper - n_lower + 1)

for (i in 1:nsim) {
  for (j in n_lower:n_upper) {
    xsamp <- rnorm(j, mean = 1, sd = 1)
    test <- t.test(x = xsamp, mu = 0, alternative = "greater") # nolint
    p_value <- test$p.value
    if (p_value < 0.05) {
      x[i, j - n_lower + 1] <- 1
    } else {
      x[i, j - n_lower + 1] <- 0
    }
  }
}

plot(n_lower:n_upper, colMeans(x), type = "b", xlab = "Stichprobenumfang", ylab = "Power", main = "Power vs. Stichprobenumfang")

## B
power.t.test(n = NULL, delta = 1, sd = 1, sig.level = 0.05, power = 0.8, type = "one.sample", alternative = "one.sided")
