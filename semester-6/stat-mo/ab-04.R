# Aufgabe 1

highway <- read.csv("semester-6/stat-mo/data/highway.csv", header = TRUE)

## A
fit <- lm(runoff ~ rain, data = highway)
plot(highway$rain, highway$runoff, xlab = "Regenmenge (mm)", ylab = "Abfluss (l/s)", main = "Abfluss vs. Regenmenge", pch = 19)
abline(fit, col = "red", lwd = 2)

## B
summary(fit)$r.squared
### Das R-Quadrat beträgt 0.97 was bedeutet, dass 97% der Varianz im Abfluss durch die Regenmenge erklärt werden kann.

## C
summary(fit)$coefficients

### Der p-Wert für den Koeffizienten der Regenmenge (rain) ist sehr klein (p < 0.05), was darauf hindeutet, dass es einen signifikanten Zusammenhang zwischen Regenmenge und Abfluss gibt.
### Also für jede zusätzliche mm Regenmenge steigt der Abfluss um ca 0.83.

##  D
source("semester-6/stat-mo/plotlmSim.R")
par(mfrow = c(2, 3)) #  mehrere Plots
plot(fit, which = 1:3)
plot.lmSim(fit)

### Was gut aussieht: Der QQ-Plot zeigt, dass die Residuen annähernd normalverteilt sind.
### Was nicht gut aussieht: Die Residuen vis fitted zeigen eine systematische Abweichung von der Regressionslinie.
### Was auch noch nicht gut: Der Scale-Location Plot zeigt eine komische abweichung von einer Wagerechten. (Links variable varianz bis ca. 40 mm Regenmenge, danach deutlich konstantere Varianz)

## E
###  Um die systematische Abweichung der Residuen "gerade" zu biegen.

##  F
highway$runoff.log <- log(highway$runoff)
highway$rain.log <- log(highway$rain)
fit.log <- lm(runoff.log ~ rain.log, data = highway)
summary(fit.log)

### Es gibt erneut einen signifikanten Zusammenhang zwischen der logarithmierten Regenmenge und dem logarithmierten Abfluss.

## G
x0 <- data.frame(rain.log = log(50))
h <- predict(fit.log, newdata = x0, interval = "prediction")

# Rücktransformation mit Korrektur (da Zielgrösse logarithmiert)
exp(h + summary(fit.log)$sigma^2 / 2)

### Der erwartete Abfluss bei einer Regenmenge von 50 liegt bei ca 40.2 mit einem Prognoseintervall von [30.1, 53.7].

## H
par(mfrow = c(2, 3)) #  mehrere Plots
plot(fit.log, which = 1:3)
plot.lmSim(fit.log)

### Die residuals vs fitted plot sieht deutlich besser aus, da die Residuen jetzt zufällig um die Regressionslinie verteilt sind.
### Der Scale-Location Plot sieht auch deutlich besser aus, da der Glätter besser and die Simultionen angepasst ist.
###  Der Normal Q-Q Plot ziemlich gleich aus.

### Daher würde ich sagen, dass die logarithmische Transformation die Modellannahmen ein wenig besser erfüllt als das ursprüngliche Modell.


# Aufgabe 2
MPIZH <- read.table("semester-6/stat-mo/data/MPIZH.dat", header = TRUE)
MPIZH

##  A
fit <- lm(MPI ~ KPI + HZ, data = MPIZH)
###  MPI = beta0 + beta1 * KPI + beta2 * HZ + E mit E ~ N(0, sigma^2) iid

##  B
coef(fit)
### beta0 (Intercept) = -68.7, beta1 (KPI) = 1.6, beta2 (HZ) = 2.0
###  Das bedeutet, dass für jede zusätzliche Einheit in KPI der MPI um 1.6 Einheiten steigt, und für jede zusätzliche Einheit in HZ der MPI um 2.0 Einheiten steigt.

## C
library(rgl)
library(car)
open3d()
scatter3d(MPI ~ KPI + HZ, data = MPIZH, axis.scale = FALSE)
rglwidget()

## D
summary(fit)
### Ja, es gibt einen signifikanten Zusammenhang zwischen MPI und einem der Koeffizienten

## E
summary(fit)$coefficients
###  Ja, beide Koeffizienten (KPI und HZ) sind signifikant, da ihre p-Werte sehr klein sind (p < 0.05).

## F
summary(fit)$r.squared
###  Das R-Quadrat beträgt 0.92, was bedeutet, dass 92% der Varianz im MPI durch die Variablen KPI und HZ erklärt werden kann.
### WICHTIG: Adjusted R-squared benutzen bei multiple Regression, da es die Anzahl der Prädiktoren berücksichtigt.
