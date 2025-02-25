# Aufgabe 2
library(stringr)
library(dplyr)
words

# A
str_flatten(words, collapse = "+")

# B
# sep: Zeichen zwischen eingabe Vektoren
# collapse: Zeichen, um alle Vektoren zu einem String to kollabieren (besser str_flatten)

# C
words[str_starts(words, "[aeiou]")] # Wörter die mit Vokalen beginnen
words[!str_detect(words, "[aeiou]")] # Wörter die nur aus konsonanten
words[str_detect(words, "ed$") & !str_detect(words, "eed$")]
words[str_detect(words, "(ing|ise)$")]

# D
gruppe_a <- words[str_detect(words, "cei|(?<!c)ie")]
gruppe_b <- words[str_detect(words, "cie|(?<!c)ei")]
length(gruppe_a)
length(gruppe_b)

# E
words[str_detect(words, "q(?!u)")]

# F
imdb_urls <- c("https://www.imdb.com/title/tt6751668/?ref_=hm_fanfav_tt_4_pd_fp1", "https://www.imdb.com/title/tt0260991/", "www.imdb.com/title/tt7282468/reviews", "https://m.imdb.com/title/tt4768776/")
str_extract(imdb_urls, "tt[0-9]{7}")

# Aufgabe 3
filenames <- c("S123.P2.C10_20120621_213422.jpg", "S10.P1.C1_20120622_050148.jpg", "S187.P2.C2_20120702_023501.jpg")

matches <- str_match(filenames, "(S\\d+)\\.(P\\d+)\\.(C\\d+)_(\\d{4})(\\d{2})(\\d{2})_(\\d{2})(\\d{2})(\\d{2})\\.jpg")
tibble(
    Site = matches[, 2],
    Person = matches[, 3],
    Camera = matches[, 4],
    Year = strtoi(matches[, 5]),
    Month = strtoi(matches[, 6]),
    Day = strtoi(matches[, 7]),
    Hour = strtoi(matches[, 8]),
    Minute = strtoi(matches[, 9]),
    Second = strtoi(matches[, 10])
)

# Aufgabe 4
# install.packages("janitor")
library(janitor)
library(readxl)
dat <- read_excel("/Users/schiba/data/pm-02/bad-table-psych.xlsx", skip = 2, n_max = 12)
names(dat)

clean_names <- function(tibble) {
    names <- names(tibble)

    # Spaltennamen beginnen immer mit einem Buchstaben
    names <- str_replace_all(names, "^\\W+(?=\\d)", "a")
    names <- str_replace_all(names, "^\\W+(?!\\d)", "")

    # Am Ende hat es keine Leer und Interpunktionszeichen
    names <- str_replace_all(names, "[^\\w]+", " ")
    names <- str_replace_all(names, "\\s+", " ")
    names <- str_replace_all(names, "\\s+$", "")
    names <- str_replace_all(names, "\\s", "_")
    names <- str_replace_all(names, "[[:punct:]]$", "_")

    # Alle  Buchstaben klein
    names <- tolower(names)

    # Umlaute werden ersetzt durch ae, oe, ue
    names <- str_replace_all(names, "ä", "ae")
    names <- str_replace_all(names, "ö", "oe")
    names <- str_replace_all(names, "ü", "ue")

    # More stuff


    # Ersetzten
    names(tibble) <- names
    return(tibble)
}
dat |>
    clean_names() |>
    names()

# Aufgabe 5
adressen <- c("Platz der Republik 1, D-11011 Berlin", "Dr.-Karl-Renner-Ring 3, A-1017 Wien", "Bundesplatz 3, CH-3005 Bern")
str_match(adressen, "^(.+)\\s(\\d{1,3}),\\s(CH|D|A)-(\\d{4,5})\\s(.+)$")

# Aufgabe 6
# install.packages("babynames")
library(babynames)
library(tidyr)

# A
babynames |>
    group_by(sex) |>
    summarise(
        unique_names = n_distinct(name),
        total_occurrences = sum(n)
    )

# B
num_shine_names <- babynames$name[str_detect(babynames$name, "shine")] |>
    length()
num_shine_names * 100 / length(babynames$name) # 0.0045%

# C
babynames$match <- str_extract(babynames$name, "[aeiouAEIOU]{4}")

babynames |>
    filter(!is.na(match)) |>
    group_by(name) |>
    summarise(
        match = first(match),
        total_occurrences = sum(n)
    )
