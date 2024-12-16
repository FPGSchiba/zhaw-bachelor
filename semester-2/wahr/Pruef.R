# ---- Aufgabe 1 ----

# B
1 - (0.6*0.2*0.99+0.6*0.8*0.91+0.4*0.97)


# C
0.6*0.8+0.4

# E
(0.6*0.2*0.01+0.6*0.8*0.09)/(1 - (0.6*0.2*0.99+0.6*0.8*0.91+0.4*0.97))

# ---- Aufgabe 2 ---- 

# A
nsim <- 10000

sports <- rbinom(nsim, 100, prob=0.25)
non_sports <- 100 - sports

guests <- rbinom(nsim, sports, prob = 0.8)
guests <- guests + rbinom(nsim, non_sports, prob = 0.3)

guests

sum(guests > 50) / nsim

# B
nsim <- 10000
songs <- c(rep("ballade", 35), rep("rock", 60))
result <- c()

for (i in 1:nsim) {
  chosen_songs <- sample(songs, size=30, replace = FALSE)
  num_ballads <- sum(chosen_songs == "ballade")
  num_rock <- 30 - num_ballads
  
  ballad_length <- sum(rnorm(num_ballads, mean=4.2, sd=1.3))
  rock_length <- sum(rnorm(num_rock, mean=3.5, sd=0.8))
  result[i] <- ballad_length + rock_length
}

quantile(result, 0.95)


# ---- Aufgabe 3 ----
# A
dpois(6, lambda=4)
1 - ppois(50, lambda=40)

# B
pnorm(501, mean=500, sd=10) - pnorm(499, mean=500, sd=10)

# C
mu <- c(30, 50)
sd <- matrix(data = c(10, sqrt(0.6*10*20), sqrt(0.6*10*20), 20), nrow = 2, ncol=2)
library(mvtnorm)

pmvnorm(c(40, 60), mean = mu, sigma = sd)

# ---- Aufgabe 4 ----

f <- function(x) 1 - exp((-1/2)*x^2)
df <- Deriv(f, "x")
df


# C
KumF <- function(x) sqrt(log(1/(1-x)^2))
test <- runif(10000)
x <- KumF(test)
quantile(x, 0.2)


# ---- Aufgabe 5 ----
# B
0.2*0.9

# C
choose(7, 4)

# D
x <- seq(-40, 40, 0.1)
plot(x, dnorm(x, mean=10
              , sd=5), type = 'l')

# E
punif(55, min=20, max=70) - punif(37, min=20, max=70)


