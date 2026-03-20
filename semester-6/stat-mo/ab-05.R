# Aufgabe 1
load("semester-6/stat-mo/data/Advertisement.rda")
adv

## A
fit.adv <- lm(sales ~ ., data = adv)
coef(fit.adv)

### Interpretation von radio:
### Der Koeffizient für radio beträgt 0.08, was bedeutet, dass für jede zusätzliche Einheit in radio die sales um 0.08 Einheiten steigen, wenn alle anderen Variablen konstant gehalten werden.

##  B
summary(fit.adv)

### Ja, es gibt mindestens eine Variable, die einen signifikanten Einfluss auf die sales hat, da der p-Wert für der F-Test insgesamt sehr klein ist (p < 0.05).

## C
confint(fit.adv, parm = "radio", level = 0.99) * 1000

## D
predict(fit.adv, newdata = data.frame(radio = 40000, newspaper = 100000, TV = 150000), interval = "prediction", level = 0.95)

## E
summary(fit.adv)

### Nein, die Zeitungen haben keinen signifikanten Einfluss auf die sales, da der p-Wert für newspaper sehr gross ist (p > 0.05).

## F
library(rgl)
library(car)
open3d()
scatter3d(sales ~ radio + TV, data = adv, axis.scale = FALSE)
rglwidget()

# Aufgabe 2
catheter <- read.table("semester-6/stat-mo/data/catheter.dat", header = TRUE, sep = ",")
catheter

##  A
par(mfrow = c(3, 2)) #  mehrere Plots
hist(catheter$Groesse, main = "Histogramm der Kathetergrössen", xlab = "Grösse (mm)", breaks = 10)
hist(catheter$Gewicht, main = "Histogramm der Kathetergewichte", xlab = "Gewicht (g)", breaks = 10)

boxplot(catheter$Groesse, main = "Boxplot der Kathetergrössen", ylab = "Grösse (mm)")
boxplot(catheter$Gewicht, main = "Boxplot der Kathetergewichte", ylab = "Gewicht (g)")

plot(catheter$Groesse, catheter$y, main = "Streudiagramm von Grösse vs Gewicht", xlab = "Grösse (mm)", ylab = "Gewicht (g)")
plot(catheter$Gewicht, catheter$y, main = "Streudiagramm von Gewicht vs Gewicht", xlab = "Gewicht (g)", ylab = "Gewicht (g)")

### Schwierig in diesen Plots etwas zu erkennen, aber ich hätte gesagt, dass die Daten ganz leicht Rechtsschief sind.

##  B
fit.cat.gro <- lm(y ~ Groesse, data = catheter)
coef(fit.cat.gro)
summary(fit.cat.gro)

### Koeffizient Steigung: 0.49, Koeffizient Intercept: -21.89
### Sigma: 4

fit.cat.gew <- lm(y ~ Gewicht, data = catheter)
coef(fit.cat.gew)
summary(fit.cat.gew)

### Koeffizient Steigung: 0.37, Koeffizient Intercept: -7.97
### Sigma: 3.8

##  C
summary(fit.cat.gro)
### Hier hat die Steigung einen signifikanten Einfluss auf y.

summary(fit.cat.gew)
###  Hier hat die Steigung auch einen signifikanten Einfluss auf y.

## D
fit.cat <- lm(y ~ Groesse + Gewicht, data = catheter)
summary(fit.cat)
### Globaler F-Test: Es gibt mindestens eine Variable, die einen signifikanten Einfluss auf y hat.
### Koeffizienten:
###  Groesse: Hat keinen signifikanten Einfluss auf y, da der p-Wert sehr gross ist (p > 0.05).
###  Gewicht: Hat auch keinen signifikanten Einfluss auf y, da der p-Wert auch sehr gross ist (p > 0.05).

##  E
summary(fit.cat)
### Das sigma ist ähnlich wie bei den einfachen Modellen.
