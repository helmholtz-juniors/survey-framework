from pathlib import Path

from data_import.data_import import LimeSurveyData

def main() -> None:
    # important files and paths
    INPUT_PATH = "/Users/carolynguthoff/Documents/05_HelmholtzJuniors/Survey2021/data/Survey2021_Package_protected/"

    XML_FILE_NAME = "Survey2021_structure.xml"
    CSV_FILE_NAME = "Survey2021_Qcode_Acode.csv"
    OUTPUT_PATH = "output/"

    survey = LimeSurveyData(
        Path(INPUT_PATH) / XML_FILE_NAME, Path(INPUT_PATH) / CSV_FILE_NAME
    )

    survey.export_Qs_to_CSV(Path(OUTPUT_PATH))

if __name__ == "__main__":
    main()
