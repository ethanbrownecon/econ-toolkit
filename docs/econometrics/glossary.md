# Glossary

Plain-English definitions of the terms you will meet in econometrics papers and on this site. Use the search box (top right) to jump to a term. Links go to the page that explains it in depth.

## A–C

| Term | Meaning |
|---|---|
| **Average marginal effect (AME)** | The average change in the outcome, usually a probability, for a one-unit change in x. Used to make [logit and probit](logit.md) results readable. |
| **Average treatment effect (ATE)** | The average effect of a treatment across everyone in the population. |
| **Average treatment effect on the treated (ATT)** | The average effect for the people who actually received the treatment. Most [matching](matching.md) and [DiD](did.md) estimates are ATTs. |
| **Bandwidth** | In [regression discontinuity](rd.md), how far from the cutoff observations can be and still be used. |
| **Bias** | When an estimator is systematically wrong: on average, it misses the true value. |
| **Binned scatter plot** | A chart that groups x into bins and plots the average y in each. See [data visualization](../data-viz/README.md#5-binned-scatter-plot). |
| **Causal effect** | How much the outcome would change if you changed the treatment and nothing else. |
| **Clustered standard errors** | Standard errors that allow observations in the same group (a state, a school, a person over time) to be related. Cluster at the level the treatment is assigned. |
| **Coefficient** | The number a regression estimates for each variable: how much the outcome changes when that variable rises by one unit, holding the others fixed. |
| **Common support** | See *overlap*. |
| **Compliers** | In [IV](iv.md), the people whose treatment is changed by the instrument. IV estimates the effect for them. |
| **Confidence interval** | A range of values consistent with the data. A 95% interval built this way contains the true value in 95% of samples. |
| **Confounder** | A variable that affects both the treatment and the outcome, creating a misleading correlation. |
| **Control group** | The units that do not receive the treatment, used to show what would have happened without it. |
| **Counterfactual** | What would have happened to the treated units if they had not been treated. Every causal method is a way to estimate it. |
| **Covariate** | Another name for a control variable. |
| **Cross-section** | Data on many units at one point in time. |
| **Cross-validation** | Splitting data into folds, training on some and testing on the rest, to judge how well a model predicts. See [machine learning](../machine-learning/README.md). |

## D–H

| Term | Meaning |
|---|---|
| **Difference-in-differences (DiD)** | Comparing the change over time in a treated group with the change in a control group. See [DiD](did.md). |
| **Dummy variable** | A variable equal to 1 or 0, such as `female` or `treated`. Also called an indicator. |
| **Elasticity** | The percentage change in y for a 1% change in x. A log-log regression estimates it directly. |
| **Endogeneity** | When a regressor is correlated with the error term, because of omitted variables, reverse causality or measurement error. OLS is then biased. |
| **Event study** | A DiD that estimates a separate effect for each period before and after treatment. Pre-treatment effects near zero support parallel trends. |
| **Exclusion restriction** | In [IV](iv.md), the assumption that the instrument affects the outcome only through the treatment. It cannot be tested. |
| **External validity** | Whether a result applies to other people, places or times. |
| **First stage** | In [IV](iv.md), the regression of the treatment on the instrument. It must be strong. |
| **Fixed effects** | A separate intercept for each unit (or period), which removes everything about it that does not change. See [panel data](panel.md). |
| **Fuzzy RD** | A [regression discontinuity](rd.md) where crossing the cutoff raises the chance of treatment but does not guarantee it. Estimated like IV. |
| **Hausman test** | A test of whether [fixed and random effects](panel.md) give significantly different answers. If they do, prefer fixed effects. |
| **Heterogeneous effects** | When the treatment affects different units by different amounts. |
| **Heteroskedasticity** | When the spread of the errors differs across observations. Use robust standard errors. |

## I–O

| Term | Meaning |
|---|---|
| **Identification** | The argument for why your estimate is a causal effect rather than just a correlation. "What is your identification strategy?" means "what is your research design?" |
| **Instrument** | A variable that shifts the treatment but has no other link to the outcome. See [IV](iv.md). |
| **Internal validity** | Whether a result is a credible causal effect for the sample studied. |
| **Interaction** | A term like `x1 × x2` that lets the effect of one variable depend on another. |
| **Intention to treat (ITT)** | The effect of being *offered* or *assigned* a treatment, whether or not people take it up. |
| **Linear probability model (LPM)** | OLS with a 0/1 outcome. Coefficients are changes in probability. See [logit and probit](logit.md). |
| **Local average treatment effect (LATE)** | The effect for compliers. What [IV](iv.md) estimates. |
| **Log-odds** | The log of p / (1 − p). Logit coefficients are changes in log-odds. |
| **Manipulation** | In [RD](rd.md), when people sort themselves to one side of the cutoff. Checked with a density test. |
| **Marginal effect** | The change in the outcome for a small change in x. |
| **Measurement error** | When a variable is recorded with noise. Error in a regressor biases its coefficient toward zero. |
| **Multicollinearity** | When regressors are highly correlated, making their separate effects imprecise. Perfect collinearity means one must be dropped. |
| **Natural experiment** | A real-world event or rule that assigns treatment as if at random, such as a lottery, a cutoff or a policy change. |
| **Odds ratio** | How a variable multiplies the odds of the outcome. Reported by logit with the `or` option. |
| **Omitted variable bias** | Bias from leaving out a confounder. The core problem with treating OLS as causal. |
| **Ordinary least squares (OLS)** | The standard linear regression: it picks coefficients that minimize squared prediction errors. See [linear regression](ols.md). |
| **Overfitting** | When a model fits noise in the training data and predicts new data poorly. |
| **Overidentification test** | With more instruments than endogenous variables, a test of whether the instruments agree. It cannot prove the exclusion restriction. |
| **Overlap** | Treated and control units with similar characteristics both exist. Needed for [matching](matching.md). |

## P–R

| Term | Meaning |
|---|---|
| **p-value** | The probability of a result at least this extreme if the true effect were zero. Below 0.05 is conventionally "statistically significant". It is not the probability that the effect is real. |
| **Panel data** | The same units observed over several periods. See [panel data](panel.md). |
| **Parallel trends** | The DiD assumption: without treatment, treated and control groups would have moved in parallel. |
| **Placebo test** | Running the analysis where there should be no effect (a fake treatment date, an unaffected outcome) to check the design. |
| **Pooled OLS** | OLS on panel data that ignores the panel structure. |
| **Potential outcomes** | The outcomes a unit would have with and without treatment. Only one is ever observed. |
| **Pre-trends** | Differences in trends between treated and control groups before treatment. They cast doubt on parallel trends. |
| **Propensity score** | The probability of being treated given observed characteristics. See [matching](matching.md). |
| **R²** | The share of variation in the outcome explained by the model. A low R² does not mean the coefficients are wrong. |
| **Random effects** | A panel model that treats unit effects as random and unrelated to the regressors. See [panel data](panel.md). |
| **Randomized controlled trial (RCT)** | An experiment where treatment is assigned by chance. The gold standard for causal effects. |
| **Reduced form** | The regression of the outcome directly on the instrument. In IV, reduced form ÷ first stage = the IV estimate. |
| **Regression discontinuity (RD)** | Comparing units just above and just below a cutoff. See [RD](rd.md). |
| **Reverse causality** | When the outcome causes the treatment rather than the other way around. |
| **Robust standard errors** | Standard errors that remain valid with heteroskedasticity. A sensible default. |
| **Running variable** | In [RD](rd.md), the score that determines treatment, such as a test score or vote margin. |

## S–Z

| Term | Meaning |
|---|---|
| **Selection bias** | When treated and untreated groups differ in ways that also affect the outcome. |
| **Selection on observables** | The assumption that, once you control for observed variables, treatment is as good as random. Behind OLS and [matching](matching.md). |
| **Staggered adoption** | When units are treated at different times. Requires modern [DiD](did.md#part-3-staggered-timing-and-why-twfe-can-mislead) estimators. |
| **Standard error** | How much an estimate would vary across samples. Smaller means more precise. |
| **Statistical significance** | When a p-value is below a chosen level, usually 0.05. Says nothing about whether an effect is large or important. |
| **Synthetic control** | A weighted mix of untreated units that tracks a treated unit before treatment. See [synthetic control](synthetic.md). |
| **t-statistic** | A coefficient divided by its standard error. Above about 2 in absolute value means p < 0.05. |
| **Treatment** | The policy, program or condition whose effect you want to measure. |
| **Two-stage least squares (2SLS)** | The standard way to estimate [IV](iv.md). |
| **Two-way fixed effects (TWFE)** | A regression with unit and time fixed effects. The classic DiD estimator. |
| **Weak instrument** | An instrument that barely moves the treatment. Rule of thumb: first-stage F below 10. |
| **Within estimator** | Another name for the fixed effects estimator: it uses variation within each unit over time. |
