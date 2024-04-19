# ---- Aufgabe 1 ----
dnbinom(6, 7, 0.22)

# ---- Aufgabe 3 ----
nsim <- 100000
lambda <- 273/24
p <- 0.05
num_cought_fishes <- c()

for (i in 1:nsim) {
  num_fishes <- rpois(5, lambda = lambda)
  cougth_fishes <- c()
  for (j in 1:5) {
    cougth_fishes[j] <- rbinom(1, num_fishes[j], p)
  }
  num_cought_fishes[i] <- sum(cougth_fishes)
}

mean(num_cought_fishes)

# ---- Aufgabe 4 ----
ppois(4, 1.2)
