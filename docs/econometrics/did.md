# Difference-in-differences (DiD)

Difference-in-differences compares how an outcome **changes** in a group that gets a treatment with how it changes in a group that does not. The control group's change shows what would have happened to the treated group anyway. It is the most common method for evaluating policies.

## When to use it

- A policy, event or program affects some groups and not others.
- You have data from **before and after** it starts, for both groups.

## The idea

\[
\text{DiD} = \underbrace{(\bar y_{\text{treated, after}} - \bar y_{\text{treated, before}})}_{\text{change for treated}} - \underbrace{(\bar y_{\text{control, after}} - \bar y_{\text{control, before}})}_{\text{change for control}}
\]

As a regression, with a treated-group dummy and an after dummy:

\[
y_{it} = \beta_0 + \beta_1\,\text{treated}_i + \beta_2\,\text{post}_t + \delta\,(\text{treated}_i \times \text{post}_t) + \varepsilon_{it}
\]

\(\delta\), the coefficient on the interaction, is the DiD estimate.

## Key assumption: parallel trends

| Assumption | In plain English | Can you test it? |
|---|---|---|
| **Parallel trends** | Without the treatment, the two groups' outcomes would have moved in parallel | Not directly. Check that trends were parallel **before** treatment with an event study. |
| No anticipation | Units do not change behavior before the treatment starts | Look for effects before treatment |
| No spillovers | Treating one group does not affect the control group | Argue it |

The groups do **not** need the same level. They need the same trend.

## Part 1: The classic two-by-two

Kiel and McClain study house prices near a garbage incinerator in North Andover, Massachusetts. Rumors of the incinerator started after 1978, and it was built in 1981. Compare houses near the site (`nearinc`) with houses farther away, in 1978 and 1981 (`y81`).

=== "Stata"

    ```stata
    bcuse kielmc, clear
    regress rprice i.nearinc##i.y81, vce(robust)
    ```

=== "R"

    ```r
    library(fixest)
    data("kielmc", package = "wooldridge")

    feols(rprice ~ nearinc * y81, data = kielmc, vcov = "hetero")
    ```

=== "Python"

    ```python
    import pyfixest as pf
    import wooldridge

    kielmc = wooldridge.data("kielmc")
    pf.feols("rprice ~ nearinc * y81", data=kielmc, vcov="hetero").summary()
    ```

**Check:**

| Coefficient | Value | Meaning |
|---|---:|---|
| `nearinc` | −18,824 | Houses near the site were already cheaper in 1978 |
| `y81` | 18,790 | Prices everywhere rose between 1978 and 1981 |
| `nearinc × y81` | **−11,864** | Houses near the incinerator lost about $11,900 relative to other houses |

The level difference in 1978 does not matter for DiD. Only the difference in **changes** does.

## Part 2: Many periods and event studies

With many groups and years, use **two-way fixed effects** (TWFE): a fixed effect for each unit and each year.

\[
y_{it} = \alpha_i + \gamma_t + \delta\,D_{it} + \varepsilon_{it}
\]

\(D_{it}\) is 1 when unit \(i\) is treated in year \(t\).

An **event study** goes further: it estimates a separate effect for each year relative to treatment. Effects **before** treatment should be close to zero. That is your check on parallel trends.

### The data

`mpdta` comes from Callaway and Sant'Anna (2021). It has teen employment for 500 US counties from 2003 to 2007. Some counties raised their minimum wage in 2004, some in 2006, some in 2007, and some never did. `first_treat` is the year a county was first treated, and 0 means never.

=== "Stata"

    ```stata
    use "https://friosavila.github.io/playingwithstata/drdid/mpdta.dta", clear

    * TWFE: one DiD coefficient
    gen treat_post = (first_treat > 0 & year >= first_treat)
    reghdfe lemp treat_post, absorb(countyreal year) vce(cluster countyreal)

    * Event study: years relative to treatment, with year -1 as the base
    gen rel = cond(first_treat == 0, -1, year - first_treat)
    gen rel_f = rel + 5                   // factor variables must be 0 or more
    reghdfe lemp ib4.rel_f, absorb(countyreal year) vce(cluster countyreal)
    ```

=== "R"

    ```r
    library(fixest)
    library(dplyr)
    data(mpdta, package = "did")          # install.packages("did")

    mpdta <- mpdta %>%
      mutate(treat_post = as.integer(first.treat > 0 & year >= first.treat),
             rel = ifelse(first.treat == 0, -1, year - first.treat))

    # TWFE: one DiD coefficient
    feols(lemp ~ treat_post | countyreal + year, data = mpdta, cluster = ~countyreal)

    # Event study, with year -1 as the base
    es <- feols(lemp ~ i(rel, ref = -1) | countyreal + year, data = mpdta, cluster = ~countyreal)
    iplot(es)                             # plot the event study
    ```

