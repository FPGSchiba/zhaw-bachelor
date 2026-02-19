data <- c(6, 5, 4, 3, 4, 3, 2, 1, 2, 3)

z <- (data - mean(data)) / sd(data)
z

N <- 5
n <- length(data)
n / N

(z[1] + z[2]) / (n / N)
(z[3] + z[4]) / (n / N)
(z[5] + z[6]) / (n / N)
(z[7] + z[8]) / (n / N)
(z[9] + z[10]) / (n / N)
