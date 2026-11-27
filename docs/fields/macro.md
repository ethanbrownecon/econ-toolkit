# Macroeconomics

Macroeconomics studies the economy as a whole: growth, recessions, unemployment, inflation, and what central banks and governments can do about them.

## Big questions

- What causes recessions, and how can policy shorten them?
- How does monetary policy affect inflation and jobs?
- Is there a trade-off between inflation and unemployment?
- What drives long-run growth?
- How large are the effects of government spending and tax cuts?

## Methods you will use

Time-series [regression](../econometrics/ols.md) · [panel data](../econometrics/panel.md) across countries or states · natural experiments and narrative identification · [charts](../data-viz/README.md) of long time series

## Data

| Source | What it has |
|---|---|
| [FRED](https://fred.stlouisfed.org/) | 800,000+ US and international series ([API guide](../data/apis.md#apis-with-a-key-fred)) |
| [Bureau of Economic Analysis](https://www.bea.gov/data) | US GDP, income and spending |
| [IMF World Economic Outlook](https://www.imf.org/en/Publications/WEO) | Forecasts and history for every country |
| [Penn World Table](https://www.rug.nl/ggdc/productivity/pwt/) | Long-run growth across countries |

## Starter project: the economy in charts

The macro starter is a full guided project on this site: **[Project 2: The economy in charts](../projects/fred.md)**. You download 75 years of US data from FRED, shade recessions, test the Phillips curve decade by decade and estimate Okun's law, in Stata, R or Python.

**Key results:** the Phillips curve holds in the 1960s (correlation −0.81) and breaks down in the 1970s (+0.14). Okun's law: each extra point of GDP growth lowers unemployment by about 0.42 points.

## More project ideas

1. **The Fed's reaction.** Plot the federal funds rate (`FEDFUNDS`) against inflation and unemployment. Does it follow a Taylor rule? Regress the rate on inflation and the unemployment gap.
2. **Recessions compared.** How long did unemployment take to return to its pre-recession level after 1982, 1991, 2001, 2008 and 2020?
3. **State business cycles.** Use FRED's state unemployment series (such as `CAUR`) to see which states were hit hardest in 2008 and 2020, and relate it to industry mix.
4. **Inflation expectations.** Compare actual inflation with the University of Michigan's inflation expectations series (`MICH`).

## Classic papers

- Okun (1962), "Potential GNP: Its Measurement and Significance", *Proceedings of the Business and Economic Statistics Section, American Statistical Association*
- Friedman (1968), "The Role of Monetary Policy", *American Economic Review*
- Romer and Romer (2004), "A New Measure of Monetary Shocks: Derivation and Implications", *American Economic Review*
