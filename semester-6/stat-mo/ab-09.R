# Aufgabe 1
load("semester-6/stat-mo/data/depression.rda")
str(depression)

## A
fit.dep <- lm(y ~ age + TRT, data = depression)
summary(fit.dep)

### Ja alle Koeffizienten sind signifikant, da die p-Werte für alle Koeffizienten kleiner als 0.05 sind.

## B
par(mfrow = c(2, 3)) #  mehrere Plots
plot(fit.dep, which = 1:3) # with which=1:3 für nur die ersten 3

source("semester-6/stat-mo/plotlmSim.R") # einlesen von funktion
plot.lmSim(fit.dep, seed = 32, nsim = 100)

###  Die Residuen vs. fitted Werte zeigen eine systematische Abweichung.

library("sfsmisc")
p.res.2x(~ age + TRT, data = fit.dep, scol = 2:1)

### Ich glaube ich sehe gruppen in den Ecken des Plots.

## C
fit.dep2 <- lm(y ~ age + TRT + age:TRT, data = depression)
summary(fit.dep2)
drop1(fit.dep2, test = "F")

### Ja die Interaktion ist signifikant, da der p-Wert für den Interaktionsterm kleiner als 0.05 ist.

##  D
par(mfrow = c(2, 3)) #  mehrere Plots
plot(fit.dep2, which = 1:3) # with which=1:3 für nur die ersten 3

source("semester-6/stat-mo/plotlmSim.R") # einlesen von funktion
plot.lmSim(fit.dep2, seed = 32, nsim = 100)

### Die residuen sehen jetzt besser aus, da sie keine systematische Abweichung mehr zeigen.

#  Aufgabe 2
load("semester-6/stat-mo/data/income.rda")
str(income)

## A
par(mfrow = c(1, 1)) #  mehrere Plots
library("ggplot2")
ggplot(income, aes(x = height, y = log(earning), color = sex)) +
  geom_point() +
  labs(title = "Log(Earning) vs. Height", x = "Height", y = "Log(Earning)")

###  Männer sind im Durchschnitt grösser als Frauen.
###  Das Einkommen scheint auch leicht mit der Körpergrösse zu steigen, aber es gibt auch viele Ausreisser, besonders bei den Männern.

## B
fit.income <- lm(log(earning) ~ height + sex + height:sex, data = income)
summary(fit.income)

ggplot(income, aes(x = height, y = log(earning), color = sex)) +
  geom_point() +
  labs(title = "Log(Earning) vs. Height", x = "Height", y = "Log(Earning)") +
  geom_line(
    data = transform(
      expand.grid(
        height = seq(min(income$height), max(income$height), length.out = 100),
        sex = levels(income$sex)
      ),
      log_earn_pred = predict(fit.income, newdata = data.frame(height = height, sex = sex))
    ),
    aes(y = log_earn_pred),
    linewidth = 1
  )

##  C
summary(fit.income)

### Keine parameter sind signifikant.

# Aufgabe 3
load("semester-6/stat-mo/data/GASKETS.rda")
GASKETS

## A
fit.gaskets <- lm(DEFECTS ~ SPEED, data = GASKETS)

ggplot(GASKETS, aes(x = SPEED, y = DEFECTS)) +
  geom_point() +
  labs(title = "Defects vs. Speed", x = "Speed", y = "Defects") +
  geom_line(
    data = transform(
      expand.grid(SPEED = seq(min(GASKETS$SPEED), max(GASKETS$SPEED), length.out = 100)),
      DEFECTS_pred = predict(fit.gaskets, newdata = data.frame(SPEED = SPEED))
    ),
    aes(y = DEFECTS_pred),
    linewidth = 1
  )

## B
par(mfrow = c(2, 3)) #  mehrere Plots
plot(fit.gaskets, which = 1:3) # with which=1:3 für nur die ersten 3
source("semester-6/stat-mo/plotlmSim.R") # einlesen von funktion
plot.lmSim(fit.gaskets, seed = 32, nsim = 100)

### Im Scale Location Plot sieht man klar eine systematische Abweichung, da die Punkte eine steigende Tendenz zeigen.

## C
