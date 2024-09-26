import pandas as pd

from ..data_import.data_import import LimeSurveyData


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
