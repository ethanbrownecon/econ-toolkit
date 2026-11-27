# International trade

International trade studies why countries trade, what they trade, and how trade and trade policy affect growth, jobs and prices.

## Big questions

- Why do countries trade, and who gains and loses?
- Do tariffs protect jobs, or raise prices for everyone?
- How did trade with China affect US manufacturing workers?
- Does trade make countries grow faster?
- How do distance, borders and language shape trade?

## Methods you will use

Cross-country [regression](../econometrics/ols.md) · the gravity model · [instrumental variables](../econometrics/iv.md) · [difference-in-differences](../econometrics/did.md) around tariff changes · [panel fixed effects](../econometrics/panel.md)

## Data

| Source | What it has |
|---|---|
| [UN Comtrade](https://comtradeplus.un.org/) | Trade flows between countries, by product |
| [CEPII Gravity database](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8) | Bilateral trade with distance, language and borders |
| [World Bank Open Data](https://data.worldbank.org/) | Trade shares, tariffs and GDP for every country |
| [US Census Bureau trade data](https://www.census.gov/foreign-trade/data/index.html) | US imports and exports by product and partner |

## Starter project: why do small countries trade more?

The United States trades less, relative to the size of its economy, than Belgium or Singapore. Is that a general pattern? Compare trade openness (exports plus imports as a share of GDP) with population, using World Bank data for 2019.

=== "Stata"

    ```stata
    ssc install wbopendata
    set timeout1 120                              // give the World Bank more time
    set timeout2 600
    wbopendata, indicator(NE.TRD.GNFS.ZS; SP.POP.TOTL) year(2019) long clear nometadata
    drop if regionname == "Aggregates"            // keep countries, not regions
    rename ne_trd_gnfs_zs trade_gdp
    gen log_pop = ln(sp_pop_totl)
    drop if missing(trade_gdp, log_pop)

    twoway (scatter trade_gdp log_pop) (lfit trade_gdp log_pop)
    regress trade_gdp log_pop, vce(robust)
    ```

=== "R"

    ```r
    library(tidyverse)
    library(fixest)
    library(WDI)

    trade <- WDI(indicator = c(trade_gdp = "NE.TRD.GNFS.ZS", pop = "SP.POP.TOTL"),
                 start = 2019, end = 2019, extra = TRUE) %>%
      filter(region != "Aggregates") %>%
      drop_na(trade_gdp, pop)

    ggplot(trade, aes(pop, trade_gdp)) + geom_point() + scale_x_log10() + geom_smooth(method = "lm")
    feols(trade_gdp ~ log(pop), data = trade, vcov = "hetero")
    ```

=== "Python"

    ```python
    import numpy as np
    import pyfixest as pf
    import wbgapi as wb

    trade = wb.data.DataFrame(["NE.TRD.GNFS.ZS", "SP.POP.TOTL"], time=2019,
                              skipAggs=True, labels=True).reset_index()
    trade.columns = ["code", "country", "trade_gdp", "pop"]
    trade = trade.dropna()
    trade["log_pop"] = np.log(trade["pop"])

    trade.plot.scatter(x="pop", y="trade_gdp", logx=True)
    pf.feols("trade_gdp ~ log_pop", data=trade, vcov="hetero").summary()
    ```

**Check:** **183 countries**. The coefficient on log population is about **−11**: a country twice as large trades about 7.6 percentage points less of its GDP (11 × ln 2). Among the least open economies in 2019 were Cuba, Sudan and the United States, each at about 23–26%.

Why? A large country contains more variety within its borders, so more of its trade is internal: Texas trades with California instead of with another country. Small countries must buy more from abroad.

## More project ideas

1. **The gravity model.** Using CEPII data, regress log bilateral trade on log GDP of both countries and log distance. Trade falls with distance almost everywhere, with an elasticity near −1.
2. **Openness and growth.** Does openness predict faster growth? Think about why a simple regression cannot answer this, and read Frankel and Romer (1999).
3. **The China shock.** Using Census trade data, track US imports from China since 2000 by industry.
4. **Tariffs.** Compare US import prices for goods hit by the 2018 tariffs with goods that were not.

## Classic papers

- Alesina and Wacziarg (1998), "Openness, Country Size and Government", *Journal of Public Economics*
- Frankel and Romer (1999), "Does Trade Cause Growth?", *American Economic Review*
- Autor, Dorn and Hanson (2013), "The China Syndrome: Local Labor Market Effects of Import Competition in the United States", *American Economic Review*
