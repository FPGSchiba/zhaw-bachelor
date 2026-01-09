# QQPlot
x <- rnorm(n = 100, mean = 1, sd = 2)
# distribution = "norm" for normal distribution
# mean and sd specify the parameters of the normal distribution
#  any other distribution can be used as well
library(car)
qqPlot(x = x, distribution = "norm", mean = 0, sd = 1)

# Cullen and Frey Graph
x <- rgamma(100, shape = 1.3, scale = 1) # Daten simulieren
# install.packages(pkgs = "fitdist")
library(fitdistrplus)
descdist(x) # Befehl für Cullen-Frey Graph

# Log Likelihood
set.seed(801)
x.gamma <- rgamma(20, shape = 3, rate = 1 / 9)

negLogLik <- function(par, x) {
  -sum(dgamma(x = x, shape = par[1], rate = par[2], log = TRUE))
}
# Startwerte für die Optimierung
start <- c(mean(x.gamma)^2 / var(x.gamma), mean(x.gamma) / var(x.gamma))
# Optimierung
result <- optim(par = start, fn = negLogLik, method = "BFGS", x = x.gamma) # Maximierung der Log-Likelihood
result$par # Geschätzte Parameter

# Konfidenzintervalle
# Manuell (z-test)
alpha <- 0.01 # Für Conf-Level: 0.99
z <- qnorm(1 - alpha / 2) # z := Quantil wert in formel geschrieben als z_{1-\frac{\alpha}{2}}
mean + c(-1, 1) * sd / sqrt(n) * z # Schlussendliches Intervall
# mean, sd und n müssen bekannt sein

# Manuell (t-test)
alpha <- 0.01 # Für conf-level: 0.99
t <- qt(1 - alpha / 2, df = n - 1)
mean + c(-1, 1) * sd / sqrt(n) * t # Schlussendliches Intervall
# mean, sd und n müssen bekannt sein

# Z-Test
library(BSDA)
x <- rnorm(20, mean = 0.5, sd = 1)
z.test(
  x = x, # Stichprobe
  sigma.x = 1, # bekannte Standardabweichung
  alternative = "two.sided", # Muss für Konfidenzintervall so gesetzt werden
  conf.level = 0.95 # Konfidenzniveau
)$conf.int # Ausgabe des Konfidenzintervalls
# Dieser test kann auch bei einer grossen Stichprobe verwendet werden, wenn die Stichprobe genügend gross ist (z.B. n > 30).
# Dafür sigma.x = sd(x) setzen.

# t-Test für Konfidenzintervall
library(BSDA)
x <- rnorm(20, mean = 0.5, sd = 1)
t.test(
  x = x, # Stichprobe
  alternative = "two.sided", # Muss für Konfidenzintervall so gesetzt werden
  conf.level = 0.95 # Konfidenzniveau
)$conf.int # Ausgabe des Konfidenzintervalls

# Binomialtest für Konfidenzintervall
library(BSDA)
binom.test(
  x = 28, # Anzahl Erfolge
  n = 1026, # Stichprobenumfang
  conf.level = 0.95 # Konfidenzniveau
)$conf.int # Ausgabe des Konfidenzintervalls

# Poissontest für Konfidenzintervall
library(BSDA)
poisson.test(
  x = 27, # Anzahl Ereignisse
  T = 3, # Beobachtungszeitraum
  conf.level = 0.95 # Konfidenzniveau
)$conf.int # Ausgabe des Konfidenzintervalls

# Bootstrap-Konfidenzintervall

# Von hand geschriebene Funktion
(xn <- rnorm(5)) # vorhandene Daten
B <- 500
Ti <- rep(NA, B)
alpha <- 0.95
for (i in 1:B) {
  # Schritt 1: Bootstrap-Stichprobe
  xbi <- sample(xn, size = length(xn), replace = TRUE)
  # Schritt 2: Berechnung der Statistik T: Hier als Beispiel das arth. Mittel
  Ti[i] <- mean(xbi)
}
# 95% Bootstrap Konfidenzintervall
quantile(x = Ti, probs = c((1 - alpha) / 2, 1 - (1 - alpha) / 2))

# Mit Library boot
library(boot)
set.seed(2017)
estimator <- function(data, ind) 1 / mean(data[ind])
boot.erg <- boot(data = x, statistic = estimator, R = 500)
boot.erg$t0 # Original Schätzung
head(boot.erg$t) # Bootstap-Schätzungen
boot.ci(boot.erg, conf = 0.95, type = c("perc", "bca"))

# Tests

# Binomialtest
binom.test(
  x = 26, # Anzahl Erfolge
  n = 112, # Stichprobenumfang
  p = 0.33, # Hypothesenwert
  alternative = "less", # "less", "greater", "two.sided" für einseitig oder zweiseitig
  conf.level = 0.95 # Konfidenzniveau
)

