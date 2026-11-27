# Coming from Excel

You already know how to do something in a spreadsheet. This page shows you the same thing in Stata, R or Python, one line at a time.

!!! tip "How to use this page"
    Pick **Stata**, **R** or **Python** in any tab below. Every other tab on the page switches with it. Then find the Excel action or formula in the left column and copy the line on the right.

## Three things that are different

1. **One line does the whole column.** In Excel you write a formula in one cell and drag it down. In Stata, R and Python one line fills the entire column.
2. **Columns have names, not letters.** You write `price`, not `C2:C500`.
3. **Your raw data never changes.** A script reads the file, works on a copy, and saves results to a new file. You can rerun every step at any time.

## Before you start

Install the packages once. Then load them at the top of every script.

=== "R"

    ```r
    # Run once, in the R console
    install.packages(c("tidyverse", "readxl", "writexl"))

    # Put at the top of every script
    library(tidyverse)  # data work and charts
    library(readxl)     # read Excel files
    ```

=== "Python"

    ```python
    # Run once, in a terminal
    # pip install pandas numpy openpyxl seaborn statsmodels

    # Put at the top of every script
    import numpy as np                       # maths
    import pandas as pd                      # data work
    import seaborn as sns                    # charts
    import statsmodels.formula.api as smf    # regression
    ```

=== "Stata"

    Stata reads and writes Excel and CSV files with no extra packages. Start every do-file from the [Stata template](../templates/stata.md).

In the tables, `df` is your sheet. `price`, `qty`, `name`, `region` and `date` stand for your own column names.

## Open and save files

=== "R"

    | Excel | R |
    |---|---|
    | Open `data.xlsx` | `df <- read_excel("data.xlsx")` |
    | Open one sheet | `df <- read_excel("data.xlsx", sheet = "Sales")` |
    | Skip title rows above the headers | `df <- read_excel("data.xlsx", skip = 3)` |
    | Open a CSV | `df <- read_csv("data.csv")` |
    | Save as Excel | `writexl::write_xlsx(df, "out.xlsx")` |
    | Save as CSV | `write_csv(df, "out.csv")` |

=== "Python"

    | Excel | Python |
    |---|---|
    | Open `data.xlsx` | `df = pd.read_excel("data.xlsx")` |
    | Open one sheet | `df = pd.read_excel("data.xlsx", sheet_name="Sales")` |
    | Skip title rows above the headers | `df = pd.read_excel("data.xlsx", skiprows=3)` |
    | Open a CSV | `df = pd.read_csv("data.csv")` |
    | Save as Excel | `df.to_excel("out.xlsx", index=False)` |
    | Save as CSV | `df.to_csv("out.csv", index=False)` |

=== "Stata"

    | Excel | Stata |
    |---|---|
    | Open `data.xlsx` | `import excel "data.xlsx", firstrow clear` |
    | Open one sheet | `import excel "data.xlsx", sheet("Sales") firstrow clear` |
    | Skip title rows above the headers | `import excel "data.xlsx", cellrange(A4) firstrow clear` |
    | Open a CSV | `import delimited "data.csv", clear` |
    | Save as Excel | `export excel "out.xlsx", firstrow(variables) replace` |
    | Save as CSV | `export delimited "out.csv", replace` |

## Look at your data

=== "R"

    | Excel | R |
    |---|---|
    | Scroll through the sheet | `View(df)` |
    | First few rows | `head(df)` |
    | Row count | `nrow(df)` |
    | Column headers | `names(df)` |
    | Column types | `glimpse(df)` |
    | `=COUNTBLANK(B:B)` | `sum(is.na(df$price))` |

=== "Python"

    | Excel | Python |
    |---|---|
    | Scroll through the sheet | `df` (in Jupyter) |
    | First few rows | `df.head()` |
    | Row count | `len(df)` |
    | Column headers | `df.columns` |
    | Column types | `df.dtypes` |
    | `=COUNTBLANK(B:B)` | `df["price"].isna().sum()` |

=== "Stata"

    | Excel | Stata |
    |---|---|
    | Scroll through the sheet | `browse` |
    | First few rows | `list in 1/5` |
    | Row count | `count` |
    | Column headers | `describe, simple` |
    | Column types | `describe` |
    | `=COUNTBLANK(B:B)` | `count if missing(price)` |

## Filter, sort and clean

