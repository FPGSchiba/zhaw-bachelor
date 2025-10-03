# Aufgabe 1

## A
lambda <- 2
lambda_hat <- replicate(10000, 1 / mean(rexp(5, rate = lambda)))

mean(lambda_hat) - lambda


## B
# Bestimmen Sie ebenfalls durch ein Simulation den MSE von ˆλ, wieder für λ = 2 und n = 5.
mean((lambda_hat - lambda)^2)

# Aufgabe 2
n <- 3
N <- 10000
s1 <- c()
s2 <- c()

for (i in 1:N) {
    x <- rnorm(n)
    m <- sum((x - mean(x))^2)
    s1[i] <- sqrt(m / n)
    s2[i] <- sqrt(m / (n - 1))
}
par(mfrow = c(1, 2))
hist(s1, main = "Standardabweichung (n)", xlab = "Werte", breaks = 30)
hist(s2, main = "Standardabweichung (n-1)", xlab = "Werte", breaks = 30)

mean(s1)
mean(s2)

# B
n_tot <- 30
s1 <- rep(0, n_tot)
s2 <- rep(0, n_tot)

for (n in 1:n_tot) {
    s1_temp <- c()
    s2_temp <- c()
    for (i in 1:N) {
        x <- rnorm(n)
        m <- sum((x - mean(x))^2)
        s1_temp[i] <- m / n
        s2_temp[i] <- m / (n - 1)
    }
    s1[n] <- mean(s1_temp)
    s2[n] <- mean(s2_temp)
}

par(mfrow = c(1, 1))
plot(1:n_tot, s1, type = "o", col = "red", ylim = c(0, 1.5), xlab = "n", ylab = "Erwartungswert (s1)")
lines(1:n_tot, s2, type = "o", col = "blue", ylim = c(0, 1.5), xlab = "n", ylab = "Erwartungswert (s2)")
legend("topright", legend = c("s1", "s2"), col = c("red", "blue"), lty = 1)
abline(h = 1, lty = 2)

# Aufgabe 4
## A
x_mean <- replicate(10000, mean(rnorm(20)))
x_med <- replicate(10000, median(rnorm(20)))

mse_mean <- mean((x_mean - 0)^2)
mse_med <- mean((x_med - 0)^2)
mse_mean / mse_med
# Der MSE des Mittelwerts ist kleiner als der des Medians, also ist der Mittelwert der effizientere Schätzer.

## B
# install.packages("extraDistr", dependencies = TRUE)
library(extraDistr)
x_mean <- replicate(10000, mean(rlaplace(20, m = 0, s = 1)))
x_med <- replicate(10000, median(rlaplace(20, m = 0, s = 1)))

mse_mean <- mean((x_mean - 0)^2)
mse_med <- mean((x_med - 0)^2)
mse_mean / mse_med
# Der MSE des Mittelwerts ist kleiner als der des Medians, also ist der Mittelwert der effizientere Schätzer.
