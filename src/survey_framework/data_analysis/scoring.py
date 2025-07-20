from enum import StrEnum
from typing import Any

import pandas as pd


class Condition(StrEnum):
    STATE_ANXIETY = "D1"
    TRAIT_ANXIETY = "D2"
    DEPRESSION = "D3"


def rate_mental_health(
    responses: pd.DataFrame,
    condition: Condition,
    keep_subscores: bool = False,
) -> pd.DataFrame:
    """Calculate State/Trait Anxiety or Depression score based on responses to
        question based on the following references:
            K. Kroenke, R. L. Spitzer, J. B. W. William, and B. Löwe., The
                Patient Health Questionnaire somatic, anxiety,and depressive
                symptom scales: a systematic review. General Hospital
                Psychiatry, 32(4):345-359, 2010.
            T. M. Marteau and H. Bekker., The development of a six-item short-
                form of the state scale of the spielberger state-trait anxiety
                inventory (STAI). British Journal of Clinical Psychology,
                31(3):301-306, 1992.

    Args:
        responses: DataFrame containing responses data
        condition: Which kind of mental health condition to rate
        keep_subscores (optional): Whether to include scores from subquestions
            in the output DataFrame, or only total score and classification.
            Default False.

    Returns:
        pd.DataFrame: Mental health condition ratings and classifications
    """

    # Set up condition-specific parameters
    match condition:
        case Condition.STATE_ANXIETY:
            num_subquestions = 6
            base_score = 10 / 3
            conversion = ["pos", "neg", "neg", "pos", "pos", "neg"]
            label = "state_anxiety"
            classification_boundaries = [20, 40, 60, 80]
            classes = ["no or low anxiety", "moderate anxiety", "high anxiety"]

        case Condition.TRAIT_ANXIETY:
            num_subquestions = 8
            base_score = 5 / 2
            conversion = [
                "pos",
                "neg",
                "neg",
                "pos",
                "neg",
                "neg",
                "pos",
                "neg",
            ]
            label = "trait_anxiety"
            classification_boundaries = [20, 40, 60, 80]
            classes = ["no or low anxiety", "moderate anxiety", "high anxiety"]

        case Condition.DEPRESSION:
            num_subquestions = 8
            base_score = 1
            conversion = ["freq" for _ in range(8)]
            label = "depression"
            classification_boundaries = [0, 4, 9, 14, 19, 24]
            classes = [
                "no to minimal depression",
                "mild depression",
                "moderate depression",
                "moderately severe depression",
                "severe depression",
            ]

        case _:
            raise AssertionError("unreachable")

    # sanity check
    q_code = responses.columns[0].split("_")[0]
    if q_code != condition:
        raise ValueError(f"expected question {condition}, got {q_code}")

    # Set up score conversion dicts
    pos_direction_scores = {
        "A1": 4 * base_score,  # "Not at all
        "A2": 3 * base_score,  # "Somewhat"
        "A3": 2 * base_score,  # "Moderately
        "A4": 1 * base_score,  # "Very much"
    }
    neg_direction_scores = {
        "A1": 1 * base_score,  # "Not at all"
        "A2": 2 * base_score,  # "Somewhat"
        "A3": 3 * base_score,  # "Moderately"
        "A4": 4 * base_score,  # "Very much"
    }
    frequency_scores = {
        "A1": 0 * base_score,  # "Not at all"
        "A2": 1 * base_score,  # "Several days"
        "A3": 2 * base_score,  # "More than half the days"
        "A4": 3 * base_score,  # "Nearly every day"
    }
    conversion_dicts = {
        "pos": pos_direction_scores,
        "neg": neg_direction_scores,
        "freq": frequency_scores,
    }

    # Map responses from code to score
    df = pd.DataFrame()
    for column, conv in zip(responses.columns, conversion, strict=True):
        df[f"{column}_score"] = responses[column].map(
            conversion_dicts[conv], na_action="ignore"
        )

    # Calculate total anxiety or depression scores
    # scaled by number of non-NaN responses
    # e.g. scale by 8/5 if 5/8 subquestions answered
    responses_counts = df.notna().sum(axis=1)
    df[f"{label}_score"] = (
        df.sum(axis=1, skipna=True).div(responses_counts).mul(num_subquestions)
    )

    # Suppress entries with less than half of all subquestions answered
    # TODO: we might want to be more strict here
    df.loc[responses_counts < num_subquestions / 2, f"{label}_score"] = None

    # Classify into categories
    df[f"{label}_class"] = pd.cut(
        df[f"{label}_score"],
        bins=classification_boundaries,
        include_lowest=True,
        labels=classes,
    )

    if not keep_subscores:
        df = df.drop(df.columns[:-2], axis=1)

    return df


