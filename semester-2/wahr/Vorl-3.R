# ---- Theorie ----


# --- Aufgabe 1 ----
q <- sqrt(18/100)
p <- 1 - sqrt(18/100)

p**2

p * q * 2


# ---- Aufgabe 2 ----
farben<-c("Kreuz", "Herz","Pik","Karo")
nummern<-c(2:10,"Bube","Dame", "Koenig","Ass")
deck<-expand.grid(Farbe=farben,Nummer=nummern)
deck<-paste(deck$Farbe,deck$Nummer)
asse<-paste(farben,"Ass")

length(deck)
haende <- matrix(NA, nrow = nsim, ncol = 2)
nsim <- 10000
for (i in 1:nsim) {
  haende[i,] <- sample(deck, size = 2, replace = F)
}

sum(haende[,1] %in% asse & haende[,2] %in% asse) / sum(haende[,1] %in% asse)

sum(haende[,2] %in% asse) / nsim

# ---- Aufgabe 3 ----

0.8 * 0.15 / (0.8 * 0.15 + 0.2 * 0.85)

# ---- Aufgabe 4 ----
# A
wahr <- function(sensitivität, spezifizität, prävalenz) {
  return (sensitivität * prävalenz / (sensitivität * prävalenz + (1 - spezifizität) * (1 - prävalenz)))
}

# B
test <- wahr(0.997, 0.985, 0.005)
test ** 2 # Das

# C

praevalenz <- seq(0.001, 0.3, 0.001)
wahrs <- c()
for (i in 1:length(praevalenz)) {
  wahrs[i] <- wahr(0.997, 0.985, praevalenz[i])
}

wahrs
data <- data.frame(praevalenz=praevalenz, wahrs=wahrs)

library(ggplot2)
# Basic line plot with points
ggplot(data=data, aes(x=praevalenz, y=wahrs, group=1)) +
  geom_line()+
  geom_point()


