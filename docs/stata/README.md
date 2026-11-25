# Stata

Stata is the most common software in applied economics. It is built for one job, analyzing a dataset, and does it with short, readable commands. Most economics papers, replication packages and research-assistant jobs use it.

!!! info "What you will learn"
    The Stata window · do-files · the one syntax pattern behind every command · variables and labels · locals and loops · regressions, panels and IV · publication tables and graphs · fixing common errors

    Every example uses data that ships with Stata, so you can run it straight away. Looking for a command you know in R or Python? See [Coming from Stata](../coming-from/stata.md).

## Get Stata

- **Through your university.** Most economics departments have a license. Ask your department or IT service. Students can also buy a discounted license through [Stata's student pricing](https://www.stata.com/order/new/edu/gradplans/student-pricing/).
- **Editions.** BE (Basic Edition) handles most coursework. SE and MP allow more variables and run faster on big data. Code is the same in all three.

## The Stata window

| Window | What it does |
|---|---|
| **Command** | Type one command and press Enter. Good for quick checks. |
| **Results** | Output appears here |
| **Variables** | Every variable in the dataset. Click one to see its label and type. |
| **Review** | Commands you have run. Click one to run it again. |
| **Do-file Editor** | Where you write scripts. Open it with ++cmd+9++ (Mac) or ++ctrl+9++ (Windows). |

!!! tip "Always work in a do-file"
    Typing in the Command window is fine for a quick look, but anything you want to keep goes in a do-file. A do-file is a record of every step, so you or anyone else can rerun the whole analysis. Start from the [do-file template](../templates/stata.md).

    In the Do-file Editor, select lines and press ++cmd+shift+d++ (Mac) or ++ctrl+d++ (Windows) to run them.

## The one pattern behind every command

Almost every Stata command follows the same pattern:

```text
command  varlist  if condition  in range,  options
```

| Part | Example | Meaning |
|---|---|---|
| `command` | `summarize` | What to do |
| `varlist` | `wage hours` | Which variables. Leave it out to use all of them. |
| `if` | `if union == 1` | Only rows where the condition is true |
| `in` | `in 1/100` | Only rows 1 to 100 |
| `, options` | `, detail` | Extra settings, always after a comma |

So `summarize wage if union == 1, detail` reads as: summarize wage, for union members, with extra detail. Once you know this pattern you can guess how most commands work.

!!! note "`=` versus `==`"
    One `=` assigns a value: `gen x = 5`. Two `==` test for equality: `if x == 5`. Mixing them up is the most common beginner error.

## Your first session

`nlsw88` is a built-in dataset of 2,246 American women in 1988.

```stata
sysuse nlsw88, clear          // load built-in data
describe                      // variables, types and labels
summarize wage                // mean, SD, min, max
summarize wage if union == 1  // same, for union members
tabulate race, missing        // counts, including missing values
tabulate union collgrad, row  // two-way table with row percentages
histogram wage, percent       // distribution of wages
```

Run each line and read the output before moving on. **Check:** the average wage is about **$7.77** an hour.

## Create and label variables

```stata
gen ln_wage = ln(wage)
gen high_earner = (wage > 15) if !missing(wage)
egen mean_wage_ind = mean(wage), by(industry)
```

- `gen` makes a new variable. `replace` changes an existing one.
- `egen` ("extended generate") does group calculations: means, totals, counts and ranks.
- `(wage > 15)` is 1 if true and 0 if false. The `if !missing(wage)` part matters, because Stata treats missing as a very large number. Without it, people with no wage would count as high earners.

**Labels** make output readable and tables publication-ready:

```stata
label variable ln_wage "Log hourly wage"

label define yesno 0 "No" 1 "Yes"     // create a set of value labels
label values high_earner yesno        // attach it to a variable
tabulate high_earner                  // now shows "No" and "Yes"
```

## Factor variables

Put `i.` before a categorical variable and Stata makes the dummies for you. Use `c.` for continuous variables and `#` or `##` for interactions.

| You write | Stata includes |
|---|---|
| `i.race` | A dummy for each race, leaving out the first as the base |
| `ib2.race` | The same, with category 2 as the base |
| `c.age#c.age` | Age squared |
| `i.collgrad#i.union` | Only the interaction terms |
| `i.collgrad##i.union` | Both main effects **and** the interaction |

You never need `tab race, gen(race_)` for a regression.

## Locals, loops and stored results

A **local** stores text or a number for later use. Put it in `` `name' `` (a backtick, then a straight quote) to use it.

```stata
local controls "age tenure i.race"
regress ln_wage collgrad `controls', vce(robust)
```

**Loops** repeat a command:

```stata
foreach v of varlist wage hours tenure {
    quietly summarize `v'
    display "`v': mean = " %6.2f r(mean)
}

forvalues g = 1/3 {
    quietly count if race == `g'
    display "race `g': " r(N)
}
```

**Stored results.** Commands leave their results in memory. `return list` shows what a command like `summarize` stored in `r()`. `ereturn list` shows what an estimation command like `regress` stored in `e()`.

```stata
regress ln_wage collgrad age tenure i.race, vce(robust)
display "Return to college: " %5.3f _b[collgrad]    // a coefficient
display "Observations: " e(N)                      // sample size
```

**Check:** the college coefficient is **0.385**, using 2,231 observations.

??? note "Globals"
    A **global** works like a local but lasts for the whole Stata session and is used with `$name`. The [template](../templates/stata.md) uses globals for folder paths. For everything else, prefer locals: a global set in one do-file can silently change another.

## Regression

```stata
regress ln_wage collgrad age tenure i.race, vce(robust)
```

| Option | Standard errors |
|---|---|
| (none) | Classical. Rarely appropriate. |
| `vce(robust)` | Robust to heteroskedasticity. A sensible default. |
| `vce(cluster state)` | Clustered by group. Use it when observations in a group are related. |

### After the regression

```stata
regress ln_wage i.collgrad##i.union age tenure, vce(robust)

