from pathlib import Path

import pytest

from survey_framework.data_analysis.scoring import (
    Condition,
    rate_burnout,
    rate_mental_health,
)
from survey_framework.data_import.data_import import LimeSurveyData


def test_state_anxiety(survey: LimeSurveyData, output_path: Path) -> None:
    res_df = rate_mental_health(
        survey.get_responses(Condition.STATE_ANXIETY),
        Condition.STATE_ANXIETY,
        keep_subscores=True,
    )
    print(res_df)


def test_trait_anxiety(survey: LimeSurveyData, output_path: Path) -> None:
    res_df = rate_mental_health(
        survey.get_responses(Condition.TRAIT_ANXIETY),
        Condition.TRAIT_ANXIETY,
        keep_subscores=True,
    )
    print(res_df)


def test_depression(survey: LimeSurveyData, output_path: Path) -> None:
    res_df = rate_mental_health(
        survey.get_responses(Condition.DEPRESSION),
        Condition.DEPRESSION,
        keep_subscores=True,
    )
    print(res_df)


def test_invalid_length(survey: LimeSurveyData, output_path: Path) -> None:
    with pytest.raises(ValueError):
        rate_mental_health(
            survey.get_responses(Condition.TRAIT_ANXIETY), Condition.STATE_ANXIETY
        )


def test_invalid_question(survey: LimeSurveyData, output_path: Path) -> None:
    with pytest.raises(ValueError):
        rate_mental_health(
            survey.get_responses(Condition.TRAIT_ANXIETY), Condition.DEPRESSION
        )


def test_burnout(survey: LimeSurveyData, output_path: Path) -> None:
    res_df = rate_burnout(survey.get_responses("D3d"))
    print(res_df)
