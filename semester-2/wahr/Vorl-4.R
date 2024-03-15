# Zufalls variable

# - Möglichkeit 1
gewinn <- c(-3, -3, 2, 2, 2)
sum(sample(gewinn, 2, replace = F))

# - Möglichkeit 2:
sample(c(4, -1, -6), 1, prob = c(3/10, 6/10, 1/10))

# ---- Aufgabe 4 ----

# Kumulative verteilung
cumsum(c(3/10, 6/10, 1/10))
plot(stepfun(c(-6, -1, 4), cumsum(c(0, 1/10, 6/10, 3/10))))

# D
nsim <- 100000
m <- c()

for (i in 1:nsim) {
  m[i] <- sample(c(4, -1, -6), 1, prob = c(3/10, 6/10, 1/10))
}

round(var(m))


# ---- Aufgabe 4 ----
36 + 6 + 48
