# Aufgabe 1
load("semester-6/stat-mo/data/Cherry.rda")
cherry

##  A
plot(cherry)

### Diameter und Volume scheinen stark linear abhängig zu sein

##  B
cherry$LogVolume <- log(cherry$Volume)
cherry$LogDiameter <- log(cherry$Diameter)
cherry$LogHeight <- log(cherry$Height)
fit.exercise <- lm(LogVolume ~ LogDiameter + LogHeight, data = cherry)
summary(fit.exercise)

### LogDiameter hat ganz klar einen signifikanten einfluss
###  LogHeight hat auch einen Signifikanten einfluss, aber nur bei 0.05 alpha

##  C
confint(fit.exercise, parm = 3, level = 0.95)
### Oder von Hand
beta.hat <- coef(fit.exercise)[3]
se.beta.hat <- summary(fit.exercise)$coefficients[3, 2]
lower.bound <- beta.hat - qnorm(0.975) * se.beta.hat
upper.bound <- beta.hat + qnorm(0.975) * se.beta.hat
c(lower.bound, upper.bound)

##  D
coef(fit.exercise)

###  LogDiameter: 2
###  LogHeight:   1

##  E
confint(fit.exercise, parm = 2, level = 0.95)
confint(fit.exercise, parm = 3, level = 0.95)

## F
x0 <- data.frame(LogDiameter = log(5.3), LogHeight = log(27))
y0 <- predict(fit.exercise, newdata = x0, interval = "prediction", level = 0.95)
exp(y0 + summary(fit.exercise)$sigma^2 / 2)

#  Aufgabe 2
load("semester-6/stat-mo/data/salary.rda")
salary$education <- factor(salary$education, levels = 1:3, ordered = TRUE)
salary

##  A
plot(salary$income, salary$experience, xlab = "Income", ylab = "Experience", pch = 16, col = as.numeric(salary$education))
legend("topleft", legend = levels(salary$education), col = 1:nlevels(salary$education), pch = 16)

##  B
fit.salary1 <- lm(income ~ experience + education, data = salary)
summary(fit.salary1)

### 2 Dummy variablen für education, da es 3 Stufen gibt

##  C

### Y = beta0 + beta1 * experience + beta2 * education2 + beta3 * education3 + epsilon

##  D
plot(salary$experience, salary$income, xlab = "Experience", ylab = "Income", pch = 16, col = as.numeric(salary$education))
abline(a = coef(fit.salary1)[1], b = coef(fit.salary1)[2], col = "blue") # education = 1
abline(a = coef(fit.salary1)[1] + coef(fit.salary1)[3], b = coef(fit.salary1)[2], col = "orange") # education = 2
abline(a = coef(fit.salary1)[1] + coef(fit.salary1)[4], b = coef(fit.salary1)[2], col = "green") # education = 3
legend("topleft", legend = levels(salary$education), col = 1:nlevels(salary$education), pch = 16)
legend("bottomright", legend = c("education = 1", "education = 2", "education = 3"), col = c("blue", "orange", "green"), lty = 1)

##  E
summary(fit.salary1)

### Die eduction.Q, also education = 2, hat keinen signifikanten Einfluss auf das Einkommen, während education = 3 einen signifikanten Einfluss hat.
### Die güte des Models ist mit einem R^2 von 0.82 ziemlich gut.

## F
x0 <- data.frame(experience = 20, education = factor(1, levels = 1:3, ordered = TRUE))
x1 <- data.frame(experience = 20, education = factor(3, levels = 1:3, ordered = TRUE))

y0 <- predict(fit.salary1, newdata = x0, interval = "confidence", level = 0.95)
y1 <- predict(fit.salary1, newdata = x1, interval = "confidence", level = 0.95)
y0
y1

###  Für education = 1, experience = 20, liegt das geschätzte Einkommen bei etwa 50.000 mit einem 95% Konfidenzintervall von [54.286, 69.132].
### Für education = 3, experience = 20, liegt das geschätzte Einkommen bei etwa 70.000 mit einem 95% Konfidenzintervall von [83.000, 97.830].
### Heisst also education ist signifikant, da die Intervalle sich nicht überlappen.

#  Aufgabe 3
diamant <- read.table("semester-6/stat-mo/data/diamant.dat", header = TRUE)
diamant

##  A
diamant$LogPrice <- log(diamant$Price)
diamant$LogCarat <- log(diamant$Carat)
fit.diamant <- lm(LogPrice ~ poly(LogCarat, degree = 2), data = diamant)
summary(fit.diamant)

## B
fit <- lm(LogPrice ~ poly(LogCarat, degree = 2) + Colour + CBody, data = diamant)
summary(fit)

### 7 Parameter kommen hinzu, da es 6 Stufen für Colour und 3 Stufen für CBody gibt, aber jeweils eine Stufe als Referenz genommen wird.

## C
summary(fit)

### Ja alle neuen Variablen sind signifikant, da alle p-Werte kleiner als 0.05 sind.


## D
summary(fit.diamant)$r.squared
summary(fit)$r.squared

### Ja das Modell wird um etwa 0.02 (2%) besser

## E
