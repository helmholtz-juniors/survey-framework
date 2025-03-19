from pathlib import Path

import pandas as pd

from survey_framework.data_analysis.scoring import (
    Condition,
    rate_burnout,
    rate_mental_health,
    rate_satisfaction,
    rate_somatic,
)
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.plotting.heatmap import plot_heatmap


def test_heatmap(survey: LimeSurveyData, output_path: Path) -> None:
    SECTION = "C"
    SATISFACTION = "C1"

    # satisfaction scores
    sat = rate_satisfaction(
        survey.get_responses(SATISFACTION), calc_average=False
    ).rename(mapper=lambda label: "_".join(label.split("_")[0:2]), axis=1)
    sat_choices = survey.get_question(SATISFACTION)["label"].to_dict()
    sat.rename(sat_choices, axis=1, inplace=True)

    figure, _ = plot_heatmap(sat, survey)

    (output_path / SECTION).mkdir(exist_ok=True)
    figure.savefig(output_path / SECTION / "satisfaction_heatmap.pdf")


def test_heatmap_crossover(survey: LimeSurveyData, output_path: Path) -> None:
    SOMATIC = "D4"
    BURNOUT = "D3d"
    SECTION = "D"

    # health scores (copied from plot_heatmap)
    sta = rate_mental_health(
        survey.get_responses(Condition.STATE_ANXIETY), Condition.STATE_ANXIETY
    ).drop("state_anxiety_class", axis=1)
    tra = rate_mental_health(
        survey.get_responses(Condition.TRAIT_ANXIETY), Condition.TRAIT_ANXIETY
    ).drop("trait_anxiety_class", axis=1)
    depr = rate_mental_health(
        survey.get_responses(Condition.DEPRESSION), Condition.DEPRESSION
    ).drop("depression_class", axis=1)
    somatic = rate_somatic(survey.get_responses(SOMATIC)).drop("somatic_class", axis=1)
    bout = (
        rate_burnout(survey.get_responses(BURNOUT))
        .set_index("id")
        .drop(["Profile", "EX_critical", "CY_critical", "PE_critical"], axis=1)
    )

    health = pd.concat([sta, tra, depr, somatic, bout], axis=1)
    health.rename(
        {
            "state_anxiety_score": "State Anxiety",
            "trait_anxiety_score": "Trait Anxiety",
            "depression_score": "Depression",
            "somatic_score": "Somatic Symptoms",
        },
        axis=1,
        inplace=True,
    )

    figure, _ = plot_heatmap(health, survey)

    (output_path / SECTION).mkdir(exist_ok=True)
    figure.savefig(output_path / SECTION / "health_heatmap.pdf")
