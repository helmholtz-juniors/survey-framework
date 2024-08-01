from textwrap import wrap

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ..data_import.data_import import LimeSurveyData
from . import helmholtzcolors as hc
from .helper_barplots import add_axes_labels
from .helper_plotenums import BarLabels, PercentCount


def plot_bar_side_by_side(
    survey: LimeSurveyData,
    data_left: pd.DataFrame,
    data_right: pd.DataFrame,
    y_left: str,
    y_right: str,
    color_left: str = hc.helmholtzblue,
    color_right: str = hc.helmholtzgreen,
    title_left: str = "",
    title_right: str = "",
    width: int = 12,
    height: int = 10,
) -> tuple[Figure, tuple[Axes, Axes]]:
    """_summary_

    Args:
        survey (LimeSurveyData): The survey object.
        data_left (pd.DataFrame): Data for the left plot.
        data_right (pd.DataFrame): Data for the right plot.
        y_left (str): Question ID (left)
        y_right (str): Question ID (right)
        color_left (str, optional): Bar color (left). Defaults to hc.helmholtzblue.
        color_right (str, optional): Bar color (right). Defaults to hc.helmholtzgreen.
        title_left (str, optional): Left plot title. Defaults to "".
        title_right (str, optional): Right plot title. Defaults to "".
        width (int, optional): Total plot width. Defaults to 12.
        height (int, optional): Total plot height. Defaults to 10.

    Returns:
        tuple[plt.figure, plt.axes]: New Figure and Axes
    """
    # TODO: check if this signature is flexible enough.
    #       What about percentCount, fontsize, etc?

    # set seaborn theme
    hc.set_plotstyle()

    # define figure and axis
    # nrows, ncols = number of rows, columns of the subplot grid
    # sharey = share the Y axis
    # https://stackoverflow.com/questions/16150819/common-xlabel-ylabel-for-matplotlib-subplots
    figure, axs = plt.subplots(
        nrows=1, ncols=2, dpi=300, figsize=(width, height), sharey=True
    )
    ax0: Axes = axs[0]  # type: ignore [index] # axs is an 2x1 ndarray
    ax1: Axes = axs[1]  # type: ignore [index] # (see matplotlib docs)

    # determine order according to answers
    order_left = [i for i in survey.questions.choices[y_left]]
    order_right = [i for i in survey.questions.choices[y_right]]

    # .loc[:,var] -> left side is for index, right side for column
    # make countplots for total numbers
    plot_left = sns.countplot(
        ax=ax0, data=data_left, y=y_left, color=color_left, order=order_left
    )
    plot_right = sns.countplot(
        ax=ax1, data=data_right, y=y_right, color=color_right, order=order_right
    )

    # remove spines from figure
    ax0.spines["top"].set_visible(False)
    ax0.spines["right"].set_visible(False)
    ax0.spines["bottom"].set_visible(False)
    ax0.spines["left"].set_visible(False)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["left"].set_visible(False)

    # set xlim equal on both sides
    ax0.set_xlim(ax1.get_xlim())

    # flip left side
    # https://stackoverflow.com/questions/68858330/right-align-horizontal-seaborn-barplot
    ax0.invert_xaxis()
    ax0.yaxis.tick_right()

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

    add_axes_labels(ax0, BarLabels.PERCENT, PercentCount.COUNT, N_left, 11)
    add_axes_labels(ax1, BarLabels.PERCENT, PercentCount.COUNT, N_right, 11)

    # get titles
    if title_left == "":
        title_left = survey.questions.label[y_left]
    if title_right == "":
        title_right = survey.questions.label[y_right]

    # set titles
    plot_left.set_title("\n".join(wrap(title_left, 40)), fontsize=14)
    plot_right.set_title("\n".join(wrap(title_right, 40)), fontsize=14)

    # set y axis big label to ""
    ax0.set_ylabel("")
    ax1.set_ylabel("")

    # set y axis small labels; labels on the right side are not shown
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

    plt.text(0, 0.99, f"N = {N_left}", ha="left", va="top", transform=ax0.transAxes)
    plt.text(
        0.99, 0.99, f"N = {N_right}", ha="right", va="top", transform=ax1.transAxes
    )

    return figure, (ax0, ax1)
