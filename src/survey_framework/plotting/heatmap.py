from enum import StrEnum

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import survey_framework.plotting.helmholtzcolors as hc
from survey_framework.data_analysis.scoring import (
    Condition,
    rate_burnout,
    rate_mental_health,
    rate_somatic,
)
from survey_framework.data_import.data_import import LimeSurveyData


class CorrMethod(StrEnum):
    """Correlation Method used by Pandas"""

    KENDALL = "kendall"  # Kendall's tau
    PEARSON = "pearson"  # Pearson's rho
    SPEARMAN = "spearman"  # Spearman's rho


def plot_heatmap(
    df: pd.DataFrame,
    survey: LimeSurveyData,
    width: float = 6.5,
    height: float = 6,
    method: CorrMethod = CorrMethod.SPEARMAN,
) -> tuple[Figure, Axes]:
    """Correlation heatmap of the input dataframe vs. all (mental) health scores.

    Args:
        df: Dataframe with numeric columns that should be correlated against health
        survey: main survey object
        width: Horizontal figure size.
        height: Vertical figure size.
        method: Statistical correlation method.

    Returns:
        tuple of matplotlib figure and axes for the heatmap
    """

    """"""
    SOMATIC = "D4"
    BURNOUT = "D3d"

    # health scores
    sta = rate_mental_health(
        survey.get_responses(Condition.STATE_ANXIETY), Condition.STATE_ANXIETY
    )
    tra = rate_mental_health(
        survey.get_responses(Condition.TRAIT_ANXIETY), Condition.TRAIT_ANXIETY
    )
    depr = rate_mental_health(
        survey.get_responses(Condition.DEPRESSION), Condition.DEPRESSION
    )
    somatic = rate_somatic(survey.get_responses(SOMATIC))
    _bout = rate_burnout(survey.get_responses(BURNOUT)).set_index("id")

    correlations = pd.DataFrame(
        {
            "State Anxiety": df.corrwith(
                sta["state_anxiety_score"], method=method.value
            ),
            "Trait Anxiety": df.corrwith(
                tra["trait_anxiety_score"], method=method.value
            ),
            "Depression": df.corrwith(depr["depression_score"], method=method.value),
            "Somatic Symptoms": df.corrwith(
                somatic["somatic_score"], method=method.value
            ),
            # "Exhaustion": df.corrwith(bout["Exhaustion"], method=method.value),
            # "Cynicism": df.corrwith(bout["Cynicism"], method=method.value),
            # "Professional Efficacy": df.corrwith(
            #     bout["Professional Efficacy"], method=method.value
            # ),
        }
    )

    correlations.sort_values(by="State Anxiety", inplace=True)
    # print(correlations)

    hc.set_plotstyle()
    figure, ax = plt.subplots(dpi=300, figsize=(width, height), layout="constrained")

    ax = sns.heatmap(correlations, annot=True, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    return figure, ax
