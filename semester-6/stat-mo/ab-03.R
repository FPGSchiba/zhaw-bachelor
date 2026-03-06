# Aufgabe 1
windmuehle <- read.table("semester-6/stat-mo/data/Windmuehle.dat", header = TRUE)

## A
fit.lin <- lm(Strom ~ Windgeschwindigkeit, data = windmuehle)
par(mfrow = c(2, 3)) #  mehrere Plots
plot(fit.lin, which = 1:3)
source("semester-6/stat-mo/plotlmSim.R") # einlesen von funktion
plot.lmSim(fit.lin)

# Nicht erfüllt der Zusammenhang ist keine Gerade zwischen Strom und Windgeschwindigkeit.

## B
windmuehle$Windgeschwindigkeit2 <- 1 / windmuehle$Windgeschwindigkeit
fit.inv <- lm(Strom ~ Windgeschwindigkeit2, data = windmuehle)

par(mfrow = c(1, 1)) # zurück zu einem Plot
plot(windmuehle$Windgeschwindigkeit, windmuehle$Strom, xlab = "Windgeschwindigkeit [m/s]", ylab = "Strom [A]", main = "verbessertes Modell", pch = 19)
xx <- seq(0.1, 30, 0.1)
lines(xx, coef(fit.inv)[1] + coef(fit.inv)[2] * (1 / xx), col = "red", lwd = 2)

##  C
# Alpha ist immernoch der Y-Achsenabschnitt
# Beta ist die Steigung der invertierten Windgeschwindigkeit

## D
par(mfrow = c(2, 3)) #  mehrere Plots
plot(fit.inv, which = 1:3)
plot.lmSim(fit.inv)

# Was gut aussieht: Residuen vs. fitted values (keine Muster, keine Heteroskedastizität) und Normal Q-Q Plot (Residuen scheinen normalverteilt zu sein).
# Was nicht so gut aussieht: Scale-Location Plot, speziell bei den simulationen verläuft das Modell nicht so gut

##  E
summary(fit.inv)

# Ja es gibt einen signifikanten Zusammenhang zwischen Strom und der inversen Windgeschwindigkeit, da der p-Wert für den Koeffizienten der inversen Windgeschwindigkeit (Windgeschwindigkeit2) sehr klein ist (p < 0.05).

## F
confint(fit.inv, parm = 1, level = 0.95)

# Das 95%-Konfidenzintervall für den durchschnittlichen Strom bei der maximalen Windgeschwindigkeit liegt zwischen ca 2.9 und 3 Ampere.

## G
x0 <- data.frame(Windgeschwindigkeit2 = 1 / 15)
predict(fit.inv, newdata = x0, interval = "prediction", level = 0.95)

#  Das Prognoseintervall liegt bei [1.74, 2.14]

# Aufgabe 2
anscombe <- read.table("semester-6/stat-mo/data/Anscombe.dat", header = TRUE)
View(anscombe)

# A
fit.a1 <- lm(y1 ~ x1, data = anscombe)
fit.a2 <- lm(y2 ~ x2, data = anscombe)
fit.a3 <- lm(y3 ~ x3, data = anscombe)
fit.a4 <- lm(y4 ~ x4, data = anscombe)
a.values <- data.frame(a = 1:4, intercept = NA, slope = NA, sigma = NA, r.squared = NA)
a.values$intercept <- c(coef(fit.a1)[1], coef(fit.a2)[1], coef(fit.a3)[1], coef(fit.a4)[1])
a.values$slope <- c(coef(fit.a1)[2], coef(fit.a2)[2], coef(fit.a3)[2], coef(fit.a4)[2])
a.values$sigma <- c(summary(fit.a1)$sigma, summary(fit.a2)$sigma, summary(fit.a3)$sigma, summary(fit.a4)$sigma)
a.values$r.squared <- c(summary(fit.a1)$r.squared, summary(fit.a2)$r.squared, summary(fit.a3)$r.squared, summary(fit.a4)$r.squared)

a.values

# B
par(mfrow = c(2, 2))
plot(anscombe$x1, anscombe$y1, xlab = "x1", ylab = "y1", main = "Datensatz 1", pch = 19)
abline(fit.a1, col = "red", lwd = 2)
plot(anscombe$x2, anscombe$y2, xlab = "x2", ylab = "y2", main = "Datensatz 2", pch = 19)
abline(fit.a2, col = "red", lwd = 2)
plot(anscombe$x3, anscombe$y3, xlab = "x3", ylab = "y3", main = "Datensatz 3", pch = 19)
abline(fit.a3, col = "red", lwd = 2)
plot(anscombe$x4, anscombe$y4, xlab = "x4", ylab = "y4", main = "Datensatz 4", pch = 19)
abline(fit.a4, col = "red", lwd = 2)

## C
#  Die tabelisierten werte sehen alle gleich aus, aber die plots zeigen, dass die Daten sehr unterschiedlich verteilt sind.


## D
par(mfrow = c(2, 2))
plot(fit.a1, which = 1)
plot(fit.a2, which = 1)
plot(fit.a3, which = 1)
plot(fit.a4, which = 1)