# Poissontest
poisson.test(
  x = c(34, 42), # Anzahl Ereignisse in beiden Gruppen
  r = 1, # Beobachtungszeitraum beider Gruppen (hier gleich lang)
  alternative = "less" # "less", "greater", "two.sided" für einseitig oder zweiseitig
)

# z-Test
library(BSDA)
x <- c(1.23, 1.24, 1.22, 1.2, 1, 3, 1.5, 1.3, 1.4, 1.25)
z.test(
  x = x, # Stichprobe
  sigma.x = 0.003, # bekannte Standardabweichung
  mu = 0.3, # Hypothesenwert
  conf.level = 0.95, # Konfidenzniveau
  alternative = "greater" # "less", "greater", "two.sided" für einseitig oder zweiseitig
) #  Ausgabe des Testergebnisses

# t-Test
library(BSDA) # Evtl nötig
out <- t.test(
  x, # Stichprobe
  alternative = "greater", # "less", "greater", "two.sided" für einseitig oder zweiseitig
  mu = 0, # Parameter der H0
  conf.level = 0.95 # Konfidenzniveau
) # 1-alpha
out$p.value # Ergibt den p-wert
out$conf.int # Ergibt das Konfidenzintervall

# Gepaarter t-Test
library(BSDA)
t.test(
  x = bs$Linux, # erste Messung
  y = bs$Windows, # zweite Messung
  paired = TRUE, # gepaarter Test
  alternative = "two.sided" #  "less", "greater", "two.sided" für einseitig oder zweiseitig
) # Ausgabe des Testergebnisses
# Oder
t.test(
  x = bs$Differenz, # Differenzen berechnen und als eine Stichprobe behandeln
  mu = 0, # Parameter der H0
  alternative = "two.sided" #  "less", "greater", "two.sided" für einseitig oder zweiseitig
) # Ausgabe des Testergebnisses

# Ungepaarter t-Test
library(Sleuth3)
data(case0101)
t.test(
  formula = Score ~ Treatment, # Formel für zwei Gruppen
  data = case0101, # Datensatz
  var.equal = TRUE, # Varianzhomogenität annehmen
  mu = 0, # Parameter der H0
  alternative = "two.sided" #  "less", "greater", "two.sided" für einseitig oder zweiseitig
) # Ausgabe des Testergebnisses

# Multipler t-Test mit ANOVA
pairwise.t.test(
  x = pulp$bright, # Werte
  g = pulp$operator, # Gruppe
  p.adjust.method = "bonf", # Abhängigkeit einrechnen
  pool.sd = FALSE # Automatische optimierung ausstellen
) # Ausgabe des Testergebnisses

# Monte-Carlo t-Test
# install.packages("coin")
library(coin)
independence_test(
  formula = Rainfall ~ Treatment, # Formel für zwei Gruppen
  data = case0301, # Datensatz
  distribution = "exact", # Exakte Verteilung verwenden
  alternative = c("two.sided") #  "less", "greater", "two.sided" für einseitig oder zweiseitig
) # Ausgabe des Testergebnisses

# Wilcoxon-Rangsummen-Test
x <- c(49.3, 48.7, 48.1, 48.6, 48.2)
y <- c(47.2, 47.9, 47.5, 50.9, 48.0)
(dat <- data.frame(
  time = c(x, y),
  g = factor(x = c(rep("MI", length(x)), rep("MII", length(y))))
))

wilcox_test(
  formula = time ~ g, # Formel für zwei Gruppen
  data = dat, # Datensatz
  alternative = "greater", #  "less", "greater", "two.sided" für einseitig oder zweiseitig
  distribution = "exact" # Exakte Verteilung verwenden
) # Ausgabe des Testergebnisses

#  Wilcoxon-Vorzeichen-Rangsummentest
library(MASS)
data(shoes)
wilcoxsign_test(
  shoes$A ~ shoes$B, # Formel für zwei Gruppen
  alternative = "less", #  "less", "greater", "two.sided" für einseitig oder zweiseitig
  distribution = "exact" # Exakte Verteilung verwenden
) # Ausgabe des Testergebnisses

# Alternativ mit long format
dat <- data.frame(
  wear = c(shoes$A, shoes$B),
  material = factor(rep(c("A", "B"), each = 10)),
  person = factor(rep(1:10, 2))
)

wilcoxsign_test(
  formula = wear ~ material | person, # Formel für gepaarte Daten
  data = dat, # Datensatz
  alternative = "less", #  "less", "greater", "two.sided" für einseitig oder zweiseitig
  distribution = "exact" # Exakte Verteilung verwenden
)

# Chi-Quadrat-Test
library(MASS)
data(UCBAdmissions)
# Kontingenztabelle erstellen
tbl <- margin.table(UCBAdmissions, c(1, 2))
chisq.test(
  x = tbl, # Kontingenztabelle
) # Ausgabe des Testergebnisses

# Konstruktion einer Tabelle mit daten
tab <- rbind(
  c(95, 300, 160, 250, 320), #  Erste spalte
  c(75, 200, 100, 230, 270) # Zweite spalte
)
