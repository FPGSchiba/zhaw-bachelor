# Aufgabe 2

# Deutschland
poisson.test(c(126,107), T = c(1,1), alternative = "greater")$p.value

# p-value: 0.1191 -> H0 wird beibehalten

# International
poisson.test(c(327,302), T = c(1,1), alternative = "greater")$p.value

# p-value: 0.1593 -> H0 wird beibehalten

# Aufgabe 3
alpha <- 0.05
sd <- 0.003
mu <- 0.3

unterlegscheiben <- readRDS("semester-5/gstat/sw-09/unterlegscheiben.rds")
mu_x <- mean(unterlegscheiben)

# H0: mu = 0.3
# HA: mu != 0.3


Z <- (mu_x - mu) / sd * sqrt(length(unterlegscheiben))
p <- 2 * (1 - pnorm(abs(Z)))
p < alpha

# p-value: 0.009698 -> H0 wird verworfen

## Alternative mit BSDA Paket
library(BSDA)
z.test(unterlegscheiben, sigma.x = sd, mu = mu, alternative = "two.sided")$p.value

# Aufgabe 4
alpha <- 0.05

## A
# t-Test, obwohl die Stichprobe relativ klein ist

## B
t <- -2.3
alpha <- 0.05
df <- 18 - 1
p <- pt(t, df = df)
p < alpha
# p-value: 0.01719352 -> H0 wird beibehalten

## C
t <- -2.7
alpha <- 0.01
p <- pt(t, df = df)
p < alpha
# p-value: 0.00758752 -> H0 wird verworfen

## D
alpha <- 0.01
p <- 2*(1- pt(abs(t), df = df))
p
p < alpha
# p-value: 0.01517504 -> H0 wird beibehalten

# Aufgabe 5
alpha <- 0.05
# H0: mu = 150
# HA: mu < 150
p <- z.test(sigma.x = 3, mu = 150, mu.x = 148, n.x = 50, alternative = "less")$p.value
p
p < alpha
# p-value: 0.00758752 -> H0 wird verworfen
