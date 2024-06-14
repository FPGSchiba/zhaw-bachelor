library(mvtnorm)
mu<-c(2,0) 
sigma <-matrix(c(1,0.5,0.5,1),nrow=2)

x1 <- seq(-4,4,0.1)
x2 <- seq(-4,4,0.1)
z <- expand.grid(x1=x1,x2=x2)
f <- dmvnorm(z, mean = mu, sigma = sigma)
fz <- matrix(f, nrow = length(x1), ncol = length(x2))
# Variante 1: 2D Bild (Kontur)
image(x1,x2,fz, las=1)
contour(x1,x2,fz, add=TRUE)
# Variante 2: 3D Bild
persp(x1,x2,fz, theta =-15, phi = 30)


pmvnorm(lower=c(-Inf,-Inf), upper=c(0,0), mean = mu, sigma = sigma)

# ---- Aufgabe 1 ----
mu <- c(7, 15)
sigma <- matrix(c(25^2, 25*(-0.4)*45,25*(-0.4)*45, 45^2), nrow=2)
# A
# E[Z] = E[0.7*X + 0.3*Y] = E[X]*0.7 + E[Y]*0.3 = 9.4
7*0.7 + 15*0.3

# B
# Var(Z) = Var(0.7*X + 0.3*Y) = 0.7^2*Var(X) + 0.3^2*Var(Y) + 2*0.7*0.3*Cov(X,Y) = 299.5
# Cov(X,Y) = Cor(X,Y)*sqrt(Var(X)*Var(Y))
# sqrt(Var(Z)) = 17.3
sqrt(0.7^2*25^2 + 0.3^2*45^2 + 2*0.7*0.3*(-0.4)*sqrt(25^2*45^2))

# C
x1 <- seq(-80,100,0.5)
x2 <- seq(-90,120,0.5)
z <- expand.grid(x1=x1,x2=x2)
f <- dmvnorm(z, mean = mu, sigma = sigma)
fz <- matrix(f, nrow = length(x1), ncol = length(x2))
# Variante 1: 2D Bild (Kontur)
image(x1,x2,fz, las=1)
contour(x1,x2,fz, add=TRUE)

# D
pmvnorm(lower=c(-Inf,-Inf), upper=c(0,0), mean = mu, sigma = sigma)[[1]] # 0.08595452

# E
# Bedingt: P(Y < 0 | X < 0) => P(X < 0 & Y < 0) / P(X <0)
pmvnorm(lower=c(-Inf,-Inf), upper=c(0,Inf), mean = mu, sigma = sigma)[[1]] # 0.3897388


factorial(50)

qgeom(0.5, 1/365)



