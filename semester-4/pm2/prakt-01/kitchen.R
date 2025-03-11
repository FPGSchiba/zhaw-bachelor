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
  mutate(datum = as.Date(datum))

# Extensions
options("lubridate.week.start" = 1)

result["wochentag"] <- result$datum |>
  ymd() |>
  wday(label = TRUE, abbr = TRUE)

result <- result |>
  mutate(wochentag = factor(wochentag,
    levels = levels(wochentag),
    labels = str_sub(levels(wochentag), 1, 2)
  ))

result["monat"] <- result$datum |>
  ymd() |>
  month(label = TRUE, abbr = TRUE)

result["jahr"] <- result$datum |>
  year()

# Visualizations
# Scatterplot for Stampfenbachstrasse
result |>
  filter(standort == "stampfenbachstrasse") |>
  ggplot(aes(x = o3_max_h1, y = strglo)) +
  geom_point() +
  geom_smooth(method = "loess", se = FALSE) +
  labs(
    x = "Maximale Ozonkonzentration während einer Stunde (µg/m³)",
    y = "Globalstrahlung (W/m²)",
    caption = "Scatterplot der Ozonkonzentration und Globalstrahlung für den Standort Stampfenbachstrasse"
  ) +
  theme(
    axis.title = element_text(size = 14),
    plot.caption = element_text(size = 12)
  )

# Plot NOx concentration over time for Schimmelstrasse and Heubeeribüel
result |>
  filter(standort %in% c("schimmelstrasse", "heubeeribuel")) |>
  mutate(nox = no + no2) |>
  ggplot(aes(x = datum, y = nox, color = standort)) +
  geom_line() +
  labs(
    x = "Datum",
    y = "NOx Konzentration (µg/m³)",
    caption = "Verlauf der NOx-Konzentration über den gesamten Zeitraum für die Standorte Schimmelstrasse und Heubeeribüel"
  ) +
  theme(
    axis.title = element_text(size = 14),
    plot.caption = element_text(size = 12),
    legend.position = "top",
    legend.title = element_blank()
  )

# Boxplot for PM10 concentration by weekday at Rosengartenstrasse
result |>
  filter(standort == "rosengartenstrasse") |>
  ggplot(aes(x = wochentag, y = pm10)) +
  geom_boxplot() +
  labs(
    x = "Wochentag",
    y = "PM10 Konzentration (µg/m³)",
    caption = "Streuung der PM10-Konzentration pro Wochentag für den Standort Rosengartenstrasse"
  ) +
  theme(
    axis.title = element_text(size = 14),
    plot.caption = element_text(size = 12)
  )

# Plot NOx concentration over time for all four stations from 2012 to 2020
result |>
  filter(datum >= as.Date("2012-01-01") & datum <= as.Date("2020-12-31")) |>
  mutate(nox = no + no2) |>
  # First calculate monthly values for each year
  group_by(standort, jahr, monat) |>
  summarise(
    year_month_mean = mean(nox, na.rm = TRUE)
  ) |>
  mutate(
    monat_date = make_date(2012, monat, 1), # Use 2012 for consistent x-axis
    jahr = as.factor(jahr) # Convert year to factor for discrete colors
  ) |>
  ggplot() +
  # Add points for individual years with color
  geom_point(aes(x = monat_date, y = year_month_mean, color = jahr),
    size = 2, alpha = 0.7
  ) +
  geom_line(aes(x = monat_date, y = year_month_mean, color = jahr, group = jahr),
    alpha = 0.4, linewidth = 0.5
  ) +
  # Add summary line and ribbon
  stat_summary(
    aes(x = monat_date, y = year_month_mean),
    fun = mean,
    geom = "line",
    linewidth = 1.2,
    color = "black"
  ) +
  stat_summary(
    aes(x = monat_date, y = year_month_mean),
    fun.data = function(y) {
      data.frame(
        ymin = mean(y) - sd(y),
        ymax = mean(y) + sd(y)
      )
    },
    geom = "ribbon",
    fill = "grey",
    alpha = 0.2
  ) +
  facet_wrap(~standort, scales = "free_y") +
  scale_x_date(date_labels = "%B", date_breaks = "1 month") +
  scale_color_viridis_d(name = "Jahr") + # Use viridis color palette
  labs(
    x = "Monat",
    y = "NOx-Konzentration (µg/m³)",
    caption = "Mittlere monatliche NOx-Konzentrationen mit Standardabweichung (2012-2020)\nFarbige Punkte und Linien zeigen Monatsmittelwerte einzelner Jahre"
  ) +
  theme_light() +
  theme(
    axis.title = element_text(size = 12),
    axis.text = element_text(size = 10),
    axis.text.x = element_text(angle = 45, hjust = 1),
    plot.caption = element_text(size = 10),
    strip.text = element_text(size = 10),
    panel.grid.minor = element_blank(),
    legend.position = "right",
    legend.title = element_text(size = 10),
    legend.text = element_text(size = 9)
  )

print(head(result), width = Inf)
