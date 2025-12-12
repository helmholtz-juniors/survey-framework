"""Functions for side-by-side horizontal bar plots."""

from textwrap import wrap
from typing import cast

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ..data_import.data_import import LimeSurveyData
from ._barplot_enums import BarLabels, Orientation, PlotStat
from ._barplots_helpers import (
    adapt_legend,
    add_bar_labels,
    add_tick_labels,
    get_hue_left,
    get_hue_right,
)
from .helmholtzcolors import helmholtzblue, helmholtzgreen, set_plotstyle


def plot_bar_side_by_side(
    survey: LimeSurveyData,
    data_left: pd.DataFrame,
    data_right: pd.DataFrame,
    y_left: str,
    y_right: str,
    stat: PlotStat = PlotStat.PERCENT,
    color_left: str = helmholtzblue,
    color_right: str = helmholtzgreen,
    title_left: str | None = None,
    title_right: str | None = None,
    width: float = 12,
    height: float = 10,
) -> tuple[Figure, tuple[Axes, Axes]]:
    """Plot two horizontal bar plots side-by-side, sharing a common y axis.

    Args:
        survey: The survey object.
        data_left: Data for the left plot.
        data_right: Data for the right plot.
        y_left: Question ID (left)
        y_right: Question ID (right)
        stat: Which metric to plot (percent / count)
        color_left: Bar color (left).
        color_right: Bar color (right).
        title_left: Left plot title.
        title_right: Right plot title.
        width: Total plot width.
        height: Total plot height.

    Returns:
        New Figure and Axes
    """
    # set seaborn theme
    set_plotstyle()

    # define figure and axis
    # nrows, ncols = number of rows, columns of the subplot grid
    # sharey = share the Y axis
    # https://stackoverflow.com/questions/16150819/common-xlabel-ylabel-for-matplotlib-subplots
    figure, axs = plt.subplots(
        nrows=1, ncols=2, dpi=300, figsize=(width, height), sharey=True
    )
    ax_left, ax_right = cast(tuple[Axes, Axes], axs)

    # determine order according to answers
    order_left = [i for i in survey.questions.choices[y_left]]
    order_right = [i for i in survey.questions.choices[y_right]]

    # .loc[:,var] -> left side is for index, right side for column
    # make countplots for total numbers
    plot_left = sns.countplot(
        ax=ax_left,
        data=data_left,
        y=y_left,
        color=color_left,
        order=order_left,
        stat=stat.value,
    )
    plot_right = sns.countplot(
        ax=ax_right,
        data=data_right,
        y=y_right,
        color=color_right,
        order=order_right,
        stat=stat.value,
    )

    # remove spines from figure
    # ax_left.spines["top"].set_visible(False)
    # ax_left.spines["right"].set_visible(False)
    # ax_left.spines["bottom"].set_visible(False)
    # ax_left.spines["left"].set_visible(False)
    # ax_right.spines["top"].set_visible(False)
    # ax_right.spines["right"].set_visible(False)
    # ax_right.spines["bottom"].set_visible(False)
    # ax_right.spines["left"].set_visible(False)

    # set xlim equal on both sides
    if stat == PlotStat.PERCENT:
        ax_left.set_xlim((0, 100))
        ax_right.set_xlim((0, 100))
    elif stat == PlotStat.PROPORTION:
        ax_left.set_xlim((0, 1))
        ax_right.set_xlim((0, 1))

    # flip left side
    # https://stackoverflow.com/questions/68858330/right-align-horizontal-seaborn-barplot
    ax_left.invert_xaxis()
    ax_left.yaxis.tick_right()
    ax_left.yaxis.set_ticks_position("none")

    # calculate how many people answered this question
    N_left = len(data_left.index)
    N_right = len(data_right.index)

    # show percentages behind bars
    # bar_container = cast(BarContainer, plot_left.containers[0])
    # bar_labels_left = [
    #     f"{i / N_left * 100:.1f}%" for i in list(bar_container.datavalues)
    # ]
    # plot_left.bar_label(bar_container, labels=bar_labels_left)

    # bar_container = cast(BarContainer, plot_right.containers[0])
    # bar_labels_right = [
    #     f"{i / N_right * 100:.1f}%" for i in list(bar_container.datavalues)
    # ]
    # plot_right.bar_label(bar_container, labels=bar_labels_right)

    add_bar_labels(ax_left, BarLabels.PERCENT, stat, n_question=N_left)
    add_bar_labels(ax_right, BarLabels.PERCENT, stat, n_question=N_right)

    # get titles
    if title_left is None:
        title_left = survey.questions.label[y_left]
    if title_right is None:
        title_right = survey.questions.label[y_right]

    # set titles
    plot_left.set_title("\n".join(wrap(title_left, 40)))
    plot_right.set_title("\n".join(wrap(title_right, 40)))

    # capitalize x axis label
    ax_left.set_xlabel(stat.capitalize())
    ax_right.set_xlabel(stat.capitalize())

    # empty y axis label
    ax_left.set_ylabel("")
    ax_right.set_ylabel("")

    # set y axis tick labels; labels on the right side are not shown
    # https://stackoverflow.com/questions/11244514/modify-tick-label-text
    y_ticklabels = [item.get_text() for item in plot_left.get_yticklabels()]
    for i in range(0, len(y_ticklabels)):
        label = survey.questions.choices[y_right][y_ticklabels[i]]
        y_ticklabels[i] = "\n".join(wrap(label, 20))
    plot_right.set_yticks(range(len(y_ticklabels)))
    plot_right.set_yticklabels(y_ticklabels)

    # more space between both subfigures
    # https://www.geeksforgeeks.org/how-to-set-the-spacing-between-subplots-in-matplotlib-in-python/
    figure.tight_layout(pad=0.5)

    plt.text(
        0, 0.01, f"N = {N_left}", ha="left", va="bottom", transform=ax_left.transAxes
    )
    plt.text(
        0.99,
        0.01,
        f"N = {N_right}",
        ha="right",
        va="bottom",
        transform=ax_right.transAxes,
    )

    return figure, (ax_left, ax_right)


