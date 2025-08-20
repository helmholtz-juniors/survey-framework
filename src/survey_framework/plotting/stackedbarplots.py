from textwrap import wrap

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from . import helmholtzcolors as hc

from ..data_import.data_import import LimeSurveyData
from ..plotting.helper_barplots import (
    adapt_legend,
    add_bar_labels,   # renamed from add_axes_labels
    add_tick_labels,
    plot_barplot,
)
from ..plotting.helper_plotenums import BarLabels, Orientation, PlotStat  # PercentCount -> PlotStat
from typing import cast, List, Optional
import seaborn as sns

def plot_stacked_bar(
    classes: pd.DataFrame,
    n_question: int,
    NA_Values: bool = False,
    label_q_data: str = "",
    orientation: Orientation = Orientation.HORIZONTAL,
    percentcount: PlotStat = PlotStat.PERCENT,   # default to percentages
    fig_size_x: int = 3.5,
    fig_size_y: int = 10,
    fontsize: int = 10,
    show_axes_labels: BarLabels = BarLabels.NONE,
    fontsize_axes_labels: int = 10,
    text_wrap: int = 25,
    legend_title: str = "Legend",
    legend_loc: str = "upper right",
    category_order: Optional[List[str]] = None
) -> tuple[Figure, Axes]:
    classes = classes.fillna("NA")
    class_counts = classes.value_counts()
    if category_order:
        category_order = category_order + ["NA"] if "NA" not in category_order else category_order
        class_counts = class_counts.reindex(category_order, fill_value=0)

    class_percentages = class_counts / class_counts.sum() * 100
    labels = class_percentages.index
    percentages = class_percentages.values

    colors = ([hc.grey] + hc.get_blues(len(labels) - 1)[::-1]) if NA_Values else hc.get_blues(len(labels))[::-1]

    fig, ax = plt.subplots(figsize=(fig_size_x, fig_size_y))

    bottom = 0
    for i, perc in enumerate(percentages):
        if perc == 0:
            continue
        ax.bar([""], [perc], bottom=bottom, label=f"{labels[i]} ({perc:.1f}%)", width=0.5, color=colors[i])

        # always percentage label, centered in segment
        ax.text(
            0,
            bottom + perc / 2,
            f"{perc:.1f}%",
            ha="center",
            va="center",
            fontsize=fontsize_axes_labels,
            color="white" if perc > 8 else "black",
        )
        bottom += perc

    plt.text(0.99, 0.99, f"N = {n_question}", ha="right", va="top", transform=ax.transAxes, fontsize=fontsize)

    # axis labels reflect percentages
    if orientation == Orientation.HORIZONTAL:
        ax.set(xlabel="Percent", ylabel=label_q_data)
    else:
        ax.set(xlabel=label_q_data, ylabel="Percent")

    handles, leg_labels = ax.get_legend_handles_labels()
    ax.legend(
        handles[::-1], leg_labels[::-1], title=legend_title,
        loc="upper center", bbox_to_anchor=(0.5, -0.1),
        fontsize=fontsize, title_fontsize=fontsize_axes_labels, frameon=True, ncol=1
    )
    plt.tight_layout(rect=[0, 0.1, 1, 1])
    return fig, ax

