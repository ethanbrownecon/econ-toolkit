# Troubleshooting

Everyone's code breaks. The difference between beginners and experienced researchers is not fewer errors, but a routine for fixing them. This page gives you that routine, then the errors students hit most often, grouped by tool.

## A five-step routine for any error

1. **Read the whole error message.** The last line usually says what went wrong. Look for a line number, a variable name or a file name.
2. **Find the exact line.** Run your script one section at a time until you find the line that fails.
3. **Check what you think is true.** Print the data, the column names, the number of rows, or the value of a variable right before the failing line. Most bugs are a wrong assumption: a column you thought existed, a filter that removed every row.
4. **Search the exact message.** Paste the error, in quotes, into a search engine. Remove anything specific to you, such as your file names.
5. **Make a small example and ask.** Cut the problem down to a few lines and a few rows of data that still show the error. Often you find the bug while doing this. If not, post it to a [forum](resources/index.md#where-to-ask-for-help).

!!! tip "Restart and run from the top"
    Many confusing problems come from leftover objects or data in memory. Restart Stata, R or Python and run the script from the first line. If it now fails earlier, or works, that tells you a lot.

## Errors in every language

| Symptom | Likely cause | Fix |
|---|---|---|
| "File not found" or "No such file or directory" | The working directory is not your project folder, or the path is wrong | Print the working directory: `pwd` in Stata, `getwd()` in R, `import os; os.getcwd()` in Python. Use paths relative to the project folder, as in the [templates](templates/index.md). |
| A package or command "not found" | It is not installed, or not loaded | Install it once (`ssc install`, `install.packages()`, `pip install`), and load it in your script (`library()`, `import`) |
| "Variable" or "column not found" | Typo, wrong capitals, or the column has a different name than you think | List the names: `describe`, `names(df)`, `df.columns` |
| Numbers stored as text | The file had commas, `$` signs or notes like "N/A" in a number column | Convert: `destring x, replace ignore(",$")`, `parse_number()`, `pd.to_numeric(..., errors="coerce")` |
| Results suddenly have far fewer rows | A filter or merge dropped rows silently, often because of missing values | Count rows after every step. Check missing values first. |
| Row count jumps after a merge | Duplicate keys in one of the files | Check keys are unique before merging. See [Coming from Stata](coming-from/stata.md#merge-append-and-reshape). |
| Strange characters (`Ã©`, `Â£`) | The file's text encoding was misread | Read with UTF-8: `import delimited ..., encoding("utf-8")`, `read_csv(locale = locale(encoding = "UTF-8"))`, `pd.read_csv(..., encoding="utf-8")` |
| Code works on your computer but not a classmate's | Absolute paths, or different package versions | Use relative paths and record package versions. See [reproducible research](reproducible-research/README.md). |

## Stata

| Error | Fix |
|---|---|
| `variable x not found` r(111) | Check spelling with `describe`. Names are case-sensitive. |
| `invalid syntax` r(198) | Look for a missing comma before options, `=` instead of `==`, or an unmatched bracket |
| `variable x already defined` r(110) | Use `replace`, or `drop x` first |
| `no observations` r(2000) | Your `if` condition matches nothing. Check it with `count if ...` |
| `command x is unrecognized` r(199) | Typo, or a user-written package that is not installed: `ssc install x` |
| `reghdfe requires ... the require package` | Run `ssc install require` and `ssc install ftools` |
| A `local` is empty | Locals vanish when a do-file finishes or when you run lines one at a time. Run the whole block together. |

Full list: [Stata guide](stata/README.md#common-errors).

## R

| Error | Fix |
|---|---|
| `object 'x' not found` | Check spelling, or run the line that creates `x` |
| `could not find function "x"` | Load the package: `library(package)` |
| `there is no package called 'x'` | `install.packages("x")` |
| `unexpected symbol` or `unexpected ')'` | A missing comma, bracket or quote on that line |
| A result is `NA` | Missing values: add `na.rm = TRUE` |
| `cannot open the connection` when reading a URL | The website blocks R's downloader. Use `download.file()` to save it first, then read the file. |

Full list: [R guide](r/README.md#common-errors).

## Python

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'x'` | `pip install x` in the **same** environment. In VS Code, check the interpreter shown in the status bar. |
| `KeyError: 'x'` | No column named `x`. Check `df.columns`. |
| `NameError: name 'x' is not defined` | Run the cell or line that creates `x` |
| `IndentationError` | Use four spaces per level, consistently |
| `SettingWithCopyWarning` | Add `.copy()` when you make a subset: `sub = df[df["x"] > 0].copy()` |
| `HTTPError: 403 Forbidden` when reading a URL | The website blocks Python's default downloader. Pass a browser-like header, for example `storage_options={"User-Agent": "Mozilla/5.0"}` in `pd.read_csv`. |

Full list: [Python guide](python/README.md#common-errors).

## Regressions that look wrong

| Symptom | Likely cause |
|---|---|
| A variable is dropped from the regression | It is perfectly collinear with others, or with the fixed effects. See [fixed effects](econometrics/panel.md). |
| Standard errors are huge | Very few observations, almost no variation in x, or highly correlated regressors |
| A coefficient has the "wrong" sign | Omitted variables, a bad control, or reverse causality. Think about the design before the code. See [linear regression](econometrics/ols.md#common-mistakes). |
| Results differ slightly between Stata, R and Python | Different default standard errors, small-sample corrections or tie-breaking. Check the options match. Small differences are normal. |
| A logit "does not converge" or says outcomes are "perfectly predicted" | Some variable separates the outcome perfectly. Look for a category where everyone is 0 or everyone is 1. |

## Git and GitHub

| Problem | Fix |
|---|---|
| `rejected ... (fetch first)` when pushing | Someone else pushed first. Run `git pull`, fix any conflicts, then push again. |
| Merge conflict markers (`<<<<<<<`) in a file | Edit the file to keep the right version, delete the markers, then `git add` and `git commit` |
| You committed a large data file or a password | Do not push. Remove it from the commit and add it to `.gitignore`. If it was already pushed, treat a password as leaked: change it. |
| `fatal: not a git repository` | You are not inside the project folder. `cd` into it. |

More in [Git & GitHub](git-github/README.md).

## VS Code

| Problem | Fix |
|---|---|
| Code runs with the wrong Python | Command Palette → **Python: Select Interpreter** → choose your `.venv` |
| R code does not run | Install the R extension and run `install.packages("languageserver")` in R |
| The terminal opens in the wrong folder | Use **File → Open Folder** on the project folder, not a single file |
| LaTeX does not build | Install a TeX distribution (MacTeX or MiKTeX) and the LaTeX Workshop extension |

More in [VS Code](vscode/README.md).

## Still stuck?

- Ask a classmate to read your code out loud with you. Explaining it often reveals the bug.
- Post a small, reproducible example to a [help forum](resources/index.md#where-to-ask-for-help).
- Found a mistake on this site? [Open an issue](https://github.com/ethanbrownecon/econ-toolkit/issues/new/choose).
