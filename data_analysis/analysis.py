import pandas as pd
from data_import.data_import import LimeSurveyData

def get_data_for_q(
    survey: LimeSurveyData,
    question_number: str,
) -> pd.DataFrame:
    """
    returns a DataFrame with the responses to a specific question without any contingent answers

    Args:
        survey (LimeSurveyData): _description_
        question_number (str): _description_

    Returns:
        pd.DataFrame: _description_
    """    
    responses = survey.get_responses(question_number, drop_other=True)
    # change types of all columns to object
    responses = responses.astype("object")
    # make id column by resetting the index
    responses = responses.reset_index()
    # change id column to type string
    responses = responses.astype({'id': "string"})
    return responses