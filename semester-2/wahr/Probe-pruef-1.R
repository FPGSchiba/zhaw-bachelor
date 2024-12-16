# ---- Aufgabe 1 ----
# B
0.56 + 0.44*0.63 + 0.44*0.28*0.75 + 0.44*0.09*0.88

# C
0.56 / (0.56 + 0.44*0.63 + 0.44*0.28*0.75 + 0.44*0.09*0.88)

# ---- Aufgabe 3 ----
# A
phyper(q=2,m=8,n=16,k=4)

# B
qnorm(0.95, mean=6.28, sd=0.12)


# ---- Aufgabe 4 ----
# C

nsim <- 100000
time <- rexp(nsim, rate=1/20) + runif(nsim, min=0, max=9) + rnorm(nsim, mean=15, sd=3)


8-round(quantile(time, 0.95),0)/60

# ---- Aufgabe 6 ----
# A 
nsim <- 100000
x <- runif(nsim, min=-1, max=1)
y <- runif(nsim, min=-1, max=1)

r <- sqrt(x^2 + y^2)
sum(r < 1) / nsim

# B

nsim <- 100000
x <- runif(nsim, min=-1, max=1)
y <- runif(nsim, min=-1, max=1)

r <- sqrt(x^2 + y^2)
hits <- sum(r < 1)
sum(r < 0.1) / hits


# ---- Aufgabe 7 ----
# A
factorial(32)/(factorial(30)*factorial(2))

# B

dpois(seq(1,12), lambda=2.02)
