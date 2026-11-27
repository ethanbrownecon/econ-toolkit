# Industrial organization

Industrial organization (IO) studies how firms compete: market power, pricing, mergers, entry and regulation. IO economists advise antitrust agencies on whether a merger will raise prices, and study why some markets are competitive while others are not.

## Big questions

- Does less competition mean higher prices?
- Will a proposed merger hurt consumers?
- How do firms set prices, and why do prices for the same product differ?
- When do new firms enter a market, and how does that change prices?
- How should digital platforms such as app stores and search engines be regulated?

## Methods you will use

[Panel fixed effects](../econometrics/panel.md) · [instrumental variables](../econometrics/iv.md) · [difference-in-differences](../econometrics/did.md) around mergers and entry · demand estimation

## Data

| Source | What it has |
|---|---|
| [BTS airline data (DB1B)](https://www.transtats.bts.gov/) | A 10% sample of US airline tickets with fares, routes and carriers |
| [SEC EDGAR](https://www.sec.gov/edgar/search/) | Company financial filings |
| [Kilts Center (NielsenIQ)](https://www.chicagobooth.edu/research/kilts/research-data) | Store-level retail prices and sales, free for academic use through universities |
| [FTC merger cases](https://www.ftc.gov/legal-library/browse/cases-proceedings) | Details of challenged mergers |

## Starter project: does less competition raise airfares?

On routes dominated by one airline, are fares higher? `airfare` has 1,149 US routes observed every year from 1997 to 2000. `concen` is the largest airline's share of passengers on the route, from 0 to 1.

=== "Stata"

    ```stata
    bcuse airfare, clear                  // ssc install bcuse
    xtset id year

    * Across routes, controlling for distance
    regress lfare concen ldist ldistsq i.year, vce(cluster id)

    * Within a route over time
    xtreg lfare concen i.year, fe vce(cluster id)
    ```

=== "R"

    ```r
    library(fixest)
    data("airfare", package = "wooldridge")

    across <- feols(lfare ~ concen + ldist + ldistsq | year, data = airfare, cluster = ~id)
    within <- feols(lfare ~ concen | id + year, data = airfare, cluster = ~id)
    etable(across, within)
    ```

=== "Python"

    ```python
    import pyfixest as pf
    import wooldridge

    airfare = wooldridge.data("airfare")
    across = pf.feols("lfare ~ concen + ldist + ldistsq | year", data=airfare, vcov={"CRV1": "id"})
    within = pf.feols("lfare ~ concen | id + year", data=airfare, vcov={"CRV1": "id"})
    pf.etable([across, within])
    ```

**Check:**

| Model | `concen` coefficient |
|---|---:|
| Across routes, controlling for distance | 0.360 |
| Within a route over time (route fixed effects) | 0.169 |

Across routes, a 10-point rise in the largest airline's share (0.1 on this scale) goes with fares about 3.6% higher. Within the same route over time, the effect halves to about 1.7%. Routes with dominant airlines differ in other ways, such as being hubs or business routes. Fixed effects remove those stable differences, which is why the estimate falls.

## More project ideas

1. **Entry by low-cost carriers.** Use BTS data to compare fares on routes before and after Southwest enters, against routes it does not enter: a [difference-in-differences](../econometrics/did.md).
2. **A merger.** Pick an airline merger, such as American and US Airways in 2013. Did fares rise on routes where both used to compete?
3. **Gas prices.** Compare gas stations' prices against how many competitors are nearby.
4. **Price dispersion.** Why do passengers on the same flight pay such different fares? Read Borenstein and Rose (1994).

## Classic papers

- Bresnahan and Reiss (1991), "Entry and Competition in Concentrated Markets", *Journal of Political Economy*
- Borenstein and Rose (1994), "Competition and Price Dispersion in the U.S. Airline Industry", *Journal of Political Economy*
- Berry, Levinsohn and Pakes (1995), "Automobile Prices in Market Equilibrium", *Econometrica*
