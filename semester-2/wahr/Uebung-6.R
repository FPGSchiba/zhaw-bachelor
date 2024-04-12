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
# Variablen
nsim <- 10000
num_machines <- 6
# Mitarbeiter:       1     2     3     4     5
service_zeiten <- c(1.3,  0.75, 1.2,  1.4,  0.9)
zustaendig     <- c(0.06, 0.08, 0.21, 0.28, 0.37)

# Experiment Matrix
# 20 wird sehr unwahrscheindlich erreicht mit rpois(1, 6)
m <- matrix(nrow = nsim, ncol = 20)

# Simulationsloop
for (i in 1:nsim) {
  # Anzahl ausgefallene Machinen, mit Poisson verteilung
  ausgefallene_machinen <- rpois(1, num_machines)
  # Pro Tag alle ausgefallenen Machine eine Wartung nach Zuständigkeiten
  m[i,0:ausgefallene_machinen] <- sample(service_zeiten, size=ausgefallene_machinen, prob = zustaendig, replace = TRUE)
}
# Bespiel Eintrag
m[100,] # [1] 0.9 0.9 0.9  NA  NA  NA  NA  NA  NA  NA  NA  NA  NA  NA  NA  NA  NA  NA  NA  NA

# Reihen summieren
daily_service <- rowSums(m, na.rm = T)
# Beispiel Eintrag
daily_service[100] # 2.7

# Durchschnittliche Dauer des Services für alle Mitarbeiter zusammen:
mean(daily_service) # ~ 6.7
median(daily_service) # ~ 6.5

# Servicezeit aller Mitarbeiter, welche in 75% aller Fälle nicht überschritten wird
quantile(daily_service, probs = 0.75) # ~ 8.5


