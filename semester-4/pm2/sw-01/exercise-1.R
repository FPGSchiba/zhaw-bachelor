library(tidyverse)
library(dplyr)
library(ggplot2)

load("/Users/schiba/data/pm-02/Uebung01/judgments.rda")

spec(judgments)
glimpse(judgments)

# Select -> Spalten
select(judgments, ends_with("date"), contains("dilemma"))
select(judgments, where("is.character"))
select(
    judgments, #-oder!bedeutetohnedieseSpalte(n)
    -gender,
    !condition,
    -starts_with(c("STAI", "REI")),
    -ends_with("id")
)

# filter -> Reihein
filter(judgments, exclude == 1)
filter(judgments, exclude == 0, mood_pre > 85)
filter(judgments, mood_pre < 20 | mood_post < 20)

# Combination
judgments |>
    filter(between(mood_pre, 40, 60)) |>
    select(age, gender, condition, mood_pre, mood_post)

# relocate -> Spalten umsortieren
filter(judgments, exclude == 0) |>
    relocate(contains("mood"))

# distinct -> einzigartige Werte
judgments |> distinct(start_date, end_date)
judgments |>
    filter(exclude == 0) |>
    select(start_date, end_date) |>
    distinct()
# oder
judgments |>
    filter(exclude == 0) |>
    distinct(start_date, end_date)

# arrange -> sortieren
judgments |>
    arrange(mood_pre, mood_post) |>
    select(subject, mood_pre, mood_post)

arrange(judgments, desc(age)) |> select(subject, age, condition)

# Aufgabe 1
judgments |>
    select(gender, subject, age, starts_with("STAI")) |>
    filter(STAI_pre > 65 & STAI_post > 40) |>
    arrange(STAI_pre, STAI_post) |>
    relocate(subject, STAI_pre, STAI_post)

# rename
rename(judgments, sex = gender, remove = exclude) |> relocate(sex, remove)
rename_with(judgments, stringr::str_to_lower, starts_with("STAI")) |> select(contains("pre"))

# mutate -> neue Spalten
judgments |>
    mutate(mood_change = mood_post - mood_pre) |>
    relocate(starts_with("mood"))

judgments |>
    mutate(mood_change = mood_post - mood_pre, mood_change_norm = abs(mood_change / mean(mood_change, na.rm = TRUE))) |>
    relocate(starts_with("mood")) |>
    arrange(desc(mood_change_norm))

judgments |>
    mutate(mood_pre = mood_pre / mean(mood_pre, na.rm = TRUE), mood_post = mood_post / mean(mood_post, na.rm = TRUE), mood_pre / mean(mood_post, na.rm = TRUE)) |>
    select(starts_with("mood"))

# case_when -> mehrere if-else bedingungen
judgments |>
    mutate(mood_pre_cat = case_when(
        mood_pre < 25 ~ "poor", # ~ = then
        mood_pre > 75 ~ "great",
        TRUE ~ "normal" # sonst
    )) |>
    select(starts_with("mood")) |>
    arrange(desc(mood_pre)) |>
    relocate(mood_pre_cat)

# across -> mehrere Spalten manipulieren
judgments |>
    filter(across(starts_with("mood_p"), is.na)) |>
    select(subject, starts_with("mood"))

judgments |>
    mutate(across(contains("STAI"), \(x){
        x + 1
    })) |>
    select(starts_with("STAI"))

judgments |>
    select(starts_with("MAIA"))

judgments |>
    mutate(across(contains("MAIA"), ~ .x + 1)) |>
    select(starts_with("MAIA"))

judgments |>
    mutate(across(contains("mood"), ~ .x / 100)) |>
    select(starts_with("mood"))

# Kompletes total STAI berechnen (alle spalten und reihen)
judgments |>
    mutate(total_stai = sum(across(contains("STAI")), na.rm = TRUE)) |>
    select(subject, total_stai, contains("STAI"))

# rowwise -> reihenweise berechnen von werten
judgments |>
    rowwise() |>
    mutate(total_stai = sum(c_across(+starts_with("STAI")), na.rm = TRUE)) |>
    select(subject, total_stai, contains("STAI"))

# count -> table in R base -> Zählen
count(judgments, condition, sort = TRUE)

# summarise -> Gruppen zählen und zusammenfassen
judgments |> summarise(min = min(mood_pre, na.rm = TRUE), max = max(mood_pre, na.rm = TRUE))
##  hilfe funktionen
judgments |> summarise(n_rows = n(), n_subject = n_distinct(subject), first_id = first(subject), last_id = last(subject), id_10 = nth(subject, n = 10))

# group_by -> Gruppen nach Spalten bilden
judgments |>
    group_by(condition) |>
    summarise(min = min(mood_pre, na.rm = TRUE), max = max(mood_pre, na.rm = TRUE))

## hirarchisch gruppieren
judgments |>
    group_by(condition, gender) |>
    summarise(n = n(), mAge = mean(age))

judgments |>
    group_by(condition, gender) |>
    summarise(n = n(), mAge = mean(age)) |>
    summarise(n = n(), mAge = mean(mAge), .groups = "drop_last")

judgments |>
    group_by(condition, gender) |>
    summarise(n_ans = n_distinct(STAI_post_1_1), .groups = "drop_last") |>
    summarise(m = sum(n_ans))

judgments |>
    group_by(condition, gender) |>
    summarise(n_ans = n_distinct(STAI_post_1_1), .groups = "drop") |>
    summarise(m = sum(n_ans))

judgments |>
    mutate(mood_pre_cat = case_when(mood_pre < 25 ~ "poor", mood_pre > 75 ~ "great", TRUE ~ "normal")) |>
    relocate(mood_pre_cat) |>
    group_by(mood_pre_cat) |>
    arrange(desc(mood_post), .by_group = TRUE) |> # Wichtig, dass sortierung nach Gruppen erfolgt
    select(mood_pre_cat, mood_post) |>
    distinct()

judgments |>
    group_by(condition, gender) |>
    reframe(range = range(mood_pre - mood_post), n = n(), .groups = "keep")

judgments |>
    filter(!is.na(mood_pre)) |>
    group_by(condition) |>
    reframe(
        value = quantile(mood_pre, +c(0.25, 0.5, 0.75)), q = paste0("Q", 1:3), # glue('Q{1:3}')
        n = n(), .groups = "keep"
    ) |>
    relocate(c(1, 3, 2, 4)) |>
    knitr::kable()

coffee_drinkers <- tribble(~student, ~coffee_shots, 21, 1, 23, 4, 28, 2)
subject_mood <- judgments |>
    select(subject, condition, gender, +starts_with("mood")) |>
    distinct()

# Joins
inner_join(subject_mood, coffee_drinkers, by = c("subject" = "student"))

# Pivot Tables
# Info wo auch immer TBC sein sollte, es wurde nicht geladen
TBC |> pivot_longer(cols = 2:4, names_to = "year", values_to = "n")
