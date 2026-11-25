# Templates

Every script you write should look the same. Then anyone, including you in six months, can open it and know where everything is.

These templates give Stata, R and Python the same structure. Download one, change the names, and start writing.

<div class="grid cards" markdown>

-   :material-chart-box-outline:{ .lg .middle } **Stata do-file**

    ---

    Header, setup, logging, global paths and `esttab` output.

    [:octicons-arrow-right-24: Stata template](stata.md)

-   :material-language-r:{ .lg .middle } **R script**

    ---

    Header, packages, `here()` paths, `fixest` and `ggsave`.

    [:octicons-arrow-right-24: R template](r.md)

-   :material-language-python:{ .lg .middle } **Python script**

    ---

    Header, imports, `pathlib` paths, runnable cells and `pyfixest`.

    [:octicons-arrow-right-24: Python template](python.md)

</div>

## The same six parts, in every language

| Part | What goes in it |
|---|---|
| **Header** | Project, file name, purpose, author, date, input files, output files |
| **0. Setup** | Packages, settings, random seed, folder paths |
| **1. Load data** | Read the raw files. Nothing else. |
| **2. Clean** | Rename, fix types, drop bad rows, check that the IDs are unique |
| **3. Create variables** | Every new variable, with a label if the language supports it |
| **4. Analysis** | Regressions and summary statistics |
| **5. Save results** | Tables, figures and the clean dataset |

## Project folder

Put each project in one folder with this layout. All three templates expect it.

```text
my-project/
├── README.md          what the project is and how to run it
├── code/
│   ├── 00_master.do   runs everything in order (or run_all.R / run_all.py)
│   ├── 01_clean.do
│   └── 02_analysis.do
├── data/
│   ├── raw/           original files: never edit these
│   └── clean/         files your code creates
└── output/
    ├── figures/
    ├── tables/
    └── logs/
```

!!! tip "Three rules that save you later"
    1. **Never edit raw data by hand.** Every change happens in code, so you can redo it.
    2. **Number your scripts.** `01_`, `02_`, `03_` shows the order to run them in.
    3. **One path to change.** Each template sets the project folder in one place. Moving to a new computer means changing one line.
