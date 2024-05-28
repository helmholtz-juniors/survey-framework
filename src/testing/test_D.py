from pathlib import Path

import matplotlib.pyplot as plt
from data_analysis.analysis import get_data_for_q
from data_import.data_import import LimeSurveyData

# from plotting.helper_plotenums import BarLabels
from plotting.likertplot import plot_likertplot


def test_plots_D(survey: LimeSurveyData, output_path: Path) -> None:
    section = "D"
    d4 = "D4"

    output = output_path / Path(section) / Path(d4 + ".pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    data_d4_all = get_data_for_q(survey, d4)

    print(data_d4_all)
    # every column in this DF should be a grouped bar in the Likert plot

    fig, ax = plot_likertplot(
        survey=survey,
        question=d4,
        data_df=data_d4_all,
        order=["A2", "A3", "A4"],
        drop=["A5", "A6"],
    )

    plt.savefig(output)


def test_D(survey: LimeSurveyData, output_path: Path) -> None:
    test_plots_D(survey, output_path)

    # get all array questions (Likert plot candidates)
    # for q, _ in survey.questions.iterrows():
    #     if survey.get_question_type(q) == "array":
    #         print(q)
