# Web scraping

Web scraping means writing code that reads a web page and pulls out the data you want: prices, tables, listings, text. Use it when the data are on a website but there is no download button and no [API](apis.md).

!!! info "What you will learn"
    When scraping is allowed · how a web page is built · reading tables in one line · scraping a page step by step · looping over many pages politely

## Before you scrape

!!! warning "Check these three things first"
    1. **Is there an API or a download?** If yes, use it. It is faster and more reliable, and the site wants you to use it.
    2. **Do the rules allow it?** Read the site's terms of service. Check `robots.txt` (for example `https://example.com/robots.txt`), which lists the pages bots should not visit.
    3. **Is the data personal?** Do not collect personal information about individuals. If your project involves people, ask your professor or your university's ethics board first.

Then scrape politely: pause between requests, do not download the same page twice, and identify yourself in a `User-Agent` header.

## How a web page is built

Web pages are written in HTML. Content sits inside **tags**, and tags have **classes** that say what they are.

```html
<article class="product_pod">
  <h3><a title="A Light in the Attic">A Light in the ...</a></h3>
  <p class="price_color">£51.77</p>
  <p class="star-rating Three"></p>
</article>
```

To scrape, you tell your code *which tags* to pick, using a **CSS selector**:

| Selector | Picks |
|---|---|
| `p` | Every `<p>` tag |
| `.price_color` | Every tag with `class="price_color"` |
| `p.price_color` | `<p>` tags with that class |
| `article h3 a` | `<a>` tags inside `<h3>` inside `<article>` |

!!! tip "Find the selector in your browser"
    Right-click the thing you want on the page and choose **Inspect**. The browser highlights its HTML, so you can read the tag and class names.

## The easy case: tables

If the data are already in an HTML table, one line reads every table on the page.

=== "R"

    ```r
    library(rvest)

    page   <- read_html("https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)")
    tables <- html_table(page)       # a list of every table on the page
    length(tables)                   # how many tables?
    gdp    <- tables[[3]]            # pick the one you want
    ```

=== "Python"

    ```python
    from io import StringIO

    import pandas as pd
    import requests

    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    html = requests.get(url, headers={"User-Agent": "student project"}, timeout=30).text
    tables = pd.read_html(StringIO(html), match="IMF")   # tables containing "IMF"
    gdp = tables[0]
    ```

Look through the tables to find the right one. Numbers often arrive as text with commas, so clean them before you use them: `parse_number()` in R, `pd.to_numeric(col.str.replace(",", ""))` in Python.

## Scrape a page step by step

[Books to Scrape](https://books.toscrape.com/) is a fake bookshop built for practicing. Each book on a page sits in an `<article class="product_pod">`, as in the HTML above.

=== "R"

    ```r
    library(tidyverse)
    library(rvest)

    html  <- read_html("https://books.toscrape.com/catalogue/page-1.html")
    books <- html_elements(html, "article.product_pod")    # 20 books

    tibble(
      title  = books %>% html_element("h3 a") %>% html_attr("title"),
      price  = books %>% html_element("p.price_color") %>% html_text() %>% parse_number(),
      rating = books %>% html_element("p.star-rating") %>% html_attr("class") %>%
                 str_remove("star-rating ")
    )
    ```

=== "Python"

    ```python
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup      # pip install beautifulsoup4

    HEADERS = {"User-Agent": "student project"}
    url = "https://books.toscrape.com/catalogue/page-1.html"

    resp = requests.get(url, headers=HEADERS, timeout=30)
    soup = BeautifulSoup(resp.content, "html.parser")
    books = soup.select("article.product_pod")              # 20 books

    pd.DataFrame({
        "title":  [b.select_one("h3 a")["title"] for b in books],
        "price":  [float(b.select_one("p.price_color").text.lstrip("£")) for b in books],
        "rating": [b.select_one("p.star-rating")["class"][1] for b in books],
    })
    ```

    Pass `resp.content` (raw bytes), not `resp.text`, to BeautifulSoup. It then detects the page's encoding correctly. Otherwise `£` can turn into `Â£` and break the price.

Each line follows the same recipe: **find the tag → take its text or an attribute → clean it.**

## Loop over many pages

Most sites split data across pages. Write a function for one page, then run it on each page with a pause in between.

=== "R"

    ```r
    scrape_page <- function(page) {
      url   <- paste0("https://books.toscrape.com/catalogue/page-", page, ".html")
      books <- read_html(url) %>% html_elements("article.product_pod")
      Sys.sleep(1)                                          # be polite
      tibble(
        title = books %>% html_element("h3 a") %>% html_attr("title"),
        price = books %>% html_element("p.price_color") %>% html_text() %>% parse_number()
      )
    }

    df <- map(1:3, scrape_page) %>% list_rbind()            # 60 books
    write_csv(df, "data/raw/books.csv")                     # save it, so you scrape once
    ```

=== "Python"

    ```python
    import time

    rows = []
    for page in range(1, 4):
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        soup = BeautifulSoup(requests.get(url, headers=HEADERS, timeout=30).content, "html.parser")
        for b in soup.select("article.product_pod"):
            rows.append({
                "title": b.select_one("h3 a")["title"],
                "price": float(b.select_one("p.price_color").text.lstrip("£")),
            })
        time.sleep(1)                                       # be polite

    df = pd.DataFrame(rows)                                 # 60 books
    df.to_csv("data/raw/books.csv", index=False)            # save it, so you scrape once
    ```

## When it does not work

| Problem | Likely cause | What to try |
|---|---|---|
| The data you see in the browser is missing from the HTML | The page loads its data with JavaScript | Open the browser's **Inspect → Network** tab and look for a JSON request you can call directly. If there is none, use [Playwright](https://playwright.dev/python/) or [Selenium](https://www.selenium.dev/) to drive a real browser. |
| `403 Forbidden` | The site blocks scripts | Add a `User-Agent` header. If it is still blocked, the site does not want to be scraped. Respect that. |
| `429 Too Many Requests` | You are going too fast | Wait longer between requests |
| Selector finds nothing | Wrong tag or class | Inspect the page again. Classes are case-sensitive. |
| Code breaks a month later | The site changed its layout | Normal for scraping. Update the selectors, and keep your saved raw files. |

## Try it

1. Scrape all 50 pages of Books to Scrape. What is the average price for each star rating?
2. [Quotes to Scrape](https://quotes.toscrape.com/) is another practice site. Collect every quote and author, then find the author with the most quotes.
3. Find a Wikipedia table relevant to your interests, read it, and make a chart from it.

## Learn more

- [rvest documentation](https://rvest.tidyverse.org/): scraping in R
- [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): scraping in Python
- [CSS selectors reference](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors): every way to pick a tag
