# ---- Theorie ----

# Sample & seed
set.seed(123)
sample(x=1:6, size=5, replace=TRUE)

# Manipulierte Würfel

p <- c(1,2,2,2,2,3) / 12
sum(p)

sample(x=1:6, size=5, replace = T, prob = p)

# Finden
nwurf <- 10000000 # Macht wahrscheindlichkeit genauer
w <- sample(x=1:6, size=nwurf, replace = T, prob = p)
sum(w == 6) / nwurf # Selektion -> 6 zählt als 1, dann summe

# For Simulationen
nsim <- 50000
w <- matrix(NA, nrow = nsim, ncol = 2)
set.seed(123)
for (i in 1:nsim) {
  w[i,] <- sample(1:6, size = 2, replace = T)
}

w_tf <- w == 6
anz_6 <- rowSums(w_tf)
sum(anz_6 >= 1) / nsim

# --- Aufgabe 1 ----
# A
data <- sample(1:6, size=1000, replace = T)
barplot(table(data))

# B
p <- c(1,1,1,1,1,10) / sum(c(1,1,1,1,1,10))
sum(p)
sample(1:6, size=10, replace = T, prob = p)

# C
nwurf <- 50000
fair <- sample(1:6, size=nwurf, replace=T)
unfair <- sample(1:6, size=nwurf, replace = T, prob = p)

sum(fair == 6) / nwurf
sum(unfair == 6) / nwurf

# D
nsim <- 100000
nwurf <- 10
data <- sample(1:6, size=nwurf, replace=T)
m <- matrix(NA, nrow = nsim, ncol = nwurf)

for (i in 1:nsim) {
  m[i,] <- sample(1:6, size=nwurf, replace=T)
}

m_tf <- rowSums(m==6)
sum(m_tf >= 7) / nsim

# --- Theorie ----



zuege<-expand.grid(chauffeur=1:6, zugfahrzeug=1:4, anhaenger=1:8)
zuege
nrow(zuege)


factorial(4)

library(combinat)
perm <- permn(c("B", "I", "R", "N", "E"))
length(perm)

perm <- permn(c("E", "R", "B", "S", "E"))
length(unique(perm))


factorial(23)/factorial(23-3)
sample(1:23,size=3,replace=FALSE)


s<-combn(x= 1:9,m=3,simplify=TRUE)
m<-ncol(s) #AnzahlmöglicheFälle
g <-sum(apply(s,2, function(x)any(x==7 ))) #AnzahlgünstigeFälle
g/m


library(partitions)
t.comb<-compositions(n=20,m= 6)
ncol(t.comb)


# ---- Aufgabe 2 ----
# A
4*3*5*10

# B
factorial(26)/factorial(22)

combn(x=0:9,m=6,simplify=TRUE)

# C
2 / factorial(5)
1/60

# D
3^13

# E
factorial(18) / factorial(15)


# F
length(c("M","I","S","S","I","S","S","I","P","P","I"))
perm <- permn(c("M","I","S","S","I","S","S","I","P","P","I"))
perm
length(unique(perm))

factorial(11)/(factorial(4)*factorial(4)*factorial(2))
