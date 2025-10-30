# Aufgabe 1

## A
ph <- 35 / 487
ph + c(-1, 1) * qnorm(p = 0.99) * sqrt(ph * (1 - ph) / 487)

# 99% Konfidenzintervall für den Anteil: [2.3%, 6.7%]

## B
ph <- 2 / 44
ph + c(-1, 1) * qnorm(p = 0.90) * sqrt(ph * (1 - ph) / 44)

# 90% Konfidenzintervall für den Anteil: [0.5%, 8.5%]

# Aufgabe 2
library(BSDA)

## A
poisson.test(x = 62, T = 12, conf.level = 0.95)$conf.int

# 95% Konfidenzintervall für die Rate: [3.96, 6.62] pro Monat

## B
load("semester-5/gstat/sw-07/asbestos.RData")

asbestos_rate <- length(asbestos) / sum(asbestos)
mean(asbestos) + c(-1, 1) * (qnorm(0.995) * sqrt(mean(asbestos) / length(asbestos))) # nolint
poisson.test(x = sum(asbestos), T = length(asbestos), conf.level = 0.99)$conf.int # nolint

# 99% Konfidenzintervall für die mittlere Asbestbelastung: [23.2, 26.2] Fasern/Stück # nolint
