library("boot")
library("car")
library("MASS")
library("moonboot")
library("Sleuth3")

# Aufgabe 1
data("ex0125")

groupA <- ex0125[ex0125$Group == "A", ]
groupB <- ex0125[ex0125$Group == "B", ]
qqPlot(groupA$Zinc)
qqPlot(groupB$Zinc)

wilcox.test(
  x = groupA$Zinc,
  y = groupB$Zinc,
  alternative = "two.sided",
  distribution = "exact"
)

# Aufgabe 2
set.seed(20250115)
x <- rbeta(n = 30, shape1 = 1 / 3, shape2 = 1 / 3)
negLogLikelyhood <- function(theta, x) {
  -sum(log(dbeta(x, shape1 = theta, shape2 = theta)))
}

optim(
  par = c(0.219),
  fn = negLogLikelyhood,
  method = "BFGS",
  x = x
)

# Aufgabe 3
dat <- SP500[999:1498]
shorth(dat)

estimator <- function(data, ind) shorth(data[ind])
boot.erg <- boot(data = dat, statistic = estimator, R = 5000)
boot.ci(boot.erg, conf = 0.99, type = c("bca"))

# Aufgabe 4
mse <- function(x, sigma) {
  mean(sum((x - sigma)^2))
}
for (n in c(5, 10, 100)) {
  dat_iqr <- mean(replicate(10000, IQR(rnorm(n)) * 1 / 1.349))
  dat_mad <- mean(replicate(10000, mad(rnorm(n))))
  var_iqr <- var(replicate(10000, IQR(rnorm(n)) * 1 / 1.349))
  var_mad <- var(replicate(10000, mad(rnorm(n))))
  dat_mse_iqr <- mean(replicate(10000, mse(IQR(rnorm(n)) * 1 / 1.349, 1)))
  dat_mse_mad <- mean(replicate(10000, mse(mad(rnorm(n)), 1)))
  print("== Werte ==")
  print(dat_iqr)
  print(dat_mad)
  print("== Var ==")
  print(var_iqr)
  print(var_mad)
  print("== MSE ==")
  print(dat_mse_iqr)
  print(dat_mse_mad)
}

#  Aufgabe 5
dbinom(11, size = 77, prob = 0.143)
dbinom(11, size = 77, prob = 0.2)
binom.test(
  x = 22,
  n = 77,
  p = 0.2,
  alternative = "two.sided",
  conf.level = 0.95
)
