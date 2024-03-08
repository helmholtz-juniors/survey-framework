# from testing.export import export
from pathlib import Path
from data_import.data_import import LimeSurveyData
from testing.test_A import test_A
# from testing.test_E import test_E


def main() -> None:
    # important files and paths
    # INPUT_PATH should be an absolute path to the survey
    INPUT_PATH = "/Users/carolynguthoff/Documents/05_HelmholtzJuniors/Survey2021/data/Survey2021_Package_protected/"
    # file name of survey structure, has ending '.xml'
    XML_FILE_NAME = "Survey2021_structure.xml"
    # file name of survey, has ending '.csv'
    CSV_FILE_NAME = "Survey2021_Qcode_Acode.csv"
    OUTPUT_PATH = "output/"

    survey = LimeSurveyData(
        Path(INPUT_PATH) / XML_FILE_NAME, Path(INPUT_PATH) / CSV_FILE_NAME
    )

    test_A(survey, Path(OUTPUT_PATH))
    # test_E(survey, Path(OUTPUT_PATH))
    # export(survey, Path(OUTPUT_PATH))


if __name__ == "__main__":
    main()
