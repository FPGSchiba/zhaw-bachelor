library(tidyverse)
library(stringr)

# Read headers and data
headers <- read.csv(path, header = FALSE, nrows = 6, stringsAsFactors = FALSE)
combined_headers <- apply(headers, 2, function(x) paste(na.omit(x[x != ""]), collapse = "_"))

data <- read.csv(path, skip = 6, header = FALSE)
names(data) <- combined_headers
names(data)[1] <- "datum"

# Extract location and parameter information
col_info <- tibble(col_name = names(data)[-1]) |>
  mutate(
    # Extract location
    location = str_extract(col_name, "(?<=Zürich\\s)[A-Za-zäöüÄÖÜ]+"),
    location = ifelse(!is.na(location),
      str_to_lower(str_extract(location, "^[A-Za-zäöüÄÖÜ]+")),
      NA_character_
    ),
    location = str_replace_all(location, c("ä" = "ae", "ö" = "oe", "ü" = "ue", "Ä" = "Ae", "Ö" = "Oe", "Ü" = "Ue")),

    # Extract parameter
    parameter = str_extract(col_name, "(?<=_)(SO2|CO|O3_max|O3_nb|NO2|NO|PM10|T|Hr|p|WVs|StrGlo|RainDur)(?=_|$)"),
    parameter = ifelse(!is.na(parameter), str_to_lower(parameter), NA_character_),

    # Transform specific parameters
    parameter = case_when(
      parameter == "o3_max" ~ "o3_max_h1",
      parameter == "o3_nb" ~ "o3_nb_h1gt120",
      TRUE ~ parameter
    )
  ) |>
  select(col_name, location, parameter)

# Convert to long format, join with column info, then to wide format
result <- data |>
  pivot_longer(cols = -datum, names_to = "col_name", values_to = "value") |>
  left_join(col_info, by = "col_name") |>
  filter(!is.na(location) & !is.na(parameter)) |>
  select(-col_name) |>
  pivot_wider(
    id_cols = c(datum, location),
    names_from = parameter,
    values_from = value
  ) |>
  mutate(across(where(is.numeric), ~ round(., 2))) |>
  rename(standort = location) |>
  mutate(datum = as.Date(datum)) |>
  mutate(across(where(is.numeric), ~ ifelse(is.nan(.), NA, .)))
