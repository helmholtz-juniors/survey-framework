import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


import pandas as pd
import numpy as np
import matplotlib.pyplot
matplotlib.use('Agg')
import seaborn as sns
from src.survey_framework.data_import.data_import import LimeSurveyData
from src.survey_framework.data_analysis.scoring import *
from src.survey_framework.plotting.helmholtzcolors import *
from src.survey_framework.plotting.stackedbarplots import *
from pathlib import Path

structure_file = Path("../data/survey_2024/survey_738345_en.xml")
responses_file = Path("../data/survey_2024/results-survey738345-Qcode-Acode.csv")

survey_data = LimeSurveyData(structure_file, responses_file)

# print(survey_data.get_responses("A8"))



def years_of_phd(survey_data):
    start_year = survey_data.get_responses("A8")
    dict_conv = {
        'A12': 2024,
        'A11': 2023,
        'A10': 2022,
        'A1':  2021,
        'A2':  2020,
        'A3':  2019,
        'A4':  2018,
        'A5':  2017,
        'A6':  2016,
        'A8':  2015,     # Converted A8 to 2015 (as an int)
        'A9':  np.nan,   # Use np.nan for missing values
        'A13': np.nan
    }

    # Replace the codes in the A8 column with the mapped numeric values.
    start_year = start_year.replace(dict_conv)
    # Convert the 'A8' column to a numeric type.
    start_year["A8"] = pd.to_numeric(start_year["A8"], errors='coerce')
    start_year.dropna(inplace=True)
    # Create a new column "Year" that calculates the difference between A8 and 2024.
    start_year["Year"] = (2024 - start_year["A8"])+1
    start_year["Year"] = np.where(start_year["Year"] > 3, ">3", start_year["Year"].astype(int).astype(str))
    # Convert the Year column to a categorical type with ordered categories: "1", "2", "3", ">3".
    start_year["Year"] = pd.Categorical(start_year["Year"], categories=["1", "2", "3", ">3"], ordered=True)

    # print(start_year)
    # sns.barplot(start_year["Year"])
    # plt.savefig('year_histogram_bar.png', dpi=300, bbox_inches='tight')
    return(start_year)

start_year = years_of_phd(survey_data)

########### Involves Scoring

# # ##################################### SA 
scoring_df = rate_mental_health(responses=survey_data.get_responses("D1"),  condition=Condition.STATE_ANXIETY)

SA_classes = scoring_df.iloc[:,1]
SA_classes = (SA_classes.cat.add_categories(['NA'])).fillna('NA')

fig,ax = plot_stacked_bar(classes=SA_classes,n_question = len(SA_classes),
                          category_order = ["NA","no or low anxiety", "moderate anxiety","high anxiety"],
                          label_q_data="Fraction",NA_Values=True,
                          legend_title='SA category')

fig.savefig("SA_plot.png", dpi=300)

# PhD Year stratified SA Plot
scoring_df = rate_mental_health(responses=survey_data.get_responses("D1"),  condition=Condition.STATE_ANXIETY)
scoring_df["Year"] = start_year["Year"]
scoring_df["state_anxiety_class"] = scoring_df["state_anxiety_class"].cat.add_categories(['NA']).fillna('NA')

fig, ax = plot_stacked_bar_by_year_side_by_side(
    df=scoring_df,
    classes_column="state_anxiety_class",
    year_column='Year',
    category_order=["NA", "no or low anxiety", "moderate anxiety", "high anxiety"],
    label_q_data="Fraction",
    NA_Values=True,
    legend_title='SA category'
)
fig.savefig("SA_plot_PhDYears_stratified.png", dpi=300)


# ###################################### TA

scoring_df = rate_mental_health(responses=survey_data.get_responses("D2"),  condition=Condition.TRAIT_ANXIETY)

TA_classes = scoring_df.iloc[:,1]
TA_classes = (TA_classes.cat.add_categories(['NA'])).fillna('NA')

fig,ax = plot_stacked_bar(classes=TA_classes,n_question = len(TA_classes.notna()),
                          category_order = ["NA","no or low anxiety", "moderate anxiety","high anxiety"],
                          label_q_data="Fraction",NA_Values=True,
                          legend_title='TA category')
fig.savefig("TA_plot.png", dpi=300)

# PhD Year stratified TA Plot
scoring_df = rate_mental_health(responses=survey_data.get_responses("D2"),  condition=Condition.TRAIT_ANXIETY)
scoring_df["Year"] = start_year["Year"]
scoring_df["trait_anxiety_class"] = scoring_df["trait_anxiety_class"].cat.add_categories(['NA']).fillna('NA')

fig, ax = plot_stacked_bar_by_year_side_by_side(
    df=scoring_df,
    classes_column="trait_anxiety_class",
    year_column='Year',
    category_order=["NA", "no or low anxiety", "moderate anxiety", "high anxiety"],
    label_q_data="Fraction",
    NA_Values=True,
    legend_title='TA category'
)
fig.savefig("TA_plot_PhDYears_stratified.png", dpi=300)


# ###################################### Depression
scoring_df = rate_mental_health(responses=survey_data.get_responses("D3"),  condition=Condition.DEPRESSION)
depression_classes = scoring_df.iloc[:,1]
depression_classes = (depression_classes.cat.add_categories(['NA'])).fillna('NA')

