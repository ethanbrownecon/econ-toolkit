# Project 1: Wages and education

Does more education mean higher wages? In this project you load a small survey dataset, clean it, explore it, and run your first wage regression. Every step is shown in Stata, R and Python. Pick one language in any tab and the whole page follows.

!!! info "What you will practice"
    Loading a CSV · looking at data · removing duplicates · fixing text · handling missing values · creating variables · summary statistics · a chart · a regression · saving results

    **Time:** about 45 minutes. **You need:** Stata, R or Python installed. See [VS Code](../vscode/README.md) to set up.

## The data

The file has 1,008 rows, one per person, from a made-up labor-force survey.

[:material-download: Download wages.csv](data/wages.csv){ .md-button .md-button--primary download }

| Column | Meaning |
|---|---|
| `id` | Person ID |
| `age` | Age in years |
| `sex` | Male or female |
| `educ` | Years of education (12 = high school, 16 = college degree) |
| `state` | US state |
| `union` | 1 if in a union, 0 if not |
| `hours` | Usual hours worked per week |
| `wage` | Hourly wage in dollars |

!!! warning "This is practice data"
    The data are simulated, not real survey responses. They contain deliberate problems for you to find and fix, just like real data. Do not cite the results.

## Step 1: Load the data

The code reads the file straight from this website, so you do not need to download it first.

=== "Stata"

    ```stata
    import delimited "https://ethanbrownecon.github.io/econ-toolkit/projects/data/wages.csv", clear
    ```

=== "R"

    ```r
    library(tidyverse)
    library(fixest)

    df <- read_csv("https://ethanbrownecon.github.io/econ-toolkit/projects/data/wages.csv")
    ```

