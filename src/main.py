from pathlib import Path

from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.testing.export import export
from survey_framework.testing.test_A import test_A
from survey_framework.testing.test_D import test_D
from survey_framework.testing.test_E import test_E


def main() -> None:
    # important files and paths
    # INPUT_PATH should be an absolute path to the survey
    INPUT_PATH = "../data/survey_2024/"
    # file name of survey structure, has ending '.xml'
    XML_FILE_NAME = "survey_738345_en.xml"
    # file name of survey, has ending '.csv'
    CSV_FILE_NAME = "results-survey738345-Qcode-Acode.csv"
    OUTPUT_PATH = "output/"

    survey = LimeSurveyData(
        Path(INPUT_PATH) / XML_FILE_NAME, Path(INPUT_PATH) / CSV_FILE_NAME
    )

    test_A(survey, Path(OUTPUT_PATH))
    test_D(survey, Path(OUTPUT_PATH))
    test_E(survey, Path(OUTPUT_PATH))
    export(survey, Path(OUTPUT_PATH))


if __name__ == "__main__":
    main()
