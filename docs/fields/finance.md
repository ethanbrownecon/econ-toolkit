# Finance

Financial economics studies markets for money and risk: stocks, bonds, interest rates, banks and how households and firms borrow, save and invest.

## Big questions

- What determines asset prices and expected returns?
- Can investors beat the market?
- Why do banking crises happen, and how can they be prevented?
- What do interest rates tell us about the future economy?
- How do households make saving and borrowing decisions, and where do they go wrong?

## Methods you will use

Time-series [regression](../econometrics/ols.md) · [logit and probit](../econometrics/logit.md) for predicting events · event studies around announcements · [panel data](../econometrics/panel.md) on firms

## Data

| Source | What it has |
|---|---|
| [FRED](https://fred.stlouisfed.org/) | Interest rates, yields, stock indexes, credit |
| [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) | Stock return factors and portfolios since 1926 |
| [SEC EDGAR](https://www.sec.gov/edgar/search/) | Company filings |
| [WRDS](https://wrds-www.wharton.upenn.edu/) | CRSP stock prices and Compustat accounts, through most universities |

## Starter project: does the yield curve predict recessions?

Normally, long-term interest rates are higher than short-term ones. When short rates rise above long rates, the yield curve **inverts**. Every US recession since the late 1960s was preceded by an inversion. Test how strong the signal is, using FRED data from 1953.

| FRED code | Series |
|---|---|
| `GS10` | 10-year Treasury yield |
| `TB3MS` | 3-month Treasury bill rate |
| `USREC` | 1 in recession months |

The outcome is whether a recession starts or continues **at any point in the next 12 months**.

=== "Stata"

    ```stata
    capture mkdir "data"
    capture mkdir "data/raw"

    capture program drop fred
    program define fred
        args series
        local file "data/raw/`series'.csv"
        capture confirm file "`file'"
        if _rc shell curl -sL -o "`file'" "https://fred.stlouisfed.org/graph/fredgraph.csv?id=`series'"
        import delimited "`file'", clear
        gen month = mofd(date(observation_date, "YMD"))
        format month %tm
        drop observation_date
    end

    fred GS10
    tempfile gs10
    save `gs10'
    fred TB3MS
    tempfile tb3ms
    save `tb3ms'
    fred USREC
    merge 1:1 month using `gs10', keep(match) nogenerate
    merge 1:1 month using `tb3ms', keep(match) nogenerate
    tsset month

    gen spread = gs10 - tb3ms
    gen future = 0
    forvalues k = 1/12 {
        replace future = future + F`k'.usrec     // recession months in the next year
    }
    gen recession_next_12m = (future > 0) if !missing(future)

    logit recession_next_12m spread
    margins, at(spread = (-1 0 1 2))
    ```

=== "R"

    ```r
    library(tidyverse)

    dir.create("data/raw", recursive = TRUE, showWarnings = FALSE)
    fred <- function(series) {
      file <- file.path("data/raw", paste0(series, ".csv"))
      if (!file.exists(file)) {
        download.file(paste0("https://fred.stlouisfed.org/graph/fredgraph.csv?id=", series),
                      file, quiet = TRUE)
      }
      read_csv(file, show_col_types = FALSE) %>% rename(date = observation_date)
    }

    yc <- fred("GS10") %>%
      inner_join(fred("TB3MS"), by = "date") %>%
      inner_join(fred("USREC"), by = "date") %>%
      arrange(date) %>%
      mutate(spread = GS10 - TB3MS)

    future <- sapply(1:12, function(k) lead(yc$USREC, k))     # recession months in the next year
    yc$recession_next_12m <- as.integer(rowSums(future) > 0)

    logit <- glm(recession_next_12m ~ spread, data = yc, family = binomial)
    predict(logit, newdata = tibble(spread = c(-1, 0, 1, 2)), type = "response")
    ```

=== "Python"

    ```python
    import urllib.request
    from pathlib import Path

    import pandas as pd
    import statsmodels.formula.api as smf

    RAW = Path("data/raw")
    RAW.mkdir(parents=True, exist_ok=True)

    def fred(series):
        file = RAW / f"{series}.csv"
        if not file.exists():
            urllib.request.urlretrieve(
                f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}", file)
        return (pd.read_csv(file, parse_dates=["observation_date"])
                .rename(columns={"observation_date": "date"}))

    yc = (fred("GS10").merge(fred("TB3MS"), on="date")
          .merge(fred("USREC"), on="date").sort_values("date"))
    yc["spread"] = yc["GS10"] - yc["TB3MS"]

    future = sum(yc["USREC"].shift(-k) for k in range(1, 13))   # recession months in the next year
    yc["recession_next_12m"] = (future > 0).astype(int).where(future.notna())

    logit = smf.logit("recession_next_12m ~ spread", data=yc.dropna()).fit()
    logit.predict(pd.DataFrame({"spread": [-1, 0, 1, 2]}))
    ```

**Check:** 871 months, from 1953 to 2025. The logit coefficient on the spread is about **−0.76**. Predicted chance of a recession within a year:

| Spread (10-year minus 3-month) | −1 (inverted) | 0 | 1 | 2 |
|---|---:|---:|---:|---:|
| Probability of recession | **64%** | 45% | 28% | 15% |

An inverted curve signals that markets expect the Fed to cut rates, which usually happens because the economy is weakening. The curve was inverted from late 2022 to late 2024, yet no recession had followed by late 2026: a reminder that a strong signal is not a guarantee.

## More project ideas

1. **Other spreads.** Use the 10-year minus 2-year spread (`T10Y2Y`). Is it a better predictor?
2. **Stock returns and the business cycle.** Use the S&P 500 or Wilshire index from FRED to compare returns in and out of recessions.
3. **The equity premium.** Use the Kenneth French data library to compute average stock returns above Treasury bills by decade.
4. **Mortgage spreads.** Plot the 30-year mortgage rate minus the 10-year Treasury. When does it widen, and why?

## Classic papers

- Shiller (1981), "Do Stock Prices Move Too Much to be Justified by Subsequent Changes in Dividends?", *American Economic Review*
- Estrella and Hardouvelis (1991), "The Term Structure as a Predictor of Real Economic Activity", *Journal of Finance*
- Fama and French (1993), "Common Risk Factors in the Returns on Stocks and Bonds", *Journal of Financial Economics*
