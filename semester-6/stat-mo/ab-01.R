# Aufgabe 1
## B
beta_hat <- 138.8
alpha_hat <- -1197682.1

y_hat_1 <- alpha_hat + beta_hat * 20100
y_hat_2 <- alpha_hat + beta_hat * 24000
y_hat_1
y_hat_2

##  C
load("semester-6/stat-mo/data/flughafen.rda")
zrh
fit <- lm(Pax ~ ATM, data = zrh)
coef(fit)

# Aufgabe 2
uhren <- read.table("semester-6/stat-mo/data/AntikeUhren.dat", header = TRUE)

## A
plot(uhren$Alter, uhren$Preis, xlab = "Alter (Jahre)", ylab = "Preis (Euro)", main = "Preis von antiken Uhren in Abhängigkeit vom Alter")

##  B
fit <- lm(Preis ~ Alter, data = uhren)
coef(fit)

## D
resid(fit)
summary(fit)$sigma

# E
plot(uhren$Alter, uhren$Preis, xlab = "Alter (Jahre)", ylab = "Preis (Euro)", main = "Preis von antiken Uhren in Abhängigkeit vom Alter")
abline(fit, col = "red")
