from enum import Enum, StrEnum
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from textwrap import wrap
import numpy as np
import matplotlib.ticker as mtick
from textwrap import wrap
import pandas as pd

import plotting.helmholtzcolors as hc
from data_import.data_import import LimeSurveyData
from data_analysis.analysis import get_data_for_q
from plotting.plotenums import PercentCount, ShowAxesLabel
from plotting.plots import add_axes_labels, add_tick_labels, plot_barplot

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Literal


def plot_bar(
    survey: LimeSurveyData,
    data_df: pd.DataFrame,
    question: str,
    n_question: int,
    label_q_data: str = "",
    orientation: Literal["v", "h"] = "h",
    percentcount: PercentCount = PercentCount.COUNT,
    fig_size_x: int = 16,
    fig_size_y: int = 10,
    fontsize: int = 10,
    show_axes_labels: ShowAxesLabel = ShowAxesLabel.NONE,
    text_wrap: int = 25,
) -> tuple[Axes, Figure, Axes]:
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
        tuple[plt.figure, plt.axes]: _description_
    """

    # plot barplot
    fig, ax, plot = plot_barplot(
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

    # add bar labels
    fig, ax = add_axes_labels(
        fig=fig,
        ax=ax,
        data_df=data_df,
        orientation=orientation,
        show_axes_labels=show_axes_labels,
    )

    plot = add_tick_labels(
        survey=survey,
        plot=plot,
        data_df=data_df,
        question=question,
        orientation=orientation,
        fontsize=fontsize,
        text_wrap=text_wrap,
    )

    # add general labels to axes
    match orientation:
        case "h":
            ax.set(xlabel=percentcount, ylabel=label_q_data)
        case "v":
            ax.set(xlabel=label_q_data, ylabel=percentcount)

    ax.autoscale()
    ax.set_autoscale_on(True)

    return plot, fig, ax
