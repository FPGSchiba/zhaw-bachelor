# ---- Aufgabe 1 ----
# A
pb <- 0.98*0.8*0.3 + 0.98*0.2*0.3 + 0.02*0.1*0.5 + 0.02*0.9*0.5
pa <- 0.98*0.8 + 0.02*0.1
pa

# ---- Aufgabe 2 ----
# E
E <- 0.1+0.2+3*0.2+5*0.2+6*0.4

# F
(1-E)**2*0.1+(2-E)**2*0.1+(3-E)**2*0.2+(5-E)**2*0.2+(6-E)**2*0.4


# ---- Aufgabe 3 ----
E <- -0.2+0.2+2*0.2

(-1-E)**2*0.2+(0-E)**2*0.4+(1-E)**2*0.2+(2-E)**2*0.2

# ---- Quizz 1 ----
# 1
0.5*(10/19) + 0.1*(18/19) + 0.4*(12/19)
# 2
15/85
# 4
ps <- 1/3
0.32*ps/ (0.32*ps+0.09*ps+0.013*ps)

# 6
choose(4*13, 10) * ((1/13)**4)

# 7
factorial(15) / factorial(1) * factorial(1) * factorial(3) * factorial(4)

# 8
choose(6, 4) * choose(6, 4)
choose(6, 4)

# 11
0.52*0.1/(0.13*0.9+0.52*0.1)

# 12
((20/27)*(7/20)) * (20/27) / (((20/27)*(7/20)) * (20/27) + ((7/27)*(3/7)) * (7/27))

# 13
(26+26+10)**6

# 14
factorial(6) / (factorial(1) * factorial(1) * factorial(2) * factorial(2))

# 15
nsim <- 100000
count <- 0
for (i in 1:nsim) {
  temp <- sample(c(1,0), size = 24*26, replace = T, prob = c(0.08, 0.92))
  for (j in 0:25) {
    if (sum(temp[j*24+1:j*24+24], na.rm = T) >= 2) {
      count <- count + 1
      break
    }
  }
}

count / nsim

# 17
(8/25)*(14/25)

# 18
(0.86)**4

# 19
nsim <- 100000
props <- c(0.0325, 0.0325, 0.0325, 0.0325, 0.44, 0.43)
count <- 0
for (i in 1:nsim) {
  silvan_count <- 0
  for (j in 1:3) {
    silvan <- sample(1:6, size=5, replace = T, prob=props)
    jennefer <- sample(1:6, size=5, replace=T)
    if (sum(silvan) > sum(jennefer)) {
      silvan_count <- silvan_count + 1
    }
  }
  if (silvan_count == 3) {
    count <- count + 1
  }
}

count/nsim

# 20
nsim <- 100000
result <- c()
probs <- c(0.148, 0.148, 0.148, 0.148, 0.148, 0.26)
for (i in 1:nsim) {
  num_wurf <- 0
  points <- 0
  while (points < 44) {
    points <- points + sample(1:6, size = 1, replace = T, prob = probs)
    num_wurf <- num_wurf + 1
  }
  result[i] <- num_wurf
}
result
sum(result) / nsim






