from typing import Literal, cast

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import to_rgb
from matplotlib.figure import Figure
from matplotlib.legend_handler import HandlerTuple
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter

import survey_framework.plotting.helmholtzcolors as hc


def rgb2gray(rgb: tuple[float, float, float]) -> float:
    """Helper that converts a colour to a greyscale value.

    Args:
        rgb: tuple of red, green, and blue floats

    Returns:
        greyscale float
    """
    # magic numbers: https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
    return float(np.dot(rgb, [0.2989, 0.5870, 0.1140]))


def plot_stacked_bar_comparison(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    col_of_interest: str,
    plot_title: str,
    order: list[str],
    legend_loc: Literal["top", "right", "bottom"] | None,
    group_labels: tuple[str, str] = ("Group 1", "Group 2"),
    colors: list[list[tuple[float, float, float]]] | None = None,
    width: float = 3,
    height: float = 4,
    ax: Axes | None = None,
    n_y_pos: float = 0.95,
) -> tuple[Figure, Axes]:
    """
    Create a vertical stacked bar plot of mental health classes for two groups.

    Args:
        df1: DataFrame for group 1 (left bar).
        df2: DataFrame for group 2 (right bar).
        col_of_interest: Data column to plot (stacked)
        plot_title: Heading for this plot
        order: Ordered list of categories for stacked bars and legend.
        legend_loc: Position of the legend, or None for no legend.
        group_labels: Tuple of group labels.
        colors: Optional list of colors (auto-generated from helmholtzcolors if None).
        width: Width of the plot.
        height: Height of the plot.
        ax: Axes to draw the plot on. Generate a new Axes if None (default).
        n_y_pos: vertical position of the N labels (default: 95% plot height)

    Returns:
        Matplotlib figure and axis.
    """
    hc.set_plotstyle()
    # Use Helmholtz color palette if not provided
    if colors is None:
        # Create group-specific color palettes
        colors = [
            list(reversed(hc.get_blues(len(order)))),  # Group 1 (df1): blues
            list(reversed(hc.get_greens(len(order)))),  # Group 2 (df2): greens
        ]

    # Normalize counts to proportions
    def get_distribution(df: pd.DataFrame) -> "pd.Series[float]":
        return (
            df[f"{col_of_interest}"]
            .value_counts(normalize=True)
            .reindex(order, fill_value=0)
        )

    dist1 = get_distribution(df1)
    dist2 = get_distribution(df2)
    distributions = [dist1, dist2]

    if ax is None:
        fig, ax = plt.subplots(figsize=(width, height), dpi=300, layout="constrained")
    else:
        fig = cast(Figure, ax.figure)
    x_positions = [0, 1]

    for i, dist in enumerate(distributions):
        # Count valid responses (non-NaN) for each group
        n_group1 = df1[col_of_interest].notna().sum()
        n_group2 = df2[col_of_interest].notna().sum()

        # Add N labels inside each bar
        ax.text(
            x_positions[0],
            n_y_pos,
            f"N = {n_group1}",
            ha="center",
            va="center",
            # color="black",
            fontsize=9,
        )

        ax.text(
            x_positions[1],
            n_y_pos,
            f"N = {n_group2}",
            ha="center",
            va="center",
            # color="black",
            fontsize=9,
        )
        bottom = 0.0
        for j, category in enumerate(order):
            height_pct = dist[category]
            # plot a stacked bar
            ax.bar(
                x=x_positions[i],
                height=height_pct,
                bottom=bottom,
                color=colors[i][j],
                edgecolor="white",
                width=0.6,
                label=category if i == 0 else None,
            )
            if height_pct > 0.05:
                # put a percent label into the bar
                ax.text(
                    x_positions[i],
                    bottom + height_pct / 2,
                    f"{height_pct * 100:.1f}%",
                    ha="center",
                    va="center",
                    fontsize=9,
                    color="black" if rgb2gray(colors[i][j]) > 0.5 else "white",
                )
            bottom += height_pct

    ax.set_xticks(x_positions)
    ax.set_xticklabels(group_labels)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Percent")
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    ax.set_title(f"{plot_title}")

    if legend_loc is not None:
        legend_handles = []
        for i, label in enumerate(order):
            patch1 = Patch(color=colors[0][i])
            patch2 = Patch(color=colors[1][i])
            legend_handles.append(((patch1, patch2), label))

        # Now create the legend with a custom handler
        match legend_loc:
            case "right":
                ax.legend(
                    handles=[h[0] for h in legend_handles][::-1],
                    labels=[h[1] for h in legend_handles][::-1],
                    handler_map={tuple: HandlerTuple(ndivide=None)},
                    loc="upper left",  # Align legend's top-left corner
                    bbox_to_anchor=(1.02, 1),  # Place it just outside top-right of plot
                    ncol=1,  # Vertical legend
                )
            case "bottom":
                ax.legend(
                    handles=[h[0] for h in legend_handles][::-1],
                    labels=[h[1] for h in legend_handles][::-1],
                    handler_map={tuple: HandlerTuple(ndivide=None)},
                    loc="upper center",  # yes, "upper" is intentional
                    bbox_to_anchor=(0.5, -0.1),  # legend below the plot
                    ncol=1,  # Spread legend entries in one row
                )
            case "top":
                ax.legend(
                    handles=[h[0] for h in legend_handles][::-1],
                    labels=[h[1] for h in legend_handles][::-1],
                    handler_map={tuple: HandlerTuple(ndivide=None)},
                    loc="lower center",  # yes, "lower" is intentional
                    bbox_to_anchor=(0.5, 1.03),  # legend above the plot
                    ncol=1,  # Spread legend entries in one row
                )

    return fig, ax


