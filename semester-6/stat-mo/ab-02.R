# Aufgabe 1
uhren <- read.table("semester-6/stat-mo/data/AntikeUhren.dat", header = TRUE)

##  A
fit <- lm(Preis ~ Alter, data = uhren)
coef(fit)

# Gleichung der Regressionsgeraden: Preis = -191.65757 + 10.47909 * Alter

## B
# H_0: beta = 0
# H_A: beta != 0
summary(fit)

# Ja das Alter hat einen signifikanten Einfluss auf den Preis,
# da der p-Wert für den Koeffizienten des Alters (10.47909) sehr klein ist (p < 0.05).

## C
# Für H_0: beta = 15, H_A: beta != 15
to_be_tested_slope <- 15
hat_beta <- coef(fit)[2]
se_beta <- summary(fit)$coefficients[2, 2]
t <- (hat_beta - to_be_tested_slope) / se_beta # realisierte Teststatistik
2 * pt(-abs(t), 30) # p-Wert
# Der p-Wert ist grösser als 0.01, daher können wir die Nullhypothese nicht ablehnen.
# Es gibt nicht genügend Beweise, um zu behaupten, dass der Koeffizient des Alters signifikant von 15 abweicht.

## D
confint(fit, parm = 2, level = 0.95)
# Das 95%-Konfidenzintervall für den Koeffizienten des Alters (beta) liegt zwischen 6.823468 und 14.13472

##  E
x0 <- data.frame(Alter = 160)
predict(fit, newdata = x0, interval = "confidence", level = 0.95)
predict(fit, newdata = x0, interval = "prediction", level = 0.95)

# Wichtiger für den Verkäufer zu wissen ist das Vorhersageintervall, da es die Unsicherheit in
# der Vorhersage für einen einzelnen neuen Datenpunkt berücksichtigt. Das Konfidenzintervall
# gibt hingegen die Unsicherheit für den durchschnittlichen Preis bei einem Alter von 160 Jahren an.

# Aufgabe 2
load("semester-6/stat-mo/data/conconi.rda")
load("semester-6/stat-mo/data/conconi2.rda")

## A
fit <- lm(puls ~ speed, data = conconi)
plot(conconi$speed, conconi$puls, xlab = "Puls (Schläge pro Minute)", ylab = "Geschwindigkeit (km/h)", main = "Conconi-Test: Geschwindigkeit vs. Puls")
abline(fit, col = "red")

##  B
summary(fit)$r.squared
# Der Prozentsatz der Varianz in der Geschwindigkeit, der durch den Puls erklärt wird,
# beträgt etwa 0.99, was auf eine sehr starke lineare Beziehung zwischen Puls und Geschwindigkeit hinweist.

## C
x0 <- data.frame(speed = 10)
predict(fit, newdata = x0, interval = "prediction", level = 0.95) #  Wichtig: Hier war ein Prognoseintervall gefragt, nicht das Konfidenzintervall!
# Er muss mit ca 150 Schlägen pro Minute rechnen, mit einem 95%-Konfidenzintervall von ca [145.7, 155.6] Schlägen pro Minute.

##  D
x0 <- data.frame(speed = 0)
predict(fit, newdata = x0, interval = "confidence", level = 0.95)
# Der geschätzte Ruhepuls beträgt ca 86 Schläge pro Minute, mit einem 95%-Konfidenzintervall von ca [81.3, 92.0] Schlägen pro Minute.
# Das ist eher hoch für einen Ruhepuls. Extrapolation!

## E
coef(fit)
confint(fit, parm = 2, level = 0.95) # Plausibilität wird mit Konfidenzintervall geprüft
# Der Puls nimmt pro km/h um ca 6.4 Schläge pro Minute zu.

## F
fit.con2 <- lm(puls ~ speed, data = conconi2)
summary(fit.con2)
coef(fit.con2)

confint(fit.con2, parm = 2, level = 0.95) # Überlappung der Konfidenzintervalle prüfen > Nicht überlappen heisst signifikant verschieden
# Ja, die Steigung ist signifikant von 0 verschieden, da das 95%-Konfidenzintervall für die Steigung (beta) nicht 0 enthält.
# Das bedeutet, dass es eine signifikante lineare Beziehung zwischen Puls und Geschwindigkeit gibt.
