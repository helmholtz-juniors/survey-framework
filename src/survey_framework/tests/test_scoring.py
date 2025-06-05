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
from survey_framework.plotting import helmholtzcolors
from survey_framework.plotting.helper_barplots import add_bar_labels, plot_barplot
from survey_framework.plotting.helper_plotenums import BarLabels, Orientation, PlotStat
from survey_framework.plotting.likertplot import plot_likertplot


def test_state_anxiety(survey: LimeSurveyData, output_path: Path) -> None:
    res_df = rate_mental_health(
        survey.get_responses(Condition.STATE_ANXIETY),
        Condition.STATE_ANXIETY,
        keep_subscores=True,
    )
    print(res_df["state_anxiety_class"].value_counts())


def test_trait_anxiety(survey: LimeSurveyData, output_path: Path) -> None:
    res_df = rate_mental_health(
        survey.get_responses(Condition.TRAIT_ANXIETY),
        Condition.TRAIT_ANXIETY,
        keep_subscores=True,
    )
    print(res_df["trait_anxiety_class"].value_counts())


def test_depression(survey: LimeSurveyData, output_path: Path) -> None:
    res_df = rate_mental_health(
        survey.get_responses(Condition.DEPRESSION),
        Condition.DEPRESSION,
        keep_subscores=True,
    )
    print(res_df["depression_class"].value_counts())


def test_somatic(survey: LimeSurveyData, output_path: Path) -> None:
    res_df = rate_somatic(survey.get_responses("D4"))
    print(res_df["somatic_class"].value_counts())


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
    # print(res_df.dropna())
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

    helmholtzcolors.set_plotstyle()
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300, layout="constrained")
    _ = sns.histplot(data=raw_df, ax=ax, kde=True, multiple="dodge")
    fig.savefig(output_path / SECTION / "D3d_raw.pdf")

    # shake this into the right data form to use our plot_barplot helper
    n = len(raw_df.dropna())
    sorting = {s: i for i, s in enumerate(Profile)}
    groups = (
        res_df.groupby("Profile")
        .count()["id"]
        .to_frame("count")
        .sort_index(key=lambda x: x.map(sorting))
        .reset_index()
    )
    groups["proportion"] = groups["count"].div(n)
    print(groups)

    fig, ax = plot_barplot(
        data_df=groups,
        question="Profile",
        orient=Orientation.VERTICAL,
        stat=PlotStat.PROPORTION,
        width=6,
        height=4,
    )

    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.yaxis.set_label_text("Percent")

    add_bar_labels(
        ax=ax,
        show_axes_labels=BarLabels.PERCENT,
        percentcount=PlotStat.PROPORTION,
        n_question=n,
    )

    fig.savefig(output_path / SECTION / "D3d_scores.pdf")


def test_satisfaction(survey: LimeSurveyData, output_path: Path) -> None:
    res_df = rate_satisfaction(survey.get_responses("C1"), calc_average=True)
    print(res_df)

    plotting_df = res_df[["C1_class"]]
    plotting_df = plotting_df.reset_index()

    result_fig, _ = plot_likertplot(
        survey,
        plotting_df,
        question="C1",
        order=[
            "A5",
            "A4",
            "A3",
            "A2",
            "A1",
        ],
        relabel_subquestions=False,
    )
    result_fig.savefig(output_path / "C" / "sat_likert.pdf", dpi=300)
