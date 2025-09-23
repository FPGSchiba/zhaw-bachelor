# Aufgabe 1

## A
data <- rexp(1000, 2/5)
war <- data >= 2 & data <= 10
sum(war) / length(war)

hist(rexp(1000, 2/5))

## B
- exp(-4) + exp(-0.8) 

## C
pexp(10, 2/5) - pexp(2, 2/5)

## D
func <- function(x) {
  dexp(x, 2/5)
}
integrate(func, lower = 2, upper = 10)