# TODO: can we merge this into `plot_bar_side_by_side` with an optional hue parameter?
def plot_sidebyside_comparison_singleQ(
    survey: LimeSurveyData,
    data_left: pd.DataFrame,
    data_right: pd.DataFrame,
    base_q_left: str,
    base_q_right: str,
    comp_q: str,
    N_left: int,
    N_right: int,
    title_left: str = "",
    title_right: str = "",
    width: float = 12,
    height: float = 10,
    fontsize: int = 10,
    plot_stat: PlotStat = PlotStat.COUNT,
    bar_labels: BarLabels = BarLabels.NONE,
    fontsize_bar_labels: int = 10,
    text_wrap: int = 25,
) -> tuple[Figure, tuple[Axes, Axes]]:
    """Plot two barplots side by side, with an additional grouping given by `comp_q`.

    Args:
        survey: The main survey object
        data_left: Data for the left question
        data_right: Data for the right question
        base_q_left: Question code for the left question
        base_q_right: Question code for the right question
        comp_q: Question code that is used as a grouper (hue) for both questions
        N_left: Size of the left population
        N_right: Size of the right population
        title_left: Title for the left plot
        title_right: Title for the right plot
        width: Total width of the plot
        height: Total height of the plot
        fontsize: Font size for titles and axis (tick) labels
        plot_stat: Whether to plot absolute (PERCENT) or relative (COUNT)
        bar_labels: Whether to label each bar
        fontsize_bar_labels: Font size for the bar labels, if enabled above
        text_wrap: After how many characters axis and legend labels should wrap

    Returns:
        New matplotlib Figure and Axes for this bar plot.
    """
    # set seaborn theme
    set_plotstyle()

    figure, axs = plt.subplots(
        nrows=1, ncols=2, dpi=300, figsize=(width, height), sharey=True, layout="tight"
    )
    ax_left, ax_right = cast(tuple[Axes, Axes], axs)

    hue_input_left, colors_left = get_hue_left(data_left, comp_q)
    hue_input_right, colors_right = get_hue_right(data_right, comp_q)

    # left
    plot_left = sns.barplot(
        ax=ax_left,
        x=data_left[plot_stat.value],
        y=list(data_left[base_q_left]),
        hue=hue_input_left,
        palette=colors_left,
        orient="h",
    )
    # right
    plot_right = sns.barplot(
        ax=ax_right,
        x=data_right[plot_stat.value],
        y=list(data_right[base_q_right]),
        hue=hue_input_right,
        palette=colors_right,
        orient="h",
    )

    # remove spines from figure
    # ax_left.spines["top"].set_visible(False)
    # ax_left.spines["right"].set_visible(False)
    # ax_left.spines["bottom"].set_visible(False)
    # ax_left.spines["left"].set_visible(False)
    # ax_right.spines["top"].set_visible(False)
    # ax_right.spines["right"].set_visible(False)
    # ax_right.spines["bottom"].set_visible(False)
    # ax_right.spines["left"].set_visible(False)

    # set xlim equal on both sides
    if plot_stat == PlotStat.PERCENT:
        ax_left.set_xlim((0, 100))
        ax_right.set_xlim((0, 100))
    elif plot_stat == PlotStat.PROPORTION:
        ax_left.set_xlim((0, 1))
        ax_right.set_xlim((0, 1))

    # flip left side
    # https://stackoverflow.com/questions/68858330/right-align-horizontal-seaborn-barplot
    ax_left.invert_xaxis()
    ax_left.yaxis.tick_right()

    # add answer options as y tick labels between the two bar plots
    ax_left = add_tick_labels(
        survey=survey,
        ax=ax_left,
        # data_df=pd.DataFrame(data_left[base_q_left].value_counts()),
        question=base_q_left,
        orientation=Orientation.HORIZONTAL,
        fontsize=fontsize,
        text_wrap=text_wrap,
    )

    if title_left == "":
        title_left = (
            base_q_left
            + ": "
            + survey.questions.loc[
                survey.questions["question_group"] == base_q_left
            ].question_label.iloc[0]
        )
    if title_right == "":
        title_right = (
            base_q_right
            + ": "
            + survey.questions.loc[
                survey.questions["question_group"] == base_q_right
            ].question_label.iloc[0]
        )

    # set title
    plot_left.set_title(
        "\n".join(wrap(title_left, 60)),
        fontsize=fontsize,
    )
    plot_right.set_title(
        "\n".join(wrap(title_right, 60)),
        fontsize=fontsize,
    )

    # return figure, (ax_left, ax_right)

    # add bar labels (the ones on top or next to bars within the plot)
    plot_left = add_bar_labels(
        ax=ax_left,
        show_axes_labels=bar_labels,
        percentcount=plot_stat,
        n_question=N_left,
        fontsize=fontsize_bar_labels,
    )

    # adapt legend
    ax_left = adapt_legend(
        survey=survey,
        ax=ax_left,
        question=comp_q,
        text_wrap=text_wrap,
        anchor=(0.4, 0.18),
    )

    ax_right = adapt_legend(
        survey=survey,
        ax=ax_right,
        question=comp_q,
        text_wrap=text_wrap,
        anchor=(1, 0.18),
    )

    # set y axis big label to ""
    ax_left.set_ylabel("")
    ax_right.set_ylabel("")

    # add number of participants to top right corner
    ax_left.text(
        0, 0.01, f"N = {N_left}", ha="left", va="bottom", transform=ax_left.transAxes
    )
    ax_right.text(
        0.99,
        0.01,
        f"N = {N_right}",
        ha="right",
        va="bottom",
        transform=ax_right.transAxes,
    )

    return figure, (ax_left, ax_right)
