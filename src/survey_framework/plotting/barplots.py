from collections.abc import Sequence
from textwrap import wrap

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.ticker import PercentFormatter

from ..data_import.data_import import LimeSurveyData
from ..plotting.helper_barplots import (
    adapt_legend,
    add_bar_labels,
    add_tick_labels,
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
    percentcount: PlotStat = PlotStat.COUNT,
    fig_size_x: int = 16,
    fig_size_y: int = 10,
    fontsize: int = 10,
    show_axes_labels: BarLabels = BarLabels.NONE,
    fontsize_axes_labels: int = 10,
    text_wrap: int = 25,
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
        stat=percentcount,
        width=fig_size_x,
        height=fig_size_y,
    )

    # add number of participants to top right corner
    plt.text(
        0.99,
        0.99,
        f"N = {n_question}",
        ha="right",
        va="top",
        transform=ax.transAxes,
        fontsize=fontsize,
    )

    # add bar labels (the ones on top or next to bars within the plot)
    ax = add_bar_labels(
        ax=ax,
        show_axes_labels=show_axes_labels,
        percentcount=percentcount,
        n_question=n_question,
        fontsize=fontsize_axes_labels,
    )

    # add tick labels (the ones below or next to the bars outside of the plot)
    ax = add_tick_labels(
        survey=survey,
        ax=ax,
        question=question,
        orientation=orientation,
        fontsize=fontsize,
        text_wrap=text_wrap,
    )

    # add general labels to axes
    match orientation:
        case Orientation.HORIZONTAL:
            ax.set(xlabel=percentcount.value.capitalize(), ylabel=label_q_data)
        case Orientation.VERTICAL:
            ax.set(xlabel=label_q_data, ylabel=percentcount.value.capitalize())

    # set title
    ax.set_title(
        "\n".join(
            wrap(
                question
                + ": "
                + survey.questions.loc[
                    survey.questions["question_group"] == question
                ].question_label.iloc[0],
                60,
            )
        ),
        fontsize=14,
    )

    ax.autoscale()
    ax.set_autoscale_on(True)

    return fig, ax


def plot_bar_comparison(
    survey: LimeSurveyData,
    data_df: pd.DataFrame,
    question: str,
    hue: str,
    hue_order: Sequence[str] | None = None,
    n_question: int | None = None,
    label_q_data: str = "",
    orient: Orientation = Orientation.HORIZONTAL,
    stat: PlotStat = PlotStat.COUNT,
    width: float = 6,
    height: float = 4,
    # fontsize: int = 10,
    show_axes_labels: BarLabels = BarLabels.NONE,
    # fontsize_axes_labels: int = 10,
    text_wrap: int = 25,
) -> tuple[Figure, Axes]:
    """
    plot comparison bar plots (single and multiple)

    Args:
        survey: The LimeSurvey object
        data_df: DataFrame with responses to be plotted
        question: Question code for the first question
        question_comparison: Question code for the second question
        n_question: Number of participants, or None if multi-center comparison
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
        orient=orient,
        stat=stat,
        width=width,
        height=height,
        comparison=PlotType.SINGLE_Q_COMPARISON
        if n_question is None
        else PlotType.MULTI_Q,
        hue=hue,
        hue_order=hue_order,
    )

    # do not tamper with legend and don't add n_question if we compare centers
    if n_question is not None:
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

        # adapt legend
        ax = adapt_legend(survey=survey, ax=ax, question=hue, text_wrap=text_wrap)

    # add bar labels (the ones on top or next to bars within the plot)
    ax = add_bar_labels(
        ax=ax,
        show_axes_labels=show_axes_labels,
        percentcount=stat,
        n_question=n_question,
        # rotation=45 if orientation == Orientation.VERTICAL else None,
        # fontsize=5,
    )

    # add tick labels (the ones below or next to the bars outside of the plot)
    ax = add_tick_labels(
        survey=survey,
        ax=ax,
        question=question,
        orientation=orient,
        # fontsize=fontsize,
        text_wrap=text_wrap,
    )

    # add general labels to axes
    pct_fmt = PercentFormatter(1.0, decimals=0, symbol=None)
    match orient:
        case Orientation.HORIZONTAL:
            ax.set(ylabel=label_q_data)
            if stat == PlotStat.PROPORTION:
                ax.xaxis.set_major_formatter(pct_fmt)
                ax.xaxis.set_label_text("Percent")
            else:
                ax.xaxis.set_label_text(stat.capitalize())
        case Orientation.VERTICAL:
            ax.set(xlabel=label_q_data)
            if stat == PlotStat.PROPORTION:
                ax.yaxis.set_major_formatter(pct_fmt)
                ax.yaxis.set_label_text("Percent")
            else:
                ax.yaxis.set_label_text(stat.capitalize())

    return fig, ax
