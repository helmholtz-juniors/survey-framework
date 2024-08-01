from typing import List, Optional

from survey_framework.data_import.data_import import LimeSurveyData


def order_alphabetical(
    survey: LimeSurveyData, question: str, append_last: Optional[List[str]] = None
) -> List[str]:
    """
    Infer an alphabetical answer order for the given question.
    Unwanted options can be moved to the end by adding them to `append_last`.
    """

    choices = list(
        map(
            lambda item: item[0],
            sorted(survey.get_choices(question).items(), key=lambda item: item[1]),
        )
    )

    if append_last:
        choices = [c for c in choices if c not in append_last]
        choices.extend(append_last)

    return choices


# ToDo: order by value (asc / desc)
