from pathlib import Path

from data_import.data_import import LimeSurveyData


def export(survey: LimeSurveyData, output_path: Path) -> None:

    survey.export_Qs_to_CSV(output_path)
