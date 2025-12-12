"""Functions for basic bar plots."""

from collections.abc import Sequence

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ..data_import.data_import import LimeSurveyData
from ._barplot_enums import BarLabels, Orientation, PlotStat, PlotType
from ._barplots_helpers import (
    adapt_legend,
    add_bar_labels,
    add_tick_labels,
    barplot_internal,
    label_axes,
)


def plot_bar(
    survey: LimeSurveyData,
    data_df: pd.DataFrame,
    question: str,
    n_question: int,
    label_q_data: str = "",
    orientation: Orientation = Orientation.HORIZONTAL,
    stat: PlotStat = PlotStat.COUNT,
    width: float = 6,
    height: float = 4,
    bar_labels: BarLabels = BarLabels.NONE,
    bar_label_size: int | None = None,
    tick_label_size: int | None = None,
    tick_label_wrap: int = 25,
) -> tuple[Figure, Axes]:
    """Plot bar plots (single and multiple).

    Args:
        survey: The LimeSurvey object
        data_df: DataFrame with responses to be plotted
        question: The question code
        n_question: Number of participants
        label_q_data: Label for axis with data from question.
        orientation: Plot orientation.
        stat: Plot absolute values or percentages?
        width: Width of figure.
        height: Height of figure.
        bar_labels: How to format bar labels.
        bar_label_size: Font size for bar labels, if enabled.
        tick_label_size: Font size for tick labels.
        tick_label_wrap: How many characters are allowed per line in tick labels.

    Returns:
        New matplotlib Figure and Axes for the bar plot.
    """
    # plot barplot
    fig, ax = barplot_internal(
        data_df=data_df,
        question=question,
        orient=orientation,
        stat=stat,
        width=width,
        height=height,
    )

    # add number of participants to top right corner
    plt.text(
        0.99,
        0.99,
        f"N = {n_question}",
        ha="right",
        va="top",
        transform=ax.transAxes,
        # fontsize=fontsize,
    )

    # add bar labels (the ones on top or next to bars within the plot)
    ax = add_bar_labels(
        ax=ax,
        show_axes_labels=bar_labels,
        percentcount=stat,
        n_question=n_question,
        fontsize=bar_label_size,
    )

    # add tick labels (the ones below or next to the bars outside of the plot)
    ax = add_tick_labels(
        survey=survey,
        ax=ax,
        question=question,
        orientation=orientation,
        fontsize=tick_label_size,
        text_wrap=tick_label_wrap,
    )

    # add general labels to axes
    label_axes(ax=ax, orientation=orientation, label_q_data=label_q_data, stat=stat)

    return fig, ax


def plot_bar_comparison(
    survey: LimeSurveyData,
    data_df: pd.DataFrame,
    question: str,
    hue: str,
    hue_order: Sequence[str] | None = None,
    n_participants: dict[str, int] | None = None,
    label_q_data: str = "",
    orient: Orientation = Orientation.HORIZONTAL,
    stat: PlotStat = PlotStat.COUNT,
    width: float = 6,
    height: float = 4,
    bar_labels: BarLabels = BarLabels.NONE,
    bar_label_size: int | None = None,
    tick_label_size: int | None = None,
    tick_label_wrap: int = 25,
) -> tuple[Figure, Axes]:
    """Plot comparison bar plots (single and multiple).

    Args:
        survey: The LimeSurvey object
        data_df: DataFrame with responses to be plotted
        question: Question code for the first question
        hue: Question code for the second question
        hue_order: Order of answer options for the second question.
        n_participants: Number of participants per hue group (usually centers),
            or None to suppress printing N.
        label_q_data: Label for axis with data from question.
        orient: Plot orientation.
        stat: Plot absolute values or percentages?
        width: Width of figure.
        height: Height of figure.
        bar_labels: How to format bar labels.
        bar_label_size: Font size for bar labels.
        tick_label_size: Font size for tick labels.
        tick_label_wrap: Number of letters after which tick labels wrap.

    Returns:
        New matplotlib Figure and Axes for the bar plot.
    """
    # plot barplot
    fig, ax = barplot_internal(
        data_df=data_df,
        question=question,
        orient=orient,
        stat=stat,
        width=width,
        height=height,
        comparison=PlotType.SINGLE_Q_COMPARISON
        if n_participants is not None
        else PlotType.MULTI_Q,
        hue=hue,
        hue_order=hue_order,
    )

    # adapt legend
    ax = adapt_legend(
        survey=survey, ax=ax, question=hue, text_wrap=40, group_n=n_participants
    )

    # add bar labels (the ones on top or next to bars within the plot)
    ax = add_bar_labels(
        ax=ax,
        show_axes_labels=bar_labels,
        percentcount=stat,
        n_question=None,
        # rotation=45 if orientation == Orientation.VERTICAL else None,
        fontsize=bar_label_size,
    )

    # add tick labels (the ones below or next to the bars outside of the plot)
    ax = add_tick_labels(
        survey=survey,
        ax=ax,
        question=question,
        orientation=orient,
        fontsize=tick_label_size,
        text_wrap=tick_label_wrap,
    )

    # add general labels to axes
    label_axes(ax=ax, orientation=orient, label_q_data=label_q_data, stat=stat)
    return fig, ax
