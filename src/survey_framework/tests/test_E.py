from pathlib import Path

import matplotlib.pyplot as plt

from survey_framework.data_analysis.analysis import get_data_for_q, get_data_for_single_barplot_comparison
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.plotting.barplots_sidebyside import plot_bar_side_by_side, plot_sidebyside_comparison_singleQ


def test_plots_E(survey: LimeSurveyData, output_path: Path) -> None:
    section = "E"
    # e5a = "E5a"
    # e6a = "E6a"
    # for 2024, question numbers changed.
    e5a = "E8"
    e6a = "E9"

    output = output_path / Path(section) / Path(e5a + "_" + e6a + ".pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    data_e5_all = get_data_for_q(survey, e5a)
    data_e6_all = get_data_for_q(survey, e6a)

    data_e5_all = data_e5_all.dropna()
    data_e6_all = data_e6_all.dropna()

    figure, axs = plot_bar_side_by_side(
        survey=survey,
        data_left=data_e5_all,
        data_right=data_e6_all,
        y_left=e5a,
        y_right=e6a,
    )

    plt.savefig(output)


def test_plots_E8_E9_comparison_A6(survey: LimeSurveyData, output_path: Path) -> None:
    section = "E"
    e8 = "E8"
    e9 = "E9"
    a6 = "A6"

    output = output_path / Path(section) / Path(e8 + "_" + e9 + "_comparison_" + a6 + ".pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    N_left, df_left = get_data_for_single_barplot_comparison(survey, e8, a6)
    N_right, df_right = get_data_for_single_barplot_comparison(survey, e9, a6)

    figure, axs = plot_sidebyside_comparison_singleQ(survey, df_left, df_right, e8, e9, a6, N_left)

    plt.savefig(output)