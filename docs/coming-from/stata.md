# Coming from Stata

You already know how to do something in Stata. This page shows you the same thing in R or Python, one line at a time.

!!! tip "How to use this page"
    Pick **R** or **Python** in any tab below. Every other tab on the page switches with it. Then find the task you want in the left column and copy the line on the right.

## Three things that are different

1. **You name the dataset every time.** Stata holds one dataset in memory. R and Python can hold many at once, so each line says which one to use. On this page it is always called `df`.
2. **You save the result yourself.** `keep if x > 0` changes the data in Stata. In R and Python you write the result back into `df`, for example `df = df[df["x"] > 0]`.
3. **Missing values behave differently.** Stata treats a missing value `.` as bigger than every number. R and Python do not. Read [Missing values](#missing-values) before you copy any line that uses `>`.

## Before you start

Install the packages once. Then load them at the top of every script.

=== "R"

    ```r
    # Run once, in the R console
    install.packages(c("tidyverse", "haven", "readxl", "fixest", "modelsummary"))

    # Put at the top of every script
    library(tidyverse)  # data work
    library(haven)      # read and write .dta files
    library(fixest)     # regressions
    ```

=== "Python"

    ```python
    # Run once, in a terminal
    # pip install pandas numpy pyfixest statsmodels openpyxl

    # Put at the top of every script
    import numpy as np                       # maths
    import pandas as pd                      # data work
    import pyfixest as pf                    # regressions
    import statsmodels.formula.api as smf    # logit, probit
    ```

In the tables, `x`, `y`, `id`, `year` and `state` stand for your own variable names.

## Load and save data

=== "R"

    | Task | Stata | R |
    |---|---|---|
    | Open a Stata file | `use data.dta, clear` | `df <- read_dta("data.dta")` |
    | Save a Stata file | `save data.dta, replace` | `write_dta(df, "data.dta")` |
    | Open a CSV | `import delimited data.csv, clear` | `df <- read_csv("data.csv")` |
    | Save a CSV | `export delimited data.csv, replace` | `write_csv(df, "data.csv")` |
    | Open an Excel file | `import excel data.xlsx, firstrow clear` | `df <- readxl::read_excel("data.xlsx")` |

=== "Python"

    | Task | Stata | Python |
    |---|---|---|
    | Open a Stata file | `use data.dta, clear` | `df = pd.read_stata("data.dta")` |
    | Save a Stata file | `save data.dta, replace` | `df.to_stata("data.dta", write_index=False)` |
    | Open a CSV | `import delimited data.csv, clear` | `df = pd.read_csv("data.csv")` |
    | Save a CSV | `export delimited data.csv, replace` | `df.to_csv("data.csv", index=False)` |
    | Open an Excel file | `import excel data.xlsx, firstrow clear` | `df = pd.read_excel("data.xlsx")` |

## Look at your data

=== "R"

    | Task | Stata | R |
    |---|---|---|
    | List variables and types | `describe` | `glimpse(df)` |
    | Show the first 5 rows | `list in 1/5` | `head(df, 5)` |
    | Open a spreadsheet view | `browse` | `View(df)` |
    | Count rows | `count` | `nrow(df)` |
    | Summary statistics | `summarize` | `summary(df)` |
    | Summary of one variable | `summarize x` | `summary(df$x)` |
    | Frequency table | `tabulate x` | `count(df, x)` |
    | Two-way table | `tabulate x y` | `table(df$x, df$y)` |
    | Count missing values | `misstable summarize` | `colSums(is.na(df))` |
    | Check for duplicates | `duplicates report id year` | `sum(duplicated(df[c("id", "year")]))` |

=== "Python"

    | Task | Stata | Python |
    |---|---|---|
    | List variables and types | `describe` | `df.info()` |
    | Show the first 5 rows | `list in 1/5` | `df.head(5)` |
    | Open a spreadsheet view | `browse` | `df` (in Jupyter) |
    | Count rows | `count` | `len(df)` |
    | Summary statistics | `summarize` | `df.describe()` |
    | Summary of one variable | `summarize x` | `df["x"].describe()` |
    | Frequency table | `tabulate x` | `df["x"].value_counts()` |
    | Two-way table | `tabulate x y` | `pd.crosstab(df["x"], df["y"])` |
    | Count missing values | `misstable summarize` | `df.isna().sum()` |
    | Check for duplicates | `duplicates report id year` | `df.duplicated(["id", "year"]).sum()` |

## Keep and drop

=== "R"

    | Task | Stata | R |
    |---|---|---|
    | Keep rows that meet a condition | `keep if x > 0` | `df <- filter(df, x > 0)` |
    | Drop rows with a missing value | `drop if missing(x)` | `df <- filter(df, !is.na(x))` |
    | Keep rows that match a list | `keep if inlist(state, "CA", "NY")` | `df <- filter(df, state %in% c("CA", "NY"))` |
    | Keep rows in a range | `keep if inrange(age, 18, 65)` | `df <- filter(df, between(age, 18, 65))` |
    | Keep some variables | `keep id year x` | `df <- select(df, id, year, x)` |
    | Drop a variable | `drop x` | `df <- select(df, -x)` |
    | Sort | `sort id year` | `df <- arrange(df, id, year)` |
    | Sort largest first | `gsort -x` | `df <- arrange(df, desc(x))` |

=== "Python"

    | Task | Stata | Python |
    |---|---|---|
    | Keep rows that meet a condition | `keep if x > 0` | `df = df[df["x"] > 0]` |
    | Drop rows with a missing value | `drop if missing(x)` | `df = df.dropna(subset=["x"])` |
    | Keep rows that match a list | `keep if inlist(state, "CA", "NY")` | `df = df[df["state"].isin(["CA", "NY"])]` |
    | Keep rows in a range | `keep if inrange(age, 18, 65)` | `df = df[df["age"].between(18, 65)]` |
    | Keep some variables | `keep id year x` | `df = df[["id", "year", "x"]]` |
    | Drop a variable | `drop x` | `df = df.drop(columns="x")` |
    | Sort | `sort id year` | `df = df.sort_values(["id", "year"])` |
    | Sort largest first | `gsort -x` | `df = df.sort_values("x", ascending=False)` |

## Create and change variables

=== "R"

    | Task | Stata | R |
    |---|---|---|
    | New variable | `gen y = x^2` | `df <- mutate(df, y = x^2)` |
    | Natural log | `gen lny = ln(y)` | `df <- mutate(df, lny = log(y))` |
    | Dummy variable | `gen d = (x > 100)` | `df <- mutate(df, d = as.integer(x > 100))` |
    | Change values that meet a condition | `replace y = 0 if x < 0` | `df <- mutate(df, y = if_else(x < 0, 0, y))` |
    | Rename | `rename old new` | `df <- rename(df, new = old)` |
    | Text to number | `destring x, replace` | `df <- mutate(df, x = as.numeric(x))` |
    | Number to text | `tostring x, replace` | `df <- mutate(df, x = as.character(x))` |
    | Text to categories | `encode state, gen(state_id)` | `df <- mutate(df, state_id = factor(state))` |
    | Quartiles | `xtile q = x, nq(4)` | `df <- mutate(df, q = ntile(x, 4))` |
    | Text to date | `gen date = date(s, "YMD")` | `df <- mutate(df, date = lubridate::ymd(s))` |
    | Year from a date | `gen yr = year(date)` | `df <- mutate(df, yr = lubridate::year(date))` |

=== "Python"

    | Task | Stata | Python |
    |---|---|---|
    | New variable | `gen y = x^2` | `df["y"] = df["x"] ** 2` |
    | Natural log | `gen lny = ln(y)` | `df["lny"] = np.log(df["y"])` |
    | Dummy variable | `gen d = (x > 100)` | `df["d"] = (df["x"] > 100).astype(int)` |
    | Change values that meet a condition | `replace y = 0 if x < 0` | `df.loc[df["x"] < 0, "y"] = 0` |
    | Rename | `rename old new` | `df = df.rename(columns={"old": "new"})` |
    | Text to number | `destring x, replace` | `df["x"] = pd.to_numeric(df["x"], errors="coerce")` |
    | Number to text | `tostring x, replace` | `df["x"] = df["x"].astype(str)` |
    | Text to categories | `encode state, gen(state_id)` | `df["state_id"] = df["state"].astype("category")` |
    | Quartiles | `xtile q = x, nq(4)` | `df["q"] = pd.qcut(df["x"], 4, labels=False) + 1` |
    | Text to date | `gen date = date(s, "YMD")` | `df["date"] = pd.to_datetime(df["s"])` |
    | Year from a date | `gen yr = year(date)` | `df["yr"] = df["date"].dt.year` |

## Work by group

These replace `bysort`, `egen` and `collapse`.

=== "R"

    | Task | Stata | R |
    |---|---|---|
    | Group mean on every row | `bysort id: egen m = mean(x)` | `df <- mutate(df, m = mean(x, na.rm = TRUE), .by = id)` |
    | Rows per group | `bysort id: gen n = _N` | `df <- mutate(df, n = n(), .by = id)` |
    | Number rows within a group | `bysort id (year): gen t = _n` | `df <- df %>% arrange(id, year) %>% mutate(t = row_number(), .by = id)` |
    | Previous value in the group | `bysort id (year): gen lag_x = x[_n-1]` | `df <- df %>% arrange(id, year) %>% mutate(lag_x = lag(x), .by = id)` |
    | One row per group | `collapse (mean) x, by(state)` | `df <- summarise(df, x = mean(x, na.rm = TRUE), .by = state)` |
    | Several statistics per group | `collapse (mean) x (sum) y, by(state year)` | `df <- summarise(df, x = mean(x, na.rm = TRUE), y = sum(y, na.rm = TRUE), .by = c(state, year))` |

=== "Python"

    | Task | Stata | Python |
    |---|---|---|
    | Group mean on every row | `bysort id: egen m = mean(x)` | `df["m"] = df.groupby("id")["x"].transform("mean")` |
    | Rows per group | `bysort id: gen n = _N` | `df["n"] = df.groupby("id")["id"].transform("size")` |
    | Number rows within a group | `bysort id (year): gen t = _n` | `df = df.sort_values(["id", "year"])`<br>`df["t"] = df.groupby("id").cumcount() + 1` |
    | Previous value in the group | `bysort id (year): gen lag_x = x[_n-1]` | `df = df.sort_values(["id", "year"])`<br>`df["lag_x"] = df.groupby("id")["x"].shift(1)` |
    | One row per group | `collapse (mean) x, by(state)` | `df = df.groupby("state", as_index=False)["x"].mean()` |
    | Several statistics per group | `collapse (mean) x (sum) y, by(state year)` | `df = df.groupby(["state", "year"], as_index=False).agg(x=("x", "mean"), y=("y", "sum"))` |

??? note "Lags in panels with gaps"
    `x[_n-1]` and the lines above take the previous **row**, even if a year is missing. Stata's `L.x` after `xtset id year` takes the previous **year** and gives a missing value if that year is absent. In R, `fixest::panel(df, ~id + year)` followed by `l(x)` matches `L.x`.

## Merge, append and reshape

!!! warning "Stata keeps everything by default. R and Python do not."
    Stata's `merge` keeps rows from both files, matched or not. R and Python only do this if you ask. Always say which rows you want to keep.

=== "R"

    | Task | Stata | R |
    |---|---|---|
    | Merge, keep everything | `merge 1:1 id using other` | `df <- full_join(df, other, by = "id")` |
    | Merge, keep all of `df` | `merge m:1 state using other, keep(master match)` | `df <- left_join(df, other, by = "state")` |
    | Merge, keep matches only | `merge 1:1 id using other, keep(match)` | `df <- inner_join(df, other, by = "id")` |
    | Stack two datasets | `append using other` | `df <- bind_rows(df, other)` |
    | Wide to long | `reshape long inc, i(id) j(year)` | `df <- pivot_longer(df, starts_with("inc"), names_to = "year", names_prefix = "inc", values_to = "inc")` |
    | Long to wide | `reshape wide inc, i(id) j(year)` | `df <- pivot_wider(df, names_from = year, values_from = inc, names_prefix = "inc")` |

=== "Python"

    | Task | Stata | Python |
    |---|---|---|
    | Merge, keep everything | `merge 1:1 id using other` | `df = df.merge(other, on="id", how="outer")` |
    | Merge, keep all of `df` | `merge m:1 state using other, keep(master match)` | `df = df.merge(other, on="state", how="left")` |
    | Merge, keep matches only | `merge 1:1 id using other, keep(match)` | `df = df.merge(other, on="id", how="inner")` |
    | Stack two datasets | `append using other` | `df = pd.concat([df, other], ignore_index=True)` |
    | Wide to long | `reshape long inc, i(id) j(year)` | `df = pd.wide_to_long(df, stubnames="inc", i="id", j="year").reset_index()` |
    | Long to wide | `reshape wide inc, i(id) j(year)` | `df = df.pivot(index="id", columns="year", values="inc").add_prefix("inc").reset_index()` |

??? note "Check that a merge is 1:1 or m:1"
    Stata stops with an error if the keys are not unique. To get the same check, add `relationship = "one-to-one"` (or `"many-to-one"`) in R, or `validate="1:1"` (or `"m:1"`) in Python. To see which rows matched, like `_merge`, add `indicator=True` in Python.

## Run regressions

R uses **fixest** and Python uses **pyfixest**. Both use the same formula style: outcome `~` regressors, then fixed effects after `|`.

=== "R"

    | Task | Stata | R |
    |---|---|---|
    | OLS | `reg y x1 x2` | `fit <- feols(y ~ x1 + x2, data = df)` |
    | Robust standard errors | `reg y x, robust` | `fit <- feols(y ~ x, data = df, vcov = "hetero")` |
    | Clustered standard errors | `reg y x, cluster(state)` | `fit <- feols(y ~ x, data = df, cluster = ~state)` |
    | Dummies for a category | `reg y x i.state` | `fit <- feols(y ~ x + i(state), data = df)` |
    | Interaction | `reg y c.x##i.treat` | `fit <- feols(y ~ x * factor(treat), data = df)` |
    | Fixed effects | `reghdfe y x, absorb(id)` | `fit <- feols(y ~ x | id, data = df)` |
    | Two-way fixed effects | `reghdfe y x, absorb(id year)` | `fit <- feols(y ~ x | id + year, data = df)` |
    | Instrumental variables | `ivregress 2sls y (x = z)` | `fit <- feols(y ~ 1 | x ~ z, data = df)` |
    | Logit | `logit d x` | `fit <- feglm(d ~ x, data = df, family = binomial)` |
    | Probit | `probit d x` | `fit <- feglm(d ~ x, data = df, family = binomial(link = "probit"))` |

=== "Python"

    | Task | Stata | Python |
    |---|---|---|
    | OLS | `reg y x1 x2` | `fit = pf.feols("y ~ x1 + x2", data=df)` |
    | Robust standard errors | `reg y x, robust` | `fit = pf.feols("y ~ x", data=df, vcov="hetero")` |
    | Clustered standard errors | `reg y x, cluster(state)` | `fit = pf.feols("y ~ x", data=df, vcov={"CRV1": "state"})` |
    | Dummies for a category | `reg y x i.state` | `fit = pf.feols("y ~ x + C(state)", data=df)` |
    | Interaction | `reg y c.x##i.treat` | `fit = pf.feols("y ~ x * C(treat)", data=df)` |
    | Fixed effects | `reghdfe y x, absorb(id)` | `fit = pf.feols("y ~ x | id", data=df)` |
    | Two-way fixed effects | `reghdfe y x, absorb(id year)` | `fit = pf.feols("y ~ x | id + year", data=df)` |
    | Instrumental variables | `ivregress 2sls y (x = z)` | `fit = pf.feols("y ~ 1 + [x ~ z]", data=df)` |
    | Logit | `logit d x` | `fit = smf.logit("d ~ x", data=df).fit()` |
    | Probit | `probit d x` | `fit = smf.probit("d ~ x", data=df).fit()` |

## After a regression

=== "R"

    | Task | Stata | R |
    |---|---|---|
    | Show results | (printed automatically) | `summary(fit)` |
    | Coefficients | `display _b[x]` | `coef(fit)` |
    | Standard errors | `display _se[x]` | `se(fit)` |
    | Fitted values | `predict yhat` | `predict(fit)` |
    | Residuals | `predict e, residuals` | `resid(fit)` |
    | Table of several models | `esttab m1 m2` | `etable(m1, m2)` |
    | Save the table for LaTeX | `esttab m1 m2 using table.tex` | `etable(m1, m2, tex = TRUE, file = "table.tex")` |

=== "Python"

    | Task | Stata | Python |
    |---|---|---|
    | Show results | (printed automatically) | `fit.summary()` |
    | Coefficients | `display _b[x]` | `fit.coef()` |
    | Standard errors | `display _se[x]` | `fit.se()` |
    | Fitted values | `predict yhat` | `fit.predict()` |
    | Residuals | `predict e, residuals` | `fit.resid()` |
    | Table of several models | `esttab m1 m2` | `pf.etable([m1, m2])` |
    | Save the table for LaTeX | `esttab m1 m2 using table.tex` | `pf.etable([m1, m2], type="tex")` |

## Missing values

The same line can give different answers when `x` is missing.

| What you write | Stata | R | Python |
|---|---|---|---|
| `x > 100` | true (missing counts as very large) | `NA` | `False` |
| Mean of a column with gaps | skips missing | `NA`, unless you add `na.rm = TRUE` | skips missing |

!!! warning "Watch out"
    In Stata, `gen rich = (income > 100000)` marks people with missing income as rich. Stata users fix this with `if !missing(income)`. R and Python do not have this problem, so their results can differ from old Stata output.

## Basics

=== "R"

    | Task | Stata | R |
    |---|---|---|
    | Get help | `help regress` | `?lm` |
    | Install a package | `ssc install reghdfe` | `install.packages("fixest")` |
    | Comment | `* comment` | `# comment` |
    | Store a number | `local n = 5` | `n <- 5` |
    | Set a random seed | `set seed 42` | `set.seed(42)` |
    | Loop over numbers | `forvalues i = 1/10 { ... }` | `for (i in 1:10) { ... }` |
    | Loop over variables | `foreach v of varlist x y { ... }` | `for (v in c("x", "y")) { ... }` |

=== "Python"

    | Task | Stata | Python |
    |---|---|---|
    | Get help | `help regress` | `help(pd.read_csv)` |
    | Install a package | `ssc install reghdfe` | `pip install pyfixest` (in a terminal) |
    | Comment | `* comment` | `# comment` |
    | Store a number | `local n = 5` | `n = 5` |
    | Set a random seed | `set seed 42` | `rng = np.random.default_rng(42)` |
    | Loop over numbers | `forvalues i = 1/10 { ... }` | `for i in range(1, 11): ...` |
    | Loop over variables | `foreach v of varlist x y { ... }` | `for v in ["x", "y"]: ...` |

---

This page follows the layout of the "Coming from Stata" chapter in Arthur Turrell's [Coding for Economists](https://aeturrell.github.io/coding-for-economists/coming-from-stata.html).
