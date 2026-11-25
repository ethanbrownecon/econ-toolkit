# Command line basics

The command line, also called the terminal or shell, lets you control your computer by typing instead of clicking. You need a little of it to install packages, run scripts, use Git and keep projects reproducible. This page covers the twenty or so commands you will actually use.

!!! tip "You do not need to memorize this"
    Keep this page open the first few times. After a week, the common commands become habit.

## Open a terminal

The easiest place is inside VS Code: **View → Terminal**, or ++ctrl+grave++. It opens already inside your project folder.

=== "Mac"

    VS Code's terminal, or the **Terminal** app (search for it with ++cmd+space++). Both run `zsh`, so every command on this page works.

=== "Windows"

    Install [Git for Windows](https://git-scm.com/download/win). It includes **Git Bash**, which understands the same commands as Mac and Linux. In VS Code, click the **⌄** next to **+** in the terminal panel and choose **Git Bash**.

    Windows' own **PowerShell** also works, but some commands differ. The [cheat sheet](#cheat-sheet) shows both.

## Where am I?

The terminal is always "in" one folder, called the working directory. Commands act on that folder unless you say otherwise.

| Task | Command |
|---|---|
| Show the current folder | `pwd` |
| List the files here | `ls` |
| List files with details and hidden files | `ls -la` |
| Go into a folder | `cd code` |
| Go up one folder | `cd ..` |
| Go to your home folder | `cd ~` |
| Go to a full path | `cd ~/projects/my-project` |
| Go back to the previous folder | `cd -` |

!!! tip "Press Tab"
    Type the first few letters of a file or folder name and press ++tab++. The terminal fills in the rest. Fewer typos, less typing.

## Paths

A path is the address of a file.

| Kind | Example | Meaning |
|---|---|---|
| Absolute | `/Users/sam/projects/thesis/data/raw/cps.dta` | Starts from the top of the drive. Works from anywhere, but only on your computer. |
| Relative | `data/raw/cps.dta` | Starts from the current folder. Works on any computer with the same project layout. |
| Home | `~/projects/thesis` | `~` is your home folder |
| Up one | `../output` | `..` is the folder above |

- Use **forward slashes** (`/`). They work in Stata, R and Python on every system, including Windows.
- Put paths with spaces in quotes: `cd "My Documents"`. Better still, avoid spaces in file and folder names. Use `-` or `_` instead.
- Use relative paths inside your code so the project runs on other computers. The [templates](../templates/index.md) show how.

## Work with files and folders

| Task | Command |
|---|---|
| Make a folder | `mkdir output` |
| Make nested folders in one go | `mkdir -p data/raw data/clean output/tables` |
| Create an empty file | `touch notes.md` |
| Copy a file | `cp data/raw/cps.dta backup/cps.dta` |
| Copy a folder | `cp -r output output_backup` |
| Move or rename | `mv draft.tex paper.tex` |
| Show a file's contents | `cat README.md` |
| Show the first 10 lines | `head data/raw/prices.csv` |
| Count lines in a file | `wc -l data/raw/prices.csv` |
| Find files by name | `find . -name "*.do"` |
| Search inside files | `grep -rn "reghdfe" code/` |
| Open a file or folder in its usual app | `open .` (Mac) or `start .` (Windows) |
| Open the folder in VS Code | `code .` |

!!! warning "`rm` deletes for good"
    `rm file.csv` deletes a file and `rm -r folder` deletes a folder and everything in it. There is no Recycle Bin or Trash. Run `ls` first to check exactly what you are about to delete, and never run `rm -r` on a path you have not checked.

## Run your code

| Language | Command |
|---|---|
| Python | `python code/01_analysis.py` |
| R | `Rscript code/01_analysis.R` |
| Stata (Mac) | `/Applications/Stata/StataSE.app/Contents/MacOS/stata-se -b do code/00_master.do` |
| Stata (Windows) | `"C:\Program Files\Stata18\StataSE-64.exe" /e do code\00_master.do` |
| LaTeX | `latexmk -pdf paper.tex` |

The Stata path depends on your version and edition (BE, SE or MP). Batch mode writes the output to a `.log` file in the current folder instead of opening a window.

Running scripts from the terminal is the best test that a project is reproducible. If `python code/01_analysis.py` works in a fresh terminal, the script does not depend on anything you clicked earlier.

## Install software

### Package managers

A package manager installs and updates software with one command.

| What | Mac | Windows |
|---|---|---|
| Apps and tools | [Homebrew](https://brew.sh/): `brew install git` | [winget](https://learn.microsoft.com/windows/package-manager/winget/) (built in): `winget install Git.Git` |
| Python packages | `pip install pandas` | `pip install pandas` |
| R packages | In R: `install.packages("fixest")` | In R: `install.packages("fixest")` |
| Stata packages | In Stata: `ssc install reghdfe` | In Stata: `ssc install reghdfe` |

### Python virtual environments

A virtual environment is a private folder of Python packages for one project. It stops projects from breaking each other when they need different package versions.

=== "Mac / Git Bash"

    ```bash
    python3 -m venv .venv              # create it, once per project
    source .venv/bin/activate          # turn it on, every new terminal
    pip install pandas pyfixest        # install packages into it
    pip freeze > requirements.txt      # record exact versions
    deactivate                         # turn it off
    ```

=== "Windows PowerShell"

    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install pandas pyfixest
    pip freeze > requirements.txt
    deactivate
    ```

    If PowerShell refuses to run the activate script, run this once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

When the environment is on, the prompt starts with `(.venv)`. Someone else can rebuild it with `pip install -r requirements.txt`. Add `.venv/` to your `.gitignore` so Git does not track it.

## Environment variables and secrets

Some data services give you an API key, a password-like code. Never type it into a script you share or commit to Git. Store it as an environment variable instead.

```bash
# In the terminal (lasts until you close it)
export FRED_API_KEY="your-key-here"
```

```python
import os
key = os.environ["FRED_API_KEY"]
```

```r
key <- Sys.getenv("FRED_API_KEY")
```

To keep a key between sessions, put it in a `.env` file in the project folder. Add `.env` to `.gitignore` **before** you create the file.

## Habits that save time

| Do this | How |
|---|---|
| Rerun a recent command | Press ++arrow-up++ |
| Search your command history | ++ctrl+r++, then type part of the command |
| Stop a command that is running | ++ctrl+c++ |
| Clear the screen | `clear` or ++cmd+k++ (Mac) |
| Get help on a command | `ls --help`, or `man ls` on Mac |
| Copy from the terminal | Select the text, then ++cmd+c++ (Mac) or right-click (Windows) |

## Cheat sheet

| Task | Mac, Linux, Git Bash | Windows PowerShell |
|---|---|---|
| Current folder | `pwd` | `pwd` |
| List files | `ls` | `ls` or `dir` |
| Change folder | `cd folder` | `cd folder` |
| Make folder | `mkdir folder` | `mkdir folder` |
| Copy file | `cp a.csv b.csv` | `cp a.csv b.csv` |
| Move or rename | `mv a.csv b.csv` | `mv a.csv b.csv` |
| Delete file | `rm a.csv` | `rm a.csv` |
| Show file | `cat a.csv` | `cat a.csv` |
| First lines | `head a.csv` | `Get-Content a.csv -Head 10` |
| Search in files | `grep -rn "text" .` | `Select-String -Path *.do -Pattern "text"` |
| Set a variable | `export KEY="value"` | `$env:KEY = "value"` |
| Clear screen | `clear` | `cls` |

## Learn more

- [The Unix Shell](https://swcarpentry.github.io/shell-novice/): Software Carpentry's beginner lesson
- [The Missing Semester](https://missing.csail.mit.edu/): MIT's course on the shell, editors and Git
- [explainshell.com](https://explainshell.com/): paste a command and see what each part does
