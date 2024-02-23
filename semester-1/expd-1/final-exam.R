load('./data/data_pruefung_2023.rda')

# ---- Aufgabe 1 ----

# A
nrow(cyber)

# B
nrow(cyber[cyber$Type == "Theft",])

# C
?sort
sort(cyber$State)

head(sort(tapply(cyber, cyber$State, nrow), decreasing = T), 3)

# D
?sapply
?tapply
sapply(cyber, mean)

tapply(cyber$Affected, cyber$State, mean)

# E
?sub
cyber$YearNumeric <- as.numeric(sub("MMM_", "", cyber$MonthYear))

# F
plot(cyber$YearNumeric, log(cyber$Affected))

cor(cyber$YearNumeric, cyber$Affected)
cor(cyber$YearNumeric, cyber$Affected, method = "pearson")

# G
cyber_location <- cyber[cyber$Location == "Laptop" | cyber$Location == "Desktop Computer" | cyber$Location == "Network Server",]
cyber_location

k <- 1.58 * (IQR(cyber_location$Affected) / sqrt(nrow(cyber_location)))
k

# ---- Aufgabe 3 ----

str(Gigglezol)

library(ggplot2)
?geom_boxplot
ggplot(data=Gigglezol, mapping = aes(y=Lachwert, x=Gruppe)) +
  geom_boxplot()

ggplot(data=Gigglezol, mapping = aes(y=Lachwert, x=Gruppe, fill=Geschlecht)) +
  geom_boxplot()

nrow(Gigglezol[Gigglezol$Gruppe == "Kontroll" & Gigglezol$Geschlecht == "Mann",])
nrow(Gigglezol[Gigglezol$Gruppe == "Kontroll" & Gigglezol$Geschlecht == "Frau",])

nrow(Gigglezol[Gigglezol$Gruppe == "Treatment" & Gigglezol$Geschlecht == "Mann",])
nrow(Gigglezol[Gigglezol$Gruppe == "Treatment" & Gigglezol$Geschlecht == "Frau",])

# ---- Aufgabe 4 ----
# A
gold_price$Price <- as.numeric(gold_price$Price)
gold_news$Forecast <- as.numeric(gold_news$Forecast)

# B
?as.Date()

gold_price$Date <- as.Date(gold_price$Date, format = "%m/%d/%Y")
gold_news$Date <- as.Date(gold_news$Date, format = "%m/%d/%Y")

# C
?grep()
?regexpr()

gold_news[regexpr("inflation", gold_news$Event, ignore.case = T) != -1,]


?search
?match

# D
gold_merged <- merge(gold_price, gold_news)

# E
get_80pc_span <- function(x) {
  quant <- quantile(x, c(0.1, 0.9))
  result <- quant[2] - quant[1]
  return(result[1])
}

get_80pc_span(gold_merged$Price)

# F

tapply(gold_merged$Price, gold_merged$Country, get_80pc_span)

# --- Aufgabe 5 ----
plot(Siebenkampf[5:11])

pca <- prcomp(Siebenkampf[5:11], scale=T)
summary(pca)
pca$rotation
biplot(pca)