fig,ax = plot_stacked_bar(classes=depression_classes,n_question = len(depression_classes.notna()),
                          category_order=["NA","no to minimal depression", "mild depression","moderate depression", 
                                          "moderately severe depression","severe depression"],NA_Values=True,
                          label_q_data="Fraction",
                          legend_title='DS category')
fig.savefig("DS_plot.png", dpi=300)

# PhD Year stratified Depression Plot
scoring_df = rate_mental_health(responses=survey_data.get_responses("D3"),  condition=Condition.DEPRESSION)

scoring_df["Year"] = start_year["Year"]
scoring_df["depression_class"] = scoring_df["depression_class"].cat.add_categories(['NA']).fillna('NA')

fig, ax = plot_stacked_bar_by_year_side_by_side(
    df=scoring_df,
    classes_column="depression_class",
    year_column='Year',
    category_order=["NA","no to minimal depression", "mild depression","moderate depression", 
                                          "moderately severe depression","severe depression"],
    label_q_data="Fraction",
    NA_Values=True,
    legend_title='DS category'
)
fig.savefig("DS_plot_PhDYears_stratified.png", dpi=300)


# ###################################### Somatic

scoring_df =rate_somatic(survey_data.get_responses("D4"))
somatic_classes = scoring_df.iloc[:,-1]
somatic_classes = (somatic_classes.cat.add_categories(['NA'])).fillna('NA')
# print(somatic_classes)
fig,ax = plot_stacked_bar(classes=somatic_classes,n_question = len(somatic_classes.notna()),
                          category_order=["NA","No somatic symptoms","Mild somatic symptoms",
                                          "Moderate somatic symptoms","Severe somatic symptoms",],
                          label_q_data="Fraction",
                          legend_title='Somatic Symptoms')
fig.savefig("Somatic_plot.png", dpi=300)


# # ###################################### Burnout (Might need to be investigated)
# scoring_df =rate_burnout(survey_data.get_responses("D3d"))
# burnout_classes = scoring_df.iloc[:,-1]
# fig,ax = plot_stacked_bar(classes=burnout_classes,n_question = len(burnout_classes.notna()),
#                           category_order=["NA" , "Engaged", "Ineffective", "Overextended", "Disengaged", "Burnout"],
#                           label_q_data="Fraction",
#                           legend_title='Burnout Symptoms')
# fig.savefig("Burnout_plot.png", dpi=300)


######################################################################


########### Involves Fetching and Plotting 

#scoring_df= rate_MH_help(survey_data.get_responses("D8"))
dict_list = survey_data.get_choices("D8")
# print(dict_list)
scoring_df = survey_data.get_responses("D8")
getting_help_classes = (scoring_df.iloc[:,-1]).map(dict_list)
# print(getting_help_classes.value_counts())
fig,ax = plot_bar(classes=getting_help_classes,n_question = len(getting_help_classes.notna()),
                          category_order=['No, I am not aware of any', 'Yes, but I have never used them',
                         'Yes, I have used them and I was satisfied', 'Yes, I have used them, but I was not satisfied',
                         'I don’t want to answer this question'],
                          orientation=Orientation.VERTICAL,
                          fontsize=20,
                          label_q_data="",
                          legend_loc=None) 
fig.savefig("GettingHelp_plot.png", dpi=300)


scoring_df=survey_data.get_responses("D9")
getting_help_2_classes = scoring_df.iloc[:,-2]
getting_help_2_classes = getting_help_2_classes.replace(survey_data.get_choices('D9'))
fig,ax = plot_bar(classes = getting_help_2_classes,
                  n_question = len(getting_help_2_classes.notna()),
                  category_order=["Yes","No","I don't want to answer","Other"],
                  label_q_data="", 
                  legend_loc=None) 
fig.savefig("GettingHelp_2_plot.png", dpi=300)


dict_list = survey_data.get_choices("D6")
# print(dict_list)
scoring_df = survey_data.get_responses("D6")
impact_classes = (scoring_df.iloc[:,-1]).map(dict_list)
# print(impact_classes.value_counts())

fig,ax = plot_bar(classes=impact_classes,
                  n_question = len(impact_classes.notna()),
                          category_order=['I dont want to answer this question',
                                          'I dont know','I have not been bothered by any problems','Not difficult at all',
                                          'Somewhat difficult','Very difficult',
                                          'Extremely difficult'],
                          orientation=Orientation.VERTICAL,
                          fontsize=20,
                          label_q_data="",
                          legend_loc=None) 
fig.savefig("ImpactMH_plot.png", dpi=300)

# scoring_df=survey_data.get_responses("D3b")
# sleep_timings = scoring_df.iloc[:,-1]
# sleep_timings = sleep_timings.replace(survey_data.get_choices('D3b'))
# fig,ax = plot_bar(classes=sleep_timings,n_question = len(sleep_timings.notna()),
#                         #   category_order=[],
#                           label_q_data="",
#                           legend_loc=None) 
# fig.savefig("Sleep_impact_plot.png", dpi=300)

# scoring_df=survey_data.get_responses("D3c")
# sleep_impact = scoring_df.iloc[:,-1]
# sleep_impact =sleep_impact.replace(survey_data.get_choices('D3c'))
# fig,ax = plot_bar(classes=sleep_impact,n_question = len(sleep_impact.notna()),
#                         #   category_order=[],
#                           label_q_data="",
#                           legend_loc=None) 
# fig.savefig("Sleep_impact_plot_2.png", dpi=300)







