# install.packages("fitdistrplus", dependencies = TRUE)
set.seed(801)
x.gamma <- rgamma(20, shape = 3, rate = 1 / 9)

library(fitdistrplus)
x.gamma.mle <- fitdist(
  data = x.gamma, # x = Daten von Folie 13
  distr = "gamma",
  method = "mle"
)

c(x.gamma.mle$estimate[1], x.gamma.mle$estimate[2])
