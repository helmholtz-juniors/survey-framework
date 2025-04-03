import warnings
from textwrap import wrap
from typing import cast

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from plot_likert import plot_likert as _likert  # type: ignore [import-untyped]

from ..data_import.data_import import LimeSurveyData
from . import helmholtzcolors as hc
from .helper_plotenums import BarLabels


def plot_likertplot(
    survey: LimeSurveyData,
    data_df: pd.DataFrame,
    question: str,
    order: list[str],
    bar_labels: BarLabels = BarLabels.PERCENT,
    width: int = 6,
    height: int = 4,
    text_wrap: int = 30,
    percent_cutoff: int = 8,
) -> tuple[Figure, Axes]:
    """
    plot the given data as a Likert plot

    Args:
        survey: the LimeSurvey object
        data_df: dataframe containing answers to be plotted
        question: question code (e.g. 'D4')
        order: ordered list of answer options. **The rest will be dropped!**
        bar_labels (optional): which kind of bar labels to use. Defaults to PERCENT.
        width (optional): width of the figure. Defaults to 16.
        height (optional): height of the figure. Defaults to 10.
        text_wrap (optional): wrap question labels after x characters. Defaults to 30.

    Returns:
        The matplotlib figure and axis
    """

    hc.set_plotstyle()
    colors = hc.palette[len(order)]

    fig, ax = plt.subplots(dpi=300, figsize=(width, height), layout="constrained")

    # remove values not present in order
    drop = set(survey.get_choices(question).keys()).difference(order)
    dropped_df = data_df.drop(columns="id").replace(list(drop), value=None)

    # use external library to actually draw the plot
    # silence FutureWarnings (already fixed upstream, not yet in PyPI)
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=FutureWarning)
        ax = _likert(dropped_df, order, colors=colors, ax=ax)

    # set the title (overarching question)
    title = survey.questions.loc[survey.questions["question_group"] == question][
        "question_label"
    ].unique()
    assert len(title) == 1, "Multiple question_labels found, check data correctness."
    # ax.set_title(title[0])

    # set subquestion labels (y ticks)
    new_labels = []
    for old_label in ax.get_yticklabels():
        label = cast(str, survey.questions.loc[old_label.get_text()]["label"])
        new_labels.append("\n".join(wrap(label, text_wrap)))
    ax.set_yticklabels(new_labels, linespacing=0.75)

    # set the legend labels
    choices = survey.questions.loc[survey.questions["question_group"] == question][
        "choices"
    ].iloc[0]  # underlying assumption: all subquestions use the same scale
    for text in ax.get_legend().get_texts():
        text.set_text(choices[text.get_text()])

    # reposition legend
    sns.move_legend(ax, "upper center", ncol=3, bbox_to_anchor=(0.25, 1.1))

    # add number of participants
    n_question = data_df.count().iloc[1]  # don't count NaNs, but count dropped answers
    plt.text(
        0.99, 0.99, f"N = {n_question}", ha="right", va="top", transform=ax.transAxes
    )

    def cutoff_fmt(x: float) -> str:
        """
        formatter for bar labels, with a 5% cutoff (no label for small bars)
        """
        percentage = x * 100 / n_question
        if percentage < percent_cutoff:
            return ""
        match bar_labels:
            case BarLabels.PERCENT:
                return f"{percentage:.1f}%"
            case BarLabels.COUNT:
                return f"{x:g}"
            case BarLabels.NONE:
                return ""

    # set bar labels
    for bc in ax.containers[1:]:
        ax.bar_label(
            container=cast(BarContainer, bc),
            label_type="center",
            weight="bold",
            fontsize="7",
            color="white",
            # path_effects=[PathEffects.withStroke(linewidth=1, foreground='black')],
            fmt=cutoff_fmt,
        )

    return fig, ax
