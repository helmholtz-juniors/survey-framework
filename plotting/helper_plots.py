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
from matplotlib.patches import Rectangle
from typing import cast, Iterable


def add_axes_labels(
    fig: Figure,
    ax: Axes,
    data_df: pd.DataFrame,
    orientation: Orientation,
    show_axes_labels: ShowAxesLabel,
    fontsize: int,
) -> tuple[Figure, Axes]:
    """
    add axes labels to bars
    for second part see: https://stackoverflow.com/questions/28931224/how-to-add-value-labels-on-a-bar-chart

    Args:
        fig (Figure): matplotlib.figure
        ax (Axes): matplotlib.axes
        data_df (pd.DataFrame): dataframe with processed data
        orientation (Orientation): orientation of plot
        show_axes_labels (ShowAxesLabel): whether axes labels should be shown

    Returns:
        tuple[Figure, Axes]: modified figure and axes
    """

    labels = []

    # add bar labels
    match show_axes_labels:
        case ShowAxesLabel.COUNT:
            # show counts
            labels = [f"n={p}" for p in data_df["count"]]
        case ShowAxesLabel.PERCENT:
            # show percentages
            labels = [f"{p:0.2f}%" for p in data_df["percentages"]]
        case ShowAxesLabel.NONE:
            # leave function
            return fig, ax

    # get the rectangles from the axes
    rects = cast(Iterable[Rectangle], ax.patches)
    # match over orientation
    match orientation:
        case Orientation.HORIZONTAL:
            for rect, label in zip(rects, labels):
                # calculate y_value
                y_value = rect.get_y() + rect.get_height() / 2
                # calculate x_value
                x_value = rect.get_width()
                # add text to bar
                ax.text(
                    x_value, y_value, label, ha="left", va="center", fontsize=fontsize
                )
        case Orientation.VERTICAL:
            for rect, label in zip(rects, labels):
                # calculate x_value
                x_value = rect.get_x() + rect.get_width() / 2
                # calculate y_value
                y_value = rect.get_height()
                # add text to bar
                ax.text(
                    x_value, y_value, label, ha="center", va="bottom", fontsize=fontsize
                )

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
    match percentcount:
        case PercentCount.COUNT:
            match orientation:
                case Orientation.HORIZONTAL:
                    # counts + horizontal
                    ax = sns.barplot(
                        x=data_df["count"],
                        y=list(data_df[question]),
                        hue=hue_input,
                        palette=colors,
                        orient="h",
                    )
                case Orientation.VERTICAL:
                    # counts + vertical
                    ax = sns.barplot(
                        y=data_df["count"],
                        x=list(data_df[question]),
                        hue=hue_input,
                        palette=colors,
                        orient="v",
                    )
        case PercentCount.PERCENT:
            match orientation:
                case Orientation.HORIZONTAL:
                    # percentages + horizontal
                    ax = sns.barplot(
                        x=data_df["percentages"],
                        y=list(data_df[question]),
                        hue=hue_input,
                        palette=colors,
                        orient="h",
                    )
                case Orientation.VERTICAL:
                    # percentages + vertical
                    ax = sns.barplot(
                        y=data_df["percentages"],
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

    # match on orientation of plot
    match orientation:
        case Orientation.HORIZONTAL:
            # get all current y-ticklabels
            y_ticklabels = [item.get_text() for item in ax.get_yticklabels()]
            # change text of all ticklabels
            for i in range(0, len(y_ticklabels)):
                # figure out if question type is SINGLE or MULTIPLE_CHOICE
                question_type = survey.get_question_type(question=question)
                label = ""
                if question_type == QuestionType.SINGLE_CHOICE:
                    label = survey.questions.choices[question][y_ticklabels[i]]
                elif question_type == QuestionType.MULTIPLE_CHOICE:
                    label = survey.questions.choices[y_ticklabels[i]]["Y"]
                # wrap labels
                y_ticklabels[i] = "\n".join(wrap(label, text_wrap))
            # update labels
            ax.set_yticks(range(len(data_df)))
            ax.set_yticklabels(y_ticklabels, fontsize=fontsize)
        case Orientation.VERTICAL:
            # get all current x-ticklabels
            x_ticklabels = [item.get_text() for item in ax.get_xticklabels()]
            # change text of all ticklabels
            for i in range(0, len(x_ticklabels)):
                # figure out if question type is SINGLE or MULTIPLE_CHOICE
                question_type = survey.get_question_type(question=question)
                label = ""
                if question_type == QuestionType.SINGLE_CHOICE:
                    label = survey.questions.choices[question][x_ticklabels[i]]
                elif question_type == QuestionType.MULTIPLE_CHOICE:
                    label = survey.questions.choices[x_ticklabels[i]]["Y"]
                # wrap labels
                x_ticklabels[i] = "\n".join(wrap(label, text_wrap))
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
    # rename legend and move below N
    handles, labels = ax.get_legend_handles_labels()
    for i in range(0, len(labels)):
        label = survey.questions.choices[question][labels[i]]
        labels[i] = "\n".join(wrap(label, 30))
    ax.legend(handles=handles, labels=labels, bbox_to_anchor=(1, 0.97))

    return ax
