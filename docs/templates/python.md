# Python script template

[:material-download: Download analysis.py](files/analysis.py){ .md-button .md-button--primary download }

## The template

```python title="code/01_analysis.py"
--8<-- "analysis.py"
```

## What each part does

| Part | Why it is there |
|---|---|
| Docstring header | Says what the file does and which files it reads and writes. |
| `# %%` | Marks a cell. In VS Code you can run one cell at a time, like a notebook, but the file stays a plain script. |
| Imports at the top | Shows every package the script needs in one place. |
| `ROOT` and `Path` | Builds paths from the project folder, so the script works on any computer. |
| `default_rng(...)` | Makes random draws give the same result every run. |
| `assert` | Stops the script if two rows share the same `id` and `year`. |
| `pf.etable(..., type="tex")` | Writes the regressions into one LaTeX table. |
| `fig.savefig()` | Saves the figure at a fixed resolution. |

!!! tip "Script or notebook?"
    Use a `.py` script with `# %%` cells for analysis you will keep. It runs from top to bottom every time and works well with Git. Use a Jupyter notebook (`.ipynb`) for quick exploration.

??? note "Run the whole project"
    Create `code/run_all.py` and run each script in order:

    ```python
    import runpy
    from pathlib import Path

    code = Path(__file__).resolve().parent
    for script in ["01_clean.py", "02_analysis.py", "03_figures.py"]:
        runpy.run_path(code / script, run_name="__main__")
    ```