=== "R"

    | Excel | R |
    |---|---|
    | Filter: price above 100 | `df <- filter(df, price > 100)` |
    | Filter: region is North or South | `df <- filter(df, region %in% c("North", "South"))` |
    | Filter: name contains "Ltd" | `df <- filter(df, str_detect(name, "Ltd"))` |
    | Sort A to Z | `df <- arrange(df, name)` |
    | Sort largest to smallest | `df <- arrange(df, desc(price))` |
    | Delete a column | `df <- select(df, -qty)` |
    | Rename a header | `df <- rename(df, new = old)` |
    | Remove Duplicates | `df <- distinct(df)` |
    | Find and Replace | `df <- mutate(df, name = str_replace_all(name, "Inc.", "Inc"))` |
    | Fill blanks with the value above | `df <- fill(df, region)` |
    | Delete rows with blanks | `df <- drop_na(df)` |

=== "Python"

    | Excel | Python |
    |---|---|
    | Filter: price above 100 | `df = df[df["price"] > 100]` |
    | Filter: region is North or South | `df = df[df["region"].isin(["North", "South"])]` |
    | Filter: name contains "Ltd" | `df = df[df["name"].str.contains("Ltd", na=False)]` |
    | Sort A to Z | `df = df.sort_values("name")` |
    | Sort largest to smallest | `df = df.sort_values("price", ascending=False)` |
    | Delete a column | `df = df.drop(columns="qty")` |
    | Rename a header | `df = df.rename(columns={"old": "new"})` |
    | Remove Duplicates | `df = df.drop_duplicates()` |
    | Find and Replace | `df["name"] = df["name"].str.replace("Inc.", "Inc", regex=False)` |
    | Fill blanks with the value above | `df["region"] = df["region"].ffill()` |
    | Delete rows with blanks | `df = df.dropna()` |

=== "Stata"

    | Excel | Stata |
    |---|---|
    | Filter: price above 100 | `keep if price > 100 & !missing(price)` |
    | Filter: region is North or South | `keep if inlist(region, "North", "South")` |
    | Filter: name contains "Ltd" | `keep if strpos(name, "Ltd") > 0` |
    | Sort A to Z | `sort name` |
    | Sort largest to smallest | `gsort -price` |
    | Delete a column | `drop qty` |
    | Rename a header | `rename old new` |
    | Remove Duplicates | `duplicates drop` |
    | Find and Replace | `replace name = subinstr(name, "Inc.", "Inc", .)` |
    | Fill blanks with the value above | `replace region = region[_n-1] if missing(region)` |
    | Delete rows with blanks | `egen nmiss = rowmiss(_all)`<br>`drop if nmiss > 0` |

## Formulas

Each line makes a new column called `new`. Change the name to whatever you like.

=== "R"

    | Excel | R |
    |---|---|
    | `=B2*C2` | `df <- mutate(df, new = price * qty)` |
    | `=ROUND(B2, 2)` | `df <- mutate(df, new = round(price, 2))` |
    | `=LN(B2)` | `df <- mutate(df, new = log(price))` |
    | `=IF(B2>100, "High", "Low")` | `df <- mutate(df, new = if_else(price > 100, "High", "Low"))` |
    | `=A2 & " " & B2` | `df <- mutate(df, new = str_c(first, " ", last))` |
    | `=LEFT(A2, 3)` | `df <- mutate(df, new = str_sub(name, 1, 3))` |
    | `=TRIM(A2)` | `df <- mutate(df, new = str_squish(name))` |
    | `=UPPER(A2)` | `df <- mutate(df, new = str_to_upper(name))` |
    | `=YEAR(A2)` | `df <- mutate(df, new = lubridate::year(date))` |
    | `=B3-B2` (change from row above) | `df <- mutate(df, new = price - lag(price))` |
    | `=B3/B2-1` (growth rate) | `df <- mutate(df, new = price / lag(price) - 1)` |
    | `=SUM($B$2:B2)` (running total) | `df <- mutate(df, new = cumsum(price))` |

