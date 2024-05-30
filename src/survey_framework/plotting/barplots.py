from textwrap import wrap

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ..data_import.data_import import LimeSurveyData
from ..plotting.helper_barplots import (
    adapt_legend,
    add_axes_labels,
    add_tick_labels,
    plot_barplot,
)
from ..plotting.helper_plotenums import BarLabels, Orientation, PercentCount


def plot_bar(
    survey: LimeSurveyData,
    data_df: pd.DataFrame,
    question: str,
    n_question: int,
    label_q_data: str = "",
    orientation: Orientation = Orientation.HORIZONTAL,
    percentcount: PercentCount = PercentCount.COUNT,
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
        orientation=orientation,
        percentcount=percentcount,
        fig_size_x=fig_size_x,
        fig_size_y=fig_size_y,
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
    ax = add_axes_labels(
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
        data_df=data_df,
        question=question,
        orientation=orientation,
        fontsize=fontsize,
        text_wrap=text_wrap,
    )

    # add general labels to axes
    match orientation:
        case Orientation.HORIZONTAL:
            ax.set(xlabel=percentcount.value.capitalize, ylabel=label_q_data)
        case Orientation.VERTICAL:
            ax.set(xlabel=label_q_data, ylabel=percentcount.value.capitalize)

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
    question_comparison: str,
    n_question: int,
    label_q_data: str = "",
    orientation: Orientation = Orientation.HORIZONTAL,
    percentcount: PercentCount = PercentCount.COUNT,
    fig_size_x: int = 16,
    fig_size_y: int = 10,
    fontsize: int = 10,
    show_axes_labels: BarLabels = BarLabels.NONE,
    fontsize_axes_labels: int = 10,
    text_wrap: int = 25,
) -> tuple[Figure, Axes]:
    """
    plot comparison bar plots (single and multiple)

    Args:
        survey: The LimeSurvey object
        data_df: DataFrame with responses to be plotted
        question: Question code for the first question
        question_comparison: Question code for the second question
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
        orientation=orientation,
        percentcount=percentcount,
        fig_size_x=fig_size_x,
        fig_size_y=fig_size_y,
        comparison=True,
        hue=question_comparison,
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
    ax = add_axes_labels(
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
        data_df=pd.DataFrame(data_df[question].value_counts()),
        question=question,
        orientation=orientation,
        fontsize=fontsize,
        text_wrap=text_wrap,
    )

    # adapt legend
    ax = adapt_legend(
        survey=survey, ax=ax, question=question_comparison, text_wrap=text_wrap
    )

    # add general labels to axes
    match orientation:
        case Orientation.HORIZONTAL:
            ax.set(xlabel=percentcount, ylabel=label_q_data)
        case Orientation.VERTICAL:
            ax.set(xlabel=label_q_data, ylabel=percentcount)

    ax.autoscale()
    ax.set_autoscale_on(True)

    return fig, ax
