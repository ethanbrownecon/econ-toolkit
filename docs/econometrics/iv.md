# Instrumental variables (IV)

When the treatment is tangled up with unmeasured factors, an **instrument** can untangle it. An instrument is something that shifts the treatment but has no other connection to the outcome. IV uses only the part of the treatment that the instrument moves, which is as good as random.

## When to use it

- You suspect omitted variable bias, reverse causality or measurement error in the treatment.
- You have a variable that changes the treatment for reasons unrelated to the outcome: distance, a lottery, a policy rule, the weather.

## The idea

Card (1995) asks whether education raises wages. Ability affects both, so OLS is biased. His instrument: whether a person grew up **near a four-year college** (`nearc4`). Living near a college makes it cheaper to attend, so it raises education. The claim is that it has no other effect on wages.

IV works in two stages, called **two-stage least squares (2SLS)**:

\[
\begin{aligned}
\text{First stage:}\quad & \text{educ}_i = \pi_0 + \pi_1\,\text{nearc4}_i + \text{controls} + v_i \\
\text{Second stage:}\quad & \ln(\text{wage}_i) = \beta_0 + \beta_1\,\widehat{\text{educ}}_i + \text{controls} + \varepsilon_i
\end{aligned}
\]

The second stage uses predicted education from the first stage. Always let the software run both stages together, so the standard errors are correct.

## Key assumptions

| Assumption | In plain English | Can you test it? |
|---|---|---|
| **Relevance** | The instrument really moves the treatment | Yes: a strong first stage. Rule of thumb: F above 10. |
| **Exclusion** | The instrument affects the outcome **only** through the treatment | No. You must argue it. |
| **Independence** | The instrument is as good as random, given the controls | Partly: check balance on observed variables |
| **Monotonicity** | The instrument pushes everyone the same direction (no one goes to less school because a college is near) | No. Usually argued. |

!!! warning "Exclusion is the whole game"
    A critic might say families who live near colleges are richer or value education more, which raises wages directly. That would break exclusion. Card controls for region and urban status to make the argument stronger. When you use IV, spend most of your writing defending this assumption.

## Run it

`card` has 3,010 men from the National Longitudinal Survey of Young Men.

=== "Stata"

    ```stata
    bcuse card, clear

    * OLS, for comparison
    regress lwage educ exper expersq black smsa south, vce(robust)

    * 2SLS: the endogenous variable and its instrument go in brackets
    ivregress 2sls lwage exper expersq black smsa south (educ = nearc4), vce(robust)
    estat firststage                    // first-stage F

    * Two instruments: test overidentifying restrictions
    ivregress 2sls lwage exper expersq black smsa south (educ = nearc4 nearc2)
    estat overid
    ```

=== "R"

    ```r
    library(fixest)
    data("card", package = "wooldridge")

    ols <- feols(lwage ~ educ + exper + expersq + black + smsa + south,
                 data = card, vcov = "hetero")

    # 2SLS: controls | fixed effects (none here) | endogenous ~ instrument
    iv <- feols(lwage ~ exper + expersq + black + smsa + south | educ ~ nearc4,
                data = card, vcov = "hetero")
    summary(iv, stage = 1)              # first stage
    fitstat(iv, ~ ivwald)               # robust first-stage F

    iv2 <- feols(lwage ~ exper + expersq + black + smsa + south | educ ~ nearc4 + nearc2,
                 data = card)
    fitstat(iv2, ~ sargan)              # overidentification test
    ```

=== "Python"

    ```python
    import pyfixest as pf
    import wooldridge

    card = wooldridge.data("card")
    controls = "exper + expersq + black + smsa + south"

    ols = pf.feols(f"lwage ~ educ + {controls}", data=card, vcov="hetero")

    # 2SLS: endogenous ~ instrument in square brackets
    iv = pf.feols(f"lwage ~ {controls} + [educ ~ nearc4]", data=card, vcov="hetero")
    iv.summary()
    iv.first_stage.diagnostics.f_stat   # robust first-stage F
    ```

## Read the output

**Check:**

| | Estimate of return to education | Standard error |
|---|---:|---:|
| OLS | 0.074 | 0.004 |
| 2SLS with `nearc4` | **0.132** | 0.049 |

| Number | Meaning |
|---|---|
| First stage: 0.337 | Growing up near a college adds about a third of a year of schooling |
| First-stage F: about 17.5 | Above 10, so the instrument is not weak |
| 2SLS: 0.132 | One more year of education raises wages by about 13%, for people whose schooling was changed by college proximity |
| Overidentification p ≈ 0.10 | With two instruments, they do not significantly disagree. This cannot prove exclusion. |

The IV estimate is **larger** than OLS, which surprises many students. One explanation is that IV measures the effect for people on the margin of going to college. They may gain more than average. The standard error is also more than ten times larger: IV trades bias for precision.

??? note "Where does 0.132 come from? The Wald estimator"
    With one instrument, the IV estimate equals the **reduced form** (instrument → outcome) divided by the **first stage** (instrument → treatment): 0.0446 / 0.337 = 0.132. Living near a college raises wages by 4.5% and schooling by 0.34 years, so each year of schooling is worth 0.0446 / 0.337 ≈ 13%.

## Common mistakes

- **Weak instruments.** If the first-stage F is small, IV is biased toward OLS and its confidence intervals are wrong. Report the first stage.
- **Running the two stages by hand.** The coefficient is right but the standard errors are wrong. Use `ivregress`, `feols` or `pf.feols`.
- **Using a bad instrument because it is significant.** A strong first stage says nothing about exclusion.
- **Forgetting it is a local effect.** IV estimates the effect for "compliers", the people the instrument moves. That may differ from the average effect.

## Learn more

- [The Effect, chapter 19: Instrumental variables](https://theeffectbook.net/ch-InstrumentalVariables.html)
- [The Mixtape, chapter 7: Instrumental variables](https://mixtape.scunning.com/07-instrumental_variables)
