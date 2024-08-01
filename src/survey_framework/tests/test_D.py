from pathlib import Path

import matplotlib.pyplot as plt

from survey_framework.data_analysis.analysis import get_data_for_q
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.plotting.likertplot import plot_likertplot


def test_plots_D(survey: LimeSurveyData, output_path: Path) -> None:
    section = "D"
    d4 = "D4"

    output = output_path / Path(section) / Path(d4 + ".pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    data_d4_all = get_data_for_q(survey, d4)
    # every column in this DF should be a grouped bar in the Likert plot

    fig, ax = plot_likertplot(
        survey=survey,
        question=d4,
        data_df=data_d4_all,
        order=["A2", "A3", "A4"],
    )

    plt.savefig(output)
