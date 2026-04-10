# Aufgabe 1
diamant <- read.table("semester-6/stat-mo/data/diamant.dat", header = TRUE)
head(diamant)

fit.model1 <- lm(Price ~ Carat + I(Carat^2), data = diamant)
fit.model2 <- lm(I(log(Price)) ~ I(log(Carat)) + I(log(Carat)^2), data = diamant)

summary(fit.model1)

## A
plot(diamant$Carat, diamant$Price, main = "Preis vs. Karat", xlab = "Karat", ylab = "Preis")
lines(sort(diamant$Carat), predict(fit.model1)[order(diamant$Carat)], col = "blue", lwd = 2)
lines(sort(diamant$Carat), exp(predict(fit.model2))[order(diamant$Carat)], col = "red", lwd = 2)
legend("topleft", legend = c("Modell 1", "Modell 2"), col = c("blue", "red"), lwd = 2)

### Den Preis zu logarithmieren, um die Beziehung zwischen Preis und Karat zu linearisieren. Macht es einfacher, die Beziehung zu modellieren und zu interpretieren.

##  B
predict(fit.model1, newdata = data.frame(Carat = c(0.22, 1.07)), interval = "prediction")

### Der lower bound für das 95%-Konfidenzintervall ist negativ, was keinen Sinn ergibt.

##  C
h <- predict(fit.model2, newdata = data.frame(Carat = c(0.22, 1.07)), interval = "prediction")
exp(h + summary(fit.model2)$sigma^2 / 2)

### Hier sehen alle bounds realistisch aus, da alle positiv sind und nicht zu weit von den vorhergesagten Preisen entfernt sind.

## D
par(mfrow = c(2, 2))
termplot(fit.model1, partial.resid = TRUE, smooth = panel.smooth, col.res = "black", col.term = "blue", col.smth = "red")

### Es gibt eine Systematische abweichung der Residuen in beiden Variablen:
### - Bei höherem karat weichen die Residuen nach unten ab.

termplot(fit.model2, partial.resid = TRUE, smooth = panel.smooth, col.res = "black", col.term = "blue", col.smth = "red")

### Ich kann keine systematische Abweichung erkennen, was auf die Qualität des Modells hindeutet.

## E
exp(fitted(fit.model2) + summary(fit.model2)$sigma^2 / 2)

## F
drop1(fit.model2, test = "F")

### Ja der quadratische Term ist signifikant, da der p-Wert kleiner als 0.05 ist. Das bedeutet, dass die Beziehung zwischen log(Preis) und log(Karat) nicht nur linear, sondern auch quadratisch ist.

## g
fit.model2.modified <- lm(I(log(Price)) ~ I(log(Carat)), data = diamant)
summary(fit.model2.modified)
par(mfrow = c(1, 1))
plot(diamant$Carat, diamant$Price, main = "Preis vs. Karat", xlab = "Karat", ylab = "Preis")
lines(sort(diamant$Carat), exp(predict(fit.model2))[order(diamant$Carat)], col = "blue", lwd = 2)
lines(sort(diamant$Carat), exp(predict(fit.model2.modified))[order(diamant$Carat)], col = "red", lwd = 2)
legend("topleft", legend = c("Modell 2", "Modell 2 modified"), col = c("blue", "red"), lwd = 2)

## h
h <- predict(fit.model2, newdata = data.frame(Carat = c(0.22, 1.07)), interval = "prediction")
points(c(0.22, 1.07), exp(h[, "fit"]), col = "blue", pch = 16)

### 0.22 ist sehr gut geschätzt, aber 1.07 ist höher geschätzt als in den Daten vorhanden.
### Evtl. ist das quadratische Modell schlechter geeignet, als das rein Log-Log Modell.

## i
h <- predict(fit.model2, newdata = data.frame(Carat = 0.4), interval = "prediction")
exp(h + summary(fit.model2)$sigma^2 / 2)

h <- predict(fit.model2, newdata = data.frame(Carat = 0.4), interval = "confidence")
exp(h + summary(fit.model2)$sigma^2 / 2)

### Er sollte das Prognoseinterval brauchen, da das Konfidenzintervall nur aussagt, dass 95 von 100 solcher Diamanten einen Mittelwert in diesem Intervall haben.

# Aufgabe 2

mpi <- read.table("semester-6/stat-mo/data/MPIZH.dat", header = TRUE)
head(mpi)

## A
fit.mpi <- lm(MPI ~ KPI + HZ, data = mpi)
summary(fit.mpi)

### Das R^2 von 0.93 zeigt, dass das Modell einen sehr grossen Teil der Varianz in MPI erklärt.

## B
par(mfrow = c(1, 2))
termplot(fit.mpi, partial.resid = TRUE, smooth = panel.smooth, col.res = "black", col.term = "blue", col.smth = "red")

### Der KPI sieht nicht ganz linear aus, aber nur eine kleine (ich nehme an) polynomielle (5ten Grades) Anpassung könnte das Problem lösen. HZ sieht sehr linear aus.
