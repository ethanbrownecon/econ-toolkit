# Public economics

Public economics studies what governments do and how it changes behavior: taxes, social insurance, welfare programs, public goods and regulation. Public economists ask both "what happened?" and "what should the government do?"

## Big questions

- How do taxes change how much people work, save and spend?
- Who really pays a tax: the people it is levied on, or someone else?
- Do welfare, unemployment insurance and food assistance help, and at what cost?
- Do people respond to taxes they do not notice?
- How should laws be designed to deter harmful behavior?

## Methods you will use

[Difference-in-differences](../econometrics/did.md) · [regression discontinuity](../econometrics/rd.md) · [synthetic control](../econometrics/synthetic.md) · [linear regression](../econometrics/ols.md) with time series

## Data

| Source | What it has |
|---|---|
| [IRS Statistics of Income](https://www.irs.gov/statistics) | Tax return statistics by income, state and county |
| [NBER TAXSIM](https://taxsim.nber.org/) | Calculate federal and state taxes for any household |
| [Census of Governments](https://www.census.gov/programs-surveys/gov-finances.html) | State and local government revenue and spending |
| [IPUMS CPS](https://cps.ipums.org/) | Program participation, income and work |

## Projects on this site

- [Replication: stand your ground laws](../projects/replication-castle.md): did a change in law increase homicides?
- [Replication: drunk driving](../projects/replication-hansen.md): do harsher penalties deter?
- [Synthetic control](../econometrics/synthetic.md): California's tobacco tax and smoking

## Starter project: do tax breaks raise birth rates?

The US tax code lets parents deduct a personal exemption for each child. A bigger exemption makes children cheaper. Did the birth rate respond? `fertil3` has US data from 1913 to 1984, the data used by Whittington, Alm and Peters (1990).

| Variable | Meaning |
|---|---|
| `gfr` | Births per 1,000 women aged 15 to 44 |
| `pe` | Real value of the personal exemption, in dollars |
| `ww2` | 1 during World War II (1941–1945) |
| `pill` | 1 from 1963, after the birth control pill became available |

=== "Stata"

    ```stata
    bcuse fertil3, clear                  // ssc install bcuse
    tsset year
    twoway line gfr year
    regress gfr pe ww2 pill, vce(robust)
    ```

=== "R"

    ```r
    library(fixest)
    data("fertil3", package = "wooldridge")

    plot(fertil3$year, fertil3$gfr, type = "l")
    feols(gfr ~ pe + ww2 + pill, data = fertil3, vcov = "hetero")
    ```

=== "Python"

    ```python
    import pyfixest as pf
    import wooldridge

    fertil3 = wooldridge.data("fertil3")
    fertil3.plot(x="year", y="gfr")
    pf.feols("gfr ~ pe + ww2 + pill", data=fertil3, vcov="hetero").summary()
    ```

**Check:** the coefficient on `pe` is **0.083** (standard error 0.027). An extra $12 of exemption goes with about one more birth per 1,000 women.

!!! warning "Time series need extra care"
    Birth rates and the exemption both trend over 72 years, so they could move together for unrelated reasons. Before trusting the result, add a time trend (`year` as a regressor) or look at year-to-year changes. Wooldridge's chapters 10 and 11 work through this example.

## More project ideas

1. **Add a trend.** Include `year` and `year` squared. What happens to the effect of `pe`?
2. **Lagged effects.** Births respond with a delay. Add `pe_1` and `pe_2`, last year's and the year before's exemption.
3. **The earned income tax credit.** Use CPS data to compare work among single mothers and single women without children before and after the 1993 EITC expansion: a classic difference-in-differences.
4. **Sales tax salience.** Do shoppers react to taxes shown on the price tag more than taxes added at the register? Read Chetty, Looney and Kroft (2009) and design a test.

## Classic papers

- Whittington, Alm and Peters (1990), "Fertility and the Personal Exemption: Implicit Pronatalist Policy in the United States", *American Economic Review*
- Chetty, Looney and Kroft (2009), "Salience and Taxation: Theory and Evidence", *American Economic Review*
- Becker (1968), "Crime and Punishment: An Economic Approach", *Journal of Political Economy*
