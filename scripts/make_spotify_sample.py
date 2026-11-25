"""
Create a fake Spotify listening history for docs/projects/spotify.md.

The file uses the same format as StreamingHistory_music_0.json in Spotify's
"Account data" export, so students can practise before their own data arrives.
All artist and track names are invented.

Run from the repository root:
    python scripts/make_spotify_sample.py
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path("docs/projects/data/StreamingHistory_music_0.json")
rng = np.random.default_rng(42)

artists = {
    "The Marginal Costs": ["Diminishing Returns", "Sunk Cost Blues", "Price Taker", "Elastic Heart", "Deadweight"],
    "Lucy and the Lagrangians": ["Shadow Price", "Constraint", "First Order", "Corner Solution"],
    "Supply Shock": ["Oil Crisis", "Stagflation", "Cost Push", "Bottleneck"],
    "Nash & the Equilibria": ["Prisoner's Dilemma", "Best Response", "Mixed Strategy", "No Regrets"],
    "Invisible Hand": ["Laissez Faire", "Pin Factory", "Self Interest"],
    "The Phillips Curves": ["Trade-off", "Natural Rate", "Expectations"],
    "Moral Hazard": ["Hidden Action", "Insured", "Principal Agent"],
    "DJ Keynes": ["Animal Spirits", "In the Long Run", "Paradox of Thrift", "Liquidity Trap"],
    "Gini Coefficient": ["Lorenz", "Zero to One", "Top Ten Percent"],
    "Comparative Advantage": ["Wine for Cloth", "Ricardo", "Gains from Trade"],
    "Okun's Law": ["Two Percent", "Output Gap"],
    "Hysteresis": ["Scarring", "Path Dependent", "Long Memory"],
}
popularity = np.array([30, 18, 12, 10, 7, 6, 5, 4, 3, 2, 2, 1], dtype=float)
popularity /= popularity.sum()
names = list(artists)
# Favourite artists get skipped less
skip_p = dict(zip(names, np.linspace(0.08, 0.40, len(names))))

# Local hour-of-day weights: quiet overnight, peaks on the commute and in the evening
hour_w = np.array([2, 1, .5, .3, .2, .3, 1, 4, 6, 4, 3, 3, 4, 4, 3, 3, 4, 6, 6, 5, 5, 5, 4, 3])
hour_w /= hour_w.sum()

rows = []
for day in pd.date_range("2025-06-01", "2025-11-30", freq="D"):
    n = rng.poisson(38 if day.day_of_week >= 5 else 26)
    hours = rng.choice(24, n, p=hour_w)
    for h in hours:
        artist = names[rng.choice(len(names), p=popularity)]
        tracks = artists[artist]
        track = tracks[min(int(rng.exponential(1.2)), len(tracks) - 1)]
        length = int(rng.integers(150_000, 260_000))
        skipped = rng.random() < skip_p[artist]
        ms = int(rng.integers(2_000, 30_000)) if skipped else length
        local = day + pd.Timedelta(hours=int(h), minutes=int(rng.integers(0, 60)))
        # Spotify records times in UTC; this listener lives in New York
        end = local.tz_localize("America/New_York", ambiguous=False, nonexistent="shift_forward").tz_convert("UTC")
        rows.append(
            {
                "endTime": end.strftime("%Y-%m-%d %H:%M"),
                "artistName": artist,
                "trackName": track,
                "msPlayed": ms,
            }
        )

rows.sort(key=lambda r: r["endTime"])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
print(f"Wrote {len(rows)} plays to {OUT}")