margins collgrad#union        // predicted log wage for each group
test 1.collgrad 1.union       // are both coefficients zero?
predict yhat                  // fitted values
predict resid, residuals      // residuals
```

## Panel data

A panel follows the same units over time. `nlswork` follows young women from 1968 to 1988.

```stata
webuse nlswork, clear
xtset idcode year             // declare the person and time variables

xtreg ln_wage tenure age c.age#c.age not_smsa south, fe vce(cluster idcode)
```

`fe` adds a fixed effect for each person, so the estimates use only changes *within* a person over time. For more than one set of fixed effects, use `reghdfe` (install with `ssc install reghdfe`, which also needs `ssc install ftools` and `ssc install require`):

```stata
reghdfe ln_wage tenure age not_smsa south, absorb(idcode year) vce(cluster idcode)
```

**Check:** the tenure coefficient is about **0.021** in both models: one more year with an employer goes with about 2% higher wages, within a person.

## Instrumental variables

```stata
webuse hsng2, clear
ivregress 2sls rent pcturban (hsngval = faminc i.region), vce(robust)
estat firststage
```

The variable in brackets (`hsngval`) is endogenous. The variables after `=` are its instruments. `estat firststage` reports first-stage F-statistics. A common rule of thumb treats an F below 10 as a sign of weak instruments.

## Difference-in-differences

The basic two-group, two-period design is a regression with an interaction. Replace the names with your own variables:

```stata
* treated = 1 for the treatment group, post = 1 after the policy
regress y i.treated##i.post, vce(cluster state)

* With many groups and periods: two-way fixed effects
reghdfe y treated_post, absorb(state year) vce(cluster state)
```

The coefficient on `1.treated#1.post`, or on `treated_post`, is the difference-in-differences estimate.

!!! warning "Staggered treatment timing"
    If units are treated at different times, two-way fixed effects can give misleading answers. Look into `csdid` or `did_imputation` and read [The Mixtape's DiD chapter](https://mixtape.scunning.com/09-difference_in_differences) before you rely on it.

## Tables

`esttab` (install with `ssc install estout`) turns stored regressions into a table:

```stata
sysuse nlsw88, clear
gen ln_wage = ln(wage)

eststo clear
eststo m1: regress ln_wage collgrad, vce(robust)
eststo m2: regress ln_wage collgrad age tenure i.race, vce(robust)

esttab m1 m2, se r2 label keep(collgrad age tenure) star(* 0.10 ** 0.05 *** 0.01)
esttab m1 m2 using "table1.tex", se r2 label booktabs replace
```

Stata 17 and later also have a built-in `etable`:

```stata
etable, estimates(m1 m2) keep(collgrad age tenure) export(table1.docx, replace)
```

Drop the `.tex` file straight into a LaTeX paper. See [LaTeX tables](../latex/README.md#tables).

## Graphs

```stata
twoway (scatter ln_wage tenure, mcolor(%20)) (lfit ln_wage tenure), ///
    xtitle("Years with employer") ytitle("Log hourly wage") legend(off)
graph export "wage_tenure.png", replace width(2000)
```

- `twoway` layers plots: scatter, line, fitted line, confidence band.
- `///` continues a command on the next line in a do-file.
- `%20` sets 20% opacity, so crowded scatter plots stay readable.
- `binscatter ln_wage tenure` (install with `ssc install binscatter`) averages the y-variable within bins of x. It is clearer than a scatter plot with thousands of points.
- `set scheme s1color` or `set scheme stcolor` (Stata 18) changes the look of every graph.

## Common errors

| Error | What it means | Fix |
|---|---|---|
| `variable x not found` r(111) | No variable has that name | Check spelling with `describe`. Variable names are case-sensitive. |
| `invalid syntax` r(198) | Stata could not read the command | Look for a missing comma before options, a stray bracket, or `=` instead of `==` |
| `variable x already defined` r(110) | `gen` with a name that exists | Use `replace`, or `drop x` first |
| `no observations` r(2000) | Nothing left after the `if` condition | Check the condition with `count if ...` |
| `file not found` r(601) | Wrong path or file name | Check the path, or `cd` to the project folder |
| `not sorted` r(5) | `by` needs sorted data | Use `bysort` instead of `by` |
| `no; dataset in memory has changed` r(4) | Unsaved changes | Add `, clear` to `use` or `sysuse` |
| `command x is unrecognized` r(199) | Typo, or a user-written package that is not installed | Check spelling, or `ssc install x` |

## Get help

- `help regress` opens the manual entry for any command. Scroll to the **Examples** section.
- `search difference in differences` searches the manuals and online resources.
- [Statalist](https://www.statalist.org/) is the official forum. Read the FAQ before posting, and include your code and output.
- The [Resources](../resources/index.md#stata) page lists the best free guides.

## Practice

- Work through [Project 1](../projects/wages.md) in Stata.
- Pick a [Wooldridge dataset](../data/datasets.md#built-into-your-software) and reproduce a textbook regression.
