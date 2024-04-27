# ---- Aufgabe 1 ----
mu <- 12.9
sigma <- 2**2
# X ~ N(12.9, 4)
# A
# P(X > 11.5)
pnorm(11.5, mean = mu, sd = sqrt(sigma), lower.tail = F)

# B
# P(11.0 < X < 14.5)
pnorm(14.5, mean=12.9, sd=sqrt(sigma)) - pnorm(11, mean=12.9, sd=sqrt(sigma))

# C
# P(X < 14)
pnorm(14, mean=mu, sd=sqrt(sigma))

# ---- Aufgabe 2 ----
# -- A --
# X := Anzhal Bisse pro Person
# X ~ Pois(3.5)
# P(X = 0)
dpois(0, 3.5)

# -- B --
# X := Länge des Möbelstückes in cm
# X ~ N(60, 0.25)
# [60 - 2*0.5, 60 + 2*0.5] = [59,61]
pnorm(61, mean=60, sd=0.5) - pnorm(59, mean=60, sd=0.5)

# -- C --
# X := Anzahl Gäste die nicht absagen und kommen
# X ~ Bin(50, 5/6)
# P(X > 45)
1 - pbinom(45, 50, 5/6)

# -- D --
# X := Wartezeit für den Bus
# X ~ Unif([0, 12])
# 
qunif(0.6, min=0, max=12)

# -- E --
# X := Zeit bis zum nächsten Erdbeben
# X ~ Exp(160/365)
# P(X > 3)
1 - pexp(3, rate=160/365)

# -- F --
# X := Lebensdauer des Rasenmähers in Jahren
# E[X] = 6 -> Rechnen
# X ~ Weibull(2, 0.1477045)
# P(X > 6)
lambda <- gamma(1.5)/6
1 - pweibull(6, shape=2, scale=1/lambda)

# -- G --
# X := Wartezeit für 2 Kunden
# X ~ G(2, 1/2)
# P(X > 5)
1 - pgamma(5, shape=2, rate=1/2)



