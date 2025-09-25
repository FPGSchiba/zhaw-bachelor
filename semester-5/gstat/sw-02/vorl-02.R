x <- rgamma(100, shape = 1.3, scale = 1) # Daten simulieren
install.packages(pkgs = "fitdist")
library(fitdistrplus)
descdist(x) # Befehl für Cullen-Frey Graph
