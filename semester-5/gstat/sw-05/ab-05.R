# Aufgabe 1
## A
?rlogis
rlogis(1, location = 0, scale = 1)
## B

## C
?optim
optim(c(0, 1), function(par, x) -sum(dlogis(x, location = par[1], scale = par[2])), x = 50)

# Aufgabe 2

c(
  (1 / 500) * 0.995,
  (1 / 500) * 0.005,
  (499 / 500) * 0.006,
  (499 / 500) * 0.994
)

# Aufgabe 4
x1 <- c(5.08774228592843, 4.68263159130066, 5.10245924334245, 4.97815588066122, 4.91573144670804, 4.94022379251288, 4.67149365210807, 5.08403749479561, 5.15667283221903, 5.12188176748088)
# Plotten Sie die Dichte der A-Priori-Verteilung, die Likelihood und die A-Posteriori-Verteilung für µ unter Verwendung der gegebenen Stichprobe.

## A
n <- length(x1)
mu0 <- 5
sigma0 <- 0.1

xachse <- seq(4.8, 5.2, 0.001)
plot(xachse, dnorm(xachse, mean = mu0, sd = sigma0), type = "l", main = "A-Priori,Likelihood,A-Posteriori", xlab = expression(mu), ylab = "Dichte/Likelihood", ylim = c(0, 10))

xquer <- mean(x1)
sigma <- 0.2

likelihood <- function(mu) prod(dnorm(x1, mean = mu, sd = sigma))
L <- Vectorize(FUN = likelihood, vectorize.args = "mu")

lines(xachse, L(xachse) / 6, col = "red")

mu1 <- ((n / sigma^2) * xquer + (1 / sigma0^2) * mu0) / (n / sigma^2 + 1 / sigma0^2)
sigma1 <- sqrt(1 / (n / sigma^2 + 1 / sigma0^2))
lines(xachse, dnorm(xachse, mean = mu1, sd = sigma1), col = "blue")
abline(v = c(mu0, xquer, mu1), col = c("black", "red", "blue"))
legend("topright", fill = c("black", "red", "blue"), legend = c("A-Priori", "Likelihood", "A-Posteriori"))

## B
# Wo hat die A-Posteriori-Verteilung ihr Maximum? Ist dieser Wert grösser oder kleiner als das Stichprobenmittel? Warum?

# Die A-Posteriori-Verteilung hat ihr Maximum bei etwa 4.95. Dieser Wert ist kleiner als das Stichprobenmittel (5.004). Dies liegt daran, dass die A-Priori-Verteilung (mit Mittelwert 5) die Schätzung nach unten zieht, da sie eine stärkere Gewichtung auf niedrigere Werte legt.

## C
x2 <- c(5.25241969628093, 5.42904043376296, 5.18137613561775, 5.08732299979658, 4.87818940768848, 4.97768870963484, 4.92892245991247, 5.34359733511405, 4.67414779074627, 4.8478412685637)

# Werfen Sie die beiden Stichproben zusammen, und führen Sie die Analyse aus a) erneut durch. Wie verändert sich die A-Posteriori-Verteilung?

x_combined <- c(x1, x2)
curve(dnorm(x, mean = 5, sd = 1), from = 3, to = 7, col = "blue", ylab = "Dichte", xlab = "x", main = "A-Priori, Likelihood und A-Posteriori Verteilung (kombinierte Stichprobe)")
curve(prod(dnorm(x_combined, mean = x, sd = 0.5)) * dnorm(x, mean = 5, sd = 1), from = 3, to = 7, col = "red", add = TRUE)
curve(dnorm(x, mean = (5 / 1 + sum(x_combined) / 0.5^2) / (1 / 1 + length(x_combined) / 0.5^2), sd = sqrt(1 / (1 / 1 + length(x_combined) / 0.5^2))), from = 3, to = 7, col = "green", add = TRUE)
legend("topright", legend = c("A-Priori", "Likelihood", "A-Posteriori"), col = c("blue", "red", "green"), lty = 1)
