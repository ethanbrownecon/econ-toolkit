# Urban and real estate economics

Urban economics studies cities: why people and firms cluster together, what drives housing costs, and how neighborhoods shape people's lives. Real estate economics focuses on housing and property markets.

## Big questions

- Why are housing costs so high in some cities?
- How much does the neighborhood you grow up in affect your future earnings?
- Why do firms and workers cluster in expensive cities?
- Do zoning and building restrictions raise prices?
- How do transport, crime and schools affect house prices?

## Methods you will use

Hedonic [regression](../econometrics/ols.md) · [difference-in-differences](../econometrics/did.md) · [regression discontinuity](../econometrics/rd.md) at school-district boundaries · [panel fixed effects](../econometrics/panel.md)

## Data

| Source | What it has |
|---|---|
| [Zillow Research](https://www.zillow.com/research/data/) | House prices and rents by region, monthly |
| [Census ACS](https://data.census.gov/) | Housing, income and population by neighborhood |
| [Opportunity Insights](https://opportunityinsights.org/data/) | Children's future earnings by the neighborhood they grew up in |
| [FRED housing series](https://fred.stlouisfed.org/categories/97) | National and metro house price indexes, mortgage rates |

## Projects on this site

- [Difference-in-differences](../econometrics/did.md#part-1-the-classic-two-by-two): an incinerator and nearby house prices
- [Environmental economics](environmental.md): what clean air adds to house prices

## Starter project: what sets a house's price?

A house is a bundle of features: size, bedrooms, land and style. A hedonic regression asks how much each feature adds to the price. `hprice1` has 88 house sales in Boston in 1990.

| Variable | Meaning |
|---|---|
| `lprice` | Log sale price |
| `lsqrft` | Log size in square feet |
| `bdrms` | Number of bedrooms |
| `llotsize` | Log lot size |
| `colonial` | 1 if colonial style |

=== "Stata"

    ```stata
    bcuse hprice1, clear                  // ssc install bcuse
    regress lprice lsqrft bdrms llotsize colonial, vce(robust)
    ```

=== "R"

    ```r
    library(fixest)
    data("hprice1", package = "wooldridge")

    feols(lprice ~ lsqrft + bdrms + llotsize + colonial, data = hprice1, vcov = "hetero")
    ```

=== "Python"

    ```python
    import pyfixest as pf
    import wooldridge

    hprice1 = wooldridge.data("hprice1")
    pf.feols("lprice ~ lsqrft + bdrms + llotsize + colonial",
             data=hprice1, vcov="hetero").summary()
    ```

**Check:** the coefficient on `lsqrft` is about **0.71**: a 10% bigger house sells for about 7% more, holding bedrooms and lot size fixed.

Notice that bedrooms add little once size is controlled for. An extra bedroom in the same total space means smaller rooms. This is a good example of why "holding other things constant" matters when you read a coefficient.

## More project ideas

1. **Price-to-rent ratios.** Use Zillow data to compare house prices and rents across metro areas. Where is buying expensive relative to renting?
2. **Neighborhoods and mobility.** Use Opportunity Insights county data to relate children's adult incomes to local school quality, segregation or income inequality.
3. **Mortgage rates and prices.** Use FRED to chart the 30-year mortgage rate against the national house price index since 2000.
4. **School districts.** Compare house prices just on either side of a school-district boundary, a [regression discontinuity](../econometrics/rd.md) design.

## Classic papers

- Roback (1982), "Wages, Rents, and the Quality of Life", *Journal of Political Economy*
- Glaeser and Gyourko (2005), "Urban Decline and Durable Housing", *Journal of Political Economy*
- Chetty, Hendren and Katz (2016), "The Effects of Exposure to Better Neighborhoods on Children: New Evidence from the Moving to Opportunity Experiment", *American Economic Review*
