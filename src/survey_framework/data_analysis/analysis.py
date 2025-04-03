from collections.abc import Sequence
from typing import cast

import pandas as pd

from survey_framework.data_analysis.helpers import shorten_center_name
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.order.order2024 import ORDER

# A2 is the "center" question
CENTER = "A2"


def get_data_for_q(survey: LimeSurveyData, question_number: str) -> pd.DataFrame:
    """
    Returns a DataFrame with the responses to a specific question
    without any contingent answers.

    Args:
        survey: The LimeSurvey object
        question_number: The question ID (like 'A1')

    Returns:
        A DataFrame with all answers to the specified question
    """
    responses = survey.get_responses(question_number, drop_other=True)
    # change types of all columns to object
    responses = responses.astype("object")
    # make id column by resetting the index
    responses = responses.reset_index()
    # change id column to type string
    responses = responses.astype({"id": "string"})
    return responses


def filter_by_center(
    survey: LimeSurveyData, responses: pd.DataFrame, center_code: str
) -> pd.DataFrame:
    """
    Filter responses by center.

    Args:
        survey: The survey object
        responses: DataFrame with responses
        center_code: ID of the center to filter by (like 'A01')

    Returns:
        Filtered DataFrame
    """
    # get IDs for the given center, then filter by the IDs
    centers = survey.get_responses(CENTER)
    center_students = centers[centers[CENTER] == center_code]
    if "id" in responses.columns:
        filtered = responses.loc[
            responses["id"].astype(int).isin(center_students.index)
        ]
    else:
        filtered = responses[responses.index.isin(center_students.index)]

    assert len(filtered) == len(center_students)
    return filtered


def get_center_series(
    survey: LimeSurveyData, center_code: str
) -> tuple["pd.Series[str]", Sequence[str]]:
    """Get a series that contains the center name for every participant, with
    all centers other than the target `center_code` replaced by "Other Centers".
    The output of this function can be nicely used with the histogram plot.

    Args:
        survey: The survey object
        center_code: ID of the center to filter by (like 'A01')

    Returns:
        Tuple of the Series and a 2-element list for center ordering.
    """
    center_name = shorten_center_name(survey.get_choices(CENTER)[center_code])
    assert center_name is not None

    # get the center question data, replace all "other" centers
    centers = survey.get_responses(CENTER)[CENTER].astype(str).rename("Center")
    centers.loc[~centers.isin([center_code])] = "Other Centers"
    centers.loc[centers.isin([center_code])] = center_name

    return centers, [center_name, "Other Centers"]


def get_as_numeric(
    survey: LimeSurveyData, q_code: str, blocklist: list[str]
) -> "pd.Series[float]":
    """Get numeric answers for the requested question code.
    Raises if non-numeric answer codes are not in the given blocklist.

    Args:
        survey: The survey object
        center_code: ID of the center to filter by (like 'A01')
        blocklist: Answer codes to be excluded from the result

    Returns:
        Numeric Series
    """
    answers = survey.get_responses(q_code)
    filtered = answers.loc[~answers[q_code].isin(blocklist)]

    choices = survey.get_choices(q_code)
    mapped = filtered.map(lambda a_code: choices[a_code])
    numeric = cast("pd.Series[float]", mapped.apply(pd.to_numeric).squeeze())
    return numeric


def get_phd_duration(
    survey: LimeSurveyData,
) -> tuple["pd.Series[int]", "pd.Series[int]"]:
    """Calculate relevant numbers from questions A8 and A9, namely:
        * How long has the participant been a doctoral researcher [years]?
        * How long do they estimate their project to last _in total_ [months]?

    Args:
        survey (LimeSurveyData): The survey object

    Returns:
        tuple[pd.Series[int], pd.Series[int]]: Tuple of current year and estimation.
    """

    Q_START = {"year": "A8", "month": "A8a"}
    Q_END = {"year": "A9", "month": "A9a"}

    # we collected the data in April / May 2024
    SURVEY_YEAR = 2024
    SURVEY_MONTH = 5

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
    phd_current_year = phd_current_year[phd_current_year != 0]  # remove year 0

    # calculate estimated total phd duration in months
    # if end month is missing, assume December
    phd_estimation_months = (
        endyear.sub(startyear)
        .mul(12)
        .add(
            endmonth.sub(startmonth, fill_value=12),
        )
    )

    return (phd_current_year, phd_estimation_months)


# TODO: There is a duplicate of this currently in the center specific report.
#       This could also use some refactoring and documentation for readability.
def get_data_for_single_barplot_comparison(
    survey: LimeSurveyData, base_q: str, comp_q: str
) -> tuple[int, pd.DataFrame]:
    responses_df_all = survey.get_responses(base_q, drop_other=True)
    responses_df_comparison = survey.get_responses(comp_q, drop_other=True)
    N_question = len(responses_df_all.index)

    responses_df_all_concat = pd.concat(
        [responses_df_comparison, responses_df_all], axis=1
    )

    responses_df_counts = (
        responses_df_all_concat[[base_q, comp_q]]
        .value_counts()
        .reset_index(name="Count")
    )

    responses_df_counts[base_q] = pd.Categorical(
        responses_df_counts[base_q], categories=ORDER[base_q], ordered=True
    )
    responses_df_counts[comp_q] = pd.Categorical(
        responses_df_counts[comp_q], categories=ORDER[comp_q], ordered=True
    )
    responses_df_counts_sorted = responses_df_counts.sort_values(by=[base_q, comp_q])

    responses_df_counts_sorted_precentages = responses_df_counts_sorted
    responses_df_counts_sorted_precentages["Percent"] = (
        responses_df_counts_sorted_precentages["Count"] / N_question
    )

    return N_question, responses_df_counts_sorted_precentages
