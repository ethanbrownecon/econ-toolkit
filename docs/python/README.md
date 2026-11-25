# Python for data work

Python is a general-purpose programming language with excellent tools for data. Economists use it for cleaning large datasets, web scraping, APIs, machine learning and, increasingly, econometrics. **pandas** handles data, **pyfixest** runs regressions, and **matplotlib** and **seaborn** make charts.

!!! info "What you will learn"
    Setting up Python · core Python in ten minutes · pandas data frames · regressions with robust and clustered errors · panels, IV and difference-in-differences · regression tables · charts · fixing common errors

    Examples use the `wooldridge` package, which contains every dataset from Wooldridge's *Introductory Econometrics*. Looking for a translation from Stata or R? See [Coming from Stata](../coming-from/stata.md) or [Coming from R](../coming-from/r.md).

## Set up

1. Install Python from [python.org](https://www.python.org/downloads/). On Windows, tick **Add python.exe to PATH** during setup.
2. Install [VS Code](../vscode/README.md) with the Python and Jupyter extensions.
3. In your project folder, create a virtual environment and install the packages. The [command line guide](../command-line/README.md#python-virtual-environments) explains each step.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install pandas numpy pyfixest statsmodels matplotlib seaborn wooldridge
```

!!! tip "Scripts or notebooks?"
    **Jupyter notebooks** (`.ipynb`) show code, output and charts together, which is great for exploring. **Scripts** (`.py`) run top to bottom every time and work better with Git. A good middle ground is a `.py` script with `# %%` cells, which VS Code runs like a notebook. The [Python template](../templates/python.md) uses this.

## Python basics in ten minutes

```python
x = 5                                   # store a value
wages = [12.5, 18.0, 22.3]              # a list
person = {"name": "Ana", "wage": 18.0}  # a dictionary: look up values by key
person["wage"]                          # 18.0

def double(v):                          # define a function
    return v * 2                        # the indented lines are its body

double(4)                               # 8
```

| Idea | What it means |
|---|---|
| **Indentation** | Python uses indentation, not brackets, to group lines. Four spaces per level. |
| **Counting from 0** | The first item of a list is `wages[0]` |
| **Import** | Load a package with `import pandas as pd`. `pd` is the standard short name. |
| **Method** | A function attached to an object, called with a dot: `df.head()`, `"text".upper()` |
| **`None` / `NaN`** | Missing values. pandas uses `NaN` and skips it in `mean()`, `sum()` and similar. |
| **Help** | `help(pd.read_csv)`, or hover over a name in VS Code |

## pandas

A **DataFrame** is a table. Each column is a **Series**.

```python
import numpy as np
import pandas as pd
import wooldridge

df = wooldridge.data("wage1")          # or pd.read_csv("data/raw/file.csv")

df.shape                               # (rows, columns): (526, 24)
df.head()                              # first five rows
df["wage"]                             # one column (a Series)
df[["wage", "educ"]]                   # several columns (a DataFrame)
df.loc[df["female"] == 1, "wage"]      # rows that meet a condition, one column
df["wage"].mean()                      # a summary
```

| Load | Code |
|---|---|
| CSV | `pd.read_csv("file.csv")` |
| Stata | `pd.read_stata("file.dta")` |
| Excel | `pd.read_excel("file.xlsx")` |
| Parquet (fast, for big data) | `pd.read_parquet("file.parquet")` |

### Chaining steps

Like the pipe in R, you can chain methods. Wrap the chain in brackets to spread it over several lines:

```python
(
    df
    .query("female == 1")                           # keep women
    .assign(lwage2=lambda d: np.log(d["wage"]))     # add a column
    ["lwage2"]
    .mean()
)
```

`lambda d:` means "the data at this point in the chain". It lets `assign` use the filtered data rather than the original `df`.

### Categories

```python
df["sex"] = df["female"].map({0: "Male", 1: "Female"})
df["sex"].value_counts()
```

The [Coming from Stata](../coming-from/stata.md) page has the full list of data tasks, including group operations, merges and reshaping.

## Regression

**pyfixest** gives robust and clustered standard errors, fixed effects and IV with one consistent syntax. It copies R's fixest, so the formulas are the same in both languages.

```python
import pyfixest as pf

m1 = pf.feols("lwage ~ educ + exper + tenure + female", data=df, vcov="hetero")
m1.summary()
```

**Check:** the education coefficient is **0.087**: one more year of school goes with about 9% higher wages.

| Standard errors | Argument |
|---|---|
| Classical | `vcov="iid"` |
| Robust (heteroskedasticity) | `vcov="hetero"` |
| Clustered | `vcov={"CRV1": "state"}` |
| Two-way clustered | `vcov={"CRV1": "state+year"}` |

| Formula piece | Meaning |
|---|---|
| `x1 + x2` | Both variables |
| `x1 * x2` | Both, plus their interaction |
| `I(x**2)` | x squared |
| `C(state)` | Dummies for each state |
| `np.log(wage)` | Log, computed inside the formula |

## Panel data

Fixed effects go after a `|`. `wagepan` follows 545 young men from 1980 to 1987.

```python
wagepan = wooldridge.data("wagepan")

fe = pf.feols("lwage ~ union + married | nr + year", data=wagepan, vcov={"CRV1": "nr"})
fe.summary()
```

**Check:** the union premium is about **0.083**, or 8%, within a person.

## Instrumental variables

Put the first stage in square brackets: `outcome ~ controls + [endogenous ~ instruments] | fixed effects`.

```python
card = wooldridge.data("card")

iv = pf.feols("lwage ~ exper + expersq + black + south + [educ ~ nearc4]",
              data=card, vcov="hetero")
iv.summary()
iv.first_stage.diagnostics.f_stat      # first-stage F-statistic
```

Card (1995) uses growing up near a four-year college (`nearc4`) as an instrument for education. **Check:** the IV estimate is about **0.22**, and the first-stage F is about 37.

!!! note "Older syntax"
    You may see IV written as `y ~ controls | educ ~ nearc4`, the R fixest style. pyfixest still accepts it but has deprecated it. Use the square-bracket form in new code.

## Difference-in-differences

```python
kielmc = wooldridge.data("kielmc")

did = pf.feols("rprice ~ nearinc * y81", data=kielmc, vcov="hetero")
did.summary()
```

Kiel and McClain study house prices near a garbage incinerator that was announced after 1978. **Check:** the `nearinc:y81` coefficient is about **−11,864**: houses near the incinerator lost about $11,900 in value relative to other houses.

For many groups and periods: `pf.feols("y ~ treated_post | unit + year", data=df, vcov={"CRV1": "unit"})`. With staggered treatment timing, see pyfixest's [difference-in-differences tools](https://py-econometrics.github.io/pyfixest/).

## Logit and marginal effects

pyfixest covers linear models and Poisson. For logit and probit, use **statsmodels**:

```python
import statsmodels.formula.api as smf

df["high"] = (df["wage"] > 8).astype(int)
logit = smf.logit("high ~ educ + exper + female", data=df).fit()
logit.get_margeff().summary()          # average marginal effects
```

**Check:** one more year of education raises the chance of earning over $8 by about **5 percentage points**.

## Regression tables

```python
pf.etable([m1, fe])                                     # shows a formatted table

with open("output/tables/table1.tex", "w") as f:        # LaTeX for your paper
    f.write(pf.etable([m1, fe], type="tex"))
```

## Charts

**seaborn** makes statistical charts in one line. **matplotlib**, which seaborn is built on, gives full control.

=== "seaborn"

    ```python
    import seaborn as sns

    g = sns.lmplot(data=df, x="educ", y="lwage", col="sex",
                   scatter_kws={"alpha": 0.3}, height=4)
    g.set_axis_labels("Years of education", "Log hourly wage")
    g.savefig("output/figures/returns.png", dpi=300)
    ```

=== "matplotlib"

    ```python
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df["wage"], bins=30)
    ax.set(xlabel="Hourly wage", ylabel="Count", title="Wage distribution")
    fig.savefig("output/figures/wages.png", dpi=300, bbox_inches="tight")
    ```

| seaborn function | Chart |
|---|---|
| `sns.scatterplot()` | Scatter |
| `sns.lineplot()` | Line, with a confidence band if there are repeated values |
| `sns.barplot()` | Bars showing the mean of each group |
| `sns.histplot()` | Histogram |
| `sns.boxplot()` | Box plot |
| `sns.regplot()` / `sns.lmplot()` | Scatter with a fitted line |

Add `hue="group"` to colour by group, and `col="group"` (in `lmplot` and `relplot`) for one panel per group.

## Common errors

| Error | What it means | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'x'` | The package is not installed in this environment | `pip install x`. In VS Code, check the selected interpreter is your `.venv`. |
| `NameError: name 'x' is not defined` | Typo, or you have not run the line that creates it | Check spelling and run earlier cells |
| `KeyError: 'x'` | No column with that name | Check `df.columns`. Names are case-sensitive. |
| `IndentationError` | Inconsistent indentation | Use four spaces. VS Code can fix it with **Format Document**. |
| `TypeError: can only concatenate str (not "int") to str` | Mixing text and numbers | Convert with `str(x)` or `pd.to_numeric(col)` |
| `SettingWithCopyWarning` | Editing a slice of a DataFrame | Add `.copy()` when you create the subset: `sub = df[df["x"] > 0].copy()` |
| `ValueError: could not convert string to float` | Text in a number column | `pd.to_numeric(df["x"], errors="coerce")` turns bad values into `NaN` |

## Practise

- Work through [Project 1](../projects/wages.md) and the [Spotify project](../projects/spotify.md) in Python.
- Try the [APIs](../data/apis.md) and [web scraping](../data/scraping.md) guides. Python is especially strong at both.
- Read [Coding for Economists](https://aeturrell.github.io/coding-for-economists/) and [Python for Data Analysis](https://wesmckinney.com/book/).
