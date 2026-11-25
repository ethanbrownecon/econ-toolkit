# Reproducible research

A project is **reproducible** when someone else, or you in a year, can take your files, run one command and get exactly the same tables and figures. Economics journals now require it, and research assistants spend much of their time on it. It also saves you: when a referee asks for one more control variable, you change one line and rerun everything.

!!! info "What you will learn"
    The five habits of a reproducible project · folder layout · one script that runs everything · locking package versions in Stata, R and Python · random seeds · documenting data · a replication-package checklist

## The five habits

1. **Never edit raw data by hand.** Every change happens in code.
2. **One command runs everything,** from raw data to final tables.
3. **Paths are relative** to the project folder, so the code runs on any computer.
4. **Package versions are recorded,** so the code runs the same way next year.
5. **Everything is in Git,** so you can see what changed and when.

## Project layout

Use the same layout for every project. The [templates](../templates/index.md) are built around it.

```text
my-project/
├── README.md              what this is and how to run it
├── code/
│   ├── 00_master.do       runs everything in order (or run_all.R / run_all.py)
│   ├── 01_clean.do
│   ├── 02_analysis.do
│   └── 03_figures.do
├── data/
│   ├── raw/               original files, never edited
│   └── clean/             created by code, safe to delete
├── output/
│   ├── tables/
│   ├── figures/
│   └── logs/
└── paper/
    └── paper.tex          reads tables and figures from output/
```

The test: delete everything in `data/clean/` and `output/`, run the master script, and check that everything comes back.

## One script runs everything

=== "Stata"

    ```stata
    * code/00_master.do
    global root "~/projects/my-project"      // the only line to change on a new computer

    do "$root/code/01_clean.do"
    do "$root/code/02_analysis.do"
    do "$root/code/03_figures.do"
    ```

=== "R"

    ```r
    # code/run_all.R
    library(here)

    source(here("code", "01_clean.R"))
    source(here("code", "02_analysis.R"))
    source(here("code", "03_figures.R"))
    ```

=== "Python"

    ```python
    # code/run_all.py
    import runpy
    from pathlib import Path

    code = Path(__file__).resolve().parent
    for script in ["01_clean.py", "02_analysis.py", "03_figures.py"]:
        runpy.run_path(code / script, run_name="__main__")
    ```

Run it from a fresh session (restart Stata, R or Python first). A script that only works after you clicked something earlier is not reproducible.

## Lock your package versions

Packages change. A command that works today can break or give different numbers after an update. Record the versions you used, and let others install the same ones.

=== "Stata"

    Install user-written packages **inside the project**, so the project carries its own copies:

    ```stata
    * At the top of 00_master.do
    sysdir set PLUS "$root/ado/plus"         // install and load packages from the project
    sysdir set PERSONAL "$root/ado/personal"

    * Run these once; the files are saved in ado/ and committed to Git
    * ssc install reghdfe
    * ssc install ftools
    ```

    Also put `version 18` (your version) at the top of every do-file, so newer Stata versions run your code under the same rules.

=== "R"

    **renv** gives each project its own package library and a lockfile listing exact versions.

    ```r
    install.packages("renv")

    renv::init()        # once: create the project library and renv.lock
    renv::snapshot()    # after installing or updating packages: record versions
    renv::restore()     # on a new computer: install exactly the recorded versions
    ```

    Commit `renv.lock` to Git. Do not commit the `renv/library/` folder.

=== "Python"

    Use a **virtual environment** per project and record versions in `requirements.txt`. The [command line guide](../command-line/README.md#python-virtual-environments) shows the setup.

    ```bash
    python -m venv .venv
    source .venv/bin/activate            # Windows: .venv\Scripts\activate
    pip install pandas pyfixest

    pip freeze > requirements.txt        # record exact versions
    pip install -r requirements.txt      # on a new computer: install them
    ```

    Commit `requirements.txt`. Add `.venv/` to `.gitignore`.

Also record the **software version** itself (Stata 18, R 4.4, Python 3.12) in your README.

## Set random seeds

Anything random (bootstraps, simulations, sample splits, machine learning, placebo tests) gives different numbers on every run unless you set a seed.

| Stata | R | Python |
|---|---|---|
| `set seed 20260101` | `set.seed(20260101)` | `rng = np.random.default_rng(20260101)` |

Set it once at the top of each script. Many commands also take their own seed option, such as `rseed()` in Stata and `random_state=` in scikit-learn.

## Document your data

For every dataset, your README should say:

| Item | Example |
|---|---|
| Source and link | Current Population Survey, via IPUMS, cps.ipums.org |
| Date downloaded | 2026-03-14 |
| Exact file or extract | `cps_00012.dat`, extract with variables listed in `data/raw/extract.txt` |
| Access conditions | Free with registration; may not be redistributed |
| Citation | The citation the provider asks for |

If the data cannot be shared, say exactly how someone can get it. The [template README](https://social-science-data-editors.github.io/template_README/) used by economics journals has a section for each item.

## Use Git

Put the project in Git from day one, and commit after each piece of work. See [Git & GitHub](../git-github/README.md).

Add a `.gitignore` so large and private files stay out:

```text
# Large or confidential data: document how to get it instead
data/raw/*

# Files your code recreates
data/clean/
output/logs/

# Software environments and system files
.venv/
renv/library/
.Rhistory
.DS_Store

# API keys and passwords
.env
```

Comments in `.gitignore` must be on their own line, starting with `#`.

## Write the paper from your outputs

- Write tables straight to files from code (`esttab`, `etable`, `pf.etable`) and `\input{}` them in LaTeX. Never retype a number.
- Save figures from code to `output/figures/` and `\includegraphics` them.
- For numbers in the text, write them to a small `.tex` file from code, or write the whole paper in [Quarto](https://quarto.org/) so numbers update automatically.

## Replication package checklist

Before you share a project or submit a paper:

- [ ] A README explains what the project does, the software and versions needed, and how long it takes to run
- [ ] Every dataset is documented: source, date, access conditions, citation
- [ ] One master script runs everything from raw data
- [ ] It runs on a clean computer, or at least a fresh session with an empty `output/` folder
- [ ] Package versions are recorded (`ado/`, `renv.lock` or `requirements.txt`)
- [ ] Random seeds are set
- [ ] Paths are relative to the project folder; no `C:\Users\yourname\...`
- [ ] Each table and figure in the paper is mapped to the script that makes it
- [ ] No passwords, API keys or confidential data are included

The [AEA Data Editor's guidance](https://aeadataeditor.github.io/aea-de-guidance/) explains what economics journals check.

## Going further: containers

A **container** (Docker) packages your code with the operating system and software it needs, so it runs identically anywhere. It is the strongest form of reproducibility and common in large projects, but most student projects do not need it. Habits 1 to 5 get you most of the way.

## Learn more

- [Code and Data for the Social Sciences](https://web.stanford.edu/~gentzkow/research/CodeAndData.pdf) by Gentzkow and Shapiro: a short, practical guide
- [DIME Analytics Data Handbook](https://worldbank.github.io/dime-data-handbook/): the World Bank's full guide to reproducible research
- [renv documentation](https://rstudio.github.io/renv/)
