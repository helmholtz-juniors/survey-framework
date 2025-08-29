from pathlib import Path

from survey_framework.data_analysis.analysis import get_phd_duration
from survey_framework.data_analysis.scoring import Condition, rate_mental_health
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.plotting.likertplot import plot_likertplot
from survey_framework.plotting.stacked import (
    plot_stacked_bar_categorical,
    plot_stacked_bar_single,
)


def test_likert(survey: LimeSurveyData, output_path: Path) -> None:
    section = "D"
    d4 = "D4"

    output = output_path / Path(section) / Path(d4 + ".pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    data_d4_all = survey.get_responses(d4)
    # every column in this DF should be a grouped bar in the Likert plot

    fig, _ = plot_likertplot(
        survey=survey,
        question=d4,
        data_df=data_d4_all,
        order=["A2", "A3", "A4"],
    )

    fig.savefig(output)


# TA plot
def test_stacked_bars_single(survey: LimeSurveyData, output_path: Path) -> None:
    output = output_path / "D" / "TA_plot.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)

    scoring_df = rate_mental_health(
        responses=survey.get_responses("D2"), condition=Condition.TRAIT_ANXIETY
    )

    TA_classes = scoring_df.iloc[:, 1]
    TA_classes = (TA_classes.cat.add_categories(["NA"])).fillna("NA")

    fig, _ = plot_stacked_bar_single(
        df1=TA_classes.to_frame("class"),
        col_of_interest="class",
        order=["NA", "no or low anxiety", "moderate anxiety", "high anxiety"],
        plot_title="",
        width=2.2,
        legend_loc="bottom",
        n_y_pos=1.02,
    )
    fig.savefig(output)


# PhD Year stratified TA Plot
def test_stacked_bars(survey: LimeSurveyData, output_path: Path) -> None:
    output = output_path / "D" / "TA_plot_PhDYears_stratified.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)

    scoring_df = rate_mental_health(
        responses=survey.get_responses("D2"), condition=Condition.TRAIT_ANXIETY
    )

    years = get_phd_duration(survey)[0].clip(1, 4)
    scoring_df = scoring_df.join(years.to_frame("Year"), how="inner")
    scoring_df["trait_anxiety_class"] = (
        scoring_df["trait_anxiety_class"].cat.add_categories(["NA"]).fillna("NA")
    )

    fig, _ = plot_stacked_bar_categorical(
        df=scoring_df,
        classes_column="trait_anxiety_class",
        category_column="Year",
        category_order=["NA", "no or low anxiety", "moderate anxiety", "high anxiety"],
        label_q_data="Year of PhD",
        na_values=True,
        legend_title="TA category",
    )

    fig.savefig(output)