def rate_somatic(
    responses: pd.DataFrame,
    keep_subscores: bool = False,
) -> pd.DataFrame:
    """Calculate Patient Health Questionaire (PHQ15) based on responses to
        question based on:
            K. Kroenke, R. L. Spitzer, J. B. W. William, and B. Löwe., The
                Patient Health Questionnaire somatic, anxiety,and depressive
                symptom scales: a systematic review. General Hospital
                Psychiatry, 32(4):345-359, 2010.

    Args:
        responses: DataFrame containing responses data
        keep_subscores (optional): Whether to include scores from subquestions
            in the output DataFrame, or only total score and classification.
            Default False.

    Returns:
        pd.DataFrame: PHQ15 classifications
    """
    PHQ15 = "D4"
    label = "somatic"

    # sanity check
    q_code = responses.columns[0].split("_")[0]
    if q_code != PHQ15:
        raise ValueError(f"expected question {PHQ15}, got {q_code}")

    num_subquestions = 14
    base_score = 15 / 14
    classification_boundaries = [0, 4, 9, 14, 30]
    classes = [
        "No somatic symptoms",
        "Mild somatic symptoms",
        "Moderate somatic symptoms",
        "Severe somatic symptoms",
    ]

    # Set up score conversion dicts
    scores = {
        "A2": 0 * base_score,  # "Not bothered
        "A3": 1 * base_score,  # "Bothered a little"
        "A4": 2 * base_score,  # "Bothered a lot
    }

    # Map responses from code to score
    df = pd.DataFrame()
    for column in responses.columns:
        df[f"{column}_score"] = responses[column].map(scores, na_action="ignore")

    # Calculate total scores scaled by number of non-NaN responses
    # e.g. scale by 8/5 if 5/8 subquestions answered
    responses_counts = df.notna().sum(axis=1)
    df[f"{label}_score"] = (
        df.sum(axis=1, skipna=True).div(responses_counts).mul(num_subquestions)
    )

    # Suppress entries with less than half of all subquestions answered
    # TODO: we might want to be more strict here
    df.loc[responses_counts < num_subquestions / 2, f"{label}_score"] = None

    # Classify into categories
    df[f"{label}_class"] = pd.cut(
        df[f"{label}_score"],
        bins=classification_boundaries,
        include_lowest=True,
        labels=classes,
    )

    if not keep_subscores:
        df = df.drop(df.columns[:-2], axis=1)

    return df


class Scale(StrEnum):
    """The three burnout scales defined by the MBI"""

    EX = "Exhaustion"
    CY = "Cynicism"
    PE = "Professional Efficacy"


class Profile(StrEnum):
    """The five burnout profiles defined in the MBI manual"""

    ENGAGED = "Engaged"
    INEFFECTIVE = "Ineffective"
    OVEREXTENDED = "Overextended"
    DISENGAGED = "Disengaged"
    BURNOUT = "Burnout"


