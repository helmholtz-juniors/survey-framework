import pandas as pd
from data_import.data_import import LimeSurveyData
from plotting.barplots import plot_bar, plot_bar_comparison
from pathlib import Path
from data_analysis.analysis import get_data_for_q
from order.order2021 import order_A2, order_A6, order_A10

import matplotlib.pyplot as plt

from plotting.helper_plotenums import Orientation, PercentCount, ShowAxesLabel


sectionA = "A"
a1 = "A1"  # participation in last N2 survey
a2 = "A2"  # institute/section/center association
a3 = "A3"  # field of work (subject)
a4 = "A4"  # type of work
a5 = "A5"  # year of birth
a6 = "A6"  # gender representation
a7 = "A7"  # sexual orientation
a8a = "A8a"  # start of PhD - month
a8b = "A8b"  # start of PhD - year
a9a = "A9a"  # expected submission date PhD - month
a9b = "A9b"  # expected submission date PhD - year
a10 = "A10"  # ethnicity
a11 = "A11"  # citizenship
a12a = "A12a"  # parents born in Germany
a12b = "A12b"  # participant born in Gerany
a13 = "A13"  # disability present
a14 = "A14"  # longtext feedback to section


def test_plots_A2_single(survey: LimeSurveyData, output_path: Path) -> None:
    output = output_path / Path(sectionA)
    output.mkdir(exist_ok=True)
    output = output / Path(a2 + ".pdf")

    N_question = survey.responses[a2].count()
    data_q_all = get_data_for_q(survey, a2)
    data_q_all_dropna = data_q_all.dropna()
    data_q_counts = (
        data_q_all_dropna.groupby([a2]).count().rename(columns={"id": "count"})
    )

    data_q_counts_sorted = data_q_counts.reset_index()
    data_q_counts_sorted[a2] = pd.Categorical(
        data_q_counts_sorted[a2], categories=order_A2, ordered=True
    )
    data_q_counts_sorted = data_q_counts_sorted.sort_values(by=a2)

    data_q_counts_sorted_percentages = data_q_counts_sorted
    data_q_counts_sorted_percentages["percentages"] = (
        data_q_counts_sorted_percentages["count"] / N_question * 100
    )

    fig, ax = plot_bar(
        survey=survey,
        data_df=data_q_counts_sorted_percentages,
        question=a2,
        n_question=N_question,
        label_q_data="Centers",
        orientation=Orientation.VERTICAL,
        show_axes_labels=ShowAxesLabel.NONE,
    )

    plt.savefig(output)


def test_plots_A10_multiple(survey: LimeSurveyData, output_path: Path) -> None:
    output = output_path / Path(sectionA)
    output.mkdir(exist_ok=True)
    output = output / Path(a10 + ".pdf")

    data_q_all = get_data_for_q(survey, a10)
    N_question = len(data_q_all.index)

    responses_df_all = survey.get_responses(a10, drop_other=True)
    responses_df_melted = pd.melt(responses_df_all)
    responses_df_melted_cleaned = responses_df_melted[responses_df_melted.value]
    responses_df_melted_cleaned_counts = (
        responses_df_melted_cleaned.groupby("name")
        .count()
        .rename(columns={"id": "count"})
    )
    responses_df_counts_sorted = responses_df_melted_cleaned_counts.reset_index()
    responses_df_counts_sorted["name"] = pd.Categorical(
        responses_df_counts_sorted["name"], categories=order_A10, ordered=True
    )
    responses_df_counts_sorted = responses_df_counts_sorted.sort_values(
        by="name"
    ).rename(columns={"value": "count", "name": a10})
    responses_df_counts_sorted_percentages = responses_df_counts_sorted
    responses_df_counts_sorted_percentages["percentages"] = (
        responses_df_counts_sorted_percentages["count"] / N_question * 100
    )

    fig, ax = plot_bar(
        survey=survey,
        data_df=responses_df_counts_sorted_percentages,
        question=a10,
        n_question=N_question,
        label_q_data="Ethnicity",
        percentcount=PercentCount.COUNT,
        orientation=Orientation.VERTICAL,
        show_axes_labels=ShowAxesLabel.PERCENT,
    )

    plt.savefig(output)


def test_plots_A2_comparison_A6(survey: LimeSurveyData, output_path: Path) -> None:
    output = output_path / Path(sectionA)
    output.mkdir(exist_ok=True)
    output = output / Path(a2 + "_" + a6 + ".pdf")

    responses_df_all = survey.get_responses(a2, drop_other=True)
    responses_df_comparison = survey.get_responses(a6, drop_other=True)
    N_question = len(responses_df_all.index)

    responses_df_all_concat = pd.concat(
        [responses_df_comparison.transpose(), responses_df_all.transpose()]
    ).transpose()

    responses_df_counts = (
        responses_df_all_concat[[a2, a6]].value_counts().reset_index(name="count")
    )

    responses_df_counts[a2] = pd.Categorical(
        responses_df_counts[a2], categories=order_A2, ordered=True
    )
    responses_df_counts[a6] = pd.Categorical(
        responses_df_counts[a6], categories=order_A6, ordered=True
    )
    responses_df_counts_sorted = responses_df_counts.sort_values(by=[a2, a6])

    responses_df_counts_sorted_precentages = responses_df_counts_sorted
    responses_df_counts_sorted_precentages["percentages"] = (
        responses_df_counts_sorted_precentages["count"] / N_question * 100
    )

    fig, ax = plot_bar_comparison(
        survey=survey,
        data_df=responses_df_counts_sorted_precentages,
        question=a2,
        question_comparison=a6,
        n_question=N_question,
        label_q_data="Centers",
        orientation=Orientation.HORIZONTAL,
        percentcount=PercentCount.COUNT,
        show_axes_labels=ShowAxesLabel.COUNT,
        fontsize_axes_labels=5,
    )

    plt.savefig(output)


def test_A(survey: LimeSurveyData, output_path: Path) -> None:
    # test_plots_A2_single(survey, output_path)

    test_plots_A10_multiple(survey, output_path)

    # test_plots_A2_comparison_A6(survey, output_path)
