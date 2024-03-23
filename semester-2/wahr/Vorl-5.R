# ---- A1 ----
sum(dbinom(x = 20:22, size = 22, prob = 28/34))

# ---- A2 ----
n <- 16
p <- 1/4

# A
dbinom(x = 8, size = n, prob = p)
pbinom(7, size = n, prob = p)
pbinom(8, size = n, prob = p)
sum(dbinom(9:n, size = n, prob = p))
sum(dbinom(8:n, size = n, prob = p))

# B
pbinom(1:n, size = n, prob = p) # 7
qbinom(0.95, size = n, prob = p)

# C
mean(rbinom(100000, n, p)) # 4
