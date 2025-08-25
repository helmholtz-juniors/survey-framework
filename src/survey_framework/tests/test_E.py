from pathlib import Path

from survey_framework.data_analysis.analysis import get_data_for_q
from survey_framework.data_analysis.count_responses import prepare_df_comparison
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.order.order2024 import ORDER
from survey_framework.plotting.barplots_sidebyside import (
    plot_bar_side_by_side,
    plot_sidebyside_comparison_singleQ,
)


# test side-by-side bar plots
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

    fig, _ = plot_bar_side_by_side(
        survey=survey,
        data_left=data_e5_all,
        data_right=data_e6_all,
        y_left=e5a,
        y_right=e6a,
    )

    fig.savefig(output)


# test "comparison" side-by-side bar plots
# (i.e., side-by-side with hue for a different question)
def test_plots_E8_E9_comparison_A6(survey: LimeSurveyData, output_path: Path) -> None:
    section = "E"
    e8 = survey.get_responses("E8")
    e9 = survey.get_responses("E9")
    a6 = survey.get_responses("A6")["A6"]

    output = output_path / section / "E8_E9_comparison_A6.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)

    df_left, N_left = prepare_df_comparison(e8, a6, "E8", "A6", ORDER)
    df_right, N_right = prepare_df_comparison(e9, a6, "E9", "A6", ORDER)

    fig, _ = plot_sidebyside_comparison_singleQ(
        survey=survey,
        data_left=df_left,
        data_right=df_right,
        base_q_left="E8",
        base_q_right="E9",
        comp_q="A6",
        N_left=sum(N_left.values()),
        N_right=sum(N_right.values()),
    )

    fig.savefig(output)
