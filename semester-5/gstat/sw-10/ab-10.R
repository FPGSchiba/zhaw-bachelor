# Aufgabe 2

## A
# Eine ungepaarte Stichprobe

## B
alpha <- 0.05
load("semester-5/gstat/sw-10/blutdruck.RData")
t.test(x = blutdruck$x, mu = 0, alternative = "greater", conf.level = 1 - alpha) # Für richtige Hypothesen Gruppe
# p = 0.052 > alpha -> H0 nicht verwerfen
t.test(x = blutdruck$y, mu = 0, alternative = "greater", conf.level = 1 - alpha) # Für test Gruppe
# p = 0.56 > alpha -> H0 nicht verwerfen

t.test(x = blutdruck$x, y = blutdruck$y, alternative = "greater", paired = FALSE, var.equal = TRUE, conf.level = 1 - alpha)
# p = 0.059 > alpha -> H0 nicht verwerfen

# Aufgabe 3
alpha <- 0.01
load("semester-5/gstat/sw-10/hals.RData")

t.test(x = hals$Before, y = hals$After, alternative = "two.sided", var.equal = TRUE, conf.level = 1 - alpha)
# p = 0076 > alpha -> H0 nicht verwerfen

# Aufgabe 4
