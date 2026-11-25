# SQL

SQL (Structured Query Language, often said "sequel") is how you ask a database for data. Most companies, central banks and government agencies store their data in databases, so SQL is one of the most requested skills in economics jobs. It reads almost like English: *select these columns from this table where this is true*.

!!! info "What you will learn"
    Running SQL with DuckDB, with no server needed · selecting and filtering · summarising by group · CASE · joins · CTEs · window functions · using SQL from R and Python

    Examples use the [wages.csv](../projects/data/wages.csv) practice data from [Project 1](../projects/wages.md).

## Set up: DuckDB

Most databases need a server. **DuckDB** does not: it runs inside R or Python and queries CSV and Parquet files directly. The SQL you learn works almost unchanged in PostgreSQL, Snowflake, BigQuery and other databases.

=== "Python"

    ```python
    # pip install duckdb
    import os
    import urllib.request

    import duckdb

    # Download the practice data once
    os.makedirs("data/raw", exist_ok=True)
    urllib.request.urlretrieve(
        "https://ethanbrownecon.github.io/econ-toolkit/projects/data/wages.csv",
        "data/raw/wages.csv",
    )

    con = duckdb.connect()
    con.sql("CREATE TABLE wages AS SELECT DISTINCT * FROM read_csv('data/raw/wages.csv')")

    con.sql("SELECT COUNT(*) AS n FROM wages")          # prints a table
    df = con.sql("SELECT * FROM wages").df()            # result as a pandas DataFrame
    ```

=== "R"

    ```r
    # install.packages(c("duckdb", "DBI"))
    library(DBI)

    # Download the practice data once
    dir.create("data/raw", recursive = TRUE, showWarnings = FALSE)
    download.file("https://ethanbrownecon.github.io/econ-toolkit/projects/data/wages.csv",
                  "data/raw/wages.csv")

    con <- dbConnect(duckdb::duckdb())
    dbExecute(con, "CREATE TABLE wages AS SELECT DISTINCT * FROM read_csv('data/raw/wages.csv')")

    dbGetQuery(con, "SELECT COUNT(*) AS n FROM wages")  # result as a data frame
    ```

`SELECT DISTINCT *` removes the duplicate rows while loading. **Check:** the table has **1,000** rows.

The rest of this page shows only the SQL. Run it with `con.sql("...")` in Python or `dbGetQuery(con, "...")` in R.

## Select and filter

```sql
SELECT id, age, educ, wage       -- which columns
FROM wages                       -- which table
WHERE wage > 50                  -- which rows
ORDER BY wage DESC               -- sort, largest first
LIMIT 5;                         -- only the first 5
```

| Clause | Does | Stata equivalent |
|---|---|---|
| `SELECT` | Pick columns. `*` means all. | `keep` |
| `FROM` | Name the table | `use` |
| `WHERE` | Keep rows that meet a condition | `keep if` |
| `ORDER BY` | Sort. Add `DESC` for largest first. | `gsort` |
| `LIMIT` | Keep the first *n* rows | `keep in 1/n` |

Conditions combine with `AND`, `OR` and `NOT`. Other useful tests: `state IN ('CA', 'NY')`, `age BETWEEN 25 AND 54`, `wage IS NULL` and `name LIKE '%Ltd%'` (contains "Ltd").

!!! note "SQL writing style"
    SQL keywords are not case-sensitive, but writing them in CAPITALS makes queries easier to read. Text values go in single quotes: `'CA'`. Comments start with `--`.

## Summarise by group

```sql
SELECT state,
       COUNT(*)            AS n,
       ROUND(AVG(wage), 2) AS mean_wage
FROM wages
WHERE wage > 0
GROUP BY state
HAVING COUNT(*) >= 100
ORDER BY mean_wage DESC;
```

- `GROUP BY` makes one row per state, like `collapse` in Stata or `summarise(.by = )` in R.
- `AS` names the new column.
- `WHERE` filters rows **before** grouping. `HAVING` filters groups **after** grouping.

| Function | Gives |
|---|---|
| `COUNT(*)` | Number of rows |
| `COUNT(wage)` | Number of non-missing wages |
| `SUM()`, `AVG()`, `MIN()`, `MAX()` | Total, mean, minimum, maximum |
| `MEDIAN()`, `STDDEV()` | Median and standard deviation (DuckDB, PostgreSQL) |

**Check:** Michigan has the highest average wage, **$25.39**.

## Missing values

Missing values are `NULL` in SQL. Test for them with `IS NULL`, never `= NULL`.

```sql
SELECT COUNT(*) - COUNT(wage) AS missing_wages FROM wages;   -- 25
```

