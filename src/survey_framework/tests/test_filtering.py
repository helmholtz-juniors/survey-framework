from pathlib import Path

from survey_framework.data_analysis.analysis import filter_by_center, get_data_for_q
from survey_framework.data_import.data_import import LimeSurveyData


def test_filtering(survey: LimeSurveyData, output_path: Path) -> None:
    """This test is for a specific regression:
    Data filtering was broken if one used `get_data_for_q()` instead of
    `survey.get_responses()` due to the reindexing happening.
    """
    set1 = get_data_for_q(survey, "A6")
    set2 = survey.get_responses("A6", True)
    assert len(set1) == len(set2)

    filt1 = filter_by_center(survey, set1, "A18")
    filt2 = filter_by_center(survey, set2, "A18")
    assert len(filt1) == len(filt2)
