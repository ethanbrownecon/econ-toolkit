# Political economy and law

Political economy studies how political institutions shape economic outcomes: elections, voting, lobbying and the design of government. Law and economics applies economic reasoning to laws, crime and courts.

## Big questions

- Do politicians already in office have an unfair advantage?
- Do more police reduce crime?
- How do harsher punishments affect behavior?
- Do democracies grow faster than autocracies?
- How do campaign spending and lobbying affect policy?

## Methods you will use

[Regression discontinuity](../econometrics/rd.md) at election cutoffs and legal thresholds · [difference-in-differences](../econometrics/did.md) around law changes · [instrumental variables](../econometrics/iv.md) · [synthetic control](../econometrics/synthetic.md)

## Data

| Source | What it has |
|---|---|
| [MIT Election Data and Science Lab](https://electionlab.mit.edu/data) | US election results by state, county and district |
| [Voteview](https://voteview.com/data) | Every roll-call vote in Congress, with ideology scores |
| [FBI Crime Data Explorer](https://cde.ucr.cjis.gov/) | Reported crime by agency and year |
| [V-Dem](https://www.v-dem.net/data/) | Democracy indicators for every country since 1789 |

## Projects on this site

- [Replication: drunk driving](../projects/replication-hansen.md): do harsher penalties deter repeat offenses?
- [Replication: stand your ground laws](../projects/replication-castle.md): did expanding self-defense law increase homicides?

## Starter project: the incumbency advantage

Does holding a Senate seat help a party win it again? Comparing seats a party won by a landslide with seats it lost is unfair, because those states differ. Comparing **very close** elections is fair: a party that won by 0.5 points and one that lost by 0.5 points faced almost identical voters.

This is the worked example on the **[regression discontinuity page](../econometrics/rd.md#run-it)**, with code in Stata, R and Python.

**Key result:** barely winning a Senate seat raises the party's vote share in the next election for that seat by about **7.4 percentage points**.

## More project ideas

1. **House elections.** Repeat the incumbency design for the US House using MIT Election Lab data, following Lee (2008).
2. **Police and crime.** Do cities that hire more police have less crime? Think about why a simple regression is misleading, then read Levitt (1997).
3. **Close elections and policy.** Do cities that narrowly elect a mayor from one party spend differently? Combine election results with Census of Governments finances.
4. **Polarization.** Use Voteview ideology scores to chart how far apart the two parties in Congress have moved since 1950.

## Classic papers

- Becker (1968), "Crime and Punishment: An Economic Approach", *Journal of Political Economy*
- Levitt (1997), "Using Electoral Cycles in Police Hiring to Estimate the Effect of Police on Crime", *American Economic Review*
- Lee (2008), "Randomized Experiments from Non-random Selection in U.S. House Elections", *Journal of Econometrics*
