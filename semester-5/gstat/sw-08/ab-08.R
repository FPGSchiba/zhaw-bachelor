# Aufgabe 2

##  A
alpha <- 0.1

## B
# X ~ Bin(n=20, p=0.5)

## C
# H_1: T > v_grenze

## D
T <- rbinom(1, size = 20, prob = 0.5)
p_hat <- T / 20

## E
hist(rbinom(1000, size = 20, prob = p_hat))

## F
v_grenze <- qbinom(p = 0.05, size = 20, prob = 0.5)
v_grenze

## G
if (T > v_grenze) {
  print("H_0 wird verworfen")
} else {
  print("H_0 wird beibehalten")
}

## H
p_value <- 1 - pbinom(15, size = 20, prob = p_hat)
p_value
p_value < alpha

## I
binom.test(15, n = 20, p = 0.5, alternative = "greater")
