from collections.abc import Iterable, Sequence
from textwrap import wrap
from typing import cast

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from matplotlib.ticker import PercentFormatter

from survey_framework.order.shortening import SHORTENED

from ..data_import.data_import import LimeSurveyData, QuestionType
from .helmholtzcolors import (
    get_blues,
    get_greens,
    helmholtzblue,
    helmholtzgreen,
    set_plotstyle,
)
from .helper_plotenums import (
    BarLabels,
    Orientation,
    PlotStat,
    PlotType,
)


def add_bar_labels(
    ax: Axes,
    show_axes_labels: BarLabels,
    percentcount: PlotStat,
    n_question: int | None,
    fontsize: int | None = None,
    rotation: int = 0,
) -> Axes:
    """
    add labels to each bar in a bar plot

    Args:
        ax (Axes): matplotlib.axes
        show_axes_labels (ShowAxesLabel): whether axes labels should be shown
        percentcount (PercentCount): whether the data plotted is absolute or relative
        n_question (int): the total number of answers, needed for percent calculation
        fontsize (int): font size for the bar labels

    Returns:
        Axes: modified axes
    """

    # Define a label formatter.
    # This is straightforward if the plotted number is the one to be shown.
    # If not, calculate the value to be displayed using N.
    def fmt(n: float) -> str:
        match show_axes_labels, percentcount:
            case BarLabels.COUNT, PlotStat.COUNT:
                return f"{n:g}"
            case BarLabels.PERCENT, PlotStat.PERCENT:
                return f"{n:.1f}%"
            case BarLabels.PERCENT, PlotStat.PROPORTION:
                return f"{n * 100:.1f}%"
            case BarLabels.PERCENT, PlotStat.COUNT:
                assert n_question is not None, "cannot calculate percentage"
                return f"{n * 100 / n_question:.1f}%"
            case BarLabels.COUNT, _:
                raise NotImplementedError(
                    "Percentages on axis with absolute counts on bars not implemented."
                )
            case BarLabels.NONE, _:
                return ""
        # match is exhaustive, but mypy doesn't get that
        raise AssertionError("unreachable")

    # actually label the bars, using matplotlib sugar
    for bc in cast(Iterable[BarContainer], ax.containers):
        ax.bar_label(bc, padding=1, fontsize=fontsize, fmt=fmt, rotation=rotation)

    return ax


def plot_barplot(
    data_df: pd.DataFrame,
    question: str,
    orient: Orientation,
    stat: PlotStat,
    width: float,
    height: float,
    comparison: PlotType = PlotType.SINGLE_Q,
    hue: str | None = None,
    hue_order: Sequence[str] | None = None,
) -> tuple[Figure, Axes]:
    """
    plot bar plot with processed data

    Args:
        data_df: dataframe with processed data
        question: question codename
        orient: orientation of the plot (horizontal / vertical)
        stat: whether the plot shows counts or percentages
        width: x-axis size of figure
        height: y-axis size of figure
        hue: DF column to use for hue. If None (default), use answer choices for hue.
        hue_order: order within hue to enforce consistent coloring. Defaults to None.

    Returns:
        tuple[Figure, Axes]: modified figure and axes
    """

    # built input for hue and colors for plotting
    hue_input = list()
    colors: list[str] | list[tuple[float, float, float]] = list()
    match comparison:
        case PlotType.MULTI_Q:
            # if it's a comparison bar plot, hue needs to be filled
            # with a list of comparison data
            hue_input = list(data_df[hue])
            colors = get_blues(len(data_df[hue].value_counts()))
        case PlotType.SINGLE_Q:
            # otherwise, hue needs to be equal to the question data
            hue_input = list(data_df[question])
            colors = get_blues(len(data_df))
        case PlotType.SINGLE_Q_COMPARISON:
            hue_input = list(data_df[hue])
            assert len(data_df[hue].value_counts() == 2)
            colors = [helmholtzblue, helmholtzgreen]
        case PlotType.MULTI_Q_COMPARISON:
            raise NotImplementedError("multi-question comparison not yet supported")

    # set seaborn style
    set_plotstyle()

    # initialize plot and set colors
    fig, ax = plt.subplots(dpi=300, figsize=(width, height), layout="constrained")

    # plot graphs
    match orient:
        case Orientation.HORIZONTAL:
            # x = data, y = labels
            ax = sns.barplot(
                x=data_df[stat.value],
                y=list(data_df[question]),
                hue=hue_input,
                hue_order=hue_order,
                palette=colors,
                orient="h",
            )
        case Orientation.VERTICAL:
            # x = labels, y = data
            ax = sns.barplot(
                y=data_df[stat.value],
                x=list(data_df[question]),
                hue=hue_input,
                hue_order=hue_order,
                palette=colors,
                orient="v",
            )

    return fig, ax


