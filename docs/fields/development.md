# Development economics

Development economics asks why some countries are rich and others poor, and what can make poor people better off. It ranges from cross-country comparisons of growth and institutions to randomized trials of programs in single villages.

## Big questions

- Why did some countries grow rich while others stayed poor?
- Do institutions, geography or culture matter most?
- Which programs (cash transfers, microfinance, deworming, schooling) actually reduce poverty?
- How do health and income affect each other?
- Does foreign aid work?

## Methods you will use

[Randomized experiments](../econometrics/glossary.md#pr) · [instrumental variables](../econometrics/iv.md) · [difference-in-differences](../econometrics/did.md) · [regression discontinuity](../econometrics/rd.md) · cross-country [regression](../econometrics/ols.md)

## Data

| Source | What it has |
|---|---|
| [World Bank Open Data](https://data.worldbank.org/) | 1,400+ indicators for every country ([API guide](../data/apis.md)) |
| [Penn World Table](https://www.rug.nl/ggdc/productivity/pwt/) | Comparable GDP, capital and productivity |
| [Demographic and Health Surveys](https://dhsprogram.com/) | Household surveys on health, fertility and wealth in 90+ countries |
| [Our World in Data](https://ourworldindata.org/) | Clean long-run data on poverty, health and growth |

## Starter project: richer countries, longer lives

In 1975, Samuel Preston showed that life expectancy rises steeply with income in poor countries and flattens in rich ones: the **Preston curve**. Reproduce it with World Bank data for 2019, the last year before COVID.

=== "Stata"

    ```stata
    ssc install wbopendata
    wbopendata, indicator(NY.GDP.PCAP.KD; SP.DYN.LE00.IN) year(2019) long clear nometadata
    drop if regionname == "Aggregates"          // keep countries, not regions
    rename ny_gdp_pcap_kd gdp_pc
    rename sp_dyn_le00_in life_exp
    drop if missing(gdp_pc, life_exp)
    gen log_gdp_pc = ln(gdp_pc)

    twoway (scatter life_exp gdp_pc) , xscale(log)
    regress life_exp log_gdp_pc, vce(robust)
    ```

    If `wbopendata` times out, run `set timeout1 120` and `set timeout2 600`, then try again.

=== "R"

    ```r
    library(tidyverse)
    library(fixest)
    library(WDI)                                # install.packages("WDI")

    dev <- WDI(indicator = c(gdp_pc = "NY.GDP.PCAP.KD", life_exp = "SP.DYN.LE00.IN"),
               start = 2019, end = 2019, extra = TRUE) %>%
      filter(region != "Aggregates") %>%        # keep countries, not regions
      drop_na(gdp_pc, life_exp)

    ggplot(dev, aes(gdp_pc, life_exp)) + geom_point() + scale_x_log10()
    feols(life_exp ~ log(gdp_pc), data = dev, vcov = "hetero")
    ```

=== "Python"

    ```python
    # pip install wbgapi pyfixest
    import numpy as np
    import pyfixest as pf
    import wbgapi as wb

    dev = wb.data.DataFrame(["NY.GDP.PCAP.KD", "SP.DYN.LE00.IN"], time=2019,
                            skipAggs=True, labels=True).reset_index()   # skip regions
    dev.columns = ["code", "country", "gdp_pc", "life_exp"]
    dev = dev.dropna()
    dev["log_gdp_pc"] = np.log(dev["gdp_pc"])

    dev.plot.scatter(x="gdp_pc", y="life_exp", logx=True)
    pf.feols("life_exp ~ log_gdp_pc", data=dev, vcov="hetero").summary()
    ```

**Check:** about **208 countries**. The coefficient on log GDP per capita is about **4.6**, and income alone explains about 70% of the variation in life expectancy (R² ≈ 0.69). Doubling income goes with about 3.2 more years of life (4.6 × ln 2).

!!! note "The World Bank list varies slightly"
    Stata's `wbopendata` returns 209 economies and a coefficient of 4.59, because its country list differs by one economy. Small differences like this are normal when data come from a live source.

The relationship is not causal on its own. Healthier people can work more, and richer countries can afford better health care, so causation runs both ways. Development economists use experiments and natural experiments to untangle it.

## More project ideas

1. **Move the curve.** Repeat for 1960, 1990 and 2019. Has the whole curve shifted up? Preston argued most gains came from shifts, such as new medicines, not from moving along the curve.
2. **Outliers.** Which countries live much longer, or shorter, than their income predicts? Use the residuals.
3. **Education and income.** Replace life expectancy with years of schooling (`SE.SCH.LIFE`) or literacy.
4. **Growth and investment.** Use the Penn World Table to relate investment rates to growth over 30 years.

## Classic papers

- Preston (1975), "The Changing Relation between Mortality and Level of Economic Development", *Population Studies*
- Acemoglu, Johnson and Robinson (2001), "The Colonial Origins of Comparative Development: An Empirical Investigation", *American Economic Review*
- Miguel and Kremer (2004), "Worms: Identifying Impacts on Education and Health in the Presence of Treatment Externalities", *Econometrica*
- Banerjee and Duflo (2011), *Poor Economics*: an accessible book on what works against poverty
