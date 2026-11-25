"""
Project:  My project
File:     01_analysis.py
Purpose:  Clean the survey data and estimate the wage regressions
Author:   Your Name
Created:  2026-01-01
Inputs:   data/raw/survey.dta
Outputs:  data/clean/survey_clean.dta
          output/tables/wage_regs.tex
          output/figures/wage_educ.png
"""

# %% 0. Setup -------------------------------------------------------------------

# Packages: run once per computer, in a terminal
# pip install pandas numpy pyfixest seaborn matplotlib

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyfixest as pf
import seaborn as sns

# Project folder. Works when you run the file and when you run cells.
try:
    ROOT = Path(__file__).resolve().parents[1]  # this file lives in code/
except NameError:
    ROOT = Path.cwd().parent if Path.cwd().name == "code" else Path.cwd()

RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
TABLES = ROOT / "output" / "tables"
FIGURES = ROOT / "output" / "figures"

rng = np.random.default_rng(20260101)  # makes random draws repeatable


# %% 1. Load data ---------------------------------------------------------------

df = pd.read_stata(RAW / "survey.dta")


# %% 2. Clean -------------------------------------------------------------------

df.columns = df.columns.str.lower()  # all column names in lower case
df = df.dropna(subset=["id"])

assert not df.duplicated(["id", "year"]).any(), "id-year is not unique"


# %% 3. Create variables --------------------------------------------------------

df["ln_wage"] = np.log(df["wage"])


# %% 4. Analysis ----------------------------------------------------------------

m1 = pf.feols("ln_wage ~ educ", data=df, vcov="hetero")
m2 = pf.feols("ln_wage ~ educ | id + year", data=df, vcov={"CRV1": "id"})

pf.etable([m1, m2])


# %% 5. Save results ------------------------------------------------------------

(TABLES / "wage_regs.tex").write_text(pf.etable([m1, m2], type="tex"))

fig, ax = plt.subplots(figsize=(6, 4))
sns.regplot(data=df, x="educ", y="ln_wage", scatter_kws={"alpha": 0.3}, ax=ax)
ax.set(xlabel="Years of education", ylabel="Log hourly wage")
fig.savefig(FIGURES / "wage_educ.png", dpi=300, bbox_inches="tight")

df.to_stata(CLEAN / "survey_clean.dta", write_index=False)
