import matplotlib.pyplot as plt
import pandas as pd

from data_import.data_import import LimeSurveyData
from plotting.helper_plotenums import Orientation, PercentCount, ShowAxesLabel
from plotting.helper_plots import (
    adapt_legend,
    add_axes_labels,
    add_tick_labels,
    plot_barplot,
)

from matplotlib.axes import Axes
from matplotlib.figure import Figure


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
    show_axes_labels: ShowAxesLabel = ShowAxesLabel.NONE,
    fontsize_axes_labels: int = 10,
    text_wrap: int = 25,
) -> tuple[Figure, Axes]:
    """
    plot bar plots (single and multiple)

    Args:
        survey (LimeSurveyData): _description_
        data_df (pd.DataFrame): _description_
        question (str): _description_
        n_question (int): _description_
        label_q_data (str): Label for axis with data from question. Defaults to "".
        orientation (Orientation, optional): Options: 'h' = horizontal, 'v' = vertical. Defaults to 'h'.
        percentcount (PercentCount, optional): 'p' = percent, 'c' = count. Defaults to 'c'.
        fig_size_x (int, optional): Width of figure. Defaults to 16.
        fig_size_y (int, optional): Height of figure. Defaults to 10.
        fontsize (int, optional): Size of font. Defaults to 10.
        show_axes_labels (ShowAxesLabel, optional): 'n' = show none, 'c' = show counts, 'p' = show percent. Defaults to 'n'.
        text_wrap (int, optional): Number of letters after which text labels warp. Defaults to 25.

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
    fig, ax = add_axes_labels(
        fig=fig,
        ax=ax,
        data_df=data_df,
        orientation=orientation,
        show_axes_labels=show_axes_labels,
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
            ax.set(xlabel=percentcount, ylabel=label_q_data)
        case Orientation.VERTICAL:
            ax.set(xlabel=label_q_data, ylabel=percentcount)

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
    show_axes_labels: ShowAxesLabel = ShowAxesLabel.NONE,
    fontsize_axes_labels: int = 10,
    text_wrap: int = 25,
) -> tuple[Figure, Axes]:
    """
    plot comparison bar plots (single and multiple)

    Args:
        survey (LimeSurveyData): _description_
        data_df (pd.DataFrame): _description_
        question (str): _description_
        question_comparison (str): _description_
        n_question (int): _description_
        label_q_data (str): Label for axis with data from question. Defaults to "".
        orientation (Orientation, optional): Options: 'h' = horizontal, 'v' = vertical. Defaults to 'h'.
        percentcount (PercentCount, optional): 'p' = percent, 'c' = count. Defaults to 'c'.
        fig_size_x (int, optional): Width of figure. Defaults to 16.
        fig_size_y (int, optional): Height of figure. Defaults to 10.
        fontsize (int, optional): Size of font. Defaults to 10.
        show_axes_labels (ShowAxesLabel, optional): 'n' = show none, 'c' = show counts, 'p' = show percent. Defaults to 'n'.
        text_wrap (int, optional): Number of letters after which text labels warp. Defaults to 25.

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
    fig, ax = add_axes_labels(
        fig=fig,
        ax=ax,
        data_df=data_df,
        orientation=orientation,
        show_axes_labels=show_axes_labels,
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