def plot_stacked_bar_single(
    df1: pd.DataFrame,
    col_of_interest: str,
    plot_title: str,
    order: list[str],
    legend_loc: Literal["top", "right", "bottom"] | None,
    colors: list[list[tuple[float, float, float]]] | None = None,
    width: float = 3,
    height: float = 4,
    ax: Axes | None = None,
    n_y_pos: float = 0.95,
) -> tuple[Figure, Axes]:
    """
    Create a vertical stacked bar plot of mental health classes for one group.

    NOTE: This is a quick-fix. It might make sense to merge it with
    histplot.py/simple_histplot() where stacking should be implemented anyway

    Args:
        df1: DataFrame for group 1 (left bar).
        col_of_interest: Data column to plot (stacked)
        plot_title: Heading for this plot
        order: Ordered list of categories for stacked bars and legend.
        legend_loc: Position of the legend, or None for no legend.
        group_labels: Tuple of group labels.
        colors: Optional list of colors (auto-generated from helmholtzcolors if None).
        width: Width of the plot.
        height: Height of the plot.
        ax: Axes to draw the plot on. Generate a new Axes if None (default).
        n_y_pos: vertical position of the N labels (default: 95% plot height)

    Returns:
        Matplotlib figure and axis.
    """
    hc.set_plotstyle()
    # Use Helmholtz color palette if not provided
    if colors is None:
        # Create group-specific color palettes
        colors = [
            list(reversed(hc.get_blues(len(order)))),  # Group 1 (df1): blues
        ]

    # Normalize counts to proportions
    def get_distribution(df: pd.DataFrame) -> "pd.Series[float]":
        return (
            df[f"{col_of_interest}"]
            .value_counts(normalize=True)
            .reindex(order, fill_value=0)
        )

    dist1 = get_distribution(df1)
    distributions = [dist1]

    if ax is None:
        fig, ax = plt.subplots(figsize=(width, height), dpi=300, layout="constrained")
    else:
        fig = cast(Figure, ax.figure)
    x_positions = [0]

    for i, dist in enumerate(distributions):
        # Count valid responses (non-NaN) for each group
        n_group1 = df1[col_of_interest].notna().sum()

        # Add N labels inside each bar
        ax.text(
            x_positions[0],
            n_y_pos,
            f"N = {n_group1}",
            ha="center",
            va="center",
            # color="black",
            fontsize=9,
        )

        bottom = 0.0
        for j, category in enumerate(order):
            height_pct = dist[category]
            # plot a stacked bar
            ax.bar(
                x=x_positions[i],
                height=height_pct,
                bottom=bottom,
                color=colors[i][j],
                edgecolor="white",
                width=0.6,
                label=category if i == 0 else None,
            )
            if height_pct > 0.05:
                # put a percent label into the bar
                ax.text(
                    x_positions[i],
                    bottom + height_pct / 2,
                    f"{height_pct * 100:.1f}%",
                    ha="center",
                    va="center",
                    fontsize=9,
                    color="black" if rgb2gray(colors[i][j]) > 0.5 else "white",
                )
            bottom += height_pct

    ax.set_xticks(x_positions)
    ax.set_xticklabels([""])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Percent")
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    ax.set_title(f"{plot_title}")

    if legend_loc is not None:
        legend_handles = []
        for i, label in enumerate(order):
            patch1 = Patch(color=colors[0][i])
            # patch2 = Patch(color=colors[1][i])
            # legend_handles.append(((patch1, patch2), label))
            legend_handles.append(((patch1), label))

        # Now create the legend with a custom handler
        match legend_loc:
            case "right":
                ax.legend(
                    handles=[h[0] for h in legend_handles][::-1],
                    labels=[h[1] for h in legend_handles][::-1],
                    handler_map={tuple: HandlerTuple(ndivide=None)},
                    loc="upper left",  # Align legend's top-left corner
                    bbox_to_anchor=(1.02, 1),  # Place it just outside top-right of plot
                    ncol=1,  # Vertical legend
                )
            case "bottom":
                ax.legend(
                    handles=[h[0] for h in legend_handles][::-1],
                    labels=[h[1] for h in legend_handles][::-1],
                    handler_map={tuple: HandlerTuple(ndivide=None)},
                    loc="upper center",  # yes, "upper" is intentional
                    bbox_to_anchor=(0.5, -0.1),  # legend below the plot
                    ncol=1,  # Spread legend entries in one row
                )
            case "top":
                ax.legend(
                    handles=[h[0] for h in legend_handles][::-1],
                    labels=[h[1] for h in legend_handles][::-1],
                    handler_map={tuple: HandlerTuple(ndivide=None)},
                    loc="lower center",  # yes, "lower" is intentional
                    bbox_to_anchor=(0.5, 1.03),  # legend above the plot
                    ncol=1,  # Spread legend entries in one row
                )

    return fig, ax


