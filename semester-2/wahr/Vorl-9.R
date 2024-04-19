# ----- Aufgabe 1 -----
# A
lambda <- 1/1000

# B
pexp(100, lambda)

# C
pexp(1000, lambda)

# D
1 - pexp(1000, lambda)

# E
1 - pexp(4000, lambda)

# F
pexp(1200, lambda) - pexp(900, lambda)

# ---- Aufgabe 2 ----
beta <- 2.2
lambda <- 1/8.7
# A
1 - pweibull(4, shape=beta, scale = 1/lambda)

# B
x <- seq(0, 25, 0.01)
plot(x, dweibull(x, shape = beta, scale = 1/lambda), type='l')

# C
qweibull(0.05, shape = 2.2, scale = 8.7)

# D
qweibull(0.632, shape = 2.2, scale = 8.7)

# E
mean(rweibull(100000, shape=2.2, scale=8.7))

8.7 * gamma(1+1/2.2)
