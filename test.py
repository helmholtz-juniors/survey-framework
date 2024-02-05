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

WARNING: For this to work H1a_SQ008 has to be adapted in the XML file from ` to ' in the don't (otherwise H1a_SQ008 and H1b_SQ008 will not map to each other)
"""

from data_import.data_import import LimeSurveyData
from pathlib import Path


def main() -> None:
    # important files and paths
    INPUT_PATH = ""
    XML_FILE_NAME = "data/survey_structure_2021_v2.xml"
    CSV_FILE_NAME = "data/dummy_data_2021_codeonly_v2.csv"

    _ = LimeSurveyData(
        Path(INPUT_PATH + XML_FILE_NAME), Path(INPUT_PATH + CSV_FILE_NAME)
    )

    print("HelloWorld")


if __name__ == "__main__":
    main()
