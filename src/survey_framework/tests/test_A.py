from pathlib import Path

import pandas as pd

from survey_framework.data_analysis.analysis import get_data_for_q
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.order.order2024 import ORDER
from survey_framework.plotting.barplots import plot_bar, plot_bar_comparison
from survey_framework.plotting.helper_plotenums import (
    BarLabels,
    Orientation,
    PlotStat,
)

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
    output = output_path / sectionA
    output.mkdir(exist_ok=True, parents=True)
    output = output / Path(a2 + ".pdf")

    N_question = survey.responses[a2].count()
    data_q_all = get_data_for_q(survey, a2)
    # data_q_all_dropna = data_q_all.dropna()
    data_q_counts = data_q_all.groupby([a2]).count().rename(columns={"id": "count"})

    # TODO: ordering helper
    data_q_counts_sorted = data_q_counts.reset_index()
    data_q_counts_sorted[a2] = pd.Categorical(
        data_q_counts_sorted[a2], categories=ORDER["A2"], ordered=True
    )
    data_q_counts_sorted = data_q_counts_sorted.sort_values(by=a2)

    data_q_counts_sorted_percentages = data_q_counts_sorted
    data_q_counts_sorted_percentages["percent"] = (
        data_q_counts_sorted_percentages["count"] / N_question * 100
    )

    fig, _ = plot_bar(
        survey=survey,
        data_df=data_q_counts_sorted_percentages,
        question=a2,
        n_question=N_question,
        label_q_data="Centers",
        orientation=Orientation.VERTICAL,
        show_axes_labels=BarLabels.NONE,
    )

    fig.savefig(output)


def test_plots_A10_multiple(survey: LimeSurveyData, output_path: Path) -> None:
    output = output_path / sectionA
    output.mkdir(exist_ok=True, parents=True)
    output = output / Path(a10 + ".pdf")

    data_q_all = get_data_for_q(survey, a10)
    N_question = len(data_q_all.index)

    responses_df_all = survey.get_responses(a10, drop_other=True)
    responses_df_melted = pd.melt(responses_df_all)
    responses_df_melted_cleaned = responses_df_melted[responses_df_melted.value]
    responses_df_melted_cleaned_counts = responses_df_melted_cleaned.groupby(
        "name"
    ).count()
    responses_df_counts_sorted = responses_df_melted_cleaned_counts.reset_index()
    # responses_df_counts_sorted["name"] = pd.Categorical(
    #     responses_df_counts_sorted["name"], categories=order_a10, ordered=True
    # )
    responses_df_counts_sorted = responses_df_counts_sorted.sort_values(
        by="value", ascending=False
    ).rename(columns={"value": "count", "name": a10})
    responses_df_counts_sorted_percentages = responses_df_counts_sorted
    responses_df_counts_sorted_percentages["percent"] = (
        responses_df_counts_sorted_percentages["count"] / N_question * 100
    )

    fig, _ = plot_bar(
        survey=survey,
        data_df=responses_df_counts_sorted_percentages,
        question=a10,
        n_question=N_question,
        label_q_data="Ethnicity",
        percentcount=PlotStat.COUNT,
        orientation=Orientation.VERTICAL,
        show_axes_labels=BarLabels.PERCENT,
    )

    fig.savefig(output)


def test_plots_A2_comparison_A6(survey: LimeSurveyData, output_path: Path) -> None:
    output = output_path / sectionA
    output.mkdir(exist_ok=True, parents=True)
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
        responses_df_counts[a2], categories=ORDER[a2], ordered=True
    )
    responses_df_counts[a6] = pd.Categorical(
        responses_df_counts[a6], categories=ORDER[a6], ordered=True
    )
    responses_df_counts_sorted = responses_df_counts.sort_values(by=[a2, a6])

    responses_df_counts_sorted_precentages = responses_df_counts_sorted
    responses_df_counts_sorted_precentages["percent"] = (
        responses_df_counts_sorted_precentages["count"] / N_question * 100
    )

    fig, _ = plot_bar_comparison(
        survey=survey,
        data_df=responses_df_counts_sorted_precentages,
        question=a2,
        question_comparison=a6,
        label_q_data="Centers",
        orientation=Orientation.HORIZONTAL,
        percentcount=PlotStat.COUNT,
        show_axes_labels=BarLabels.COUNT,
        n_question=N_question,
        height=10,
        width=16,
    )

    fig.savefig(output)
