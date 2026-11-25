# Coming from R

You already know how to do something in R. This page shows you the same thing in Python, one line at a time.

!!! tip "How to use this page"
    Find the task in the left column. The R line you know is in the middle. The Python line is on the right.

## Four things that are different

1. **Methods instead of functions.** R writes `mean(df$x)`. Python writes `df["x"].mean()`: the data comes first, then a dot, then the action.
2. **Counting starts at 0.** The first row is row `0`, not row `1`.
3. **No `na.rm = TRUE`.** Python skips missing values in `sum()`, `mean()` and similar by default.
4. **Regressions look almost the same.** The Python package `pyfixest` copies the formula style of `fixest`. Put the formula in quotes and you are mostly done.

## Before you start

```python
# Run once, in a terminal
# pip install pandas numpy pyfixest seaborn

# Put at the top of every script
import numpy as np                 # maths
import pandas as pd                # data work
import pyfixest as pf              # regressions
import seaborn as sns              # charts
import matplotlib.pyplot as plt    # saving charts
```

In the tables, `df` is your data frame. `x`, `y`, `id`, `year` and `state` stand for your own column names.

## Basics

| Task | R | Python |
|---|---|---|
| Install a package | `install.packages("pkg")` | `pip install pkg` (in a terminal) |
| Load a package | `library(dplyr)` | `import pandas as pd` |
| Get help | `?mean` | `help(pd.DataFrame.mean)` |
| Store a value | `x <- 5` | `x = 5` |
| Vector or list | `c(1, 2, 3)` | `[1, 2, 3]` |
| Numbers 1 to 10 | `1:10` | `range(1, 11)` |
| Length | `length(v)` | `len(v)` |
| Join text | `paste0("a", "b")` | `"a" + "b"` |
| True and false | `TRUE`, `FALSE` | `True`, `False` |
| Missing value | `NA` | `np.nan` |
| Loop | `for (i in 1:10) { ... }` | `for i in range(1, 11): ...` |
| Function | `f <- function(x) x^2` | `def f(x): return x ** 2` |

## Load and look at data

| Task | R | Python |
|---|---|---|
| Open a CSV | `df <- read_csv("data.csv")` | `df = pd.read_csv("data.csv")` |
| Save a CSV | `write_csv(df, "out.csv")` | `df.to_csv("out.csv", index=False)` |
| Open a Stata file | `df <- haven::read_dta("data.dta")` | `df = pd.read_stata("data.dta")` |
| Columns and types | `glimpse(df)` | `df.info()` |
| First rows | `head(df)` | `df.head()` |
| Summary statistics | `summary(df)` | `df.describe()` |
| Rows and columns | `dim(df)` | `df.shape` |
| One column | `df$x` | `df["x"]` |
| First row | `df[1, ]` | `df.iloc[0]` |
| Frequency table | `count(df, x)` | `df["x"].value_counts()` |
| Count missing | `sum(is.na(df$x))` | `df["x"].isna().sum()` |

## dplyr verbs

| Task | R | Python |
|---|---|---|
| Keep rows | `filter(df, x > 0)` | `df[df["x"] > 0]` |
| Keep rows, two conditions | `filter(df, x > 0, y < 5)` | `df[(df["x"] > 0) & (df["y"] < 5)]` |
| Keep rows in a list | `filter(df, state %in% c("CA", "NY"))` | `df[df["state"].isin(["CA", "NY"])]` |
| Drop missing | `filter(df, !is.na(x))` | `df.dropna(subset=["x"])` |
| Keep columns | `select(df, id, x)` | `df[["id", "x"]]` |
| Drop a column | `select(df, -x)` | `df.drop(columns="x")` |
| Rename | `rename(df, new = old)` | `df.rename(columns={"old": "new"})` |
| New column | `mutate(df, z = x + y)` | `df["z"] = df["x"] + df["y"]` |
| If/else column | `mutate(df, z = if_else(x > 0, 1, 0))` | `df["z"] = np.where(df["x"] > 0, 1, 0)` |
| Sort | `arrange(df, id, year)` | `df.sort_values(["id", "year"])` |
| Sort descending | `arrange(df, desc(x))` | `df.sort_values("x", ascending=False)` |
| Remove duplicates | `distinct(df)` | `df.drop_duplicates()` |

