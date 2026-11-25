# APIs: get data with code

An API (application programming interface) lets your code ask a website for data directly. Instead of clicking **Download**, saving a CSV and loading it, one line pulls the latest numbers straight into Stata, R or Python. Rerun the script next month and the data updates itself.

!!! info "What you will learn"
    What an API is · which economics APIs exist · the easy way (a package) · the general way (a raw request) · API keys and how to keep them secret

## How an API works

You send a web address with your question in it. The server sends back data, usually as JSON.

```text
https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.PCAP.KD?format=json&date=2020:2023
└──────────── base ────────────┘└ country ┘└──── indicator ────┘└──── options ─────────┘
```

Paste that address into your browser and you will see the raw data. Code does the same thing, then turns the result into a data frame.

| Term | Meaning |
|---|---|
| **Endpoint** | The address you send requests to |
| **Parameters** | Options after the `?`, such as dates or format |
| **JSON** | A text format for data that most APIs return |
| **API key** | A free password-like code that some APIs require so they know who is asking |
| **Rate limit** | The maximum number of requests you may send per minute or day |

## APIs economists use

| Source | What it has | Key? | Stata | R | Python |
|---|---|---|---|---|---|
| [FRED](https://fred.stlouisfed.org/docs/api/fred/) | 800,000+ US and international time series | Free key | `import fred` | `fredr` | `fredapi` |
| [World Bank](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) | Development indicators for every country | None | `wbopendata` | `WDI` | `wbgapi` |
| [BLS](https://www.bls.gov/developers/) | US employment, wages and prices | Optional | — | `httr2` | `requests` |
| [Census](https://www.census.gov/data/developers.html) | American Community Survey, population, business | Free key | — | `tidycensus` | `census` |
| [BEA](https://apps.bea.gov/api/) | US GDP, income and trade | Free key | — | `bea.R` | `requests` |
| [IMF](https://data.imf.org/) | International finance and trade | None | — | `httr2` | `requests` |
| [OECD](https://data-explorer.oecd.org/) | Statistics for OECD countries | None | — | `OECD` | `requests` |

A dash means no dedicated package. You can still use the raw request method below.

## The easy way: a package

Packages hide the web addresses and JSON. You name the series and get a data frame back. This example gets GDP per capita (constant US dollars) for the United States, China and India.

=== "Stata"

    ```stata
    ssc install wbopendata                     // once
    wbopendata, country(USA;CHN;IND) indicator(NY.GDP.PCAP.KD) ///
        year(2000:2023) long clear
    ```

=== "R"

    ```r
    install.packages("WDI")                    # once
    library(WDI)

    df <- WDI(country = c("US", "CN", "IN"),
              indicator = c(gdp_pc = "NY.GDP.PCAP.KD"),
              start = 2000, end = 2023)
    ```

=== "Python"

    ```python
    # pip install wbgapi                       (once, in a terminal)
    import wbgapi as wb

    df = wb.data.DataFrame("NY.GDP.PCAP.KD", ["USA", "CHN", "IND"],
                           time=range(2000, 2024))
    ```

!!! tip "Finding indicator codes"
    Every series has a code. Search the source's website: on [data.worldbank.org](https://data.worldbank.org/), open an indicator and the code is at the end of the address. On [FRED](https://fred.stlouisfed.org/), the code sits next to the series title, such as `UNRATE` for the unemployment rate.

## The general way: a raw request

When no package exists, request the address yourself and convert the JSON. The same request as above:

=== "R"

    ```r
    library(tidyverse)
    library(httr2)

    resp <- request("https://api.worldbank.org/v2/country/USA;CHN;IND/indicator/NY.GDP.PCAP.KD") %>%
      req_url_query(format = "json", date = "2000:2023", per_page = 500) %>%
      req_perform()

    body <- resp_body_json(resp, simplifyVector = TRUE)
    rows <- body[[2]]                    # item 1 is page info, item 2 is the data

    df <- tibble(
      country = rows$country$value,
      year    = as.integer(rows$date),
      gdp_pc  = rows$value
    )
    ```

=== "Python"

    ```python
    import pandas as pd
    import requests

    url = "https://api.worldbank.org/v2/country/USA;CHN;IND/indicator/NY.GDP.PCAP.KD"
    params = {"format": "json", "date": "2000:2023", "per_page": 500}

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()              # stop if the request failed

    page_info, rows = resp.json()        # item 1 is page info, item 2 is the data
    df = pd.json_normalize(rows)[["country.value", "date", "value"]]
    df.columns = ["country", "year", "gdp_pc"]
    ```

The pattern is always the same: **build the address → send the request → check it worked → turn the JSON into a table.**

## APIs with a key: FRED

FRED needs a free key. Get one in two minutes: create an account at [fred.stlouisfed.org](https://fred.stlouisfed.org/), then go to **My Account → API Keys**.

!!! warning "Never put a key in your code"
    Anyone who sees your script, including everyone on GitHub, can use your key. Store it outside the code, as shown below. If a key leaks, delete it on the website and make a new one.

=== "Stata"

    ```stata
    set fredkey YOUR-KEY-HERE, permanently     // once; saved in Stata, not in your do-file
    import fred UNRATE CPIAUCSL, daterange(2000-01-01 .) clear
    ```

=== "R"

    ```r
    # Once: run usethis::edit_r_environ(), add the line FRED_API_KEY=your-key, save, restart R
    install.packages("fredr")
    library(fredr)                     # reads FRED_API_KEY automatically

    unrate <- fredr(series_id = "UNRATE", observation_start = as.Date("2000-01-01"))
    ```

=== "Python"

    ```python
    # Once: set FRED_API_KEY as an environment variable (see the command line guide)
    # pip install fredapi
    import os
    from fredapi import Fred

    fred = Fred(api_key=os.environ["FRED_API_KEY"])
    unrate = fred.get_series("UNRATE", observation_start="2000-01-01")
    ```

The [command line guide](../command-line/README.md#environment-variables-and-secrets) explains environment variables.

## Good habits

- **Save what you download.** Write the result to `data/raw/` with the date in the file name. Data get revised, and your results should not change silently.
- **Respect rate limits.** In a loop, pause between requests: `Sys.sleep(1)` in R, `time.sleep(1)` in Python.
- **Check every response.** A failed request can return an error page instead of data. `raise_for_status()` and `req_perform()` stop with an error rather than giving you garbage.
- **Read the documentation.** Every API page lists its endpoints, parameters and limits. The links in the table above go straight to them.

## Try it

1. Download the US unemployment rate (`UNRATE`) from FRED and plot it since 2000.
2. Use the World Bank API to compare life expectancy (`SP.DYN.LE00.IN`) in five countries you choose.
3. Find a FRED series about your home state and add it to a chart.