def add_tick_labels(
    survey: LimeSurveyData,
    ax: Axes,
    question: str,
    orientation: Orientation,
    text_wrap: int,
    fontsize: int | None = None,
) -> Axes:
    """
    add axis labels for question
    horizontal --> add labels to y-axis
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
    # maximum allowed lines of text for each tick label.
    max_lines = 3

    # function to rename a single label using the survey data
    def renamed(label: str, max_lines: int) -> str:
        # get labels from survey data
        match survey.get_question_type(question=question):
            case QuestionType.SINGLE_CHOICE:
                lookup_name = survey.questions.choices[question].get(label)
                new_label = label if lookup_name is None else lookup_name
            case QuestionType.MULTIPLE_CHOICE:
                new_label = survey.questions.choices[label]["Y"]
            case other:
                raise NotImplementedError(f"Labels for {other} not implemented.")
        # clean up & shorten labels
        new_label = new_label.replace("/", " / ")
        new_label = new_label.replace("doctoral researcher", "DR")
        new_label = new_label.replace("Doctoral researcher", "DR")
        new_label = new_label.replace(", please specify", "")
        # wrap labels
        if new_label in SHORTENED and SHORTENED[new_label] != "":
            new_label = SHORTENED[new_label]
        return "\n".join(wrap(new_label, text_wrap, max_lines=max_lines))

    # match on orientation of plot
    match orientation:
        case Orientation.HORIZONTAL:
            # get all current y-ticklabels
            y_ticklabels = [
                renamed(item.get_text(), max_lines) for item in ax.get_yticklabels()
            ]
            # update labels
            ax.set_yticks(ax.get_yticks())
            ax.set_yticklabels(y_ticklabels, fontsize=fontsize)

        case Orientation.VERTICAL:
            # get all current x-ticklabels
            # if the number of tick labels is more than 5, reduce the number of
            # allowed lines of text for each tick label to prevent spatial collisions
            if len(ax.get_xticklabels()) > 5:
                max_lines = 2
            x_ticklabels = [
                renamed(item.get_text(), max_lines) for item in ax.get_xticklabels()
            ]
            # update labels
            ax.set_xticks(ax.get_xticks())
            ax.set_xticklabels(
                x_ticklabels,
                fontsize=fontsize,
                rotation=45,
                ha="right",
                rotation_mode="anchor",
                linespacing=0.9,
            )

    return ax


def adapt_legend(
    survey: LimeSurveyData,
    ax: Axes,
    question: str,
    text_wrap: int,
    group_n: dict[str, int] | None = None,
    anchor: tuple[float, float] | None = None,
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
    for i, old_label in enumerate(labels):
        if group_n is not None:
            # This legend is for a comparison plot. Keep the label, just add the given N
            label = f"{old_label} ({group_n[old_label]})"
        else:
            # Just rename the label, assuming it is a valid question ID
            label = survey.get_choices(question)[old_label]
        labels[i] = "\n".join(wrap(label, text_wrap))
    ax.legend(handles=handles, labels=labels, bbox_to_anchor=anchor)

    return ax


def get_hue_left(
    data_df: pd.DataFrame, hue: str
) -> tuple[list[str], list[tuple[float, float, float]]]:
    hue_input = list()
    colors = list()
    hue_input = list(data_df[hue])
    colors = get_blues(len(data_df[hue].value_counts()))

    return hue_input, colors


def get_hue_right(
    data_df: pd.DataFrame, hue: str
) -> tuple[list[str], list[tuple[float, float, float]]]:
    hue_input = list()
    colors = list()
    hue_input = list(data_df[hue])
    colors = get_greens(len(data_df[hue].value_counts()))

    return hue_input, colors


def label_axes(
    ax: Axes, orientation: Orientation, label_q_data: str, stat: PlotStat
) -> None:
    prop_fmt = PercentFormatter(1.0, symbol=None)
    perc_fmt = PercentFormatter(100, symbol=None)
    match orientation:
        case Orientation.HORIZONTAL:
            ax.set(ylabel=label_q_data)
            match stat:
                case PlotStat.PROPORTION:
                    ax.xaxis.set_major_formatter(prop_fmt)
                    ax.xaxis.set_label_text("Percent")
                case PlotStat.PERCENT:
                    ax.xaxis.set_major_formatter(perc_fmt)
                    ax.xaxis.set_label_text("Percent")
                case PlotStat.COUNT:
                    ax.xaxis.set_label_text(stat.capitalize())
        case Orientation.VERTICAL:
            ax.set(xlabel=label_q_data)
            match stat:
                case PlotStat.PROPORTION:
                    ax.yaxis.set_major_formatter(prop_fmt)
                    ax.yaxis.set_label_text("Percent")
                case PlotStat.PERCENT:
                    ax.yaxis.set_major_formatter(perc_fmt)
                    ax.yaxis.set_label_text("Percent")
                case PlotStat.COUNT:
                    ax.yaxis.set_label_text(stat.capitalize())
