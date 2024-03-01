# survey-plots
This repo should contain the code for plots

# Initialization

DO NOT ADD LIMESURVEY FILES FROM THE N2SURVEY TO THIS REPOSITORY!!

0. Add Survey data to your file system
     1. Sign NDA
     2. Get access to the data
     3. Unzip file and put folder somewhere.
     4. You will for example need the following files: `Survey2021_structure.xml` and `Survey2021_Qcode_Acode.csv`
2. Go to the terminal on your computer. 
3. Clone project to your computer. 
```
git clone git@github.com:helmholtz-juniors/survey-framework.git
```
4. DO NOT ADD THE SURVEY DATA INTO THE REPOSITORY ON YOUR COMPUTER. 
5. If you are using an IDE, it will ask you to install all requirements from `requirements.txt`. 

# Setup Development Environment
We use [pre-commit](https://pre-commit.com/#intro) to ensure quality of code. This is automatically installed with the requirements and should warn you if you are commiting dysfunctional code. Our pre-commit checks also if you are using [Python typing](https://docs.python.org/3/library/typing.html).

```
pip install -r requirements.txt
```

# DocStrings
Style: Google
https://google.github.io/styleguide/pyguide.html#Comments

# Nice to Know
- contingent questions are the longtext open ended questions added to other questions, e.g. `A2` and `A2other` 

# How to Commit
1. pull the current project status `git pull`
     1. if git tells you to clean up your repository first, stash your code with `git stash` oder `git stash pull`
     2. afterwards pull the current status with `git pull`
     3. pop the stash to resolve merge conflicts with git `git stash pop`
          1. remember that there can be more than one stash, if you don't want to pop the last one check `git stash list` and then use `git stash apply` or `git stash apply stash@{2}` or whichever one you want to apply
          2. `git stash pop` will also remove the last added stash from the stash list
2. use `pre-commit` to check whether `ruff` and `mypy` are happy 
     1. do this within the `(.venv)` environment to make sure your version complys with the requirements in `requirements.txt`
3. add files to be comitted 
4. commit everything to a (new) branch
5. github checks with lint what mistakes are still in the code
6. make ruff happy
7. stash and merge brange to origin master


## Helpful commands to locally apply
- use `pre-commit` in the Terminal to check for errors
- use `ruff format` to format files, e.g. `ruff format test.py` to format `test.py` or `ruff format` to format everything
- use `mypy --strict [folder]` for sth ???
- use `run check --fix` for sth ???



