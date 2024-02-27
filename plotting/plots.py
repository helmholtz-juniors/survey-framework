from textwrap import wrap
from matplotlib import pyplot as plt
import pandas as pd
from data_import.data_import import LimeSurveyData, QuestionType
from plotting.plotenums import PercentCount, ShowAxesLabel
import seaborn as sns
import plotting.helmholtzcolors as hc

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from typing import Literal, cast, Iterable


def add_axes_labels(
    fig: Figure,
    ax: Axes,
    data_df: pd.DataFrame,
    orientation: Literal["h", "v"],
    show_axes_labels: ShowAxesLabel,
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
        case "h":
            for rect, label in zip(rects, labels):
                # calculate y_value
                y_value = rect.get_y() + rect.get_height() / 2
                # calculate x_value
                x_value = rect.get_width()
                # add text to bar
                ax.text(x_value, y_value, label, ha="left", va="center")
        case "v":
            for rect, label in zip(rects, labels):
                # calculate x_value
                x_value = rect.get_x() + rect.get_width() / 2
                # calculate y_value
                y_value = rect.get_height()
                # add text to bar
                ax.text(x_value, y_value, label, ha="center", va="bottom")

    return fig, ax


def plot_barplot(
    data_df: pd.DataFrame,
    question: str,
    orientation: Literal["h", "v"],
    percentcount: PercentCount,
    fig_size_x: int,
    fig_size_y: int,
) -> tuple[Figure, Axes, Axes]:
    """
    plot bar plot with processed data

    Args:
        data_df (pd.DataFrame): dataframe with processed data
        question (str): str of question
        orientation (Orientation): orientation of plot
        percentcount (PercentCount): whether plot shows counts or percent
        fig_size_x (int): x-axis size of figure
        fig_size_y (int): y-axis size of figure

    Returns:
        tuple[Figure, Axes, Axes]: modified figure, axes and plot
    """

    # set seaborn style
    sns.set_style("darkgrid", {"axes.facecolor": "#f2f0f0"})

    # initialize plot and set colors
    fig, ax = plt.subplots(
        dpi=300, figsize=(fig_size_x, fig_size_y), layout="constrained"
    )
    colors = hc.get_blues(len(data_df))

    # plot graphs
    match percentcount:
        case PercentCount.COUNT:
            match orientation:
                case "h":
                    # counts + horizontal
                    plot = sns.barplot(
                        x=data_df["count"],
                        y=list(data_df[question]),
                        hue=list(data_df[question]),
                        palette=colors,
                        orient=orientation,
                    )
                case "v":
                    # counts + vertical
                    plot = sns.barplot(
                        y=data_df["count"],
                        x=list(data_df[question]),
                        hue=list(data_df[question]),
                        palette=colors,
                        orient=orientation,
                    )
        case PercentCount.PERCENT:
            match orientation:
                case "h":
                    # percentages + horizontal
                    plot = sns.barplot(
                        x=data_df["percentages"],
                        y=list(data_df[question]),
                        hue=list(data_df[question]),
                        palette=colors,
                        orient=orientation,
                    )
                case "v":
                    # percentages + vertical
                    plot = sns.barplot(
                        y=data_df["percentages"],
                        x=list(data_df[question]),
                        hue=list(data_df[question]),
                        palette=colors,
                        orient=orientation,
                    )

    return fig, ax, plot


def add_tick_labels(
    survey: LimeSurveyData,
    plot: Axes,
    data_df: pd.DataFrame,
    question: str,
    orientation: Literal["h", "v"],
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
        case "h":
            # get all current y-ticklabels
            y_ticklabels = [item.get_text() for item in plot.get_yticklabels()]
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
            plot.set_yticks(range(len(data_df)))
            plot.set_yticklabels(y_ticklabels, fontsize=fontsize)
        case "v":
            # get all current x-ticklabels
            x_ticklabels = [item.get_text() for item in plot.get_xticklabels()]
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
            plot.set_xticks(range(len(data_df)))
            plot.set_xticklabels(
                x_ticklabels,
                fontsize=fontsize,
                rotation=45,
                ha="right",
                rotation_mode="anchor",
            )

    return plot
