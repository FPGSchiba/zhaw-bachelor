dir()
getwd()

setwd(paste0(getwd(), "/semester-5/gstat/quiz-2"))
getwd()

# Aufgabe 1
load("p_werte.rda")
p_werte

alpha_original <- 0.05
alpha_bonferroni <- alpha_original / length(p_werte)
sum(p_werte < alpha_bonferroni)

# Aufgabe 2

load("marktforschungtabelle.rda")
marktforschungtabelle
tabelle_bereinigt <- marktforschungtabelle[1:2, 1:2]
markt.test <- chisq.test(tabelle_bereinigt)

markt.test$p.value
markt.test$expected
markt.test$observed
markt.test$residuals

# Aufgabe 6
5.103389 - 4.017361

# Aufgabe 7
load("pilze.rda")
pilze
t.test(formula = Gewicht ~ Behandelt, data = pilze, var.equal = TRUE, alternative = "less")

# Aufgabe 8
load("kaffeepulver.rda")
kaffeepulver
t.test(x = kaffeepulver$Abfuellanlage_A, y = kaffeepulver$Abfuellanlage_B, var.equal = TRUE, alternative = "two.sided", conf.level = 0.99)

# Aufgabe 9
load("testscores.rda")
testscores
t.test(x = testscores$Vorher, y = testscores$Nachher, paired = TRUE, alternative = "less")
