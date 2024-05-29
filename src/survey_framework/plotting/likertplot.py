import warnings
from textwrap import wrap

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from plot_likert import plot_likert as _likert  # type: ignore

from ..data_import.data_import import LimeSurveyData
from . import helmholtzcolors as hc
from .helper_plotenums import BarLabels


def plot_likertplot(
    survey: LimeSurveyData,
    data_df: pd.DataFrame,
    question: str,
    order: list[str],
    bar_labels: BarLabels = BarLabels.PERCENT,
    fig_size_x: int = 16,
    fig_size_y: int = 10,
    text_wrap: int = 30,
) -> tuple[Figure, Axes]:
    """
    plot the given data as a Likert plot

    Args:
        survey: the LimeSurvey object
        data_df: dataframe containing answers to be plotted
        question: question code (e.g. 'D4')
        order: ordered list of answer options. **The rest will be dropped!**
        bar_labels: which kind of labels bars should have. Defaults to PERCENT.
        fig_size_x: width of the figure. Defaults to 16.
        fig_size_y: height of the figure. Defaults to 10.
        text_wrap: number of characters before a question label wraps. Defaults to 30.

    Returns:
        The matplotlib figure and axis
    """

    hc.set_plotstyle()
    colors = hc.palette[len(order)]

    fig, ax = plt.subplots(
        dpi=300, figsize=(fig_size_x, fig_size_y), layout="constrained"
    )

    # remove values not present in order
    drop = set(survey.get_choices(question).keys()).difference(order)
    dropped_df = data_df.drop(columns="id").replace(drop, value=None)

    # use external library to actually draw the plot
    # silence FutureWarnings (already fixed upstream, not yet in PyPI)
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=FutureWarning)
        # TODO: support percentages?
        ax = _likert(dropped_df, order, colors=colors, ax=ax)

    # set the title (overarching question)
    title = survey.questions.loc[survey.questions["question_group"] == question][
        "question_label"
    ].unique()
    assert len(title) == 1, "Multiple question_labels found, check data correctness."
    ax.set_title(title[0])

    # set subquestion labels (y ticks)
    new_labels = []
    for old_label in ax.get_yticklabels():
        label = survey.questions.loc[old_label.get_text()]["label"]
        new_labels.append("\n".join(wrap(label, text_wrap)))
    ax.set_yticklabels(new_labels)
    # TODO: use plot_helpers instead?
    # add_tick_labels(survey=survey, ax=ax, data_df=data_df,
    # question=question, orientation=Orientation.HORIZONTAL, fontsize=10, text_wrap=30)

    # set the legend labels
    choices = survey.questions.loc[survey.questions["question_group"] == question][
        "choices"
    ].iloc[0]  # underlying assumption: all subquestions use the same scale
    for label in ax.get_legend().get_texts():
        label.set_text(choices[label.get_text()])

    # reposition legend
    ax.get_legend().set_bbox_to_anchor((1, 0.97))

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
        if percentage < 5:
            return ""
        match bar_labels:
            case BarLabels.PERCENT:
                return f"{percentage:.2f}%"
            case BarLabels.COUNT:
                return f"{x:g}"
            case BarLabels.NONE:
                return ""

    # set bar labels
    for bc in ax.containers[1:]:
        ax.bar_label(
            bc, label_type="center", weight="bold", color="white", fmt=cutoff_fmt
        )

    return fig, ax
