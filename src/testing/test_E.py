# import pandas as pd
from pathlib import Path

# from order.order2021 import *
import matplotlib.pyplot as plt
from data_analysis.analysis import get_data_for_q
from data_import.data_import import LimeSurveyData

# from plotting.barplots import plot_bar
from plotting.barplots_sidebyside import plot_bar_side_by_side


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

    figure, axis = plot_bar_side_by_side(
        survey=survey,
        data_left=data_e5_all,
        data_right=data_e6_all,
        y_left=e5a,
        y_right=e6a,
    )

    plt.savefig(output)


def test_E(survey: LimeSurveyData, output_path: Path) -> None:
    test_plots_E(survey, output_path)

    # get all multiple choice questions
    # for q, _ in survey.questions.iterrows():
    #     if survey.get_question_type(q) == "multiple-choice":
    #         print(q)
