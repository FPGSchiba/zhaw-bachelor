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


# ---- Aufgabe 6 ----
nsim <- 50000
complete_reset_cards <- function() {
  return(c(rep(1, 8), rep(2, 7), rep(3, 7), rep(4, 7), rep(5, 6), rep(6, 6), rep(-1, 3), rep(-2, 6)))
}
cards <- complete_reset_cards()
m <- matrix(nrow = nsim, ncol = 2)

reduct_card <- function(card) {
  return(cards[cards == card])
}

reset_cards <- function(num_schrecken) {
  return(c(rep(1, 8), rep(2, 7), rep(3, 7), rep(4, 7), rep(5, 6), rep(6, 6), rep(-1, 3), rep(-2, 6 - num_schrecken)))
}


for (i in 1:nsim) {
  running <- TRUE
  num_voegel <- 0
  num_katzen <- 0
  num_schrecken <- 0
  while(running) {
    card <- sample(cards, 1)
    if (card < 0) {
      if (card == -1) {
        num_katzen <- num_katzen + 1
        num_voegel <- 0
        cards <- reset_cards(num_schrecken)
      }
      if (card == -2) {
        num_schrecken <- num_schrecken + 1
        cards <- reduct_card(-2)
      }
    } else {
      num_voegel <- num_voegel + card
      cards <- reduct_card(card)
    }
    
    if (num_schrecken == 6) {
      running <- FALSE
    }
  }
  complete_reset_cards()
  m[i,1] <- num_voegel
  m[i,2] <- num_katzen
}

mean(m[,1])
mean(m[,2])



