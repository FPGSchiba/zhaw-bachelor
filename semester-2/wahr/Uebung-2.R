# ---- Aufgabe 1 ----
nsim <- 10000
m <- matrix(NA, nrow=nsim, ncol=2)

for (i in 1:nsim) {
  m[i,] <- sample(1:3, size=2, replace=F, prob = c(4, 2, 3) / 9)
}
sum(rowSums(m == 3) == 0) / nsim

# ---- Aufgabe 2 ----
nsim <- 100000
zaehler <- 0
p <- c(0.25 / 2, 0.25, 0.25 / 2, 0.5)
sum(p)

for (i in 1:nsim) {
  rad_dreh <- sample(c(1,2,4,7), size=5, replace = T, prob = p)
  number <- as.numeric(paste(rad_dreh, collapse = ""))
  if (41721 > number) {
    zaehler <- zaehler + 1
  }
}

zaehler / nsim

# ---- Aufgabe 3 ----
# A
factorial(5) / factorial(2)
factorial(4) / factorial(2)
12/60

# B
factorial(7) * factorial(2) / factorial(8)

# C
factorial(11) / factorial(6)

# D

choose(5, 2) * choose(7, 3)
5 * choose(7, 3)

# E
choose(90, 3) / choose(100, 3)

# f
factorial(35) / factorial(30)
choose(10, 5)

# ---- Afugabe 4 ----
# A
0.5**4
0.5**3
0.5**2
0.5**1
