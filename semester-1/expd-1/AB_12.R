library(ggplot2)
# ---- Aufgabe 1 ----
dat <- read.table('./data/zehnkampf_2021.csv', sep = ';', header = T)
str(dat)

# A
boxplot(dat[4:13], las = 2)

pca <-prcomp(dat[4:13], scale=T)
summary(pca)
biplot(pca)
screeplot(pca, type = "line")

apply(dat, 2, sd)

?merge

vec <- c(TRUE, FALSE, NaN)
vec[is.na(vec)] <- FALSE
vec
