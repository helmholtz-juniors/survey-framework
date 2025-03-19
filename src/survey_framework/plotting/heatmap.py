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


def plot_heatmap(
    df: pd.DataFrame,
    survey: LimeSurveyData,
    fig_size_x: int = 10,
    fig_size_y: int = 6,
) -> tuple[Figure, Axes]:
    """Correlation heatmap of the input dataframe vs. all (mental) health scores.
    This is currently hard-coded to use Spearman's rho.

    Args:
        df: Dataframe with numeric columns that should be correlated against health
        survey: main survey object
        fig_size_x: Horizontal figure size. Defaults to 10.
        fig_size_y: Vertical figure size. Defaults to 6.

    Returns:
        tuple: matplotlib figure and axes for the heatmap
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
    bout = rate_burnout(survey.get_responses(BURNOUT)).set_index("id")

    correlations = pd.DataFrame(
        {
            "State Anxiety": df.corrwith(sta["state_anxiety_score"], method="spearman"),
            "Trait Anxiety": df.corrwith(tra["trait_anxiety_score"], method="spearman"),
            "Depression": df.corrwith(depr["depression_score"], method="spearman"),
            "Somatic Symptoms": df.corrwith(
                somatic["somatic_score"], method="spearman"
            ),
            "Exhaustion": df.corrwith(bout["Exhaustion"], method="spearman"),
            "Cynicism": df.corrwith(bout["Cynicism"], method="spearman"),
            "Professional Efficacy": df.corrwith(
                bout["Professional Efficacy"], method="spearman"
            ),
        }
    )

    correlations.sort_values(by="State Anxiety", inplace=True)
    print(correlations)

    hc.set_plotstyle()
    figure, ax = plt.subplots(
        dpi=300, figsize=(fig_size_x, fig_size_y), layout="constrained"
    )

    ax = sns.heatmap(correlations, annot=True, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    return figure, ax
