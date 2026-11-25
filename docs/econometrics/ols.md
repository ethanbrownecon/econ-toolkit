# Linear regression (OLS)

Ordinary least squares (OLS) fits the straight line, or plane, that best predicts an outcome from one or more variables. It is the foundation for almost every other method in this section.

## When to use it

- To describe how an outcome varies with several variables at once.
- To estimate a causal effect **if** you can measure and control for everything that affects both the treatment and the outcome.
- As the first, baseline model before you try a stronger design.

## The idea

\[
\ln(\text{wage}_i) = \beta_0 + \beta_1\,\text{educ}_i + \beta_2\,\text{exper}_i + \beta_3\,\text{exper}_i^2 + \beta_4\,\text{tenure}_i + \beta_5\,\text{female}_i + \varepsilon_i
\]

OLS picks the \(\beta\)s that make the squared prediction errors \(\varepsilon_i\) as small as possible. \(\beta_1\) is the change in the outcome for a one-unit change in education, **holding the other variables constant**.

## Key assumptions

| Assumption | In plain English | What breaks if it fails |
|---|---|---|
| **No omitted confounders** | Nothing left in \(\varepsilon\) affects both education and wages | \(\beta_1\) is biased. This is the big one for causal claims. |
| Linearity in parameters | The model is a weighted sum of the variables (you can still include logs and squares) | The fit is poor |
| No perfect collinearity | No variable is an exact combination of others | The software drops a variable |
| Errors uncorrelated across observations | One person's error says nothing about another's | Standard errors are too small. Cluster them. |

Heteroskedasticity (error variance that differs across observations) does not bias \(\beta\), but it does make classical standard errors wrong. **Always use robust or clustered standard errors.**

## Run it

`wage1` has 526 workers from the 1976 Current Population Survey.

=== "Stata"

    ```stata
    bcuse wage1, clear
    regress lwage educ c.exper##c.exper tenure female, vce(robust)
    ```

=== "R"

    ```r
    library(fixest)
    data("wage1", package = "wooldridge")

    m <- feols(lwage ~ educ + exper + I(exper^2) + tenure + female,
               data = wage1, vcov = "hetero")
    summary(m)
    ```

=== "Python"

    ```python
    import pyfixest as pf
    import wooldridge

    wage1 = wooldridge.data("wage1")
    m = pf.feols("lwage ~ educ + exper + I(exper**2) + tenure + female",
                 data=wage1, vcov="hetero")
    m.summary()
    ```

## Read the output

**Check:** the coefficient on `educ` is **0.081**, with an R² of 0.43.

| Number | What it tells you |
|---|---|
| Coefficient on `educ`: 0.081 | One more year of education goes with about **8.1% higher** wages, for people with the same experience, tenure and sex |
| Coefficient on `female`: −0.298 | Women earn about 26% less than men with the same education, experience and tenure (\(e^{-0.298} - 1 = -0.26\)) |
| Standard error | How precisely the coefficient is estimated |
| t-statistic and p-value | Whether the coefficient is distinguishable from zero. \(|t| > 1.96\) means p < 0.05. |
| 95% confidence interval | The range of values consistent with the data |
| R² | Share of the variation in the outcome that the model explains. A low R² does not mean the coefficients are wrong. |

### Interpreting logs

| Model | Interpretation of \(\beta\) |
|---|---|
| \(y = \beta x\) | One more unit of x changes y by \(\beta\) units |
| \(\ln y = \beta x\) | One more unit of x changes y by about \(100\beta\)% |
| \(y = \beta \ln x\) | A 1% increase in x changes y by \(\beta/100\) units |
| \(\ln y = \beta \ln x\) | A 1% increase in x changes y by \(\beta\)% (an elasticity) |

## Common mistakes

- **Reading a coefficient as causal without a design.** Here, people with more education may also have more ability, which raises wages on its own. The 8.1% is a correlation, holding the controls fixed. See [IV](iv.md) for one fix.
- **Controlling for "bad controls".** Do not control for something the treatment itself causes. For example, controlling for occupation when estimating the effect of education removes part of the effect you want.
- **Using classical standard errors.** Use `vce(robust)`, `vcov = "hetero"`, or cluster when observations are grouped.
- **Forgetting the squared term's interpretation.** With \(\text{exper}\) and \(\text{exper}^2\), the effect of experience depends on its level: \(\beta_2 + 2\beta_3\,\text{exper}\).

## Learn more

- [The Effect, chapter 13: Regression](https://theeffectbook.net/ch-StatisticalAdjustment.html)
- [Introduction to Econometrics with R, chapters 4–7](https://www.econometrics-with-r.org/)
