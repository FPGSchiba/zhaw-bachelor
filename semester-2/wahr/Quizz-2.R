# ---- Afugabe 1 ----
qpois(0.93, lambda=6)

# ---- Aufgabe 2 ----
nsim <- 10000
lambda <- 387 / 24
p <- 0.04
fishes_cought <- c()

for (i in 1:nsim) {
  count <- 0
  for (j in 1:8) {
    num_fish <- rpois(1, lambda)
    count <- count + rbinom(1, num_fish, p)
  }
  fishes_cought[i] <- count
}

mean(fishes_cought)

# ---- Aufgabe 3 ----
dbinom(8, 16, 0.37)

# ---- Aufgabe 4 ----
(1 - 0.73)/0.73**2

# ---- Aufgabe 5 ----
qgeom(0.91, 1/5)
pgeom(4, 1/5)

# ---- Aufgabe 7 ----
dbinom(0, 8, 0.23)
# ---- Aufgabe 8 ----
4*7/(7+5)
# ---- Aufgabe 9 ----
qpois(0.93, 1)
# ---- Aufgabe 11 ----
set.seed(1384)
median(rhyper(50, 30, 10, 4))

# ---- Aufgabe 12 ----
19 * 0.29 * (1 - 0.29)

# ---- Aufgabe 14 ----
nsim <- 10000
p <- 0.112
lambda <- 150
num_breads <- 15
results <- c()

for (i in 1:nsim) {
  customers <- rpois(1, lambda)
  bread_purchased <- rbinom(1, customers, p)
  results[i] <- bread_purchased <= num_breads
}

results

sum(results) / nsim
