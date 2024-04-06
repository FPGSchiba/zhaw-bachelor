# ---- Aufgabe 1 ----

sum((pnbinom(0:1000, size = 10, prob = 0.09) >= 0.95) == FALSE) + 10

# ---- Aufgabe 2 ----
# A
dhyper(0, 3, 32, 4)

# B
dhyper(1, 3, 32, 4)

# C
dhyper(1, 3, 32, 4) * 1/3

# ---- Aufgabe 3 ----
lambda = 122/10/20
1 - ppois(4, lambda = lambda)
# ---- Aufgabe 4 ----