def rate_burnout(responses: pd.DataFrame) -> pd.DataFrame:
    """Calculate burnout scores for the MBI-GS scale according to the
            Maslach Burnout Inventory Manual, Fourth Edition.

    Args:
        responses: responses to question D3d (burnout)

    Returns:
        SUM scores for each `Scale` (3 ints) and a burnout `Profile` (1 string)
    """

    SCORE_MAP = {
        "A2": 0,  # "Never"
        "A3": 1,  # "A few times a year or less"
        "A4": 2,  # "Once a month or less"
        "A5": 3,  # "A few times a month"
        "A6": 4,  # "Once a week"
        "A7": 5,  # "A few times a week"
        "A8": 6,  # "Every day"
    }

    scales = [
        Scale.EX,  # I feel emotionally drained from my work.
        Scale.EX,  # I feel used up at the end of the workday.
        Scale.EX,  # I feel tired when I get up in the morning and have to ...
        Scale.EX,  # Working all day is really a strain for me.
        Scale.PE,  # I can effectively solve the problems that arise in my work.
        Scale.EX,  # I feel burned out from my work.
        Scale.PE,  # I feel I am making an effective contribution to what ...
        Scale.CY,  # I have become less interested in my work since I ...
        Scale.CY,  # I have become less enthusiastic about my work.
        Scale.PE,  # In my opinion, I am good at my job.
        Scale.PE,  # I feel exhilarated when I accomplish something at work.
        Scale.PE,  # I have accomplished many worthwhile things in this job.
        Scale.CY,  # I just want to do my job and not be bothered.
        Scale.CY,  # I have become more cynical about whether my work ...
        Scale.CY,  # I doubt the significance of my work.
        Scale.PE,  # At my work, I feel confident that I am effective at ...
    ]

    # make empty df with three columns
    df = pd.DataFrame(responses.index)
    df[Scale.EX], df[Scale.CY], df[Scale.PE] = 0, 0, 0

    for col, scale in zip(responses.columns, scales, strict=True):
        # sum up the score in the relevant category
        col_scores = responses[col].map(SCORE_MAP, na_action="ignore")
        df[scale] += col_scores

    # boolean classification according to Table 3 in the manual
    # for PE, critical == good, hence the ">" instead of ">="
    df["EX_critical"] = df[Scale.EX].div(5).map(lambda x: x >= 2.90, na_action="ignore")
    df["CY_critical"] = df[Scale.CY].div(5).map(lambda x: x >= 2.86, na_action="ignore")
    df["PE_critical"] = df[Scale.PE].div(6).map(lambda x: x > 4.30, na_action="ignore")

    def classify(row: "pd.Series[Any]") -> Profile:
        """assign burnout profiles according to Table 1 in the manual

        Args:
            row: a single participant

        Returns:
            burnout `Profile` of the participant
        """

        exhausted = row["EX_critical"]
        cynical = row["CY_critical"]
        effective = row["PE_critical"]
        assert isinstance(exhausted, bool)
        assert isinstance(cynical, bool)
        assert isinstance(effective, bool)

        if not exhausted and not cynical and effective:
            return Profile.ENGAGED
        elif not exhausted and not cynical and not effective:
            return Profile.INEFFECTIVE
        elif exhausted and not cynical:
            return Profile.OVEREXTENDED
        elif not exhausted and cynical:
            return Profile.DISENGAGED
        elif exhausted and cynical:
            return Profile.BURNOUT
        else:
            raise AssertionError("unreachable")

    df["Profile"] = df.dropna().apply(classify, axis=1, result_type="reduce")
    return df


def rate_satisfaction(
    responses: pd.DataFrame,
    calc_average: bool = True,
) -> pd.DataFrame:
    """Calculate satisfaction rating for each subquestion and average over all
    subquestions. Numeric scale from 1 = very dissatisfied to 5 = very satisfied.

    Args:
        responses: DataFrame containing responses data
        calc_average: Whether to calculate average satisfaction. Default True.
    Returns:
        Satisfaction ratings for each component (and overall average)
    """
    # safety check: only questions where we verified that they use a scale from
    # A1 (very satisfied) to A5 (very dissatisfied) should be added to this list
    SATISFACTION_QUESTIONS = ["C1"]

    q_code = responses.columns[0].split("_")[0]
    if q_code not in SATISFACTION_QUESTIONS:
        raise ValueError(f"{q_code} is not a satisfaction-scale question")

    # Set up score conversion dicts for individual questions
    satisfaction_question_scores = {
        "A1": 5.0,  # "Very satisfied"
        "A2": 4.0,  # "Satisfied"
        "A3": 3.0,  # "Neither/nor"
        "A4": 2.0,  # "Dissatisfied"
        "A5": 1.0,  # "Very dissatisfied"
    }

    # Map responses to score
    df = pd.DataFrame()
    for column in responses.columns:
        df[f"{column}_score"] = responses[column].map(
            satisfaction_question_scores, na_action="ignore"
        )

    # Calculate mean rating and round (ignoring NaN)
    if calc_average:
        df[f"{q_code}_score"] = df.mean(axis=1, skipna=True).round()
        df[f"{q_code}_class"] = df[f"{q_code}_score"].map(
            {v: k for k, v in satisfaction_question_scores.items()}
        )

    return df
