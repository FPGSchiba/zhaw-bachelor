# ---- Aufgabe 1 ----
# E(X) = (a + b)/2 -> 0
# Var(X) (a + b)^2/12 -> 1/12

# S_225 ~ N(0, 225/12)
# P(S_225 <= 5) - P(S_255 < - 5)

pnorm(5, mean = 0, sd = sqrt(225/12)) - pnorm(-5, mean=0,  sd=sqrt(225/12))

# ---- Aufgabe 2 ----

# S_69 ~ N(69*14, 69*9^2)
# P(S_96 > 1000)

1 - pnorm(1000, mean = 69*14, sd = sqrt(69*9))


# --- Quizz ----

# 2
hist(messdaten)
hist(log(messdaten))

# 3
# S_35 ~ N(5*223 + 30*119, 35*35)

5*223 + 30*119
35*35

# 4
6.17*exp(-6.17*0.18)


# 6
nsim <- 100000
gewinn <- c()
n_baum <- 118

for (i in 1:nsim) {
  umfang <- rnorm(n_baum, mean = 1.72, sd = 0.33)
  gewinn[i] <- 0
  for (umf in umfang) {
    if (umf < 0) {
      umf <- 0
    }
    
    if (1.4 < umf && umf < 2.6) {
      gewinn[i] <- gewinn[i]
    } else if (umf <= 1.4) {
      gewinn[i] <- gewinn[i] + 32
    } else if (umf >= 2.6) {
      gewinn[i] <- gewinn[i] - 32
    }
  }
}

mean(gewinn)

# 7
nsim <- 100000

time <- c()

for (i in 1:nsim) {
  kabelbaum_zeit <- rnorm(1, mean = 32, sd = sqrt(3))
  anz_orte <- rgeom(1, 0.57)
  such_zeit <- sum(runif(anz_orte, min = 7, max= 19))
  scheinwerfer_zeit <- rexp(1, 1/35.4)
  time[i] <- 19 + kabelbaum_zeit + such_zeit + scheinwerfer_zeit
}

quantile(time, 0.15)


# 8

u <- runif(100000)
g <- function(x,lambda,beta){((-log(1-x))^(beta/3))/(3*lambda)}
x <- g(u,lambda=1.2,beta=3.7)
mean(x)

# 9

log(140.56 + 1)


# 11
1 - pexp(4, rate = 1/5.5)

# 12
pgamma(14, shape=3, rate=1/4)

# 13
1 - plnorm(14, meanlog=2.06, sdlog=sqrt(0.17))

# 14
pnorm(6.3, mean=5.8, sd=0.9) - pnorm(4.7, mean=5.8, sd=0.9)

# 15
punif(15, min=0, max=20) - punif(5, min=0, max=20)

# 16
pweibull(3, shape=0.328, scale=3.1)

# 17
70*0.4^2
70*8.1


