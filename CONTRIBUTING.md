# Contributing to The Econ Toolkit

Thank you for helping. Corrections, clearer explanations, new examples and topic ideas are all welcome.

## Ways to help

- **Report a mistake.** A wrong command, a broken link or a confusing sentence. [Open a correction issue](https://github.com/ethanbrownecon/econ-toolkit/issues/new?template=correction.yml).
- **Suggest a topic.** A tool, command or workflow that students need. [Open a topic request](https://github.com/ethanbrownecon/econ-toolkit/issues/new?template=topic-request.yml).
- **Fix it yourself.** Every page has an edit button (the pencil icon). It opens the Markdown file on GitHub, where you can propose a change.

## Writing style

The guide is written for undergraduates. Keep every page easy to approach.

- Use short sentences and plain English. Explain a term the first time you use it.
- Lead with the task ("Drop rows with a missing value"), then show the code.
- Keep code examples small and runnable. Use placeholder names such as `df`, `x`, `y`, `id` and `year`.
- Put advanced detail in a collapsible note (`??? note`) so it does not crowd the main page.
- Link to official documentation instead of copying it.

## Making a change locally

```bash
git clone https://github.com/ethanbrownecon/econ-toolkit.git
cd econ-toolkit
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Before you open a pull request, check that the site builds with no warnings:

```bash
mkdocs build --strict
```

## Pull requests

1. Create a branch for one focused change.
2. Explain what you changed and why in the pull request description.
3. If you changed code in a template, say how you tested it.

By contributing, you agree that your writing is licensed under CC BY 4.0 and your code under the MIT License, the same as the rest of the project.

The site rebuilds and deploys automatically when a pull request is merged into `main`.
