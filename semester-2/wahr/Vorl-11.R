# ---- Aufgabe 1 ----
u <- runif(100000, 0, 1)

g <- function(u){u^2}

x <- g(u)
x

hist(x, freq = FALSE)
f_x <- seq(0,1,0.01)
f <- function(x){1/(2*sqrt(x))}
lines(f_x, f(f_x))


# ---- Aufgabe 3 ----
pnorm(250, mean = 100*2.4, sd=sqrt(100*4))

      