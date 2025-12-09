# Workflow

This document describes the current workflow for working in the helmholtz-juniors organization on github. 

# Plots
Overview of plots: https://notes.desy.de/s/X42lW1ct-

# Tasks
- all currently available tasks can be found in the Project ['Survey'](https://github.com/orgs/helmholtz-juniors/projects/3)
- go to this project and pick a task from the 'Ready' column
	- if you are interested in the conceptional side of things and want to work on getting tasks ready for assignment, get in touch with Carolyn Guthoff (there might be no availability for this, but it's still good to know)
- assign yourself to this task (please only assign yourself to one task at a time)
- once you've started working on the task, move it to the column 'In progress'
	- check out the 'How to Commit' section in the `README.md` file in `survey-framework` (it is important that you follow the how to commit-workflow, because due to this being a private project, github doesn't automatically enforce the rules)
	- remember to write loads of comments in your code, so others can easily understand what is happening
- after you've finished the task, move it to the column 'Review' and assign two of the following three for review on the task (Florian Hantke, Keno Hassler, Carolyn Guthoff)

## Helpful notes 
- Every task should have an adaquate description of what should be done. Sometimes this includes looking through older code. Here's a list of all the repositories that include code connected to the survey framework: 
	- [https://github.com/helmholtz-juniors](https://github.com/helmholtz-juniors)
		- this is the organization connected to this document
	- [https://github.com/N2-Survey/SurveyFramework/tree/main](https://github.com/N2-Survey/SurveyFramework/tree/main)
		- this is the framework that our survey framework is based on, it can be helpful to look through the wiki or the code if things are unclear
	- [https://github.com/JennPopp/HelmholtzSurvey2023](https://github.com/JennPopp/HelmholtzSurvey2023)
		- this is the old repository for the survey reports that was planned in 2023 but was moved to 2024
		- if you want access, get in touch with Jenn Popp
	- [https://github.com/JennPopp/HelmholtzReport_Survey2021](https://github.com/JennPopp/HelmholtzReport_Survey2021)
		- this is the repository for the 2021 Helmholtz Report, it is very helpful to look here for any types of plots 
		- if you want access, get in touch with Jenn Popp
	- [https://github.com/joca-k/N2-survey-center-specific-reports](https://github.com/joca-k/N2-survey-center-specific-reports)


# Writing Code

- In general, it is important to write code as reusable as possible. For the survey framework this means, that no hard coded references should be included except for testing purposes where functions are tested with real data. 
- If you want some references, look in `plotting/barplots.py`, `plotting/helper_barplots.py` for the functions and in `testing/test_A.py` and `testing/test_E.py` for examples. 
- We can recommend using Jupiter Notebooks for testing initially how things work and how to best handle the data. However, it is strictly forbidden to commit Jupyter Notebooks to the github project. These files are however useful to write documentations. Just remember, to use dummy data for any figures to not leak any confidentail data. 

# Documentation 

- Write adaquate documentations in the `documentation` folder on how to use the code you wrote. Once there's an example available, we'll link it here :) 
