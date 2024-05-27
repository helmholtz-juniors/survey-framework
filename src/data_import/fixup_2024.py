from typing import cast

from bs4.element import Tag

from .types import QuestionTypeAlias, ResponseTypeAlias


def count_responses(responses: list[ResponseTypeAlias]) -> int:
    """
    Get the number of responses, reduced by one for question A2.

    The reason for this hack is that question A2 is falsely detected as a
    multiple choice question because it has multiple responses and choices.
    In fact, the second response is an optional comment field.
    """

    if len(responses) == 2 and responses[0][0]["name"] == "A2":
        return 1

    else:
        return len(responses)


def name_response(response: Tag) -> str:
    """
    There is one question where responses do not have a varName (B4).
    B4 consists of ten subquestions, with each having two dimensions:
    kind of contract (B4_SQ0xx_1) and contract duration (B4_SQ0xx_2).

    We first tag the response here, and later rename the question.
    """

    name = cast(str, response.get("varName"))

    if name is None:
        assert response.parent is not None
        for sq in response.parent.find_all("subQuestion"):
            assert sq["varName"].startswith(
                "B4_SQ"
            ), "only question B4 is known to have empty response tags"

        choices = response.find_all("value")
        if len(choices) == 7:
            return "B4-1"
        elif len(choices) == 8:
            return "B4-2"
        else:
            raise AssertionError("expected 7 choices for B4-1 and 8 choices for B4-2.")

    else:
        return name


def rename_question(questions: list[QuestionTypeAlias]) -> list[QuestionTypeAlias]:
    """
    Rename the B4 subquestions (ten each) to include a suffix to indicate
    the dimension, based on the name assigned to the response above.
    This way, the format matches the one from the CSV file.
    """

    for question in questions:
        if question["question_group"] == "B4-1":
            question["name"] = cast(str, question["name"]) + "_1"
        elif question["question_group"] == "B4-2":
            question["name"] = cast(str, question["name"]) + "_2"
    return questions
