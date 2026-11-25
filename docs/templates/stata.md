# Stata do-file template

[:material-download: Download analysis.do](files/analysis.do){ .md-button .md-button--primary download }
[:material-download: Download master.do](files/master.do){ .md-button download }

## The template

```stata title="code/01_analysis.do"
--8<-- "analysis.do"
```

## What each part does

| Part | Why it is there |
|---|---|
| Header comment | Says what the file does and which files it reads and writes. |
| `version 18` | Runs the code with Stata 18 rules, so results do not change after you upgrade. |
| `clear all` | Starts from an empty memory, so nothing from an earlier session leaks in. |
| `set varabbrev off` | Stops Stata guessing that `inc` means `income`. A typo becomes an error, not a silent mistake. |
| `set seed` | Makes random draws (bootstraps, samples) give the same result every run. |
| `global root` | The only line you change on a new computer. Every other path builds on it. |
| `log using` | Saves everything the do-file prints, so you can check the results later. |
| `isid id year` | Stops the do-file if two rows share the same `id` and `year`. |
| `eststo` / `esttab` | Stores each regression and writes them into one LaTeX table. |

## Run the whole project

When a project has several do-files, a master file runs them in order. Set `global root` here and remove it from the other files.

```stata title="code/00_master.do"
--8<-- "master.do"
```

??? note "Packages used"
    `reghdfe` runs fixed-effects regressions. It needs `require` and `ftools`. `estout` provides `eststo` and `esttab`. Install them once with `ssc install`, as shown in the setup section.
