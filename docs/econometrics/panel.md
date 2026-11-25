# Panel data: fixed and random effects

Panel data follow the same units (people, firms, states) over several periods. That lets you compare each unit **with itself**, which removes everything about the unit that does not change over time, even things you cannot measure.

## When to use it

- You observe the same units at least twice.
- You worry that unmeasured, stable traits (ability, culture, management quality) affect both the treatment and the outcome.

## The idea

\[
y_{it} = \beta x_{it} + \alpha_i + \gamma_t + \varepsilon_{it}
\]

- \(\alpha_i\) is everything fixed about unit \(i\): measured or not.
- \(\gamma_t\) is everything common to all units in period \(t\), such as a recession.

| Estimator | How it treats \(\alpha_i\) | Use it when |
|---|---|---|
| **Pooled OLS** | Ignores it | \(\alpha_i\) is unrelated to \(x\). Rarely believable. |
| **Fixed effects (FE)** | Removes it by comparing each unit with its own average | \(\alpha_i\) may be related to \(x\). The usual choice in economics. |
| **Random effects (RE)** | Treats it as random noise, unrelated to \(x\) | You are confident \(\alpha_i\) is unrelated to \(x\), or you need time-invariant variables |

!!! note "The cost of fixed effects"
    FE uses only changes **within** a unit. Variables that never change for a unit, such as race or years of schooling for adults, are absorbed by \(\alpha_i\), so FE cannot estimate their effects. Variables that rarely change give imprecise estimates.

## Run it

`wagepan` follows 545 young men every year from 1980 to 1987. The question: do union members earn more?

=== "Stata"

    ```stata
    bcuse wagepan, clear
    xtset nr year                       // declare person and time

    * Fixed effects, with year effects and clustered errors
    xtreg lwage expersq married union i.year, fe vce(cluster nr)

    * Random effects
    xtreg lwage educ black hisp exper expersq married union i.year, re vce(cluster nr)

    * Hausman test: FE or RE?
    quietly xtreg lwage expersq married union i.year, fe
    estimates store fe
    quietly xtreg lwage expersq married union i.year, re
    estimates store re
    hausman fe re
    ```

=== "R"

    ```r
    library(fixest)
    library(plm)
    data("wagepan", package = "wooldridge")

    # Fixed effects: person and year
    fe <- feols(lwage ~ expersq + married + union | nr + year,
                data = wagepan, cluster = ~nr)

    # Random effects
    pdat <- pdata.frame(wagepan, index = c("nr", "year"))
    re <- plm(lwage ~ educ + black + hisp + exper + expersq + married + union + factor(year),
              data = pdat, model = "random")

    # Hausman test
    fe_h <- plm(lwage ~ expersq + married + union + factor(year), data = pdat, model = "within")
    re_h <- plm(lwage ~ expersq + married + union + factor(year), data = pdat, model = "random")
    phtest(fe_h, re_h)
    ```

=== "Python"

    ```python
    import pyfixest as pf
    import wooldridge
    from linearmodels.panel import RandomEffects

    wagepan = wooldridge.data("wagepan")

    # Fixed effects: person and year
    fe = pf.feols("lwage ~ expersq + married + union | nr + year",
                  data=wagepan, vcov={"CRV1": "nr"})

    # Random effects (linearmodels needs a person-year index)
    panel = wagepan.set_index(["nr", "year"])
    re = RandomEffects.from_formula(
        "lwage ~ 1 + educ + black + hisp + exper + expersq + married + union"
        " + d81 + d82 + d83 + d84 + d85 + d86 + d87",
        data=panel,
    ).fit(cov_type="clustered", cluster_entity=True)
    ```

## Read the output

**Check:** the union premium is:

| Estimator | Union coefficient |
|---|---:|
| Pooled OLS | 0.180 |
| Random effects | 0.106 |
| Fixed effects | **0.080** |

The estimate falls as we control more tightly for who joins a union. Pooled OLS compares union members with different people. FE compares the same man in years he is and is not in a union, so stable traits like ability cannot explain the gap. **Within a person, union membership goes with about 8% higher wages.**

The **Hausman test** asks whether FE and RE give significantly different answers. Here p < 0.001, so they do: RE's assumption fails, and FE is preferred. This is the usual result in economics.

!!! note "Why is experience missing from the FE model?"
    In this sample, experience rises by exactly one each year for everyone, so it moves in lockstep with the person and year effects. FE cannot separate them, so only `expersq` is included. Software drops such variables automatically.

## Common mistakes

- **Not clustering.** Errors for the same unit are correlated over time. Cluster by unit.
- **Expecting FE to estimate time-invariant effects.** It cannot. If you need them, use RE (and defend the assumption) or a correlated random effects model.
- **Treating FE as a cure-all.** FE removes **stable** confounders. Something that changes over time and affects both \(x\) and \(y\) still biases the estimate.
- **Forgetting time effects.** Add year fixed effects so common shocks are not mistaken for the effect of \(x\).

## Learn more

- [The Effect, chapter 16: Fixed effects](https://theeffectbook.net/ch-FixedEffects.html)
- [The Mixtape, chapter 8: Panel data](https://mixtape.scunning.com/08-panel_data)
