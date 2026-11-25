# Econometrics and causal inference

Most interesting questions in economics are about **cause and effect**. Does going to college raise wages? Did a minimum wage increase cut jobs? Does a job-training program work? This section explains the main methods economists use to answer questions like these, with code in Stata, R and Python for each.

!!! info "How each page works"
    Every method page has the same parts: **when to use it**, **the idea** in one equation, **the key assumptions**, **runnable code** in Stata, R and Python, **how to read the output**, and **common mistakes**. Pick a language in any tab and every page follows.

## The core problem: correlation is not causation

People who go to college earn more. But people who go to college also differ in other ways: family background, ability, motivation. Some of the wage gap would exist even without college. This is **selection bias**, and it is why a simple comparison or regression often does not give a causal effect.

Each method below is a different strategy for getting around selection bias:

| Method | Strategy | Key assumption |
|---|---|---|
| [Linear regression](ols.md) | Compare people who look alike on the variables you control for | No important differences left that you did not measure |
| [Panel fixed effects](panel.md) | Compare each unit with itself over time | What you cannot measure does not change over time |
| [Instrumental variables](iv.md) | Use something that shifts the treatment but has no other link to the outcome | The instrument affects the outcome only through the treatment |
| [Difference-in-differences](did.md) | Compare the change over time in a treated group with the change in an untreated group | Without treatment, both groups would have followed parallel trends |
| [Synthetic control and synthetic DiD](synthetic.md) | Build a weighted comparison group that tracks the treated unit before treatment | The weighted group is a good stand-in for the treated unit |
| [Regression discontinuity](rd.md) | Compare units just above and just below a cutoff | Units just either side of the cutoff are alike |
| [Matching and propensity scores](matching.md) | Pair each treated unit with similar untreated units | No important differences left that you did not measure |

[Logit and probit](logit.md) are not identification strategies. They are models for yes/no outcomes, and you can combine them with the strategies above.

## Which method should I use?

Start from your data and your setting, not from the method.

| Your situation | Try |
|---|---|
| Cross-section data, and you can measure the main confounders | [Linear regression](ols.md), [matching](matching.md) |
| The outcome is yes/no | [Logit or probit](logit.md), or a linear probability model |
| The same units are observed over several periods | [Panel fixed effects](panel.md) |
| A policy hit some groups and not others, at a known date | [Difference-in-differences](did.md) |
| One or a few treated units, such as a single state or country | [Synthetic control or synthetic DiD](synthetic.md) |
| Treatment depends on a score crossing a cutoff (test score, age, vote share) | [Regression discontinuity](rd.md) |
| Something as-good-as-random shifts who gets treated (distance, lottery, weather) | [Instrumental variables](iv.md) |

## Before you start

The examples use real datasets from Wooldridge's *Introductory Econometrics* and well-known papers. Install the data packages once:

=== "Stata"

    ```stata
    ssc install bcuse          // loads any Wooldridge dataset: bcuse wage1, clear
    ssc install reghdfe
    ssc install ftools
    ssc install require
    ```

=== "R"

    ```r
    install.packages(c("wooldridge", "fixest", "marginaleffects", "plm"))
    ```

=== "Python"

    ```bash
    pip install wooldridge pyfixest statsmodels linearmodels
    ```

## Learn more

- [The Effect](https://theeffectbook.net/) by Nick Huntington-Klein: the clearest introduction to research design, free online.
- [Causal Inference: The Mixtape](https://mixtape.scunning.com/) by Scott Cunningham: every method here, with Stata, R and Python code.
- [Mostly Harmless Econometrics](https://www.mostlyharmlesseconometrics.com/) by Angrist and Pischke: the classic graduate-level guide.
