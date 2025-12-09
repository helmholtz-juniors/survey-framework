![GitHub License](https://img.shields.io/github/license/helmholtz-juniors/survey-framework)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/helmholtz-juniors/survey-framework/docs.yml?label=Docs)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/helmholtz-juniors/survey-framework/lint_and_typing.yml?label=Lint)
![GitHub Tag](https://img.shields.io/github/v/tag/helmholtz-juniors/survey-framework)

# survey_framework
This repo contains the code for data import, analysis and plotting.
It is *public*, so it should at no point contain data or text for reports.

> [!WARNING]  
> Never commit raw survey data to this repository! Due to internals of git,
> it is almost impossible to erase accidentally committed data from history.
> We suggest you follow the folder structure outlined below.

## Getting started
Check out the **[:book: documentation](https://blog.helmholtz-juniors.de/survey-framework)**! Feel free to extend it by adding a file to [`docs/`](docs/). (We should perhaps also move some content from this README into it?)

### Folder Organization
We suggest the following folder structure:
```tree
n2_survey
|-- survey-framework (this repository)
|   |-- data (dummy data)
|   |-- documentation
|   |-- src
|   |-- .venv (python environment)
|   |-- pyproject.toml
|   `-- README.md (this file)
|-- data (CONFIDENTIAL!)
|   |-- survey_2021
|   `-- survey_2024
|       |-- survey_738345_en.xml (structure description)
|       `-- results-survey738345-Qcode-Acode.csv (answers)
|-- survey-center-specific-2024
    `-- .venv (python environment)
`-- survey-general-2024
```

### Using survey data

1. Sign NDA
2. Get access to the data
3. Unzip file and move the folder. **Keep it outside any git repositories** (see suggested structure above)!
4. You will for example need the following files: `Survey2021_structure.xml` and `Survey2021_Qcode_Acode.csv`


### Setting up the development environment

1. Navigate to the n2_survey directory
    ```sh
    cd n2_survey
    ```
2. Clone this project to your computer
    ```sh
    git clone git@github.com:helmholtz-juniors/survey-framework.git
    ```
3. Create and activate a virtual environment
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    Run the last command whenever you come back to the project to re-activate the virtual environment.
4. Install this package (in editable mode). This way, it can be used from other packages and still be modified.
    ```sh
    cd survey_framework
    python3 -m pip install -e .'[lint]'
    ```

### Kick the tires

To check if everything works, run (inside the survey_framework directory):
```sh
pytest
```
This should run the test cases and generate a few basic plots in the output subdirectory.

### Preparing a commit
Our CI pipeline automatically checks for code formatting and typing errors.
To do the same locally, use `ruff` for linting, `ruff format` for code formatting and `mypy --strict` for type checking.
If you are not familiar with it, maybe check out the documentation for [Python typing](https://docs.python.org/3/library/typing.html).

To make our life easier, we defined a pre-commit hook.
It does the above automatically when you try to commit files in git and informs you what needs to be changed.
If you like, install pre-commit in the venv (`python3 -m pip install pre-commit`) and run `pre-commit install` inside the survey_framework folder to set it up.


## Code Documentation

### DocStrings
We currently use 
[Google-style](https://google.github.io/styleguide/pyguide.html#Comments) DocStrings.
If you use a decent IDE (recommendations: VS Code or PyCharm), it will display documentation for functions when you hover over their name. Nice!

### Nice to Know
- contingent questions are the longtext open ended questions added to other questions, e.g. `A2` and `A2other` 

## Attribution
This project started as a fork of [N2-Survey/SurveyFramework](https://github.com/N2-Survey/SurveyFramework), however, we diverged quite a bit over time.
Most of the code in data_import is still similar to the original (which is under the [MIT License](LICENSE), as well as our fork).

## Appendix: Beginner's guide to git
### How to upload (commit) your work

> [!IMPORTANT]  
> Please don't commit directly to main, this makes it easier to work in parallel
> and we can review each other's code before it gets merged.

1. Create a new branch like `git branch 'my-epic-branch-name'` and switch to it (`git switch 'my-epic-branch-name'`).
2. Mark files for upload by name using `git add <file>`. Finally, `git commit` everything.
3. Upload your commit using `git push -u origin 'my-epic-branch-name'`.
4. Create a pull request for the new branch on GitHub.
5. GitHub CI checks for compliance with our linting rules (see below).
   Request a review in the pull request, don't merge it yourself.

### Helpful commands to locally apply
We use linting and type checking to enforce a certain degree of code quality.
You can run the following tools after activating the virtual environment:
- use `pre-commit` in the Terminal to run the CI checks locally
- use `ruff format` to format files, e.g. `ruff format test.py` to format `test.py` or `ruff format` to format everything
- use `mypy --strict [folder]` to check for typing errors, also makes sense for debugging
- use `ruff check --fix` to have the linter check your code (and automatically fix some simple issues).
