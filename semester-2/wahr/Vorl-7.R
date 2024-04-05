# ---- Aufgabe 1 ----
# A
dnbinom(4, size = 12, prob = 0.45)

# B
pnbinom(7, 12, 0.45)

# C
(12 * (1 - 0.45))/0.45 + 12 # Anzahl Würfe bis zum 12ten Erfolg
(12 * (1 - 0.45))/0.45 # Anzahl Misserfolge

# ---- Aufgabe 2 ----
# A
# X ~ Hyper(4, 10, 5)
dhyper(0:4, m=4, n=10, k=5) # Verteilung
# phyper -> Kumulativ

# B
# m := Anzahl Faule Äpfel
# n := Anzhal Gute Äpfel
# k := Anzahl eingepackter Äpfel

# C 
dhyper(0, m=4, n=10, k=5)

# D
# P(X <= 2)
phyper(2, m = 4, n=10, k=5)
5*(4/14)

# ---- Aufgabe 3 ----
# A
# X ~ Pois(3.8)
# X = "Kletterunfälle pro Jahr"

# B
# lambda = 3.8 -> Jahresschnitt

# C
# n = infinity

# D
dpois(0:10, 3.8)

# E
nsim <- 100000
sum(rpois(nsim, 3.8)) / nsim
var(rpois(nsim, 3.8))

