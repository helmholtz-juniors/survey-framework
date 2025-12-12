from pathlib import Path

from survey_framework.data_analysis.analysis import get_phd_duration
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.plotting.survivalplot import plot_survival_plot

Q_FIELD = "A3"


def test_survival(survey: LimeSurveyData, output_path: Path) -> None:
    phd_current_year, phd_estimation_months = get_phd_duration(survey)

    # combine both Series into a DataFrame
    combined = phd_current_year.to_frame(name="phd_year")
    combined["data"] = phd_estimation_months

    fig, ax = plot_survival_plot(
        combined,
        category="phd_year",
        ticks=range(0, 144, 24),
        tick_map=lambda x: str(x // 12),
        legend_replace={"6": "6+"},
        legend_title="Year of PhD",
    )

    ax.set_xlabel("Estimated PhD Completion Time [a]")
    ax.set_ylabel("Proportion of DRs Not Finished [%]")

    output = output_path / "A" / "survival.pdf"
    fig.savefig(output)


def test_survival_by_field(survey: LimeSurveyData, output_path: Path) -> None:
    # filter by dropping categories (important so they don't show up later)
    fields = survey.get_responses(Q_FIELD, drop_other=True)
    fields[Q_FIELD] = fields[Q_FIELD].cat.remove_categories(["A10", "-oth-"])
    filtered = fields.dropna()

    choices = survey.get_choices(Q_FIELD)
    mapped = filtered.map(lambda a_code: choices[a_code])

    # add data column
    _, phd_estimation_months = get_phd_duration(survey)
    mapped["data"] = phd_estimation_months

    fig, ax = plot_survival_plot(
        mapped,
        category="A3",
        ticks=range(0, 144, 24),
        tick_map=lambda x: str(x // 12),
        legend_title="Field of Research",
    )

    ax.set_xlabel("Estimated PhD Completion Time [a]")
    ax.set_ylabel("Proportion of DRs Not Finished [%]")

    output = output_path / "A" / "survival_by_field.pdf"
    fig.savefig(output)