??? note "What about the pipe?"
    pandas chains methods with dots instead of `%>%`. Wrap the chain in brackets to spread it over several lines:

    ```python
    result = (
        df
        .query("x > 0")
        .sort_values("year")
        .head(10)
    )
    ```

## Work by group

| Task | R | Python |
|---|---|---|
| One row per group | `summarise(df, m = mean(x), .by = state)` | `df.groupby("state", as_index=False)["x"].mean()` |
| Several statistics | `summarise(df, m = mean(x), n = n(), .by = state)` | `df.groupby("state", as_index=False).agg(m=("x", "mean"), n=("x", "size"))` |
| Group mean on every row | `mutate(df, m = mean(x), .by = state)` | `df["m"] = df.groupby("state")["x"].transform("mean")` |
| Previous value in group | `mutate(df, lag_x = lag(x), .by = id)` | `df["lag_x"] = df.groupby("id")["x"].shift(1)` |
| Running total in group | `mutate(df, cx = cumsum(x), .by = id)` | `df["cx"] = df.groupby("id")["x"].cumsum()` |
| Count by group | `count(df, state)` | `df["state"].value_counts()` |

## Joins and reshaping

| Task | R | Python |
|---|---|---|
| Left join | `left_join(df, other, by = "id")` | `df.merge(other, on="id", how="left")` |
| Inner join | `inner_join(df, other, by = "id")` | `df.merge(other, on="id", how="inner")` |
| Full join | `full_join(df, other, by = "id")` | `df.merge(other, on="id", how="outer")` |
| Stack rows | `bind_rows(df, other)` | `pd.concat([df, other], ignore_index=True)` |
| Wide to long | `pivot_longer(df, -id, names_to = "year", values_to = "inc")` | `df.melt(id_vars="id", var_name="year", value_name="inc")` |
| Long to wide | `pivot_wider(df, names_from = year, values_from = inc)` | `df.pivot(index="id", columns="year", values="inc").reset_index()` |

## Text and dates

| Task | R | Python |
|---|---|---|
| Contains text | `str_detect(s, "abc")` | `df["s"].str.contains("abc")` |
| Replace text | `str_replace_all(s, "a", "b")` | `df["s"].str.replace("a", "b")` |
| Lower case | `str_to_lower(s)` | `df["s"].str.lower()` |
| First 3 characters | `str_sub(s, 1, 3)` | `df["s"].str[:3]` |
| Text to number | `as.numeric(x)` | `pd.to_numeric(df["x"], errors="coerce")` |
| Text to date | `lubridate::ymd(s)` | `pd.to_datetime(df["s"])` |
| Year from a date | `lubridate::year(d)` | `df["d"].dt.year` |

## Regressions

| Task | R (fixest) | Python (pyfixest) |
|---|---|---|
| OLS | `fit <- feols(y ~ x, data = df)` | `fit = pf.feols("y ~ x", data=df)` |
| Robust standard errors | `feols(y ~ x, data = df, vcov = "hetero")` | `pf.feols("y ~ x", data=df, vcov="hetero")` |
| Clustered standard errors | `feols(y ~ x, data = df, cluster = ~state)` | `pf.feols("y ~ x", data=df, vcov={"CRV1": "state"})` |
| Fixed effects | `feols(y ~ x | id + year, data = df)` | `pf.feols("y ~ x | id + year", data=df)` |
| Instrumental variables | `feols(y ~ 1 | x ~ z, data = df)` | `pf.feols("y ~ 1 | x ~ z", data=df)` |
| Show results | `summary(fit)` | `fit.summary()` |
| Coefficients | `coef(fit)` | `fit.coef()` |
| Table of models | `etable(m1, m2)` | `pf.etable([m1, m2])` |

## Charts

| Task | R (ggplot2) | Python (seaborn) |
|---|---|---|
| Scatter | `ggplot(df, aes(x, y)) + geom_point()` | `sns.scatterplot(data=df, x="x", y="y")` |
| Line by group | `ggplot(df, aes(year, y, colour = state)) + geom_line()` | `sns.lineplot(data=df, x="year", y="y", hue="state")` |
| Histogram | `ggplot(df, aes(x)) + geom_histogram()` | `sns.histplot(data=df, x="x")` |
| Fitted line | `+ geom_smooth(method = "lm")` | `sns.regplot(data=df, x="x", y="y")` |
| Save | `ggsave("fig.png")` | `plt.savefig("fig.png", dpi=300)` |
