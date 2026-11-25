# ==============================================================================
# Project:  My project
# File:     01_analysis.R
# Purpose:  Clean the survey data and estimate the wage regressions
# Author:   Your Name
# Created:  2026-01-01
# Inputs:   data/raw/survey.dta
# Outputs:  data/clean/survey_clean.dta
#           output/tables/wage_regs.tex
#           output/figures/wage_educ.png
# ==============================================================================


# 0. Setup ---------------------------------------------------------------------

# Packages: run once per computer
# install.packages(c("tidyverse", "haven", "fixest", "here"))

library(tidyverse)  # data work and charts
library(haven)      # read and write .dta files
library(fixest)     # regressions
library(here)       # file paths that start at the project folder

set.seed(20260101)  # makes random draws repeatable

raw     <- here("data", "raw")
clean   <- here("data", "clean")
tables  <- here("output", "tables")
figures <- here("output", "figures")


# 1. Load data -----------------------------------------------------------------

df <- read_dta(file.path(raw, "survey.dta"))


# 2. Clean ---------------------------------------------------------------------

df <- df %>%
  rename_with(str_to_lower) %>%      # all column names in lower case
  filter(!is.na(id))

# Stop if id-year is not unique
stopifnot(anyDuplicated(df[c("id", "year")]) == 0)


# 3. Create variables ----------------------------------------------------------

df <- df %>%
  mutate(ln_wage = log(wage))


# 4. Analysis ------------------------------------------------------------------

m1 <- feols(ln_wage ~ educ, data = df, vcov = "hetero")
m2 <- feols(ln_wage ~ educ | id + year, data = df, cluster = ~id)

etable(m1, m2)


# 5. Save results --------------------------------------------------------------

etable(m1, m2, tex = TRUE, file = file.path(tables, "wage_regs.tex"), replace = TRUE)

p <- ggplot(df, aes(educ, ln_wage)) +
  geom_point(alpha = 0.3) +
  geom_smooth(method = "lm") +
  labs(x = "Years of education", y = "Log hourly wage")

ggsave(file.path(figures, "wage_educ.png"), p, width = 6, height = 4, dpi = 300)

write_dta(df, file.path(clean, "survey_clean.dta"))
