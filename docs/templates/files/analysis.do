/*==============================================================================
  Project:  My project
  File:     01_analysis.do
  Purpose:  Clean the survey data and estimate the wage regressions
  Author:   Your Name
  Created:  2026-01-01
  Inputs:   data/raw/survey.dta
  Outputs:  data/clean/survey_clean.dta
            output/tables/wage_regs.tex
            output/figures/wage_educ.png
==============================================================================*/


* 0. Setup ---------------------------------------------------------------------

version 18              // run with Stata 18 rules, even on newer Stata
clear all
set more off
set varabbrev off       // stop Stata guessing variable names
set seed 20260101       // makes random draws repeatable

* Project folder: change this one line on a new computer
global root "~/projects/my-project"

global raw     "$root/data/raw"
global clean   "$root/data/clean"
global tables  "$root/output/tables"
global figures "$root/output/figures"
global logs    "$root/output/logs"

capture log close
log using "$logs/01_analysis.log", replace text

* Packages: remove the * and run once per computer
* ssc install require, replace
* ssc install reghdfe, replace
* ssc install ftools, replace
* ssc install estout, replace


* 1. Load data -----------------------------------------------------------------

use "$raw/survey.dta", clear


* 2. Clean ---------------------------------------------------------------------

rename *, lower                 // all variable names in lower case
drop if missing(id)
isid id year                    // stop if id-year is not unique


* 3. Create variables ----------------------------------------------------------

gen ln_wage = ln(wage)
label variable ln_wage "Log hourly wage"
label variable educ    "Years of education"


* 4. Analysis ------------------------------------------------------------------

eststo clear
eststo m1: regress ln_wage educ, vce(robust)
eststo m2: reghdfe ln_wage educ, absorb(id year) vce(cluster id)


* 5. Save results --------------------------------------------------------------

esttab m1 m2 using "$tables/wage_regs.tex", replace se label booktabs

twoway (scatter ln_wage educ) (lfit ln_wage educ)
graph export "$figures/wage_educ.png", replace width(1800)

save "$clean/survey_clean.dta", replace

log close
