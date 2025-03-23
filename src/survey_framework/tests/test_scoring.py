from pathlib import Path

import matplotlib.pyplot as plt
import pytest
import seaborn as sns
from matplotlib.ticker import PercentFormatter

from survey_framework.data_analysis.scoring import (
    Condition,
    Profile,
    Scale,
    rate_burnout,
    rate_mental_health,
    rate_satisfaction,
    rate_somatic,
)
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.plotting.helper_barplots import plot_barplot
from survey_framework.plotting.helper_plotenums import Orientation, PercentCount


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


def test_somatic(survey: LimeSurveyData, output_path: Path) -> None:
    res_df = rate_somatic(survey.get_responses("D4"))
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


def test_burnout_invalid(survey: LimeSurveyData, output_path: Path) -> None:
    # conversion should fail when using the wrong questions as input
    with pytest.raises(ValueError):
        rate_burnout(survey.get_responses("D1"))
    with pytest.raises(ValueError):
        rate_burnout(survey.get_responses("D2"))
    with pytest.raises(ValueError):
        rate_burnout(survey.get_responses("D3"))

    with pytest.raises(TypeError):
        rate_burnout(survey.get_responses("D4"))


def test_burnout_plot(survey: LimeSurveyData, output_path: Path) -> None:
    SECTION = "D"

    res_df = rate_burnout(survey.get_responses("D3d"))
    raw_df = res_df[[Scale.EX, Scale.CY, Scale.PE]]

    fig, ax = plt.subplots(layout="constrained")
    _ = sns.kdeplot(data=raw_df, ax=ax)
    fig.savefig(output_path / SECTION / "D3d_raw.pdf")

    # shake this into the right data form to use our plot_barplot helper
    n = len(raw_df.dropna())
    sorting = {s: i for i, s in enumerate(Profile)}
    groups = (
        res_df.groupby("Profile")
        .count()["id"]
        .to_frame("Count")
        .sort_index(key=lambda x: x.map(sorting))
        .reset_index()
    )
    groups["Percent"] = groups["Count"].div(n)
    print(groups)

    fig, ax = plot_barplot(
        data_df=groups,
        question="Profile",
        orientation=Orientation.VERTICAL,
        percentcount=PercentCount.PERCENT,
        fig_size_x=16,
        fig_size_y=10,
    )
    ax.yaxis.set_major_formatter(PercentFormatter(1))

    fig.savefig(output_path / SECTION / "D3d_scores.pdf")


def test_satisfaction(survey: LimeSurveyData, output_path: Path) -> None:
    res_df = rate_satisfaction(survey.get_responses("C1"), calc_average=False)
    print(res_df)
