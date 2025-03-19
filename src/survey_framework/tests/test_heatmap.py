from pathlib import Path

from survey_framework.data_analysis.scoring import (
    rate_satisfaction,
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
