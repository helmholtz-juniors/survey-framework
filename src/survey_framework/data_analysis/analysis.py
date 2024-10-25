import pandas as pd
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.order.order2024 import ORDER


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
    # A2 is the "center" question
    CQ = "A2"

    # get IDs for the given center, then filter by the IDs
    centers = get_data_for_q(survey, CQ).filter([CQ])
    center_students = centers[centers[CQ] == center_code]
    filtered = responses[responses.index.isin(center_students.index)]

    return filtered


def get_data_for_single_barplot_comparison(
    survey: LimeSurveyData, base_q: str, comp_q: str
) -> pd.DataFrame:
    responses_df_all = survey.get_responses(base_q, drop_other=True)
    responses_df_comparison = survey.get_responses(comp_q, drop_other=True)
    N_question = len(responses_df_all.index)

    responses_df_all_concat = pd.concat(
        [responses_df_comparison.transpose(), responses_df_all.transpose()]
    ).transpose()

    responses_df_counts = (
        responses_df_all_concat[[base_q, comp_q]]
        .value_counts()
        .reset_index(name="count")
    )

    responses_df_counts[base_q] = pd.Categorical(
        responses_df_counts[base_q], categories=ORDER[base_q], ordered=True
    )
    responses_df_counts[comp_q] = pd.Categorical(
        responses_df_counts[comp_q], categories=ORDER[comp_q], ordered=True
    )
    responses_df_counts_sorted = responses_df_counts.sort_values(by=[base_q, comp_q])

    responses_df_counts_sorted_precentages = responses_df_counts_sorted
    responses_df_counts_sorted_precentages["percentages"] = (
        responses_df_counts_sorted_precentages["count"] / N_question * 100
    )

    return N_question, responses_df_counts_sorted_precentages
