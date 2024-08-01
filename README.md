# survey_framework
This repo should contain the code for data import, analysis and plotting.

## Getting started

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

NEVER COMMIT LIMESURVEY DATA TO THIS (OR ANY) REPOSITORY!

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


## Beginner's guide to git
### How to Commit
DON'T COMMIT TO MAIN! (We cannot enforce it right now, but please don't).

1. pull the current project status `git pull`
    1. if git tells you to clean up your repository first, stash your code with `git stash`
    2. afterwards pull the current status with `git pull`
    3. pop the stash to resolve merge conflicts with git `git stash pop`
        1. remember that there can be more than one stash, if you don't want to pop the last one check `git stash list` and then use `git stash apply` or `git stash apply stash@{2}` or whichever one you want to apply
        2. `git stash pop` will also remove the last added stash from the stash list
2. add files to be comitted 
3. use `pre-commit` to check whether `ruff` and `mypy` are happy 
    1. do this within the `(.venv)` environment to make sure your version complys with the requirements in `requirements.txt`
4. commit everything to a (new) branch
5. github checks with lint what mistakes are still in the code
6. make ruff happy
7. create a pull request on github
    1. go to Pull requests in the top menu
    2. click on `New pull request` in the top right
8. request review in pull request 

### Helpful commands to locally apply
- use `pre-commit` in the Terminal to check for errors
- use `ruff format` to format files, e.g. `ruff format test.py` to format `test.py` or `ruff format` to format everything
- use `mypy --strict [folder]` for typing errors, also makes sense for debugging
- use `ruff check --fix` for python linter that warns for imports you didn't use or things you did wrong