=== "Python"

    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import pyfixest as pf
    import seaborn as sns

    df = pd.read_csv("https://ethanbrownecon.github.io/econ-toolkit/projects/data/wages.csv")
    ```

## Step 2: Look before you touch

Always look at new data before changing it. You are checking three things: what the columns are, what the values look like, and whether anything looks wrong.

=== "Stata"

    ```stata
    describe            // columns and types
    list in 1/5         // first five rows
    summarize           // mean, min, max of every number column
    tabulate sex        // every value of sex and how often it appears
    ```

=== "R"

    ```r
    glimpse(df)         # columns and types
    head(df, 5)         # first five rows
    summary(df)         # mean, min, max of every column
    count(df, sex)      # every value of sex and how often it appears
    ```

=== "Python"

    ```python
    df.info()                    # columns and types
    df.head(5)                   # first five rows
    df.describe()                # mean, min, max of every number column
    df["sex"].value_counts()     # every value of sex and how often it appears
    ```

??? question "What problems can you spot? Think first, then click."
    1. **`sex` has six spellings:** `Male`, `male`, `MALE`, `Female`, `female` and `FEMALE`. They should be two.
    2. **`wage` has missing values.** Its count is lower than the other columns.
    3. **The minimum `wage` is negative.** Nobody earns −$1 an hour, so that is a data-entry error.
    4. **Some rows are duplicates.** You cannot see this yet. Step 3 checks for it.

## Step 3: Clean the data

Clean one problem at a time and check the row count after each step.

### Remove duplicate rows

=== "Stata"

    ```stata
    duplicates report
    duplicates drop
    count
    ```

=== "R"

    ```r
    sum(duplicated(df))
    df <- distinct(df)
    nrow(df)
    ```

=== "Python"

    ```python
    df.duplicated().sum()
    df = df.drop_duplicates()
    len(df)
    ```

**Check:** 8 duplicates removed. You should have **1,000** rows.

### Fix the text in `sex`

Make every value lower case, so `Male`, `male` and `MALE` all become `male`.

=== "Stata"

    ```stata
    replace sex = lower(sex)
    tabulate sex
    ```

=== "R"

    ```r
    df <- mutate(df, sex = str_to_lower(sex))
    count(df, sex)
    ```

=== "Python"

    ```python
    df["sex"] = df["sex"].str.lower()
    df["sex"].value_counts()
    ```

**Check:** only two values are left, `female` and `male`.

### Drop missing and impossible wages

=== "Stata"

    ```stata
    misstable summarize
    drop if missing(wage)
    drop if wage <= 0
    count
    ```

=== "R"

    ```r
    colSums(is.na(df))
    df <- filter(df, !is.na(wage), wage > 0)
    nrow(df)
    ```

=== "Python"

    ```python
    df.isna().sum()
    df = df.dropna(subset=["wage"])
    df = df[df["wage"] > 0]
    len(df)
    ```

**Check:** 25 missing and 4 impossible wages removed. You should have **971** rows.

!!! tip "Write down what you dropped"
    In a real project, note every row you remove and why: "Dropped 25 people with no wage and 4 with a wage of zero or less." Your reader needs to know.

## Step 4: Create new variables

| New variable | Why |
|---|---|
| `ln_wage` | The log of wage. Economists use it because a coefficient then reads as an approximate percentage change. |
| `exper` | Potential experience: years since leaving school, `age − educ − 6`. |
| `female` | A dummy: 1 for women, 0 for men. Regressions need numbers, not text. |

=== "Stata"

    ```stata
    gen ln_wage = ln(wage)
    gen exper   = age - educ - 6
    gen female  = (sex == "female")
    ```

=== "R"

    ```r
    df <- mutate(df,
      ln_wage = log(wage),
      exper   = age - educ - 6,
      female  = as.integer(sex == "female")
    )
    ```

=== "Python"

    ```python
    df["ln_wage"] = np.log(df["wage"])
    df["exper"]   = df["age"] - df["educ"] - 6
    df["female"]  = (df["sex"] == "female").astype(int)
    ```

## Step 5: Summary statistics

=== "Stata"

    ```stata
    summarize wage educ exper
    tabstat wage, by(sex) statistics(mean median n)
    ```

=== "R"

    ```r
    summary(select(df, wage, educ, exper))
    summarise(df, mean = mean(wage), median = median(wage), n = n(), .by = sex)
    ```

=== "Python"

    ```python
    df[["wage", "educ", "exper"]].describe()
    df.groupby("sex")["wage"].agg(["mean", "median", "count"])
    ```

**Check:** the average wage is about **$24.35**. Women average about **$22.76** and men about **$25.89**.

## Step 6: Make a chart

A scatter plot of log wage against education, with a fitted line.

=== "Stata"

    ```stata
    twoway (scatter ln_wage educ, msize(small) mcolor(%30)) (lfit ln_wage educ), ///
        xtitle("Years of education") ytitle("Log hourly wage") legend(off)
    ```

=== "R"

    ```r
    ggplot(df, aes(educ, ln_wage)) +
      geom_jitter(width = 0.2, alpha = 0.3) +
      geom_smooth(method = "lm") +
      labs(x = "Years of education", y = "Log hourly wage")
    ```

=== "Python"

    ```python
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.regplot(data=df, x="educ", y="ln_wage", x_jitter=0.2, scatter_kws={"alpha": 0.3}, ax=ax)
    ax.set(xlabel="Years of education", ylabel="Log hourly wage")
    plt.show()
    ```

The line slopes upward: people with more education tend to earn more.

## Step 7: Run a regression

This is a classic Mincer wage equation. It estimates the return to a year of education while holding experience, sex and union status constant. `vce(robust)` and `"hetero"` give robust standard errors.

=== "Stata"

    ```stata
    regress ln_wage educ c.exper##c.exper female union, vce(robust)
    ```

=== "R"

    ```r
    model <- feols(ln_wage ~ educ + exper + I(exper^2) + female + union,
                   data = df, vcov = "hetero")
    summary(model)
    ```

=== "Python"

    ```python
    model = pf.feols("ln_wage ~ educ + exper + I(exper**2) + female + union",
                     data=df, vcov="hetero")
    model.summary()
    ```

**Check:** you should get these numbers, give or take rounding.

| Variable | Coefficient | What it means |
|---|---:|---|
| `educ` | 0.090 | One more year of education goes with about **9% higher** wages |
| `exper` | 0.034 | Wages rise with experience... |
| `exper²` | −0.0005 | ...but more slowly as experience grows |
| `female` | −0.137 | Women earn about **13% less** than similar men in this data |
| `union` | 0.100 | Union members earn about **10% more** |

??? note "Why “about 9%” and not exactly 9%?"
    With a log outcome, a coefficient *b* means a change of (e<sup>b</sup> − 1) × 100 percent. For small *b* that is close to *b* × 100. For `female`, e<sup>−0.137</sup> − 1 = −12.8%, so "about 13% less".

## Step 8: Save your work

=== "Stata"

    ```stata
    save "wages_clean.dta", replace
    graph export "wage_educ.png", replace
    ```

=== "R"

    ```r
    write_csv(df, "wages_clean.csv")
    ggsave("wage_educ.png", width = 6, height = 4, dpi = 300)
    etable(model, tex = TRUE, file = "wage_regression.tex", replace = TRUE)
    ```

=== "Python"

    ```python
    df.to_csv("wages_clean.csv", index=False)
    fig.savefig("wage_educ.png", dpi=300, bbox_inches="tight")
    open("wage_regression.tex", "w").write(pf.etable([model], type="tex"))
    ```

Next, move this code into a proper script using the [templates](../templates/index.md), so you can rerun everything with one click.

## Try it yourself

Answer each question with code, then open the answer to check.

**1. Which state has the highest average wage?**

??? success "Answer"

    === "Stata"

        ```stata
        tabstat wage, by(state) statistics(mean)
        ```

    === "R"

        ```r
        df %>% summarise(mean_wage = mean(wage), .by = state) %>% arrange(desc(mean_wage))
        ```

    === "Python"

        ```python
        df.groupby("state")["wage"].mean().sort_values(ascending=False)
        ```

    Michigan, at about $25.39.

**2. What share of workers are in a union?**

??? success "Answer"

    === "Stata"

        ```stata
        summarize union
        ```

    === "R"

        ```r
        mean(df$union)
        ```

    === "Python"

        ```python
        df["union"].mean()
        ```

    About 0.12, or 12%. The mean of a 0/1 dummy is the share of 1s.

**3. Add state fixed effects to the regression. Does the education coefficient change?**

??? success "Answer"

    === "Stata"

        ```stata
        regress ln_wage educ c.exper##c.exper female union i.state, vce(robust)
        ```

    === "R"

        ```r
        feols(ln_wage ~ educ + exper + I(exper^2) + female + union | state,
              data = df, vcov = "hetero")
        ```

    === "Python"

        ```python
        pf.feols("ln_wage ~ educ + exper + I(exper**2) + female + union | state",
                 data=df, vcov="hetero").summary()
        ```

    It barely moves, staying close to 0.09. In this data, state does not explain the link between education and wages.

## What you learned

- [x] Load a CSV from a web address
- [x] Inspect data before changing it
- [x] Remove duplicates, fix text and drop bad values, checking the row count each time
- [x] Create log, difference and dummy variables
- [x] Summarize by group, chart a relationship and run a regression with robust standard errors
- [x] Interpret coefficients when the outcome is a log
