from pathlib import Path

import pytest

from survey_framework.data_import.data_import import LimeSurveyData

### important files and paths
# path to the survey
INPUT_PATH = Path("../data/survey_2024/")
# file name of survey structure, has ending '.xml'
XML_FILE_NAME = "survey_738345_en.xml"
# file name of survey, has ending '.csv'
CSV_FILE_NAME = "results-survey738345-Qcode-Acode.csv"
# output directory
OUTPUT_PATH = Path("output")


@pytest.fixture
def survey() -> LimeSurveyData:
    return LimeSurveyData(
        Path(INPUT_PATH) / XML_FILE_NAME, Path(INPUT_PATH) / CSV_FILE_NAME
    )


@pytest.fixture
def output_path() -> Path:
    return OUTPUT_PATH
