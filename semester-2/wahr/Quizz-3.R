# ---- Aufgabe 1 ----
pexp(27.9, rate=8) - pexp(0.6, rate=8)

# ---- Aufgabe 2 ----
1/3.8
# ---- Aufgabe 3 ----
1-exp(-3.82*0.93)

# ---- Aufgabe 4 ----
nsim <- 100000
hinweg_rueck <- 22
hin_ampel <- runif(nsim, min= 0, max=2)
rueck_ampel <- runif(nsim, min=0, max=2)
einkauf <- rnorm(nsim, mean=14, sd=0.5)
kasse <- rexp(nsim, rate=1/4) + 2
way <- hinweg_rueck + hin_ampel + rueck_ampel + einkauf + kasse
median(way)

# ---- Aufgabe 5 ----
# S_89 ~ N(2.2*89, 2.7^2*89)

pnorm(208, mean=2.2*89, sd=sqrt(2.7^2*89))
