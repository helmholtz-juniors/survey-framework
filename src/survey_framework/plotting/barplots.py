from collections.abc import Sequence

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ..data_import.data_import import LimeSurveyData
from ..plotting.helper_barplots import (
    adapt_legend,
    add_bar_labels,
    add_tick_labels,
    label_axes,
    plot_barplot,
)
from ..plotting.helper_plotenums import BarLabels, Orientation, PlotStat, PlotType


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
    """
    plot bar plots (single and multiple)

    Args:
        survey: The LimeSurvey object
        data_df: DataFrame with responses to be plotted
        question: The question code
        n_question: Number of participants
        label_q_data: Label for axis with data from question. Defaults to "".
        orientation: Plot orientation. Defaults to HORIZONTAL.
        percentcount: Plot absolute values or percentages? Defaults to COUNT.
        fig_size_x: Width of figure. Defaults to 16.
        fig_size_y: Height of figure. Defaults to 10.
        fontsize: Font size for tick labels. Defaults to 10.
        show_axes_labels: How to format bar labels. Defaults to NONE (no labels).
        fontsize_axes_labels: Font size for bar labels. Defaults to 10.
        text_wrap: Number of letters after which text labels wrap. Defaults to 25.

    Returns:
        tuple[plt.figure, plt.axes, plt.axes]: _description_
    """

    # plot barplot
    fig, ax = plot_barplot(
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
    """
    plot comparison bar plots (single and multiple)

    Args:
        survey: The LimeSurvey object
        data_df: DataFrame with responses to be plotted
        question: Question code for the first question
        question_comparison: Question code for the second question
        n_participants: Number of participants per hue group (usually centers),
            or None to suppress printing N. Defaults to None.
        label_q_data: Label for axis with data from question. Defaults to "".
        orientation: Plot orientation. Defaults to HORIZONTAL.
        percentcount: Plot absolute values or percentages? Defaults to COUNT.
        fig_size_x: Width of figure. Defaults to 16.
        fig_size_y: Height of figure. Defaults to 10.
        bar_labels: How to format bar labels. Defaults to NONE (no labels).
        bar_label_size: Font size for bar labels. Defaults to None (automatic).
        tick_label_size: Font size for tick labels. Defaults to None (automatic).
        tick_label_wrap: Number of letters after which tick labels wrap. Defaults to 25.

    Returns:
        tuple[plt.figure, plt.axes, plt.axes]: _description_
    """

    # plot barplot
    fig, ax = plot_barplot(
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
