# Health economics

Health economics studies health, health care and health insurance: what makes people healthy, how much care costs, who gets insured, and how policy changes all three.

## Big questions

- Does health insurance make people healthier, or just change how they use care?
- How much do conditions at birth matter for health and earnings later in life?
- Why does US health care cost so much more than in other countries?
- How do taxes, bans and information change smoking, drinking and eating?
- How does pollution affect health?

## Methods you will use

[Randomized experiments](../econometrics/glossary.md#pr) · [regression discontinuity](../econometrics/rd.md) · [difference-in-differences](../econometrics/did.md) · [matching](../econometrics/matching.md) · [logit and probit](../econometrics/logit.md)

## Data

| Source | What it has |
|---|---|
| [CDC WONDER](https://wonder.cdc.gov/) | Births, deaths and disease by county and year |
| [MEPS](https://meps.ahrq.gov/mepsweb/) | Medical Expenditure Panel Survey: health spending and insurance |
| [BRFSS](https://www.cdc.gov/brfss/) | Health behaviors such as smoking, drinking and exercise, by state |
| [IPUMS Health Surveys](https://healthsurveys.ipums.org/) | National Health Interview Survey microdata since 1963 |

## Projects on this site

- [Matching](../econometrics/matching.md): smoking during pregnancy and birthweight, with propensity scores
- [Synthetic control](../econometrics/synthetic.md): California's tobacco tax and cigarette sales

## Starter project: smoking and birthweight

How much does smoking during pregnancy lower a baby's birthweight? `bwght` has 1,388 births from the 1988 National Health Interview Survey.

| Variable | Meaning |
|---|---|
| `bwght` | Birthweight in ounces |
| `cigs` | Cigarettes smoked per day during pregnancy |
| `faminc` | Family income, in thousands of dollars |
| `male`, `parity` | Baby is male; birth order |

=== "Stata"

    ```stata
    bcuse bwght, clear                    // ssc install bcuse
    regress bwght cigs, vce(robust)
    regress bwght cigs faminc male parity, vce(robust)
    ```

=== "R"

    ```r
    library(fixest)
    data("bwght", package = "wooldridge")

    simple   <- feols(bwght ~ cigs, data = bwght, vcov = "hetero")
    controls <- feols(bwght ~ cigs + faminc + male + parity, data = bwght, vcov = "hetero")
    etable(simple, controls)
    ```

=== "Python"

    ```python
    import pyfixest as pf
    import wooldridge

    bwght = wooldridge.data("bwght")
    simple = pf.feols("bwght ~ cigs", data=bwght, vcov="hetero")
    controls = pf.feols("bwght ~ cigs + faminc + male + parity", data=bwght, vcov="hetero")
    pf.etable([simple, controls])
    ```

**Check:** each daily cigarette goes with **0.51 ounces** lower birthweight, or **0.48** with controls. A pack a day (20 cigarettes) means about 9.5 ounces, more than half a pound. Only 15% of mothers in the data smoked.

Mothers who smoke differ in other ways too, such as income, education and diet. Controlling for income barely changes the estimate, which is reassuring but not proof. The [matching page](../econometrics/matching.md) tackles the same question with different data and a different method, and finds a similar effect.

## More project ideas

1. **Who smokes?** Run a [logit](../econometrics/logit.md) of whether a mother smoked on income and education.
2. **Cigarette taxes.** Combine state cigarette tax rates with BRFSS smoking rates in a [difference-in-differences](../econometrics/did.md) design.
3. **Medicare at 65.** Use the NHIS to test whether insurance coverage and doctor visits jump at age 65, in the style of Card, Dobkin and Maestas (2008).
4. **Pollution and infant health.** Combine EPA air quality data with CDC births by county.

## Classic papers

- Almond, Chay and Lee (2005), "The Costs of Low Birth Weight", *Quarterly Journal of Economics*
- Card, Dobkin and Maestas (2008), "The Impact of Nearly Universal Insurance Coverage on Health Care Utilization: Evidence from Medicare", *American Economic Review*
- Finkelstein et al. (2012), "The Oregon Health Insurance Experiment: Evidence from the First Year", *Quarterly Journal of Economics*
