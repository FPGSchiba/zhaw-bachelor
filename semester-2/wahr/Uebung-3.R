# ---- Aufgabe 2 ----
(0.25*0.2) + (0.7 * 0.5) + (0.5 * 0.3)

(0.25 * 0.2) / 0.55

# ---- Aufgabe 3 ----
(0.8 * 0.05) + (0.2 * 0.99)

0.2 * 0.01

# ---- Aufgabe 4 ----
?log
sqrt(2 * 365 * log(2, base = exp(1)))

# C
nsim <- 10000
m <- matrix(nrow = nsim, ncol = 2)
for (i in 1:nsim) {
  m[i,] <- sample(1:365, size = 2, replace = T)
}

df <- data.frame(m)
nrow(df[df$X1 == df$X2,]) / nrow(m)
