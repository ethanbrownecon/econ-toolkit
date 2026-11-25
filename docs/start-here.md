# Start here

New to all of this? This page gives you an order to work through the site, so you always know what to do next. You do not need to read everything. Pick the path that matches your goal.

!!! tip "How long does it take?"
    The core path takes about **six weeks at three to four hours a week**. Each step lists what to read and what to do. Tick the boxes as you go. They reset when you reload the page, so keep your own notes too.

## The core path

### Week 1: Set up your computer

- [ ] Install [VS Code](vscode/README.md) and open a project folder
- [ ] Learn the [command line basics](command-line/README.md): moving between folders and running a script
- [ ] Install one language: Stata (through your university), [R](r/README.md#set-up) or [Python](python/README.md#set-up)
- [ ] Learn enough [Markdown](markdown/README.md) to write a README

**Goal:** you can open a terminal in a project folder and run a one-line script.

### Week 2: Learn your language

- [ ] Read the guide for your language: [Stata](stata/README.md), [R](r/README.md) or [Python](python/README.md)
- [ ] Download the matching [template](templates/index.md) and set up the standard project folder
- [ ] Work through [Project 1: Wages and education](projects/wages.md)

**Goal:** you can load a dataset, clean it and run a regression.

### Week 3: Save your work properly

- [ ] Learn [Git & GitHub](git-github/README.md) and put your Project 1 folder on GitHub
- [ ] Read [reproducible research](reproducible-research/README.md) and add a master script to your project

**Goal:** your project runs from start to finish with one command, and its history is saved.

### Week 4: Find and chart data

- [ ] Browse the [datasets](data/datasets.md) page
- [ ] Work through [Project 2: The economy in charts](projects/fred.md)
- [ ] Read [data visualization](data-viz/README.md) and remake one of your charts using its rules

**Goal:** you can download real data and make a clear, labeled chart.

### Week 5: Think about cause and effect

- [ ] Read the [econometrics overview](econometrics/index.md)
- [ ] Read [linear regression](econometrics/ols.md) and [difference-in-differences](econometrics/did.md), running the code
- [ ] Read one more method that interests you

**Goal:** you can explain why a regression coefficient is not always a causal effect, and name a design that does better.

### Week 6: Do real research

- [ ] Work through the [Hansen replication](projects/replication-hansen.md)
- [ ] Write up your results in a short [LaTeX](latex/README.md) document with one table and one figure exported from code

**Goal:** you have replicated a published paper and written it up like a researcher.

## Paths by goal

### "I am taking my first econometrics class"

1. Set up your language: [Stata](stata/README.md), [R](r/README.md) or [Python](python/README.md)
2. [Linear regression](econometrics/ols.md), then [logit and probit](econometrics/logit.md)
3. [Project 1](projects/wages.md) for hands-on practice
4. [Fixed effects](econometrics/panel.md) and [instrumental variables](econometrics/iv.md) when your class reaches them
5. [LaTeX](latex/README.md) for problem sets with equations

### "I am starting a research assistant job"

1. [Git & GitHub](git-github/README.md): you will use it daily
2. The [Stata guide](stata/README.md) and the [do-file template](templates/stata.md): most economics RA work is in Stata
3. [Reproducible research](reproducible-research/README.md): what professors expect from your code
4. [Difference-in-differences](econometrics/did.md) and [regression discontinuity](econometrics/rd.md): the most common designs in applied work
5. The [Hansen replication](projects/replication-hansen.md): practice for the tasks you will be given

### "I am writing a senior thesis"

1. Choose a question and a [method](econometrics/index.md#which-method-should-i-use)
2. Find data on the [datasets](data/datasets.md) page, or with [APIs](data/apis.md) and [web scraping](data/scraping.md)
3. Set up your project with a [template](templates/index.md) and [Git](git-github/README.md)
4. Make charts with [data visualization](data-viz/README.md) and write in [LaTeX](latex/README.md)
5. Use the [replication checklist](reproducible-research/README.md#replication-package-checklist) before you submit

### "I know Stata and want to learn R or Python"

1. [Coming from Stata](coming-from/stata.md): every common command, translated
2. The [R guide](r/README.md) or [Python guide](python/README.md)
3. Redo [Project 1](projects/wages.md) in the new language
4. Try something Stata finds hard: the [Spotify project](projects/spotify.md), [APIs](data/apis.md) or [web scraping](data/scraping.md)

### "I want a job in data or economic consulting"

1. [Python](python/README.md) and [SQL](sql/README.md): the most requested skills
2. [Data visualization](data-viz/README.md), including the dashboards section
3. [Machine learning](machine-learning/README.md)
4. Put two projects on GitHub to show employers: [Project 2](projects/fred.md) and one of your own

## When you get stuck

- Every guide ends with a **Common errors** table. Check it first.
- Search the exact error message online, in quotes.
- See [where to ask for help](resources/index.md#where-to-ask-for-help) on the Resources page.
- Found a mistake on this site? [Open an issue](https://github.com/ethanbrownecon/econ-toolkit/issues/new/choose).