def plot_stacked_bar_categorical(
    df: pd.DataFrame,
    classes_column: str,
    category_column: str,
    na_values: bool = False,
    label_q_data: str = "",
    width: int = 6,
    height: int = 4,
    fontsize: int | None = None,
    fontsize_axes_labels: int | None = None,
    legend_title: str = "",
    category_order: list[str] | None = None,
) -> tuple[Figure, Axes]:
    """This might be what we want instead of the above --
    arbitrary number of bars supported. Code needs a cleanup though.

    Args:
        df: _description_
        classes_column: _description_
        category_column: _description_
        na_values: _description_. Defaults to False.
        label_q_data: _description_. Defaults to "".
        width: _description_. Defaults to 6.
        height: _description_. Defaults to 4.
        fontsize: _description_. Defaults to None.
        fontsize_axes_labels: _description_. Defaults to None.
        legend_title: _description_. Defaults to "".
        category_order: _description_. Defaults to None.

    Returns:
        tuple[Figure, Axes]: _description_
    """
    hc.set_plotstyle()

    year_categories = (
        list(df[category_column].cat.categories)
        if isinstance(df[category_column].dtype, pd.CategoricalDtype)
        else sorted(df[category_column].unique())
    )
    n_years = len(year_categories)
    bar_width, bar_gap = 0.8, 0.1
    x_positions = np.arange(n_years) * (bar_width + bar_gap)
    fig, ax = plt.subplots(figsize=(width, height), layout="constrained")

    if category_order:
        category_order_mod = category_order.copy()
        if "NA" not in category_order_mod:
            category_order_mod.append("NA")
    else:
        all_classes = df[classes_column]
        if isinstance(all_classes.dtype, pd.CategoricalDtype):
            category_order_mod = list(all_classes.cat.categories)
            if "NA" not in category_order_mod:
                category_order_mod.append("NA")
        else:
            category_order_mod = ["NA"] + sorted(all_classes.dropna().unique())

    n_resp = len(category_order_mod)
    colors_list = (
        [to_rgb(hc.grey), *hc.get_blues(n_resp - 1)[::-1]]
        if na_values
        else list(hc.get_blues(n_resp)[::-1])
    )
    color_mapping = {
        cat: color for cat, color in zip(category_order_mod, colors_list, strict=True)
    }

    for i, yr in enumerate(year_categories):
        subset = df[df[category_column] == yr]
        n_question = len(subset)
        classes = subset[classes_column].fillna("NA")
        class_counts = classes.value_counts().reindex(category_order_mod, fill_value=0)
        class_percentages = class_counts / class_counts.sum() * 100

        bottom = 0
        for cat in category_order_mod:
            perc = class_percentages[cat]
            if perc == 0:
                continue
            ax.bar(
                x_positions[i],
                perc,
                bottom=bottom,
                width=bar_width,
                color=color_mapping[cat],
                label=cat if i == 0 else None,
            )

            # always percentage label, centered in segment
            ax.text(
                x_positions[i],
                bottom + perc / 2,
                f"{perc:.1f}%",
                ha="center",
                va="center",
                fontsize=fontsize_axes_labels,
                color="black" if rgb2gray(color_mapping[cat]) > 0.5 else "white",
            )
            bottom += perc

        ax.text(
            x_positions[i],
            bottom + 1,
            f"N = {n_question}",
            ha="center",
            va="bottom",
            fontsize=fontsize,
        )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(year_categories, fontsize=fontsize)
    ax.set_ylabel("Percentage", fontsize=fontsize)
    ax.set_xlabel(label_q_data, fontsize=fontsize)

    handles, labels_leg = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        labels_leg,
        title=legend_title,
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
        fontsize=fontsize,
        title_fontsize=fontsize_axes_labels,
    )

    return fig, ax