=== "Python"

    | Excel | Python |
    |---|---|
    | `=B2*C2` | `df["new"] = df["price"] * df["qty"]` |
    | `=ROUND(B2, 2)` | `df["new"] = df["price"].round(2)` |
    | `=LN(B2)` | `df["new"] = np.log(df["price"])` |
    | `=IF(B2>100, "High", "Low")` | `df["new"] = np.where(df["price"] > 100, "High", "Low")` |
    | `=A2 & " " & B2` | `df["new"] = df["first"] + " " + df["last"]` |
    | `=LEFT(A2, 3)` | `df["new"] = df["name"].str[:3]` |
    | `=TRIM(A2)` | `df["new"] = df["name"].str.split().str.join(" ")` |
    | `=UPPER(A2)` | `df["new"] = df["name"].str.upper()` |
    | `=YEAR(A2)` | `df["new"] = df["date"].dt.year` |
    | `=B3-B2` (change from row above) | `df["new"] = df["price"].diff()` |
    | `=B3/B2-1` (growth rate) | `df["new"] = df["price"].pct_change()` |
    | `=SUM($B$2:B2)` (running total) | `df["new"] = df["price"].cumsum()` |

=== "Stata"

    | Excel | Stata |
    |---|---|
    | `=B2*C2` | `gen new = price * qty` |
    | `=ROUND(B2, 2)` | `gen new = round(price, 0.01)` |
    | `=LN(B2)` | `gen new = ln(price)` |
    | `=IF(B2>100, "High", "Low")` | `gen new = cond(missing(price), "", cond(price > 100, "High", "Low"))` |
    | `=A2 & " " & B2` | `gen new = first + " " + last` |
    | `=LEFT(A2, 3)` | `gen new = substr(name, 1, 3)` |
    | `=TRIM(A2)` | `gen new = stritrim(strtrim(name))` |
    | `=UPPER(A2)` | `gen new = upper(name)` |
    | `=YEAR(A2)` | `gen new = year(date)`, or `year(dofc(date))` if `describe` shows `date` as `%tc` |
    | `=B3-B2` (change from row above) | `gen new = price - price[_n-1]` |
    | `=B3/B2-1` (growth rate) | `gen new = price / price[_n-1] - 1` |
    | `=SUM($B$2:B2)` (running total) | `gen new = sum(price)` |

## Lookups

`VLOOKUP` and `XLOOKUP` become a **join**. `other` is the lookup sheet, and `id` is the column both sheets share.

=== "R"

    | Excel | R |
    |---|---|
    | `=XLOOKUP(...)` or `=VLOOKUP(..., FALSE)` | `df <- left_join(df, other, by = "id")` |
    | Keep only rows that found a match | `df <- inner_join(df, other, by = "id")` |
    | Find rows with no match (`#N/A`) | `anti_join(df, other, by = "id")` |
    | Paste one sheet below another | `df <- bind_rows(df, other)` |

=== "Python"

    | Excel | Python |
    |---|---|
    | `=XLOOKUP(...)` or `=VLOOKUP(..., FALSE)` | `df = df.merge(other, on="id", how="left")` |
    | Keep only rows that found a match | `df = df.merge(other, on="id", how="inner")` |
    | Find rows with no match (`#N/A`) | `df[~df["id"].isin(other["id"])]` |
    | Paste one sheet below another | `df = pd.concat([df, other], ignore_index=True)` |

=== "Stata"

    | Excel | Stata |
    |---|---|
    | `=XLOOKUP(...)` or `=VLOOKUP(..., FALSE)` | `merge m:1 id using "other.dta", keep(master match) nogenerate` |
    | Keep only rows that found a match | `merge m:1 id using "other.dta", keep(match) nogenerate` |
    | Find rows with no match (`#N/A`) | `merge m:1 id using "other.dta"`<br>`list if _merge == 1` |
    | Paste one sheet below another | `append using "other.dta"` |

In Stata, save the lookup sheet as `other.dta` first: `import excel "other.xlsx", firstrow clear` then `save "other.dta"`.

??? note "Why did my row count go up?"
    `VLOOKUP` stops at the first match. A join returns every match. If an `id` appears twice in `other`, that row of `df` appears twice in the result. Make the lookup sheet unique first: `duplicates drop id, force` in Stata, `distinct(other, id, .keep_all = TRUE)` in R, `other.drop_duplicates("id")` in Python. Stata's `merge m:1` stops with an error if `id` is not unique in `other.dta`, which catches the problem for you.

## Summaries and pivot tables

