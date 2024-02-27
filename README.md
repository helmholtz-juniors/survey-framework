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


