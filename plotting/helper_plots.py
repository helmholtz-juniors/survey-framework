from textwrap import wrap
from matplotlib import pyplot as plt
import pandas as pd
from data_import.data_import import LimeSurveyData, QuestionType
from plotting.helper_plotenums import (
    Orientation,
    PercentCount,
    ShowAxesLabel,
)
import seaborn as sns
import plotting.helmholtzcolors as hc

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.container import BarContainer
from typing import cast, Iterable


def add_axes_labels(
    fig: Figure,
    ax: Axes,
    show_axes_labels: ShowAxesLabel,
    percentcount: PercentCount,
    n_question: int,
    fontsize: int,
) -> tuple[Figure, Axes]:
    """
    add labels to each bar in a bar plot

    Args:
        fig (Figure): matplotlib.figure
        ax (Axes): matplotlib.axes
        show_axes_labels (ShowAxesLabel): whether axes labels should be shown
        percentcount (PercentCount): whether the data plotted is absolute or relative
        n_question (int): the total number of answers, needed for percent calculation
        fontsize (int): font size for the bar labels

    Returns:
        tuple[Figure, Axes]: modified figure and axes
    """

    # Define a label formatter.
    # This is straightforward if the plotted number is the one to be shown.
    # If not, calculate the value to be displayed using N.
    def fmt(n: float) -> str:
        match show_axes_labels, percentcount:
            case ShowAxesLabel.COUNT, PercentCount.COUNT:
                return f"{n:g}"
            case ShowAxesLabel.PERCENT, PercentCount.PERCENT:
                return f"{n:0.2f}%"
            case ShowAxesLabel.PERCENT, PercentCount.COUNT:
                return f"{n * 100 / n_question:.2f}%"
            case ShowAxesLabel.COUNT, PercentCount.PERCENT:
                raise NotImplementedError(
                    "Percentages on axis with absolute counts on bars is not implemented yet."
                )
            case ShowAxesLabel.NONE, _:
                return ""
        # match is exhaustive, but mypy doesn't get that
        assert False, "unreachable"

    # actually label the bars, using matplotlib sugar
    for bc in cast(Iterable[BarContainer], ax.containers):
        ax.bar_label(bc, padding=1, fontsize=fontsize, fmt=fmt)

    return fig, ax


def plot_barplot(
    data_df: pd.DataFrame,
    question: str,
    orientation: Orientation,
    percentcount: PercentCount,
    fig_size_x: int,
    fig_size_y: int,
    comparison: bool = False,
    hue: str = "",
) -> tuple[Figure, Axes]:
    """
    plot bar plot with processed data

    Args:
        data_df (pd.DataFrame): dataframe with processed data
        question (str): str of question
        orientation (Orientation): orientation of plot
        percentcount (PercentCount): whether plot shows counts or percent
        fig_size_x (int): x-axis size of figure
        fig_size_y (int): y-axis size of figure
        hue (str): hue for plot. Defaults to "".

    Returns:
        tuple[Figure, Axes]: modified figure and axes
    """

    # built input for hue and colors for plotting
    hue_input = list()
    colors = list()
    if comparison:
        # if it's a comparison bar plot, hue needs to be filled with a list of comparison data
        hue_input = list(data_df[hue])
        colors = hc.get_blues(len(data_df[hue].value_counts()))
    else:
        # otherwise, hue needs to be equal to the question data
        hue_input = list(data_df[question])
        colors = hc.get_blues(len(data_df))

    # set seaborn style
    sns.set_style("darkgrid", {"axes.facecolor": "#f2f0f0"})

    # initialize plot and set colors
    fig, ax = plt.subplots(
        dpi=300, figsize=(fig_size_x, fig_size_y), layout="constrained"
    )

    # plot graphs
    match orientation:
        case Orientation.HORIZONTAL:
            # x = data, y = labels
            ax = sns.barplot(
                x=data_df[percentcount.value],
                y=list(data_df[question]),
                hue=hue_input,
                palette=colors,
                orient="h",
            )
        case Orientation.VERTICAL:
            # x = labels, y = data
            ax = sns.barplot(
                y=data_df[percentcount.value],
                x=list(data_df[question]),
                hue=hue_input,
                palette=colors,
                orient="v",
            )

    return fig, ax


def add_tick_labels(
    survey: LimeSurveyData,
    ax: Axes,
    data_df: pd.DataFrame,
    question: str,
    orientation: Orientation,
    fontsize: int,
    text_wrap: int,
) -> Axes:
    """
    add axis labels for question
    horizontl --> add labels to y-axis
    vertical --> add labels to x-axis

    Args:
        survey (LimeSurveyData): survey data
        plot (Axes): plot
        data_df (pd.DataFrame): dataframe of processed data
        question (str): str of question
        orientation (Orientation): orientation of plot
        fontsize (int): fontsize
        text_wrap (int): after how many letters text should be wrapped

    Returns:
        Axes: _description_
    """

    # function to rename a single label using the survey data
    def renamed(label: str) -> str:
        match survey.get_question_type(question=question):
            case QuestionType.SINGLE_CHOICE:
                new_label = survey.questions.choices[question][label]
            case QuestionType.MULTIPLE_CHOICE:
                new_label = survey.questions.choices[label]["Y"]
            case other:
                raise NotImplementedError(f"Labels for {other} not implemented.")
        # wrap labels
        return "\n".join(wrap(new_label, text_wrap))

    # match on orientation of plot
    match orientation:
        case Orientation.HORIZONTAL:
            # get all current y-ticklabels
            y_ticklabels = [renamed(item.get_text()) for item in ax.get_yticklabels()]

            # update labels
            ax.set_yticks(range(len(data_df)))
            ax.set_yticklabels(y_ticklabels, fontsize=fontsize)

        case Orientation.VERTICAL:
            # get all current x-ticklabels
            x_ticklabels = [renamed(item.get_text()) for item in ax.get_xticklabels()]

            # update labels
            ax.set_xticks(range(len(data_df)))
            ax.set_xticklabels(
                x_ticklabels,
                fontsize=fontsize,
                rotation=45,
                ha="right",
                rotation_mode="anchor",
            )

    return ax


def adapt_legend(
    survey: LimeSurveyData, ax: Axes, question: str, text_wrap: int
) -> Axes:
    """
    rename legend and move below N

    Args:
        survey (LimeSurveyData): survey data
        ax (Axes): plot
        question (str): str of question
        text_wrap (int): after how many letters text should be wrapped

    Returns:
        Axes: _description_
    """

    handles, labels = ax.get_legend_handles_labels()
    for i in range(0, len(labels)):
        label = survey.questions.choices[question][labels[i]]
        labels[i] = "\n".join(wrap(label, text_wrap))
    ax.legend(handles=handles, labels=labels, bbox_to_anchor=(1, 0.97))

    return ax