Any comparison with `NULL` is neither true nor false, so `WHERE wage > 0` quietly drops missing wages too.

## Create categories with CASE

```sql
SELECT CASE
         WHEN educ < 12  THEN 'No diploma'
         WHEN educ = 12  THEN 'High school'
         WHEN educ < 16  THEN 'Some college'
         ELSE 'College degree'
       END AS education,
       COUNT(*) AS n,
       ROUND(AVG(wage), 2) AS mean_wage
FROM wages
WHERE wage > 0
GROUP BY education
ORDER BY mean_wage;
```

`CASE` checks each condition in order and uses the first one that is true, like `case_when()` in R. **Check:** average wages rise from **$16.40** with no diploma to **$30.44** with a college degree.

## Join tables

A join combines two tables using a column they share. Here a small table of minimum wages is built inside the query and joined to the wages table by `state`.

```sql
WITH min_wage(state, min_wage) AS (
    VALUES ('CA', 16.00), ('NY', 15.50), ('TX', 7.25), ('FL', 13.00)
)
SELECT w.state,
       m.min_wage,
       ROUND(AVG(w.wage), 2) AS mean_wage
FROM wages AS w
LEFT JOIN min_wage AS m ON w.state = m.state
WHERE w.wage > 0
GROUP BY w.state, m.min_wage
ORDER BY w.state;
```

`w` and `m` are short names (aliases) for the tables. `w.state` means "the state column from `wages`".

| Join | Keeps | Stata `merge` equivalent |
|---|---|---|
| `INNER JOIN` | Only rows that match in both tables | `keep(match)` |
| `LEFT JOIN` | Every row of the left table. Missing matches become `NULL`. | `keep(master match)` |
| `FULL JOIN` | Every row of both tables | default `merge` |

States not in the minimum wage table, such as Georgia, get `NULL`. The illustrative minimum wage values are made up for this example.

## Build queries in steps with WITH

A **CTE** (common table expression) names an intermediate result, so you can build a long query in readable steps.

```sql
WITH clean AS (
    SELECT *, LOWER(sex) AS sex_clean
    FROM wages
    WHERE wage > 0
)
SELECT sex_clean, ROUND(AVG(wage), 2) AS mean_wage
FROM clean
GROUP BY sex_clean;
```

Step 1 cleans the data. Step 2 summarises the clean version. **Check:** women average **$22.76** and men **$25.89**, the same as Project 1.

## Window functions

A window function calculates across a group of rows **without** collapsing them, like `bysort state: egen` in Stata.

```sql
SELECT id, state, wage,
       ROUND(AVG(wage) OVER (PARTITION BY state), 2)       AS state_mean,
       RANK() OVER (PARTITION BY state ORDER BY wage DESC) AS rank_in_state
FROM wages
WHERE wage > 0
QUALIFY rank_in_state <= 2
ORDER BY state, rank_in_state;
```

- `OVER (PARTITION BY state)` means "within each state".
- `RANK()`, `ROW_NUMBER()`, `LAG(wage)` and `SUM(wage) OVER (ORDER BY date)` (a running total) are the most useful.
- `QUALIFY` filters on a window function. It works in DuckDB, Snowflake and BigQuery. In PostgreSQL, wrap the query in a CTE and filter with `WHERE` instead.

The result shows the two top earners in each state next to their state's average.

## The order SQL runs in

You write `SELECT` first, but the database runs the clauses in this order. Knowing it explains most confusing errors. For example, most databases do not let `WHERE` use a name created in `SELECT`, because `WHERE` runs first. DuckDB is more forgiving, but write portable SQL anyway.

```text
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| `Referenced column "x" not found` | Typo, or a column alias used in `WHERE` | Check spelling. Repeat the expression in `WHERE` or use a CTE. |
| `column "x" must appear in the GROUP BY clause` | A selected column is neither grouped nor summarised | Add it to `GROUP BY` or wrap it in `AVG()`, `MAX()` and so on |
| `Parser Error: syntax error at or near` | Missing comma, extra comma before `FROM`, or unmatched bracket | Look just before the position the error names |
| Text comparison returns nothing | Double quotes around text, or different capitals | Use single quotes. `LOWER(sex) = 'male'` ignores case. |
| Row count jumps after a join | Duplicate keys in one table | Check keys are unique: `SELECT state, COUNT(*) FROM t GROUP BY state HAVING COUNT(*) > 1` |

## Practise

1. Which age group (under 30, 30–49, 50 and over) has the highest share of union members?
2. For each state, what share of workers earn over $30 an hour?
3. Use `LAG()` to rank states by average wage and show how far each state is below the one above it.
4. Try [SQLBolt](https://sqlbolt.com/) for short interactive lessons in the browser.
