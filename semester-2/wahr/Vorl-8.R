# ---- Aufgabe 1 ----
# B
f <- function(x) {
  c <- 6
  if (1 >= x & x >= 0) {
    return(c*x - c*x^2)
  } else {
    return(0)
  }
}

f_better <- function(x) {
  c <- 6
  ifelse(1 >= x & x >= 0, c*x - c*x^2, 0)
}

x <- seq(-1, 2, by=0.01)

plot(x, lapply(x, FUN=f), type='l')
plot(x, f_better(x), type='l')

# ---- Aufgabe 2 ---- 
# A
# X ~ Unif([0.24,0.26])
a <- 0.24
b <- 0.26

# B
# P(X < 0.245)
punif(0.245, min=a, max=b)

# C
# P(X > 0.253)
1 - punif(0.253, min=a, max=b)

# D
(a+b)/2
nsim <- 100000
mean(runif(nsim, min=a, max=b))
