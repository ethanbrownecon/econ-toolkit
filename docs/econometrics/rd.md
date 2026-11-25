# Regression discontinuity (RD)

Many rules use a **cutoff**: a scholarship for test scores above 1200, Medicare at age 65, winning an election with more than 50% of the vote. People just above and just below the cutoff are almost identical, except that one side gets the treatment. Comparing them gives a causal effect.

## When to use it

- Treatment is decided by a score (the **running variable**) crossing a known cutoff.
- People cannot precisely control which side of the cutoff they land on.

## The idea

Fit a line, or a smooth curve, on each side of the cutoff, using only observations close to it. The **jump** at the cutoff is the effect.

\[
\tau = \lim_{x \downarrow c} E[y \mid x] - \lim_{x \uparrow c} E[y \mid x]
\]

| Choice | What modern practice does |
|---|---|
| How close to the cutoff (bandwidth) | Choose it with a data-driven method, as `rdrobust` does |
| Shape of the fit | Local **linear** on each side. Avoid high-order polynomials. |
| Weighting | More weight on observations nearer the cutoff (triangular kernel) |
| Inference | Robust bias-corrected confidence intervals |

## Key assumptions

| Assumption | In plain English | Can you test it? |
|---|---|---|
| **No precise manipulation** | People cannot sort themselves to just above the cutoff | Yes: check for a jump in the **number** of observations at the cutoff (a density test) |
| Continuity | Nothing else changes at the cutoff | Partly: check that other variables do **not** jump |

## Run it

Do politicians gain from already holding office? `senate` (Cattaneo, Frandsen and Titiunik, 2015) has US Senate elections from 1914 to 2010. The running variable `margin` is the Democratic margin of victory in one election: above 0 means the Democrat won. The outcome `vote` is the Democratic vote share in the **next** election for that seat.

=== "Stata"

    ```stata
    net install rdrobust, from("https://raw.githubusercontent.com/rdpackages/rdrobust/master/stata") replace
    net install rddensity, from("https://raw.githubusercontent.com/rdpackages/rddensity/master/stata") replace
    net install lpdensity, from("https://raw.githubusercontent.com/rdpackages/lpdensity/master/stata") replace

    use "https://raw.githubusercontent.com/rdpackages/rdrobust/master/stata/rdrobust_senate.dta", clear

    rdplot vote margin                    // picture first
    rdrobust vote margin                  // estimate
    rddensity margin                      // manipulation test
    ```

=== "R"

    ```r
    library(rdrobust)                     # install.packages("rdrobust")
    data(rdrobust_RDsenate)

    rdplot(y = rdrobust_RDsenate$vote, x = rdrobust_RDsenate$margin)
    summary(rdrobust(y = rdrobust_RDsenate$vote, x = rdrobust_RDsenate$margin))
    ```

=== "Python"

    ```python
    # pip install rdrobust
    import pandas as pd
    from rdrobust import rdplot, rdrobust

    senate = pd.read_csv("https://raw.githubusercontent.com/rdpackages/rdrobust/master/Python/rdrobust_senate.csv")

    rdplot(y=senate["vote"], x=senate["margin"])
    print(rdrobust(y=senate["vote"], x=senate["margin"]))
    ```

## Read the output

**Check:**

| Number | Value | Meaning |
|---|---:|---|
| Conventional estimate | **7.41** | Barely winning a Senate seat raises the party's vote share in the next election by about 7.4 percentage points |
| Robust 95% confidence interval | [4.09, 10.92] | Use this one for inference |
| Bandwidth | 17.75 | Only elections within 17.75 points of a tie are used |
| Effective observations | 360 left, 323 right | How many elections the estimate actually rests on |
| Density test p-value (Stata) | 0.38 | No sign that parties manipulate which side of 50% they land on |

**Start with the graph.** `rdplot` shows binned averages on each side and fitted curves. If you cannot see a jump in the picture, be skeptical of a significant estimate.

## Fuzzy RD

Sometimes crossing the cutoff only **raises the chance** of treatment: not every eligible student takes the scholarship. This is a **fuzzy** RD. It works like [IV](iv.md), with crossing the cutoff as the instrument. Add the treatment variable with `fuzzy(treatment)` in Stata, or `fuzzy = treatment` in R and Python.

## Common mistakes

- **Using a global high-order polynomial.** Fitting a 4th-order polynomial to all the data can create fake jumps. Use local linear fits, as `rdrobust` does.
- **Forgetting the result is local.** RD estimates the effect **at the cutoff**: for close elections, not landslides.
- **Ignoring manipulation.** If people can push themselves over the cutoff (grades rounded up to a pass mark), RD fails. Run the density test.
- **Not checking other variables.** Variables decided before the cutoff should not jump at it.

## Learn more

- [The Effect, chapter 20: Regression discontinuity](https://theeffectbook.net/ch-RegressionDiscontinuity.html)
- [The Mixtape, chapter 6: Regression discontinuity](https://mixtape.scunning.com/06-regression_discontinuity)
- [rdpackages](https://rdpackages.github.io/): documentation for rdrobust, rddensity and related tools, by the method's developers
