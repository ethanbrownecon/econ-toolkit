# Logit and probit

When the outcome is yes or no (works or not, defaults or not, votes or not), you want to model a **probability**. Logit and probit keep predicted probabilities between 0 and 1. The linear probability model (plain OLS on a 0/1 outcome) is a simpler alternative that often gives similar answers.

## When to use it

- The outcome is binary: coded 1 for yes and 0 for no.
- You want predicted probabilities, or effects measured in percentage points.

## The idea

\[
P(y_i = 1 \mid x_i) = G(\beta_0 + \beta_1 x_{1i} + \dots)
\]

\(G\) squeezes any number into the range 0 to 1.

| Model | \(G\) | Notes |
|---|---|---|
| **Linear probability model (LPM)** | No squeezing: \(G(z) = z\) | Easy to read, but predictions can fall below 0 or above 1 |
| **Logit** | Logistic function | Coefficients are changes in the log-odds |
| **Probit** | Normal distribution | Very similar results to logit |

!!! tip "Report marginal effects, not raw coefficients"
    Logit and probit coefficients are not changes in probability, and they are not directly comparable to each other. Convert them to **average marginal effects**: the average change in the probability for a one-unit change in x. Those are comparable across logit, probit and the LPM.

## Run it

`mroz` has 753 married women in 1975. The outcome `inlf` is 1 if the woman was in the labor force.

=== "Stata"

    ```stata
    bcuse mroz, clear

    logit inlf nwifeinc educ c.exper##c.exper age kidslt6 kidsge6
    margins, dydx(*)                     // average marginal effects

    logit inlf nwifeinc educ c.exper##c.exper age kidslt6 kidsge6, or   // odds ratios

    probit inlf nwifeinc educ c.exper##c.exper age kidslt6 kidsge6
    margins, dydx(*)
    ```

=== "R"

    ```r
    library(marginaleffects)
    data("mroz", package = "wooldridge")

    f <- inlf ~ nwifeinc + educ + exper + I(exper^2) + age + kidslt6 + kidsge6

    logit  <- glm(f, data = mroz, family = binomial(link = "logit"))
    probit <- glm(f, data = mroz, family = binomial(link = "probit"))

    avg_slopes(logit)                    # average marginal effects
    exp(coef(logit))                     # odds ratios
    avg_slopes(probit)
    ```

=== "Python"

    ```python
    import numpy as np
    import statsmodels.formula.api as smf
    import wooldridge

    mroz = wooldridge.data("mroz")
    f = "inlf ~ nwifeinc + educ + exper + I(exper**2) + age + kidslt6 + kidsge6"

    logit = smf.logit(f, data=mroz).fit()
    probit = smf.probit(f, data=mroz).fit()

    logit.get_margeff().summary()        # average marginal effects
    np.exp(logit.params)                 # odds ratios
    probit.get_margeff().summary()
    ```

## Read the output

The effect of having a child under 6 (`kidslt6`), measured three ways:

| Model | Raw coefficient | Average marginal effect |
|---|---:|---:|
| Logit | −1.443 | **−0.258** |
| Probit | −0.868 | **−0.261** |
| Linear probability model | −0.262 | −0.262 |

The raw coefficients look very different. The marginal effects agree: **each young child lowers the probability of working by about 26 percentage points.**

Other numbers you will see:

| Number | Meaning |
|---|---|
| Marginal effect of `educ`: 0.039 | One more year of education raises the probability of working by about 3.9 percentage points |
| Odds ratio for `educ`: 1.248 | One more year of education multiplies the odds of working by 1.25 (a 25% increase in the **odds**, not the probability) |
| Pseudo R² | A rough measure of fit. Not comparable to OLS R². |

## Which one should I use?

- **Logit or probit:** pick one. They almost always give similar marginal effects. Logit is more common in applied economics and medicine because of odds ratios.
- **LPM:** fine for average effects, especially with fixed effects or IV, where logit and probit get complicated. Always use robust standard errors with an LPM.

## Common mistakes

- **Reporting raw logit coefficients as probabilities.** −1.443 does not mean a 144% drop. Use marginal effects.
- **Confusing odds with probability.** Odds of 1.25 times is not a 25 percentage point increase.
- **Using logit with many fixed effects.** Logit with unit fixed effects can be biased in short panels (the "incidental parameters problem"). Use an LPM with fixed effects, or a conditional logit (`clogit` in Stata).

## Learn more

- [Introduction to Econometrics with R, chapter 11: Regression with a binary dependent variable](https://www.econometrics-with-r.org/11-rwabdv.html)
- [marginaleffects documentation](https://marginaleffects.com/): marginal effects for almost any model in R and Python
