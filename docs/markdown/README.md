# Markdown

Markdown is plain text with a few symbols that turn into formatting. A `#` makes a heading, `**bold**` makes **bold**, and a line starting with `-` makes a bullet point. It is how you write README files, GitHub issues, Jupyter notes, Quarto papers and every page of this guide.

!!! tip "Why learn it"
    You learn Markdown once and use it everywhere: GitHub, VS Code, Jupyter, Quarto, R Markdown, Slack, Notion and Reddit all understand it. It takes about ten minutes.

## Try it

1. In VS Code, create a file called `notes.md`.
2. Type some of the examples below.
3. Press ++cmd+shift+v++ (Mac) or ++ctrl+shift+v++ (Windows) to see the formatted preview.

## The basics

| You type | You get |
|---|---|
| `# Title` | A top-level heading |
| `## Section` | A section heading |
| `### Subsection` | A smaller heading |
| `**bold**` | **bold** |
| `*italic*` | *italic* |
| `` `code` `` | `code` |
| `~~struck out~~` | ~~struck out~~ |
| `[Link text](https://example.com)` | [Link text](https://example.com) |
| `![Alt text](figure.png)` | An image |
| `---` on its own line | A horizontal line |

!!! note "Leave a blank line between paragraphs"
    A single line break does not start a new paragraph. Leave an empty line between paragraphs, and before and after headings, lists, tables and code blocks.

## Lists

=== "Bullets"

    ```markdown
    - Clean the data
    - Run the regressions
      - OLS
      - Fixed effects
    - Write up the results
    ```

    Indent by two spaces to nest an item.

=== "Numbered"

    ```markdown
    1. Download the data
    2. Run `01_clean.do`
    3. Run `02_analysis.do`
    ```

=== "Checklist"

    ```markdown
    - [x] Collect data
    - [ ] Clean data
    - [ ] Estimate model
    ```

    Checklists work on GitHub, where you can tick them in an issue.

## Code blocks

Wrap code in three backticks. Add the language name after the first three to get colors.

````markdown
```stata
regress ln_wage educ, vce(robust)
```

```r
feols(ln_wage ~ educ, data = df, vcov = "hetero")
```

```python
pf.feols("ln_wage ~ educ", data=df, vcov="hetero")
```
````

Common language names: `stata`, `r`, `python`, `sql`, `bash`, `latex`, `json`, `yaml`, `text`.

## Tables

```markdown
| Variable | Mean | SD   |
|----------|-----:|-----:|
| Wage     | 24.1 | 11.3 |
| Educ     | 13.2 |  2.8 |
```

| Variable | Mean | SD |
|---|---:|---:|
| Wage | 24.1 | 11.3 |
| Educ | 13.2 | 2.8 |

- The second line separates the header from the rows. It needs at least three dashes per column.
- A colon on the right (`-----:`) right-aligns the column, which suits numbers. A colon on the left aligns left, and colons on both sides center the column.
- The columns do not need to line up in the text file. Neat spacing just makes the file easier to read.

!!! tip "Do not type big tables by hand"
    For a regression or summary table, export it from your code: `esttab` in Stata, `modelsummary` or `knitr::kable()` in R, and `df.to_markdown()` in Python.

## Maths

Many Markdown tools, including GitHub, Jupyter and Quarto, render LaTeX maths between dollar signs.

| You type | Where it appears |
|---|---|
| `$y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$` | Inside the sentence |
| `$$\hat\beta = (X'X)^{-1}X'y$$` | On its own line, centered |

See the [LaTeX guide](../latex/README.md#equations) for the maths commands.

## Quotes, footnotes and comments

```markdown
> Correlation is not causation.

This result is robust to clustering.[^1]

[^1]: Standard errors clustered by state.

<!-- A comment: visible in the file, hidden in the output -->
```

Footnotes work on GitHub and in Quarto, but not in every Markdown tool.

## Write a good README

Every project folder should have a `README.md`. It is the first file anyone, including future you, will open.

```markdown
# Minimum wage and teen employment

Replication code for my senior thesis, 2026.

## Data

- `data/raw/cps_extract.dta`: CPS monthly files, 2010–2019, from IPUMS
- `data/raw/min_wage.csv`: state minimum wages, from the Department of Labor

## How to run

1. Set the project folder in `code/00_master.do`
2. Run `code/00_master.do` in Stata 18

## Outputs

- `output/tables/main_results.tex`: Table 2 in the paper
- `output/figures/event_study.png`: Figure 3 in the paper
```

The [templates](../templates/index.md) section has a matching project folder layout.

## Markdown on GitHub

GitHub adds a few extras to standard Markdown:

| Feature | You type | What it does |
|---|---|---|
| Mention | `@username` | Notifies that person |
| Issue link | `#12` | Links to issue or pull request 12 |
| Callout | `> [!NOTE]` on the first line of a quote | Shows a colored note box. `[!TIP]`, `[!WARNING]` and `[!IMPORTANT]` also work. |
| Collapsible section | `<details><summary>Title</summary> ... </details>` | Hides long content until clicked |

## Where Markdown goes next

| Tool | What it adds |
|---|---|
| [Jupyter notebooks](https://jupyter.org/) | Markdown cells between Python code cells |
| [Quarto](https://quarto.org/) | Papers, slides and websites that mix Markdown with R, Python or Stata code, exported to PDF, Word or HTML |
| [R Markdown](https://rmarkdown.rstudio.com/) | The older R version of Quarto |
| [MkDocs](https://www.mkdocs.org/) | Builds a website, like this one, from a folder of Markdown files |

## Learn more

- [Markdown Guide](https://www.markdownguide.org/): every piece of syntax, with examples
- [GitHub's Markdown documentation](https://docs.github.com/en/get-started/writing-on-github): the GitHub extras in full
