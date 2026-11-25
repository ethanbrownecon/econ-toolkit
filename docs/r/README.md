# R for econometrics

R is a free language for statistics and data analysis. With the **tidyverse** for data work, **fixest** for regressions and **ggplot2** for charts, it covers everything Stata does and makes some of the best charts in economics.

!!! info "What you will learn"
    Setting up R · objects and functions · packages · the tidyverse pipe and verbs · regressions with robust and clustered errors · panels, IV and difference-in-differences · regression tables · ggplot2 charts · fixing common errors

    Examples use the `wooldridge` package, which contains every dataset from Wooldridge's *Introductory Econometrics*. Looking for a translation from Stata? See [Coming from Stata](../coming-from/stata.md).

## Set up

1. Install R from [CRAN](https://cloud.r-project.org/).
2. Install an editor: [RStudio](https://posit.co/download/rstudio-desktop/) is the standard for R. [VS Code](../vscode/README.md) with the R extension also works.
3. Install the packages used on this page. Run this once:

```r
install.packages(c("tidyverse", "fixest", "modelsummary", "marginaleffects", "wooldridge", "here"))
```

!!! tip "Use an RStudio Project"
    **File → New Project** creates a project folder with an `.Rproj` file. Opening that file starts R in the right folder every time. Combined with `here()` (see the [R template](../templates/r.md)), your paths work on any computer.

## R basics in five minutes

```r
x <- 5                              # store a value; <- is "gets"
wages <- c(12.5, 18.0, 22.3)        # c() combines values into a vector
mean(wages)                         # a function: name(arguments)
wages * 2                           # maths works on the whole vector
```

| Idea | What it means |
|---|---|
| **Object** | Anything you store with `<-`: a number, a vector, a dataset, a model |
| **Vector** | A column of values of one type |
| **Data frame** (or tibble) | A table: columns are vectors of equal length |
| **Function** | Takes inputs in brackets and returns a result: `mean(x)`, `log(x)` |
| **Package** | A bundle of functions. Install once with `install.packages()`, load each session with `library()`. |
| **`NA`** | A missing value. Most functions need `na.rm = TRUE` to skip it. |
| **Help** | `?mean` opens the help page for `mean` |

## Load data

```r
library(tidyverse)

df <- read_csv("data/raw/survey.csv")                  # CSV
df <- haven::read_dta("data/raw/survey.dta")           # Stata file
df <- readxl::read_excel("data/raw/survey.xlsx")       # Excel

data("wage1", package = "wooldridge")                 # textbook data
df <- as_tibble(wage1)
```

## The tidyverse way

The **pipe** `%>%` passes the result of one step into the next. Read it as "and then". R 4.1+ also has a built-in pipe, `|>`, which works the same way for most code.

```r
df %>%
  filter(female == 1) %>%                    # keep women, and then
  summarise(mean_wage = mean(wage), n = n()) # average their wages
```

Five verbs do most data work:

| Verb | What it does | Example |
|---|---|---|
| `filter()` | Keep rows | `filter(df, educ >= 16)` |
| `select()` | Keep columns | `select(df, wage, educ, female)` |
| `mutate()` | Add or change columns | `mutate(df, lwage = log(wage))` |
| `summarise()` | Collapse to summary statistics | `summarise(df, avg = mean(wage), .by = female)` |
| `arrange()` | Sort | `arrange(df, desc(wage))` |

The [Coming from Stata](../coming-from/stata.md) page has the full list, including joins and reshaping.

### Factors

A **factor** is R's categorical variable. Regressions treat factors as a set of dummies automatically.

```r
df <- df %>%
  mutate(sex = factor(female, levels = c(0, 1), labels = c("Male", "Female")))
count(df, sex)
```

## Regression

Base R has `lm()`. For robust and clustered standard errors, fixed effects and IV, use **fixest**: it is fast and uses one consistent syntax.

```r
library(fixest)

m1 <- feols(lwage ~ educ + exper + tenure + female, data = df, vcov = "hetero")
summary(m1)
```

**Check:** the education coefficient is **0.087**: one more year of school goes with about 9% higher wages.

| Standard errors | Argument |
|---|---|
| Classical | `vcov = "iid"` |
| Robust (heteroskedasticity) | `vcov = "hetero"` |
| Clustered | `cluster = ~state` |
| Two-way clustered | `cluster = ~state + year` |

The formula reads as `outcome ~ regressors`. Useful formula pieces:

| You write | Meaning |
|---|---|
| `x1 + x2` | Both variables |
| `x1 * x2` | Both, plus their interaction |
| `I(x^2)` | x squared (`I()` means "do this maths") |
| `i(state)` or `factor(state)` | Dummies for each state |
| `log(wage)` | Log, computed inside the formula |

## Panel data

Fixed effects go after a `|`. `wagepan` follows 545 young men from 1980 to 1987.

```r
data("wagepan", package = "wooldridge")

fe <- feols(lwage ~ union + married | nr + year, data = wagepan, cluster = ~nr)
summary(fe)
```

`nr + year` adds person and year fixed effects. **Check:** the union premium is about **0.083**, or 8%, *within* a person.

!!! note "Why did a variable disappear?"
    fixest drops variables that cannot be separated from the fixed effects. Experience rises by one every year for everyone, so it is collinear with person plus year effects. fixest tells you when it does this.

## Instrumental variables

Add the first stage as a third part of the formula: `outcome ~ controls | fixed effects | endogenous ~ instruments`. Use `0` or leave out the middle part when there are no fixed effects.

```r
data("card", package = "wooldridge")

iv <- feols(lwage ~ exper + expersq + black + south | educ ~ nearc4,
            data = card, vcov = "hetero")
summary(iv)
fitstat(iv, "ivf")             # first-stage F-statistic
```

Card (1995) uses growing up near a four-year college (`nearc4`) as an instrument for education. **Check:** the IV estimate is about **0.22**, and the first-stage F is about 35.

## Difference-in-differences

```r
data("kielmc", package = "wooldridge")

did <- feols(rprice ~ nearinc * y81, data = kielmc, vcov = "hetero")
summary(did)
```

Kiel and McClain study house prices near a garbage incinerator that was announced after 1978. `nearinc * y81` includes both dummies and their interaction. **Check:** the interaction is about **−11,864**: houses near the incinerator lost about $11,900 in value relative to other houses.

For many groups and periods, use two-way fixed effects: `feols(y ~ treated_post | unit + year, data = df, cluster = ~unit)`. With staggered treatment timing, see the [did](https://bcallaway11.github.io/did/) package.

## Logit and marginal effects

```r
library(marginaleffects)

logit <- feglm(I(wage > 8) ~ educ + exper + female, data = df, family = "logit")
avg_slopes(logit)              # average marginal effects
```

Logit coefficients are hard to read. `avg_slopes()` turns them into changes in probability. **Check:** one more year of education raises the chance of earning over $8 by about **5 percentage points**.

## Regression tables

```r
library(modelsummary)

modelsummary(list("OLS" = m1, "Panel FE" = fe),
             stars = TRUE, gof_map = c("nobs", "r.squared"))
```

`modelsummary` shows the table in RStudio's Viewer. Add `output = "table1.docx"` for Word or `output = "table1.html"` for a web page.

For LaTeX, fixest's own `etable` writes a file you can `\input` into a paper with no extra setup:

```r
etable(m1, fe, tex = TRUE, file = "output/tables/table1.tex", replace = TRUE)
```

## Charts with ggplot2

Every ggplot has the same three parts: **data**, **aesthetics** (which variable goes on which axis or color), and **geoms** (what to draw). Add layers with `+`.

```r
ggplot(df, aes(x = educ, y = lwage)) +
  geom_point(alpha = 0.3) +                       # scatter
  geom_smooth(method = "lm") +                    # fitted line with confidence band
  facet_wrap(~sex) +                              # one panel per group
  labs(x = "Years of education", y = "Log hourly wage",
       title = "Returns to education") +
  theme_minimal()

ggsave("output/figures/returns.png", width = 7, height = 4, dpi = 300)
```

| Geom | Chart |
|---|---|
| `geom_point()` | Scatter |
| `geom_line()` | Line, for time series |
| `geom_col()` | Bars with heights you supply |
| `geom_histogram()` | Histogram |
| `geom_boxplot()` | Box plot |
| `geom_smooth()` | Fitted line or curve |

Put a variable in `aes(colour = ...)` or `aes(fill = ...)` to color by group.

## Common errors

| Error | What it means | Fix |
|---|---|---|
| `object 'x' not found` | No object or column with that name | Check spelling and capitals. Did you run the line that creates it? |
| `could not find function "x"` | The package is not loaded | Run `library(package)` first |
| `there is no package called 'x'` | The package is not installed | `install.packages("x")` |
| `unexpected symbol` / `unexpected ')'` | A typo: a missing comma, bracket or quote | Read the line carefully. RStudio highlights matching brackets. |
| `non-numeric argument to binary operator` | Maths on text | Convert with `as.numeric()` |
| A result is `NA` | There are missing values | Add `na.rm = TRUE` |
| `could not find function "%>%"` | The tidyverse is not loaded | `library(tidyverse)` |

## Write papers in R

[Quarto](https://quarto.org/) mixes text, code and output in one document and exports to PDF, Word or slides. Your numbers and charts update automatically when the data change. See the [Markdown guide](../markdown/README.md#where-markdown-goes-next).

## Practice

- Work through [Project 1](../projects/wages.md) and the [Spotify project](../projects/spotify.md) in R.
- Read [R for Data Science](https://r4ds.hadley.nz/), the best free introduction.
- Work through [Introduction to Econometrics with R](https://www.econometrics-with-r.org/) alongside your econometrics course.
