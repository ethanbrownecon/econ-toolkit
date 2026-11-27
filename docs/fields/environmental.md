# Environmental economics

Environmental economics studies pollution, climate change and natural resources. A central problem is that clean air and a stable climate have no market price, so economists find ways to measure what people are willing to pay for them.

## Big questions

- What is clean air, or a stable climate, worth to people?
- Do carbon taxes and cap-and-trade cut emissions, and at what cost?
- How does pollution affect health, learning and productivity?
- Who bears the costs of pollution, and is it fair?
- How should countries share the costs of climate change?

## Methods you will use

Hedonic [regression](../econometrics/ols.md) · [difference-in-differences](../econometrics/did.md) · [regression discontinuity](../econometrics/rd.md) · [instrumental variables](../econometrics/iv.md)

## Data

| Source | What it has |
|---|---|
| [EPA Air Quality System](https://www.epa.gov/aqs) | Pollution readings from monitors across the US |
| [NOAA Climate Data](https://www.ncei.noaa.gov/cdo-web/) | Weather and climate records |
| [EIA Open Data](https://www.eia.gov/opendata/) | Energy production, prices and emissions |
| [Our World in Data: CO₂](https://ourworldindata.org/co2-and-greenhouse-gas-emissions) | Emissions by country since 1750 |

## Projects on this site

- [Difference-in-differences](../econometrics/did.md#part-1-the-classic-two-by-two): an incinerator lowers nearby house prices

## Starter project: what is clean air worth?

If people value clean air, they will pay more for houses in less polluted neighborhoods. Comparing house prices across areas with different pollution, while holding the house fixed, reveals that value. This is a **hedonic** regression. `hprice2` has 506 Boston-area communities from Harrison and Rubinfeld (1978).

| Variable | Meaning |
|---|---|
| `lprice` | Log median house price |
| `lnox` | Log nitrogen oxide concentration (air pollution) |
| `rooms` | Average rooms per house |
| `stratio` | Student-teacher ratio in local schools |
| `dist` | Distance to employment centers |

=== "Stata"

    ```stata
    bcuse hprice2, clear                  // ssc install bcuse
    regress lprice lnox rooms stratio dist, vce(robust)
    ```

=== "R"

    ```r
    library(fixest)
    data("hprice2", package = "wooldridge")

    feols(lprice ~ lnox + rooms + stratio + dist, data = hprice2, vcov = "hetero")
    ```

=== "Python"

    ```python
    import pyfixest as pf
    import wooldridge

    hprice2 = wooldridge.data("hprice2")
    pf.feols("lprice ~ lnox + rooms + stratio + dist", data=hprice2, vcov="hetero").summary()
    ```

**Check:** the coefficient on `lnox` is about **−0.97**. Both variables are in logs, so this is an elasticity: a 10% increase in pollution goes with about 10% lower house prices, holding house size, schools and location fixed.

Polluted areas may also differ in ways the data miss, such as industry, noise or crime. Chay and Greenstone (2005) solve this with a natural experiment: the Clean Air Act forced some counties, but not others, to cut pollution.

## More project ideas

1. **The environmental Kuznets curve.** Do emissions rise and then fall as countries get richer? Regress CO₂ per person (`EN.GHG.CO2.PC.CE.AR5` from the World Bank) on log GDP per capita and its square, using the [development starter](development.md#starter-project-richer-countries-longer-lives) as a template.
2. **Heat and productivity.** Combine NOAA temperatures with county employment or output. Do very hot days lower productivity?
3. **Power plant closures.** Use a [difference-in-differences](../econometrics/did.md) design around coal plant closures and nearby pollution or health.
4. **Carbon prices.** Compare emissions in countries before and after they adopted a carbon tax, using [synthetic control](../econometrics/synthetic.md).

## Classic papers

- Harrison and Rubinfeld (1978), "Hedonic Housing Prices and the Demand for Clean Air", *Journal of Environmental Economics and Management*
- Chay and Greenstone (2005), "Does Air Quality Matter? Evidence from the Housing Market", *Journal of Political Economy*
- Currie and Walker (2011), "Traffic Congestion and Infant Health: Evidence from E-ZPass", *American Economic Journal: Applied Economics*
