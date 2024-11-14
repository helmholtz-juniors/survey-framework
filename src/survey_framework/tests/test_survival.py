from pathlib import Path

from survey_framework.data_analysis.analysis import get_as_numeric
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.plotting.survivalplot import plot_survival_plot

Q_FIELD = "A3"
Q_START = {"year": "A8", "month": "A8a"}
Q_END = {"year": "A9", "month": "A9a"}

# we collected the data in April / May 2024
SURVEY_YEAR = 2024
SURVEY_MONTH = 5


def test_survival(survey: LimeSurveyData, output_path: Path) -> None:
    # filter out "before 2015" / I don't know / IDWA
    startyear = get_as_numeric(survey, Q_START["year"], ["A8", "A9", "A13"])
    startmonth = get_as_numeric(survey, Q_START["month"], ["A13", "A14"])
    endyear = get_as_numeric(survey, Q_END["year"], ["A11", "A12", "A13", "A14", "A15"])
    endmonth = get_as_numeric(survey, Q_END["month"], ["A13", "A14", "A15"])

    # calculate phd year relative to survey time (0 means not yet started)
    phd_current_month = (
        startyear.rsub(SURVEY_YEAR)
        .mul(12)
        .add(
            startmonth.rsub(SURVEY_MONTH),
        )
        .dropna()
        .astype(int)
    )
    phd_current_year = phd_current_month.floordiv(12).add(1)
    phd_current_year.clip(0, 6, inplace=True)  # clamp after 6 years

    # calculate estimated total phd duration in months
    # if end month is missing, assume December
    phd_estimation_months = (
        endyear.sub(startyear)
        .mul(12)
        .add(
            endmonth.sub(startmonth, fill_value=12),
        )
    )

    # combine both Series into a DataFrame
    combined = phd_current_year.to_frame(name="phd_year")
    combined["data"] = phd_estimation_months

    fig, ax = plot_survival_plot(
        combined,
        category="phd_year",
        ticks=range(0, 144, 24),
        tick_map=lambda x: str(x // 12),
        legend_replace={"0": "not started", "6": "6+"},
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

    # filter out "before 2015" / I don't know / IDWA
    startyear = get_as_numeric(survey, Q_START["year"], ["A8", "A9", "A13"])
    startmonth = get_as_numeric(survey, Q_START["month"], ["A13", "A14"])
    endyear = get_as_numeric(survey, Q_END["year"], ["A11", "A12", "A13", "A14", "A15"])
    endmonth = get_as_numeric(survey, Q_END["month"], ["A13", "A14", "A15"])

    # calculate estimated total phd duration in months
    # if end month is missing, assume December
    phd_estimation_months = (
        endyear.sub(startyear)
        .mul(12)
        .add(
            endmonth.sub(startmonth, fill_value=12),
        )
    )

    # add data column
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
