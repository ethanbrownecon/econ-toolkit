# Synthetic control and synthetic DiD

When only **one or a few units** are treated, such as a single state or country, there may be no single good comparison. Synthetic control builds one: a **weighted average of untreated units** that tracks the treated unit closely before the treatment. Synthetic difference-in-differences (SDID) combines this idea with DiD.

## When to use it

- One or a handful of treated units: a state passes a law, a country leaves a trade union.
- Many untreated units to draw from.
- A long stretch of data before treatment.

## The idea

California raised its cigarette tax in 1989 with Proposition 99. How much did smoking fall because of it? No other state looks exactly like California. But a weighted mix of states might, for 1970–1988. That mix becomes "synthetic California", and the gap after 1989 is the effect.

| Method | Comparison group | Weights on years |
|---|---|---|
| **Difference-in-differences** | All control states, equally weighted | All pre-years equally |
| **Synthetic control** | A weighted mix of states that matches California's **level** before treatment | Not used |
| **Synthetic DiD** | A weighted mix of states that matches California's **trend** before treatment | Weights pre-years that look most like the post period |

Synthetic DiD (Arkhangelsky, Athey, Hirshberg, Imbens and Wager, 2021) only needs parallel trends with the synthetic group, not identical levels. It is more robust than either method alone.

## Key assumptions

| Assumption | In plain English |
|---|---|
| Good pre-treatment fit | The synthetic unit tracks the treated unit closely before treatment. Check it on a graph. |
| No spillovers | The treatment did not affect the control units |
| No other shocks | Nothing else hit only the treated unit at the same time |

## Run it

`prop99` has cigarette packs sold per person in 39 states from 1970 to 2000. California is the only treated state, from 1989.

=== "Stata"

    ```stata
    ssc install sdid

    webuse set www.damianclarke.net/stata/
    webuse prop99_example.dta, clear
    webuse set                            // reset to Stata's default location

    sdid packspercapita state year treated, vce(placebo) seed(1213) graph
    ```

    Add `method(sc)` for synthetic control or `method(did)` for plain DiD.

=== "R"

    ```r
    # install.packages("remotes")
    # remotes::install_github("synth-inference/synthdid")
    library(synthdid)

    data("california_prop99")
    setup <- panel.matrices(california_prop99)

    tau_sdid <- synthdid_estimate(setup$Y, setup$N0, setup$T0)
    tau_sc   <- sc_estimate(setup$Y, setup$N0, setup$T0)
    tau_did  <- did_estimate(setup$Y, setup$N0, setup$T0)

    tau_sdid
    sqrt(vcov(tau_sdid, method = "placebo"))     # standard error
    plot(tau_sdid)
    ```

=== "Python"

    There is no well-maintained Python package for synthetic DiD at the moment. The older `synthdid` package on PyPI does not install on current Python versions.

    Run this method in R or Stata. For classic synthetic control in Python, see [pysyncon](https://sdfordham.github.io/pysyncon/).

## Read the output

**Check:** the three estimates of Prop 99's effect, in packs per person per year:

| Method | Estimate |
|---|---:|
| Difference-in-differences | −27.3 |
| Synthetic control | −19.6 |
| **Synthetic DiD** | **−15.6** |

These match Arkhangelsky et al. (2021). Plain DiD overstates the effect because California's smoking was already falling faster than the average state's. Synthetic DiD's standard error is about 9 to 10 packs, so this single-state estimate is imprecise.

!!! note "Placebo inference"
    With one treated unit, the usual standard errors do not work. `vce(placebo)` pretends each control state was treated, re-estimates, and uses the spread of those fake effects as the standard error. Set a seed so the result is reproducible.

## Common mistakes

- **Not showing the pre-treatment fit.** The graph of the treated unit and its synthetic version before treatment is the main evidence. Always include it.
- **Including control units hit by similar policies.** Drop states that passed their own tobacco taxes.
- **Over-interpreting one unit.** A single treated state gives an imprecise estimate. Be honest about the uncertainty.

## Learn more

- [The Mixtape, chapter 11: Synthetic control](https://mixtape.scunning.com/11-synthetic_control)
- [synthdid package guide](https://synth-inference.github.io/synthdid/)
- Arkhangelsky et al. (2021), "Synthetic Difference-in-Differences", *American Economic Review*
