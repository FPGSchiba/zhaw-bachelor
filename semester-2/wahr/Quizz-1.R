# ---- A1 ----
choose(47+5-1, 5)*choose(15+2-1,2)

# ---- A3 ----
nsim <- 100000
result <- c()
0.78/5
probs <- c(0.156,0.156,0.156,0.156,0.156,0.22)
for (i in 1:nsim) {
  points <- 0
  wurf_count <- 0
  while (points < 48) {
    wurf <- sample(1:6, size=1, replace = F, prob = probs)
    points <- points + wurf
    wurf_count <- wurf_count + 1
  }
  result[i] <- wurf_count
}

mean(result)

# ---- A4 ----
0.5*0.4+(5/6)*0.6

(0.5*0.4)/0.7
