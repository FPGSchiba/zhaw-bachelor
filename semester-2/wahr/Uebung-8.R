# ---- Aufgabe 1 ----
# A
# X ~ Exp(0.34)

# B
pexp(1, rate = 0.34)

# C
pexp(5, rate=0.34) - pexp(4, rate=0.34) 

# D
# X ~ G(3, 0.34)
n <- 100000
m3 <- rgamma(n, shape=3, rate=0.34)
hist(tabulate(m3))

# E
x <- seq(1, n, 0.1)
plot(x, dgamma(x, shape=3, rate=0.34), add=TRUE, type='l')



# ---- Aufgabe 2 ----
# A
p_lambda <- c(0.6, 0.4)
choose_Lambda <- c(30, 10)
nsim <- 20000
num_guests <- c()
for (i in 1:nsim) {
  lambda <- sample(choose_Lambda, 1, prob=p_lambda)
  num_guests[i] <- rpois(1, lambda = lambda)
}

mean(num_guests)

# B
