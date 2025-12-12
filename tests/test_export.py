from pathlib import Path

from survey_framework.data_import.data_import import LimeSurveyData


def test_export(survey: LimeSurveyData, output_path: Path) -> None:
    survey.export_Qs_to_CSV(output_path)
