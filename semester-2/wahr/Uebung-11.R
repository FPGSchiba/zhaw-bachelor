# ---- Aufgabe 1 ----
# E(X) = (a + b)/2 -> 0
# Var(X) (a + b)^2/12 -> 1/12

# S_225 ~ N(0, 225/12)
# P(S_225 <= 5) - P(S_255 < - 5)

pnorm(5, mean = 0, sd = sqrt(225/12)) - pnorm(-5, mean=0,  sd=sqrt(225/12))

# ---- Aufgabe 2 ----

# S_69 ~ N(69*14, 69*9^2)
# P(S_96 > 1000)

1 - pnorm(1000, mean = 69*14, sd = sqrt(69*9))
