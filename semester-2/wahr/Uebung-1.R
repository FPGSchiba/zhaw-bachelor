# ---- A3 ----
# B
n <- 500
mylist <- list()
for (i in 1:n) {
  vec <- sample(1:6,3,replace=TRUE)
  mylist[[i]] <- vec
}
experiment <- do.call("rbind",mylist)
experiment <- data.frame(experiment)
experiment[experiment$X1 != 4 & experiment$X2 != 4 & experiment$X3 != 4,]
experiment
nrow(experiment[experiment$X1 != 4 & experiment$X2 != 4 & experiment$X3 != 4,]) / nrow(experiment)

# Relativ genau mit: 0.56 - 0.63