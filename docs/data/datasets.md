# Datasets

Where to find data, from small practice files to official government statistics. Start with practice data while you learn, then move to real sources for your own projects.

!!! tip "Which kind of data do you need?"
    - **Learning a command or method?** Use [practice data](#practice-data). It is small, clean enough and loads in one line.
    - **Writing a paper or thesis?** Use [government](#us-government-data) or [international](#international-data) sources. They are documented, citable and trusted.
    - **Want something fun?** Try [other sources](#other-sources), or analyze [your own data](#your-own-data).

## Practice data

### From this site

| Dataset | What it is | Use it for |
|---|---|---|
| [wages.csv](../projects/data/wages.csv) | 1,008 workers with wages, education, age and union status. Simulated, with deliberate errors to clean. | [Project 1](../projects/wages.md): cleaning, summaries and a wage regression |
| [StreamingHistory_music_0.json](../projects/data/StreamingHistory_music_0.json) | Six months of fake Spotify plays in Spotify's real format | The [Spotify project](../projects/spotify.md) |

### Built into your software

These load with one line and need no download.

=== "Stata"

    | Command | Data |
    |---|---|
    | `sysuse auto, clear` | 74 cars from 1978: price, mileage, weight. The classic first dataset. |
    | `sysuse nlsw88, clear` | 2,246 women in 1988: wages, education, union, industry |
    | `webuse nlswork, clear` | Panel of young women, 1968–1988. Good for fixed effects. |
    | `webuse grunfeld, clear` | Panel of 10 US firms' investment, 1935–1954 |
    | `sysuse dir` | List every built-in dataset |

=== "R"

    | Code | Data |
    |---|---|
    | `install.packages("wooldridge")`<br>`data("wage1", package = "wooldridge")` | Every dataset from Wooldridge's *Introductory Econometrics* textbook |
    | `install.packages("AER")`<br>`data("CPS1985", package = "AER")` | Datasets from *Applied Econometrics with R*, including Stock and Watson examples |
    | `install.packages("gapminder")`<br>`gapminder::gapminder` | Life expectancy, population and GDP per capita by country, 1952–2007 |
    | `data(mtcars)` | Built into R: 32 cars, 1974 |

=== "Python"

    | Code | Data |
    |---|---|
    | `pip install wooldridge`<br>`wooldridge.data("wage1")` | Every dataset from Wooldridge's *Introductory Econometrics* textbook |
    | `sns.load_dataset("tips")` | Restaurant bills and tips. `sns.get_dataset_names()` lists more. |
    | `sm.datasets.macrodata.load_pandas().data` | Quarterly US macroeconomic data, 1959–2009, from statsmodels |

### Online collections

| Source | What it has |
|---|---|
| [TidyTuesday](https://github.com/rfordatascience/tidytuesday) | A new, cleaned, interesting dataset every week since 2018: food, sports, film, economics |
| [Kaggle Datasets](https://www.kaggle.com/datasets) | Thousands of datasets uploaded by users. Quality varies, so check the source. |
| [Our World in Data](https://ourworldindata.org/) | Clean long-run data on income, health, energy and more. Every chart has a download button. |
| [Google Dataset Search](https://datasetsearch.research.google.com/) | A search engine for datasets across the web |

## US government data

| Source | What it has | How to get it |
|---|---|---|
| **[FRED](https://fred.stlouisfed.org/)** | 800,000+ economic time series from many agencies, in one place | Download, or [API](apis.md#apis-with-a-key-fred) |
| [Bureau of Labor Statistics](https://www.bls.gov/data/) | Employment, unemployment, wages, CPI inflation, productivity | Download, or [API](https://www.bls.gov/developers/) |
| [Bureau of Economic Analysis](https://www.bea.gov/data) | GDP, personal income, trade, regional accounts | Download, or [API](https://apps.bea.gov/api/) |
| [Census Bureau](https://data.census.gov/) | American Community Survey, decennial census, business statistics | Download, or [API](https://www.census.gov/data/developers.html) |
| [IPUMS](https://www.ipums.org/) | Census and survey microdata (CPS, ACS) cleaned and made consistent over time | Free account, then build an extract |
| [Federal Reserve](https://www.federalreserve.gov/data.htm) | Interest rates, money supply, household debt, Survey of Consumer Finances | Download |
| [data.gov](https://data.gov/) | Catalog of 300,000+ federal datasets | Download |
| [NLSY](https://www.nlsinfo.org/) | National Longitudinal Surveys: the same people followed for decades | Free account |
| [PSID](https://psidonline.isr.umich.edu/) | Panel Study of Income Dynamics: US families since 1968 | Free account |

## International data

| Source | What it has |
|---|---|
| **[World Bank Open Data](https://data.worldbank.org/)** | 1,400+ development indicators for every country ([API](apis.md)) |
| [IMF Data](https://data.imf.org/) | World Economic Outlook, balance of payments, government finance |
| [OECD Data Explorer](https://data-explorer.oecd.org/) | Statistics for OECD member countries |
| [Eurostat](https://ec.europa.eu/eurostat/data/database) | Official statistics for the European Union |
| [Penn World Table](https://www.rug.nl/ggdc/productivity/pwt/) | Comparable GDP, capital, productivity and prices across 180+ countries |
| [ILOSTAT](https://ilostat.ilo.org/data/) | Labor market statistics for every country |
| [UN Data](https://data.un.org/) | United Nations statistics on population, trade and development |
| [UN Comtrade](https://comtradeplus.un.org/) | Detailed international trade flows by product |

## Other sources

| Source | What it has |
|---|---|
| [Opportunity Insights](https://opportunityinsights.org/data/) | Raj Chetty's data on social mobility by county, college and neighborhood |
| [ICPSR](https://www.icpsr.umich.edu/) | Archive of social science research data |
| [Harvard Dataverse](https://dataverse.harvard.edu/) | Replication data from published papers. Reproduce a paper's results. |
| [openICPSR (AEA)](https://www.openicpsr.org/openicpsr/aea) | Replication packages for American Economic Association journals |
| [Zillow Research](https://www.zillow.com/research/data/) | House prices and rents by region |
| [Yahoo Finance](https://finance.yahoo.com/) | Stock prices. In Python, the `yfinance` package downloads them. |
| [Sports Reference](https://www.sports-reference.com/) | Statistics for baseball, basketball, football, hockey and soccer |

## Your own data

Many apps let you download everything they know about you. Personal data makes a fun first project because you already know the story it should tell.

| App | How to request it |
|---|---|
| Spotify | Account → Privacy → Download your data. See the [Spotify project](../projects/spotify.md). |
| Google (Maps location history, YouTube, Fit) | [Google Takeout](https://takeout.google.com/) |
| Apple Health | Health app → your profile picture → Export All Health Data |
| Strava | Settings → My Account → Download or Delete Your Account → Request your archive |
| Netflix | Account → Profile → Download your personal information |
| Your bank | Export transactions as CSV from online banking |

!!! warning "Keep personal data private"
    Do not upload personal data exports to GitHub or share the raw files. Add the folder to `.gitignore`, and share only charts and summaries.

## Tips for working with real data

- **Read the documentation first.** Codebooks explain what each variable means, how it was measured and which values mean "missing" (often `-1`, `99` or `.`).
- **Keep the raw file untouched.** Save it in `data/raw/` and do every change in code. See the [templates](../templates/index.md).
- **Write down where it came from.** Record the source, the download date and the exact link in your README. Data get revised.
- **Cite it.** Most sources say how they want to be cited. Use that wording in your paper.
