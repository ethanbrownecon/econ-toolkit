"""
Create the simulated practice dataset used in docs/projects/wages.md.

The data are made up. They mimic a small labor-force survey and include
deliberate problems for students to clean: duplicate rows, inconsistent
capitalization, missing wages and a few impossible values.

Run from the repository root:
    python scripts/make_practice_data.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path("docs/projects/data/wages.csv")
N = 1000
rng = np.random.default_rng(20260101)

age = rng.integers(18, 65, N)
educ = rng.choice(
    np.arange(8, 21),
    size=N,
    p=np.array([1, 1, 2, 3, 22, 10, 12, 6, 22, 4, 8, 4, 5]) / 100,
)
educ = np.minimum(educ, age - 6)
exper = np.maximum(age - educ - 6, 0)
female = rng.integers(0, 2, N)
union = (rng.random(N) < 0.12).astype(int)
state = rng.choice(["CA", "TX", "NY", "FL", "OH", "MI", "GA", "WA"], size=N)
hours = np.clip(np.round(rng.normal(39, 8, N)), 10, 70).astype(int)

ln_wage = (
    1.55
    + 0.085 * educ
    + 0.032 * exper
    - 0.0005 * exper**2
    - 0.16 * female
    + 0.12 * union
    + rng.normal(0, 0.42, N)
)
wage = np.round(np.exp(ln_wage), 2)

# Messy sex labels
sex = np.where(female == 1, "Female", "Male").astype(object)
messy = rng.random(N)
sex[(messy < 0.10)] = np.where(female[messy < 0.10] == 1, "female", "male")
sex[(messy > 0.95)] = np.where(female[messy > 0.95] == 1, "FEMALE", "MALE")

df = pd.DataFrame(
    {
        "id": np.arange(1001, 1001 + N),
        "age": age,
        "sex": sex,
        "educ": educ,
        "state": state,
        "union": union,
        "hours": hours,
        "wage": wage,
    }
)

# Missing wages
missing_rows = rng.choice(N, 25, replace=False)
df["wage"] = df["wage"].astype(object)
df.loc[missing_rows, "wage"] = np.nan

# Impossible wages (data-entry errors)
bad_rows = rng.choice(np.setdiff1d(np.arange(N), missing_rows), 4, replace=False)
df.loc[bad_rows, "wage"] = [0, 0, -1, 0]

# Duplicate rows
dupes = df.sample(8, random_state=1)
df = pd.concat([df, dupes]).sort_values("id").reset_index(drop=True)

OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} rows to {OUT}")
