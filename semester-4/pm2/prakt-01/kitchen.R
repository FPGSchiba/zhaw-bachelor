# Libs
library(lubridate)
library(tidyverse)
library(stringr)

# Import
path <- "/Users/schiba/data/pm-02/ugz_luftqualitaetsmessung_seit-2012.csv"

# Read headers and data
headers <- read.csv(path, header = FALSE, nrows = 6, stringsAsFactors = FALSE)
combined_headers <- apply(headers, 2, function(x) paste(na.omit(x[x != ""]), collapse = "_"))

# Read data, ensuring all columns are read as character initially
data <- read.csv(path, skip = 6, header = FALSE, colClasses = "character")
names(data) <- combined_headers
names(data)[1] <- "datum"

# Convert columns to appropriate types
data <- data |>
  mutate(across(-datum, ~ {
    # Replace "NaN" or empty strings with NA
    . <- ifelse(. %in% c("NaN", ""), NA, .)
    # Convert to numeric where possible
    as.numeric(.)
  }))

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
view(col_info)
# Convert to long format, join with column info, then to wide format
result <- data |>
  pivot_longer(cols = -datum, names_to = "col_name", values_to = "value") |> # Convert to long format -> 1 row per value under a column that is not datum
  left_join(col_info, by = "col_name") |> # Join with column info to get location and parameter
  filter(!is.na(location) & !is.na(parameter)) |> # Filter out rows without location or parameter
  select(-col_name) |> # Remove column name (as it is no longer needed and was replaced by location and parameter)
  pivot_wider(
    id_cols = c(datum, location),
    names_from = parameter,
    values_from = value
  ) |> # Convert to wide format -> 1 row per location and date (parameter to colmn name and values to column values)
  mutate(across(where(is.numeric), ~ round(., 2))) |> # Round numeric columns to 2 decimal places -> may cause loss of precision
  rename(standort = location) |> # Rename location to standort
  mutate(datum = as.Date(datum)) # Convert datum to Date type

# Extensions
options("lubridate.week.start" = 1) # Set week start to Monday

result["wochentag"] <- result$datum |>
  ymd() |> # Convert to Date object
  wday(label = TRUE, abbr = TRUE) # Get weekday as factor with labels

result <- result |>
  mutate(wochentag = factor(wochentag,
    levels = levels(wochentag),
    labels = str_sub(levels(wochentag), 1, 2)
  )) # Mutate weekday to factor with abbreviated labels with only two characters

result["monat"] <- result$datum |>
  ymd() |> # Convert to Date object
  month(label = TRUE, abbr = TRUE) # Get month as factor with labels

result["jahr"] <- result$datum |>
  year() # Get year as factor

view(result)
