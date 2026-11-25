# Matching and propensity scores

Matching compares each treated person with untreated people **who look like them** on observed characteristics. The **propensity score**, the probability of being treated given those characteristics, makes this practical: instead of matching on many variables, you match on one number.

## When to use it

- You have cross-section data and believe you can measure everything that affects both treatment and outcome.
- Treated and untreated groups differ a lot on observed characteristics, and you want a transparent like-for-like comparison.

## The idea

1. **Estimate the propensity score.** A logit of treatment on the characteristics gives each person's probability of being treated.
2. **Match.** Pair each treated person with the untreated person, or people, with the closest score.
3. **Check balance.** After matching, the two groups should look alike on every characteristic.
4. **Compare outcomes** in the matched sample.

The usual target is the **average treatment effect on the treated (ATT)**: the effect for the people who actually got the treatment.

!!! warning "Matching does not solve selection on unobservables"
    Matching relies on the same assumption as [regression](ols.md): no important differences remain once you account for the observed variables. It makes the comparison more transparent and less dependent on the model's functional form. It does not fix omitted variables.

## Key assumptions

| Assumption | In plain English | Can you test it? |
|---|---|---|
| **Selection on observables** | Once you condition on the observed variables, treatment is as good as random | No. You must argue it. |
| **Overlap (common support)** | For each treated person, there are untreated people with similar scores | Yes: compare the score distributions |

## Run it

`cattaneo2` has 4,642 births in Pennsylvania. Does smoking during pregnancy (`mbsmoke`) lower birthweight (`bweight`, in grams)? Smokers differ from non-smokers: they are less likely to be married and have less education. Matching adjusts for marital status, age, first baby and education.

=== "Stata"

    ```stata
    webuse cattaneo2, clear

    * Nearest-neighbor propensity score matching, effect on the treated
    teffects psmatch (bweight) (mbsmoke mmarried c.mage##c.mage fbaby medu, logit), atet
    tebalance summarize                   // balance before and after

    * Inverse probability weighting, for comparison
    teffects ipw (bweight) (mbsmoke mmarried c.mage##c.mage fbaby medu), atet
    ```

=== "R"

    ```r
    library(MatchIt)                      # install.packages("MatchIt")
    library(fixest)
    library(haven)

    births <- read_dta("https://www.stata-press.com/data/r18/cattaneo2.dta") |> zap_labels()

    m <- matchit(mbsmoke ~ mmarried + mage + I(mage^2) + fbaby + medu,
                 data = births, method = "nearest", distance = "glm",
                 replace = TRUE, estimand = "ATT")
    summary(m)                            # balance before and after

    matched <- match.data(m)
    feols(bweight ~ mbsmoke, data = matched, weights = ~weights, vcov = "hetero")
    ```

=== "Python"

    ```python
    import numpy as np
    import pandas as pd
    import statsmodels.formula.api as smf

    births = pd.read_stata("https://www.stata-press.com/data/r18/cattaneo2.dta",
                           convert_categoricals=False,
                           storage_options={"User-Agent": "Mozilla/5.0"})

    # 1. Propensity score
    ps = smf.logit("mbsmoke ~ mmarried + mage + I(mage**2) + fbaby + medu", data=births).fit()
    births["pscore"] = ps.predict(births)

    treated = births[births["mbsmoke"] == 1]
    control = births[births["mbsmoke"] == 0]

    # 2. Match each smoker to the non-smokers with the closest score (ties averaged)
    by_score = control.groupby("pscore")["bweight"].mean()
    scores = by_score.index.to_numpy()
    nearest = np.abs(treated["pscore"].to_numpy()[:, None] - scores[None, :]).argmin(axis=1)

    # 3. Effect on the treated
    att = (treated["bweight"].to_numpy() - by_score.to_numpy()[nearest]).mean()
    att
    ```

    Many mothers share the same score because the variables take few values. Averaging all tied matches, as Stata does, gives a stable answer. Python has no standard matching package as mature as Stata's `teffects` or R's `MatchIt`, so for real projects consider running matching in one of those.

## Read the output

**Check:** the estimated effect of smoking on birthweight:

| Method | Estimate (grams) |
|---|---:|
| Raw difference in means | −275 |
| Regression with the same controls | −225 |
| Propensity score matching (ATT) | **about −231 to −237** |
| Inverse probability weighting (ATT) | −226 |

Matching estimates differ slightly across software because of how ties and standard errors are handled. All agree: **smoking during pregnancy lowers birthweight by roughly 230 grams** for mothers who smoke, about half a pound. The raw gap of 275 grams overstates it because smokers differ in other ways.

**Balance check:** before matching, 75% of non-smokers were married against 47% of smokers. After matching, the matched non-smokers are 47% married too. Check every variable this way. If balance is poor, matching has not done its job.

## Matching, weighting or regression?

| Method | Idea | Strength |
|---|---|---|
| Regression | Control for the variables in a linear model | Simple and familiar |
| Matching | Compare each treated unit with similar controls | Transparent; easy to check balance and overlap |
| Inverse probability weighting | Reweight controls so they resemble the treated group | Uses all the data |
| Doubly robust (`teffects aipw`) | Combine a weighting model and an outcome model | Correct if **either** model is right |

When they agree, as here, you can be more confident. When they disagree, look for poor overlap.

## Common mistakes

- **Treating matching as a causal design by itself.** It adjusts only for what you observe.
- **Skipping the balance table.** Always report balance before and after matching.
- **Ignoring overlap.** Treated units with no comparable controls should be dropped or flagged.
- **Matching on variables affected by the treatment.** Match only on characteristics fixed before treatment.

## Practice

The [LaLonde replication](../projects/replication-lalonde.md) tests matching and weighting against a randomized experiment, and shows why overlap matters.

## Learn more

- [The Effect, chapter 14: Matching](https://theeffectbook.net/ch-Matching.html)
- [The Mixtape, chapter 5: Causal cross-sectional designs](https://mixtape.scunning.com/05-causal_cross_sectional_designs)
- [MatchIt documentation](https://kosukeimai.github.io/MatchIt/)
