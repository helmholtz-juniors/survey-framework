#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: cguthoff

Created Jan 2023

A - General
B - Working Conditions
C - Satisfaction
D - Mental Health
E - Supervision
F - Power Abuse
H - Integration
	H1a support received
	H1b support needed
I - Career Development
J - Family
K - Covid-19

WARNING: For this to work H1a_SQ008 has to be adapted in the XML file from ` to ' in the "don't" (otherwise H1a_SQ008 and H1b_SQ008 will not map to each other)
"""

import pandas as pd
from data_import.data_import import LimeSurveyData
from plotting.barplots import plot_bar

# from plotting.barplots_sidebyside import plot_bar_side_by_side
from pathlib import Path
from data_analysis.analysis import get_data_for_q
from order.order2021 import *

import matplotlib.pyplot as plt

from plotting.plotenums import ShowAxesLabel


def test_plots_E(survey: LimeSurveyData, output_path: Path) -> None:
    section = "E"
    e5a = "E5a"
    e6a = "E6a"

    output = output_path / Path(section) / Path(e5a + "_" + e6a + ".png")

    data_e5_all = get_data_for_q(survey, e5a)
    data_e6_all = get_data_for_q(survey, e6a)

    data_e5_all = data_e5_all.dropna()
    data_e6_all = data_e6_all.dropna()

    # figure, axis = plot_bar_side_by_side(
    #     survey=survey,
    #     data_left=data_e5_all,
    #     data_right=data_e6_all,
    #     y_left=e5a,
    #     y_right=e6a,
    # )

    plt.savefig(output)


def main() -> None:
    # important files and paths
    INPUT_PATH = "/Users/carolynguthoff/Documents/05_HelmholtzJuniors/Survey2021/data/Survey2021_Package_protected/"
    # XML_FILE_NAME = "data/survey_structure_2021_v2.xml"
    # CSV_FILE_NAME = "data/dummy_data_2021_codeonly_v2.csv"
    XML_FILE_NAME = "Survey2021_structure.xml"
    CSV_FILE_NAME = "Survey2021_Qcode_Acode.csv"
    OUTPUT_PATH = "output/"

    survey = LimeSurveyData(
        Path(INPUT_PATH) / XML_FILE_NAME, Path(INPUT_PATH) / CSV_FILE_NAME
    )

    # survey.export_Qs_to_CSV(Path(OUTPUT_PATH))

    test_plots_E(survey, OUTPUT_PATH)

    # print(survey.get_choices("B8"))
    # print(survey.get_responses("B8"))

    # get all multiple choice questions
    # for q, _ in survey.questions.iterrows():
    #     if survey.get_question_type(q) == "multiple-choice":
    #         print(q)


if __name__ == "__main__":
    main()
