# Aufgabe 1
## A


## B

# Aufgabe 2
# install.packages(pkgs = "car", dependencies = TRUE)

## A
kunden <- read.csv(file = "semester-5/gstat/sw-02/kunden.csv")
quantile(kunden$x, probs = c(0.05, 0.25, 0.5, 0.7, 0.9, 0.975), na.rm = FALSE)

## B
library(car)
qqPlot(x = kunden$x)
qqPlot(x = kunden$x, distribution = "exp")

# eher exponentiell verteilt

## C
qqPlot(x = kunden$x, distribution = "exp", rate = 0.65, main = "lambda = 0.65")
qqPlot(x = kunden$x, distribution = "exp", rate = 0.5, main = "lambda = 0.5")

# Für lambda = 0.5 hat die Gerade eine steigung näher an 1

# Aufgabe 3
# ?

# Aufgabe 4
t_1 <- c()
t_2 <- c()
t_3 <- c()
t_6 <- c()

t_6_func <- function(x) {
  return(1/length(x) * sum((x - mean(x))^2))
}

for (i in 1:10000) {
  t_1[i] <- mean(rnorm(20, mean = 2, sd = 3))
  t_2[i] <- rnorm(20, mean = 2, sd = 3)[1]
  t_3[i] <- min(rnorm(20, mean = 2, sd = 3))
  t_6[i] <- t_6_func(rnorm(20, mean = 2, sd = 3))
}
par(mfrow = c(2, 2)) # 2x2 layout
hist(t_1, breaks = 50)
hist(t_2, breaks = 50)
hist(t_3, breaks = 50)
hist(t_6, breaks = 50)

# Oder anders
statistics <- function(x) {
  return(c(T1 = mean(x), T2 = x[1], T3 = min(x), T6 = var(x)))
}
results <- replicate(10000, statistics(rnorm(20, mean = 2, sd = 3)))
par(mfrow = c(2, 2)) # 2x2 layout
hist(results["T1", ], breaks = 50, main = "T1: Mean")
hist(results["T2", ], breaks = 50, main = "T2: Variance")
hist(results["T3", ], breaks = 50, main = "T3: Min")
hist(results["T6", ], breaks = 50, main = "T6: Max")