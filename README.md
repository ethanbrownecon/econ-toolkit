<div align="center">

<a href="https://ethanbrownecon.github.io/econ-toolkit/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/brand/logo-dark.svg">
    <img src="docs/assets/brand/logo.svg" alt="The Econ Toolkit" width="420">
  </picture>
</a>

<h3>Plain-English guides to the technical skills behind economics research</h3>

<p>Stata · R · Python · LaTeX · Git · VS Code · SQL · Reproducible research</p>

[![Deploy](https://github.com/ethanbrownecon/econ-toolkit/actions/workflows/deploy.yml/badge.svg)](https://github.com/ethanbrownecon/econ-toolkit/actions/workflows/deploy.yml)
[![Website](https://img.shields.io/badge/website-live-0f766e?logo=materialformkdocs&logoColor=white)](https://ethanbrownecon.github.io/econ-toolkit/)
[![Built with Material for MkDocs](https://img.shields.io/badge/built%20with-Material%20for%20MkDocs-526cfe?logo=materialformkdocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)
[![License: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-0f766e)](LICENSE)
[![License: MIT](https://img.shields.io/badge/code-MIT-0f766e)](LICENSE-CODE)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-65a30d)](CONTRIBUTING.md)

**[Start here](https://ethanbrownecon.github.io/econ-toolkit/start-here/)** ·
**[Templates](https://ethanbrownecon.github.io/econ-toolkit/templates/)** ·
**[Coming from Stata](https://ethanbrownecon.github.io/econ-toolkit/coming-from/stata/)** ·
**[Suggest a topic](https://github.com/ethanbrownecon/econ-toolkit/issues/new/choose)**

</div>

---

## About

Economics research runs on a stack of tools, not one language. You clean data in Stata or R, estimate models, write the paper in LaTeX and keep it all in Git. **The Econ Toolkit** explains each of those tools in plain English and connects them to the work economists do.

It is written for **undergraduates and new research assistants**. Every page is short, practical and meant to be copied from.

## What's inside

| Section | What you get |
|---|---|
| **[Get set up](https://ethanbrownecon.github.io/econ-toolkit/vscode/)** | VS Code, Git & GitHub, command line and Markdown |
| **[Templates](https://ethanbrownecon.github.io/econ-toolkit/templates/)** | Ready-to-run Stata do-file, R script and Python script templates, plus a standard project folder layout |
| **[Start here](https://ethanbrownecon.github.io/econ-toolkit/start-here/)** | A six-week learning path, plus paths for a first econometrics class, an RA job, a thesis or a data career |
| **[Projects](https://ethanbrownecon.github.io/econ-toolkit/projects/)** | Guided projects: a wage regression, macro data from FRED, replications of Hansen (2015), Cheng and Hoekstra (2013) and LaLonde (1986), analyzing your own Spotify history, and testing home advantage with COVID's empty stadiums |
| **[Data](https://ethanbrownecon.github.io/econ-toolkit/data/datasets/)** | Practice and official datasets, plus guides to APIs and web scraping |
| **[Econometrics](https://ethanbrownecon.github.io/econ-toolkit/econometrics/)** | OLS, logit, fixed and random effects, IV, DiD and event studies, synthetic DiD, regression discontinuity and matching, with Stata, R and Python code, plus a glossary |
| **[Coming from…](https://ethanbrownecon.github.io/econ-toolkit/coming-from/)** | Line-by-line translation tables: Stata → R/Python, Excel → Stata/R/Python and R → Python |
| **[Guides](https://ethanbrownecon.github.io/econ-toolkit/latex/)** | LaTeX, R, Stata, Python, SQL, data visualization, machine learning and reproducible research |
| **[Resources](https://ethanbrownecon.github.io/econ-toolkit/resources/)** | The best free books, courses and documentation, plus a troubleshooting guide |

## Roadmap

- [x] Git & GitHub
- [x] LaTeX
- [x] VS Code
- [x] Script templates (Stata, R, Python)
- [x] Coming from Stata, Excel and R
- [x] Other resources
- [x] Markdown
- [x] Command line basics
- [x] Beginner project: wages and education
- [x] Fun project: Spotify listening history
- [x] Datasets, APIs and web scraping
- [x] Stata
- [x] R for econometrics
- [x] Python for data work
- [x] SQL
- [x] Econometrics and causal inference
- [x] Data visualization
- [x] Machine learning
- [x] Reproducible research

## Run the site locally

```bash
git clone https://github.com/ethanbrownecon/econ-toolkit.git
cd econ-toolkit
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open <http://127.0.0.1:8000>. Pages reload as you edit files in `docs/`.

## Repository layout

```text
econ-toolkit/
├── docs/                 every page of the site, in Markdown
│   ├── assets/brand/     logo files
│   ├── templates/files/  downloadable Stata, R and Python templates
│   └── stylesheets/      site theme
├── mkdocs.yml            site settings and navigation
└── .github/workflows/    builds and deploys the site on every push to main
```

## Contributing

Corrections, examples and topic ideas are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), then [open an issue](https://github.com/ethanbrownecon/econ-toolkit/issues/new/choose) or a pull request.

## License

- **Writing and images** are licensed under [Creative Commons Attribution 4.0 (CC BY 4.0)](LICENSE). You may share and adapt them for any purpose, including commercial use, as long as you give credit and link back to The Econ Toolkit.
- **Code**, including the templates in `docs/templates/files/`, the code examples on every page and the site configuration, is licensed under the [MIT License](LICENSE-CODE). You may use it in your own projects without credit.

## Acknowledgements

The "Coming from" pages follow the layout of Arthur Turrell's [Coding for Economists](https://aeturrell.github.io/coding-for-economists/). The site is built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
