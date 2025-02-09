from collections.abc import Callable, Mapping
from pathlib import Path

import matplotlib.pyplot as plt

from survey_framework.data_analysis.helpers import shorten_center_name
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.plotting.helmholtzcolors import (
    helmholtzblue,
    helmholtzgreen,
    set_plotstyle,
)

### important files and paths
# path to the survey
INPUT_PATH = Path("../data/survey_2021/")
# file name of survey structure, has ending '.xml'
XML_FILE_NAME = "Survey2021_structure.xml"
# file name of survey, has ending '.csv'
CSV_FILE_NAME = "Survey2021_Qcode_Acode.csv"


def test_nation_distribution(survey: LimeSurveyData, output_path: Path) -> None:
    NATION_Q = "A11"

    nation_map = {
        "Citizen outside the European Union (EU)": "Non-EU",
        "Citizen outside the European Union": "Non-EU",
        "Citizen within the European Union (EU)": "EU",
        "Citizen within the European Union (But not German)": "EU",
        "German": "German",
    }

    plot_comparison_2021(
        survey_2024=survey,
        survey_2021=open_survey_2021(),
        output_plot=output_path / "survey2021-nations.pdf",
        q_code=NATION_Q,
        label="Nationality",
        answer_map=nation_map,
    )


def test_gender_distribution(survey: LimeSurveyData, output_path: Path) -> None:
    GENDER_Q = "A6"

    gender_map = {
        "Man": "Male",
        "Woman": "Female",
        "Gender diverse": "Diverse",
        "Gender diverse (Gender-fluid)": "Diverse",
        "Non-binary": "Diverse",
        "Other": "Diverse",
        "Other gender representations:": "Diverse",
        "I don't know": "Diverse",  # is this correct? or should we drop instead?
        # "I don't want to answer this question"
    }

    plot_comparison_2021(
        survey_2024=survey,
        survey_2021=open_survey_2021(),
        output_plot=output_path / "survey2021-genders.pdf",
        q_code=GENDER_Q,
        label="Gender",
        answer_map=gender_map,
    )


def test_center_distribution(survey: LimeSurveyData, output_path: Path) -> None:
    CENTER_Q = "A2"

    plot_comparison_2021(
        survey_2024=survey,
        survey_2021=open_survey_2021(),
        output_plot=output_path / "survey2021-centers.pdf",
        q_code=CENTER_Q,
        label="Center",
        answer_map=shorten_center_name,
    )


def plot_comparison_2021(
    survey_2024: LimeSurveyData,
    survey_2021: LimeSurveyData,
    output_plot: Path,
    q_code: str,
    label: str,
    answer_map: Mapping[str, str] | Callable[[str], str | None],
) -> None:
    """Create a comparison plot between 2021 and 2024 data.
    This presumes that the question code is the same for both years.

    Args:
        survey_2024: 2024 survey data object
        survey_2021: 2021 survey data object
        output_plot: Path to store the plot
        q_code: The alphanumeric question code
        label: x-axis label for the data in question
        answer_map: mapping to unify answer options (applied to both data sets)
    """
    choices_2024 = survey_2024.get_choices(q_code)
    choices_2021 = survey_2021.get_choices(q_code)

    # map answer codes to actual answers, convert them into a common format, count
    answers_2021 = (
        survey_2021.get_responses(q_code)[q_code].map(choices_2021).map(answer_map)  # type:ignore[arg-type]
    )
    counts_2021 = answers_2021.value_counts()
    answers_2024 = (
        survey_2024.get_responses(q_code)[q_code].map(choices_2024).map(answer_map)  # type:ignore[arg-type]
    )
    counts_2024 = answers_2024.value_counts()

    combined = counts_2021.to_frame("2021")
    combined["2024"] = counts_2024

    set_plotstyle()
    fig, ax = plt.subplots(layout="constrained")
    ax = combined.plot.bar(ax=ax, color=[helmholtzblue, helmholtzgreen])
    ax.set_xlabel(label)
    fig.savefig(output_plot)


def open_survey_2021() -> LimeSurveyData:
    return LimeSurveyData(INPUT_PATH / XML_FILE_NAME, INPUT_PATH / CSV_FILE_NAME)