def plot_stacked_bar_by_year_side_by_side(
    df: pd.DataFrame,
    classes_column: str,
    year_column: str = "Year",
    NA_Values: bool = False,
    label_q_data: str = "",
    orientation: Orientation = Orientation.HORIZONTAL,
    percentcount: PlotStat = PlotStat.PERCENT,   # default to percentages
    fig_size_x: int = 10,
    fig_size_y: int = 5,
    fontsize: int = 10,
    show_axes_labels: BarLabels = BarLabels.NONE,
    fontsize_axes_labels: int = 10,
    text_wrap: int = 25,
    legend_title: str = "Legend",
    legend_loc: str = "upper right",
    category_order: Optional[List[str]] = None
) -> tuple[Figure, Axes]:
    year_categories = list(df[year_column].cat.categories) if pd.api.types.is_categorical_dtype(df[year_column]) else sorted(df[year_column].unique())
    n_years = len(year_categories)
    bar_width, bar_gap = 0.8, 0.1
    x_positions = np.arange(n_years) * (bar_width + bar_gap)
    fig, ax = plt.subplots(figsize=(fig_size_x, fig_size_y))

    if category_order:
        category_order_mod = category_order.copy()
        if "NA" not in category_order_mod:
            category_order_mod.append("NA")
    else:
        all_classes = df[classes_column]
        if pd.api.types.is_categorical_dtype(all_classes):
            category_order_mod = list(all_classes.cat.categories)
            if "NA" not in category_order_mod:
                category_order_mod.append("NA")
        else:
            category_order_mod = ["NA"] + sorted(all_classes.dropna().unique())

    n_resp = len(category_order_mod)
    colors_list = ([hc.grey] + list(hc.get_blues(n_resp - 1)[::-1])) if NA_Values else list(hc.get_blues(n_resp)[::-1])
    color_mapping = {cat: color for cat, color in zip(category_order_mod, colors_list)}

    for i, yr in enumerate(year_categories):
        subset = df[df[year_column] == yr]
        n_question = len(subset)
        classes = subset[classes_column].fillna("NA")
        class_counts = classes.value_counts().reindex(category_order_mod, fill_value=0)
        class_percentages = class_counts / class_counts.sum() * 100

        bottom = 0
        for cat in category_order_mod:
            perc = class_percentages[cat]
            if perc == 0:
                continue
            ax.bar(x_positions[i], perc, bottom=bottom, width=bar_width, color=color_mapping[cat], label=cat if i == 0 else None)

            # always percentage label, centered in segment
            ax.text(
                x_positions[i],
                bottom + perc / 2,
                f"{perc:.1f}%",
                ha="center",
                va="center",
                fontsize=fontsize_axes_labels,
                color="white" if perc > 8 else "black"
            )
            bottom += perc

        ax.text(x_positions[i], bottom + 1, f"N = {n_question}", ha="center", va="bottom", fontsize=fontsize)

    ax.set_xticks(x_positions)
    ax.set_xticklabels(year_categories, fontsize=fontsize)
    ax.set_ylabel("Percentage", fontsize=fontsize)
    ax.set_xlabel(label_q_data, fontsize=fontsize)

    handles, labels_leg = ax.get_legend_handles_labels()
    ax.legend(
        handles, labels_leg, title=legend_title,
        loc="upper left", bbox_to_anchor=(1.02, 1),
        fontsize=fontsize, title_fontsize=fontsize_axes_labels
    )
    plt.tight_layout()
    return fig, ax

def plot_bar(
    classes: pd.DataFrame,
    n_question: int,
    label_q_data: str = "",
    orientation: Orientation = Orientation.HORIZONTAL,
    percentcount: PlotStat = PlotStat.COUNT,  # type updated
    fig_size_x: int = 15,
    fig_size_y: int = 10,
    fontsize: int = 10,
    show_axes_labels: BarLabels = BarLabels.NONE,
    fontsize_axes_labels: int = 10,
    text_wrap: int = 25,
    legend_title: str = "Legend",
    legend_loc: Optional[str] = "upper right",  # Can now be None
    category_order: Optional[List[str]] = None
) -> tuple[Figure, Axes]:
    """
    Plot a simple bar chart (single variable distribution).
    """
    from matplotlib.ticker import FuncFormatter

    # Calculate counts and percentages
    class_counts = classes.value_counts()

    # Apply the category order if provided
    if category_order:
        class_counts = class_counts.reindex(category_order, fill_value=0)

    class_percentages = class_counts / class_counts.sum() * 100

    # Prepare data for plotting
    labels = class_percentages.index
    values = class_percentages.values

    colors = hc.get_blues(len(labels))[::-1]

    # Set seaborn/matplotlib style
    hc.set_plotstyle()

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(fig_size_x, fig_size_y))

    # Plot bars
    match orientation:
        case Orientation.HORIZONTAL:
            bars = ax.barh(
                labels,
                values,
                color=colors,
                edgecolor="black"
            )
        case Orientation.VERTICAL:
            bars = ax.bar(
                labels,
                values,
                color=colors,
                edgecolor="black"
            )

    # Add number of participants to the plot
    plt.text(
        0.99, 0.99,
        f"N = {n_question}",
        ha="right", va="top",
        transform=ax.transAxes,
        fontsize=fontsize
    )

    # Define a formatter function for percentages
    def percent_formatter(x, pos):
        return f"{x:.0f}%"

    # Add axis labels with percentage formatter
    if orientation == Orientation.HORIZONTAL:
        ax.set(xlabel="Percentage", ylabel=label_q_data)
        ax.xaxis.set_major_formatter(FuncFormatter(percent_formatter))
    else:
        ax.set(xlabel=label_q_data, ylabel="Percentage")
        ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

    # Add legend only if legend_loc is not None
    if legend_loc:
        ax.legend(
            [f"{label} ({value:.1f}%)" for label, value in zip(labels, values)],
            title=legend_title,
            loc=legend_loc,
            fontsize=fontsize,
            title_fontsize=fontsize_axes_labels,
            frameon=True
        )

    # Adjust layout
    plt.tight_layout()

    return fig, ax
