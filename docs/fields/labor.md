# Labor economics

Labor economics studies how people work and earn: wages, employment, education and training, discrimination, unions and migration. It is the most data-driven field in economics, and many of the causal methods on this site were developed by labor economists.

## Big questions

- How much is an extra year of education worth?
- Why do women earn less than men, and how much is discrimination?
- Do minimum wages cost jobs?
- Do job-training programs work?
- How do immigration and automation affect workers?

## Methods you will use

[Linear regression](../econometrics/ols.md) · [panel fixed effects](../econometrics/panel.md) · [instrumental variables](../econometrics/iv.md) · [difference-in-differences](../econometrics/did.md) · [matching](../econometrics/matching.md)

## Data

| Source | What it has |
|---|---|
| [IPUMS CPS](https://cps.ipums.org/) | Monthly Current Population Survey microdata since 1962: wages, hours, jobs |
| [IPUMS USA](https://usa.ipums.org/) | Census and American Community Survey microdata |
| [Bureau of Labor Statistics](https://www.bls.gov/data/) | Unemployment, wages, employment by industry and area |
| [NLSY](https://www.nlsinfo.org/) | The same people followed over decades |

## Projects on this site

- [Project 1: Wages and education](../projects/wages.md): clean survey data and estimate a wage regression
- [Replication: job training](../projects/replication-lalonde.md): does training raise earnings?
- [Instrumental variables](../econometrics/iv.md): Card's estimate of the return to schooling

## Starter project: the gender wage gap

How much less do women earn than men, and how much of the gap is explained by education and experience? Use `wage1`, 526 workers from 1976.

=== "Stata"

    ```stata
    bcuse wage1, clear                    // ssc install bcuse
    regress lwage female, vce(robust)
    regress lwage female educ c.exper##c.exper tenure, vce(robust)
    ```

=== "R"

    ```r
    library(fixest)
    data("wage1", package = "wooldridge")

    raw      <- feols(lwage ~ female, data = wage1, vcov = "hetero")
    adjusted <- feols(lwage ~ female + educ + exper + I(exper^2) + tenure,
                      data = wage1, vcov = "hetero")
    etable(raw, adjusted)
    ```

=== "Python"

    ```python
    import pyfixest as pf
    import wooldridge

    wage1 = wooldridge.data("wage1")
    raw = pf.feols("lwage ~ female", data=wage1, vcov="hetero")
    adjusted = pf.feols("lwage ~ female + educ + exper + I(exper**2) + tenure",
                        data=wage1, vcov="hetero")
    pf.etable([raw, adjusted])
    ```

**Check:**

| Model | `female` coefficient | Gap |
|---|---:|---:|
| Raw | −0.397 | Women earn about 33% less |
| With education, experience and tenure | −0.298 | Women earn about 26% less than similar men |

Education and experience explain only a quarter of the gap. The rest could reflect discrimination, occupation, hours, or skills the data do not measure. Labor economists spend whole careers on that remaining gap.

## More project ideas

1. **The gap today.** Download recent CPS data from IPUMS. Has the gap shrunk since 1976? Add occupation controls.
2. **Returns by degree.** Compare wages for high school, some college and college graduates. Does the return differ by sex?
3. **Minimum wages.** Use BLS county data to compare teen employment in neighboring counties across a state border with different minimum wages.
4. **Union premium.** Use the [panel data page](../econometrics/panel.md) as a template and test whether the union premium has changed over time.

## Classic papers

- Card and Krueger (1994), "Minimum Wages and Employment", *American Economic Review*
- Goldin and Rouse (2000), "Orchestrating Impartiality: The Impact of 'Blind' Auditions on Female Musicians", *American Economic Review*
- Autor, Levy and Murnane (2003), "The Skill Content of Recent Technological Change", *Quarterly Journal of Economics*
- Blau and Kahn (2017), "The Gender Wage Gap: Extent, Trends, and Explanations", *Journal of Economic Literature*