=== "Python"

    ```python
    import numpy as np
    import pandas as pd
    import pyfixest as pf

    mpdta = pd.read_stata("https://friosavila.github.io/playingwithstata/drdid/mpdta.dta")
    mpdta["treat_post"] = ((mpdta["first_treat"] > 0) & (mpdta["year"] >= mpdta["first_treat"])).astype(int)
    mpdta["rel"] = np.where(mpdta["first_treat"] == 0, -1, mpdta["year"] - mpdta["first_treat"]).astype(int)

    # TWFE: one DiD coefficient
    pf.feols("lemp ~ treat_post | countyreal + year", data=mpdta, vcov={"CRV1": "countyreal"})

    # Event study, with year -1 as the base
    es = pf.feols("lemp ~ i(rel, ref=-1) | countyreal + year", data=mpdta, vcov={"CRV1": "countyreal"})
    es.iplot()                            # plot the event study
    ```

Never-treated counties get `rel = -1`, so they sit in the base category and act as the comparison group.

**Check:** the TWFE estimate is **−0.037**. The event-study coefficients:

| Years relative to treatment | −4 | −3 | −2 | −1 | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Effect on log teen employment | 0.004 | 0.025 | 0.023 | 0 (base) | −0.018 | −0.043 | −0.132 | −0.092 |

Before treatment the effects are small and not significant, which supports parallel trends. After treatment, teen employment falls, and the drop grows over time.

## Part 3: Staggered timing, and why TWFE can mislead

When units are treated at **different times**, TWFE compares some newly treated units with units that were **already treated**. If effects change over time, those comparisons can be badly biased, and the TWFE estimate can even have the wrong sign. This was one of the biggest findings in econometrics in recent years.

The fix: estimators that only compare treated units with **not-yet-treated or never-treated** units. The most widely used is **Callaway and Sant'Anna (2021)**.

=== "Stata"

    ```stata
    ssc install csdid
    ssc install drdid

    use "https://friosavila.github.io/playingwithstata/drdid/mpdta.dta", clear
    csdid lemp, ivar(countyreal) time(year) gvar(first_treat) rseed(1)

    estat simple                          // one overall effect
    estat event                           // event study
    csdid_plot                            // plot it
    ```

=== "R"

    ```r
    library(did)
    data(mpdta, package = "did")

    cs <- att_gt(yname = "lemp", tname = "year", idname = "countyreal",
                 gname = "first.treat", data = mpdta)

    aggte(cs, type = "simple")            # one overall effect
    es <- aggte(cs, type = "dynamic")     # event study
    ggdid(es)                             # plot it
    ```

=== "Python"

    ```python
    # pip install csdid
    import pandas as pd
    from csdid.att_gt import ATTgt

    mpdta = pd.read_stata("https://friosavila.github.io/playingwithstata/drdid/mpdta.dta")

    cs = ATTgt(yname="lemp", gname="first_treat", idname="countyreal",
               tname="year", data=mpdta).fit(est_method="dr")

    cs.aggte(typec="simple")              # one overall effect
    cs.aggte(typec="dynamic")             # event study
    ```

**Check:** the overall effect is **−0.040**, and the average post-treatment event-study effect is about **−0.077**. Here TWFE (−0.037) is not far off, but in other settings the gap can be large. With staggered timing, report Callaway and Sant'Anna (or a similar modern estimator) at least as a robustness check.

## Common mistakes

- **Skipping the pre-trends check.** Always show an event study. Flat pre-treatment effects make parallel trends believable. They do not prove it.
- **Using TWFE with staggered timing without checking.** Compare it with Callaway and Sant'Anna.
- **Clustering at the wrong level.** Cluster at the level the treatment is assigned, such as the state or county.
- **Choosing a control group that was also affected.** Spillovers bias the estimate toward zero.

## Learn more

- [The Effect, chapter 18: Difference-in-differences](https://theeffectbook.net/ch-DifferenceinDifference.html)
- [The Mixtape, chapter 9: Difference-in-differences](https://mixtape.scunning.com/09-difference_in_differences)
- [The Mixtape, chapter 10: Complex difference-in-differences](https://mixtape.scunning.com/10-complex_diff_in_diff): staggered timing
- [Callaway and Sant'Anna's did package guide](https://bcallaway11.github.io/did/articles/did-basics.html)
