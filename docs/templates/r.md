# R script template

[:material-download: Download analysis.R](files/analysis.R){ .md-button .md-button--primary download }

## The template

```r title="code/01_analysis.R"
--8<-- "analysis.R"
```

## What each part does

| Part | Why it is there |
|---|---|
| Header comment | Says what the file does and which files it reads and writes. |
| `# 1. Load data ----` | A comment that ends in four dashes becomes a section. RStudio and VS Code show the sections as an outline you can jump between. |
| `library()` at the top | Shows every package the script needs in one place. |
| `here()` | Builds paths from the project folder, so the script works on any computer. |
| `set.seed()` | Makes random draws give the same result every run. |
| `stopifnot()` | Stops the script if two rows share the same `id` and `year`. |
| `etable(..., tex = TRUE)` | Writes the regressions into one LaTeX table. |
| `ggsave()` | Saves the figure at a fixed size and resolution. |

!!! tip "How `here()` finds your project folder"
    `here()` looks for a marker file in the project folder. An RStudio project file (`.Rproj`) works. In VS Code, create an empty file called `.here` in the project folder.

??? note "Run the whole project"
    Create `code/run_all.R` and run each script in order:

    ```r
    source(here::here("code", "01_clean.R"))
    source(here::here("code", "02_analysis.R"))
    source(here::here("code", "03_figures.R"))
    ```
