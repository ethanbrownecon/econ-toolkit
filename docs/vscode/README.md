# VS Code

VS Code is a free code editor. One window can edit and run Python, R, LaTeX and Markdown, show your files, open a terminal and use Git. Learn one editor and use it for everything.

## Install

1. Download VS Code from [code.visualstudio.com](https://code.visualstudio.com/) and install it.
2. Open it and choose **File → Open Folder**. Pick your project folder, not a single file.
3. Install the extensions for the languages you use (see below).

!!! tip "Always open the folder"
    Opening the project folder tells VS Code where your project starts. The file tree, search, terminal and Git all work from that folder. Opening a single file loses all of that.

## The window

| Area | Where | What it does |
|---|---|---|
| **Explorer** | Left bar, top icon | Your project's files and folders |
| **Search** | Left bar, magnifying glass | Find text in every file in the project |
| **Source Control** | Left bar, branch icon | See changes, commit and push with Git |
| **Extensions** | Left bar, four squares | Install support for more languages |
| **Editor** | Center | Where you write code. Split it to see two files side by side. |
| **Terminal** | Bottom panel | A command line already inside your project folder |
| **Status bar** | Bottom edge | Current Python or R version, Git branch, errors |

## Extensions

Open the Extensions view, search for the name, and click **Install**.

=== "Python"

    | Extension | What it adds |
    |---|---|
    | **Python** (Microsoft) | Run Python, choose an environment, autocomplete |
    | **Jupyter** (Microsoft) | Notebooks and `# %%` cells in scripts |
    | **Ruff** (Astral) | Finds mistakes and tidies formatting when you save |
    | **Data Wrangler** (Microsoft) | Spreadsheet-style view of a pandas data frame |

=== "R"

    | Extension | What it adds |
    |---|---|
    | **R** (REditorSupport) | Run R, autocomplete, view data frames and plots |

    The R extension also needs one R package. Run this once in R:

    ```r
    install.packages("languageserver")
    ```

=== "Stata"

    | Extension | What it adds |
    |---|---|
    | **Stata Enhanced** (Kyle Barron) | Colors do-file syntax so it is easier to read |

    VS Code does not run Stata by itself. Write the do-file in VS Code and run it in Stata. Or install a "run in Stata" extension (search the Extensions view for "Stata run").

=== "Writing"

    | Extension | What it adds |
    |---|---|
    | **LaTeX Workshop** (James Yu) | Builds your PDF when you save and shows it beside the `.tex` file |
    | **Quarto** (Posit) | Write and preview Quarto documents |
    | **Rainbow CSV** (mechatroner) | Colors each column of a CSV file |
    | **Markdown preview** (built in) | No install needed. Press ++cmd+shift+v++ (Mac) or ++ctrl+shift+v++ (Windows). |

## Run your code

=== "Python"

    1. Open a `.py` file.
    2. Press ++cmd+shift+p++ (Mac) or ++ctrl+shift+p++ (Windows), type **Python: Select Interpreter**, and pick your environment.
    3. Run code:

    | To run | Do this |
    |---|---|
    | The whole file | Click ▶ in the top-right corner |
    | One `# %%` cell | Click **Run Cell** above the cell, or press ++shift+enter++ inside it |
    | The selected lines | Select them and press ++shift+enter++ |

    Results from cells appear in the **Interactive** window on the right, with tables and plots.

=== "R"

    1. Open a `.R` file.
    2. Run code:

    | To run | Do this |
    |---|---|
    | The current line or selection | ++cmd+enter++ (Mac) or ++ctrl+enter++ (Windows) |
    | The whole file | ++cmd+shift+s++ (Mac) or ++ctrl+shift+s++ (Windows) |

    The first run opens an R terminal at the bottom. Plots open in a panel on the right.

=== "Stata"

    1. Write your do-file in VS Code and save it.
    2. In Stata, run `do "code/01_analysis.do"`, or open the file in Stata's Do-file Editor and click **Execute**.

## Keyboard shortcuts worth learning

| Action | Mac | Windows |
|---|---|---|
| Command Palette (find any command) | ++cmd+shift+p++ | ++ctrl+shift+p++ |
| Open a file by name | ++cmd+p++ | ++ctrl+p++ |
| Show or hide the terminal | ++ctrl+grave++ | ++ctrl+grave++ |
| Show or hide the sidebar | ++cmd+b++ | ++ctrl+b++ |
| Search every file | ++cmd+shift+f++ | ++ctrl+shift+f++ |
| Comment or uncomment lines | ++cmd+slash++ | ++ctrl+slash++ |
| Move a line up or down | ++option+up++ / ++option+down++ | ++alt+up++ / ++alt+down++ |
| Copy a line down | ++shift+option+down++ | ++shift+alt+down++ |
| Edit in several places at once | ++option++ + click | ++alt++ + click |
| Rename a variable everywhere | ++f2++ | ++f2++ |
| Split the editor | ++cmd+backslash++ | ++ctrl+backslash++ |

!!! tip "Only remember one"
    If you remember nothing else, remember the **Command Palette**. Press it, type what you want ("format", "terminal", "git commit"), and pick the command from the list.

## Recommended settings

Open the Command Palette, run **Preferences: Open User Settings (JSON)**, and paste this inside the `{ }`:

```json
{
  "files.autoSave": "afterDelay",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "editor.rulers": [80],
  "editor.minimap.enabled": false,
  "[markdown]": { "editor.wordWrap": "on" },
  "[latex]": { "editor.wordWrap": "on" },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true
  }
}
```

| Setting | What it does |
|---|---|
| `files.autoSave` | Saves files a moment after you stop typing |
| `files.trimTrailingWhitespace` | Removes stray spaces at the end of lines |
| `files.insertFinalNewline` | Ends every file with a new line, which keeps Git diffs clean |
| `editor.rulers` | Draws a faint line at 80 characters, a sensible line length |
| `editor.minimap.enabled` | Hides the small code map on the right |
| `editor.wordWrap` | Wraps long lines in Markdown and LaTeX, where one paragraph is one line |
| `[python]` block | Tidies Python formatting with Ruff every time you save |

## Git in VS Code

The **Source Control** view does the everyday Git steps with buttons:

1. Changed files appear in the list. Click a file to see what changed.
2. Click **+** next to a file to stage it.
3. Type a message and click **Commit**.
4. Click **Sync Changes** to push to GitHub.

For what these steps mean, see [Git & GitHub](../git-github/README.md).

## Next step

Download a [template](../templates/index.md), save it in your project's `code/` folder, and run it cell by cell.