=== "R"

    | Excel | R |
    |---|---|
    | `=SUM(B:B)` | `sum(df$price, na.rm = TRUE)` |
    | `=AVERAGE(B:B)` | `mean(df$price, na.rm = TRUE)` |
    | `=MEDIAN(B:B)` | `median(df$price, na.rm = TRUE)` |
    | `=STDEV.S(B:B)` | `sd(df$price, na.rm = TRUE)` |
    | `=COUNTIF(C:C, "North")` | `sum(df$region == "North", na.rm = TRUE)` |
    | `=SUMIF(C:C, "North", B:B)` | `sum(df$price[df$region == "North"], na.rm = TRUE)` |
    | Pivot table: total by region | `summarise(df, total = sum(price), .by = region)` |
    | Pivot table: regions × years | `df %>% summarise(total = sum(price), .by = c(region, year)) %>% pivot_wider(names_from = year, values_from = total)` |
    | Pivot table: count of rows | `count(df, region)` |

=== "Python"

    | Excel | Python |
    |---|---|
    | `=SUM(B:B)` | `df["price"].sum()` |
    | `=AVERAGE(B:B)` | `df["price"].mean()` |
    | `=MEDIAN(B:B)` | `df["price"].median()` |
    | `=STDEV.S(B:B)` | `df["price"].std()` |
    | `=COUNTIF(C:C, "North")` | `(df["region"] == "North").sum()` |
    | `=SUMIF(C:C, "North", B:B)` | `df.loc[df["region"] == "North", "price"].sum()` |
    | Pivot table: total by region | `df.groupby("region")["price"].sum()` |
    | Pivot table: regions × years | `pd.pivot_table(df, index="region", columns="year", values="price", aggfunc="sum")` |
    | Pivot table: count of rows | `df["region"].value_counts()` |

=== "Stata"

    | Excel | Stata |
    |---|---|
    | `=SUM(B:B)` | `tabstat price, statistics(sum)` |
    | `=AVERAGE(B:B)` | `summarize price` |
    | `=MEDIAN(B:B)` | `tabstat price, statistics(median)` |
    | `=STDEV.S(B:B)` | `summarize price` |
    | `=COUNTIF(C:C, "North")` | `count if region == "North"` |
    | `=SUMIF(C:C, "North", B:B)` | `tabstat price if region == "North", statistics(sum)` |
    | Pivot table: total by region | `tabstat price, by(region) statistics(sum)` |
    | Pivot table: regions × years | `table region year, statistic(sum price)` |
    | Pivot table: count of rows | `tabulate region` |

## Charts and regression

=== "R"

    | Excel | R |
    |---|---|
    | Scatter chart | `ggplot(df, aes(qty, price)) + geom_point()` |
    | Line chart | `ggplot(df, aes(date, price)) + geom_line()` |
    | Column chart | `ggplot(df, aes(region, price)) + geom_col()` |
    | Histogram | `ggplot(df, aes(price)) + geom_histogram()` |
    | Add a trendline | `+ geom_smooth(method = "lm")` |
    | `=CORREL(A:A, B:B)` | `cor(df$qty, df$price, use = "complete.obs")` |
    | Data Analysis → Regression | `summary(lm(price ~ qty, data = df))` |

=== "Python"

    | Excel | Python |
    |---|---|
    | Scatter chart | `sns.scatterplot(data=df, x="qty", y="price")` |
    | Line chart | `sns.lineplot(data=df, x="date", y="price")` |
    | Column chart | `sns.barplot(data=df, x="region", y="price", estimator="sum")` |
    | Histogram | `sns.histplot(data=df, x="price")` |
    | Add a trendline | `sns.regplot(data=df, x="qty", y="price")` |
    | `=CORREL(A:A, B:B)` | `df["qty"].corr(df["price"])` |
    | Data Analysis → Regression | `smf.ols("price ~ qty", data=df).fit().summary()` |

=== "Stata"

    | Excel | Stata |
    |---|---|
    | Scatter chart | `scatter price qty` |
    | Line chart | `line price date, sort` |
    | Column chart | `graph bar (sum) price, over(region)` |
    | Histogram | `histogram price` |
    | Add a trendline | `twoway (scatter price qty) (lfit price qty)` |
    | `=CORREL(A:A, B:B)` | `correlate qty price` |
    | Data Analysis → Regression | `regress price qty` |

For clustered standard errors, fixed effects and other econometrics, see [Coming from Stata](stata.md#run-regressions).
