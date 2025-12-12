"""Survival Plots. Typically used to visualize change over time."""

from collections.abc import Callable, Iterable
from textwrap import wrap

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .helmholtzcolors import get_blues, set_plotstyle


def plot_survival_plot(
    df: pd.DataFrame,
    category: str | None = None,
    ticks: Iterable[int] | None = None,
    tick_map: Callable[[int], str] = str,
    legend_replace: dict[str, str] | None = None,
    legend_title: str | None = None,
    colors: list[tuple[float, float, float]] | None = None,
    width: int = 6,
    height: int = 4,
) -> tuple[Figure, Axes]:
    """Plots the given DataFrame as a survival plot, approaching zero.

    Args:
        df: DataFrame with a column of numerical data called "data".
        category: Column in `df` to categorize the data.
        ticks: Iterable of x axis ticks.
        tick_map: Function to generate strings from ticks.
        legend_replace: Replacements for legend entries.
        legend_title: Heading for the legend.
        colors: Line colors, instead of shades of blue.
        width: Horizontal figure size.
        height: Vertical figure size.

    Returns:
        The matplotlib figure and axes.
    """
    if legend_replace is None:
        legend_replace = dict()
    set_plotstyle()

    figure, ax = plt.subplots(dpi=300, figsize=(width, height), layout="constrained")

    if not colors and category:
        n_colors = len(pd.unique(df[category]))
        colors = get_blues(n_colors)

    sns.ecdfplot(
        data=df,
        ax=ax,
        x="data",  # hard-coded for simplicity
        hue=category,
        stat="percent",
        complementary=True,
        palette=colors,
    )

    if ticks:
        labels = map(tick_map, ticks)
        ax.set_xticks(list(ticks), labels)

    legend = ax.get_legend()
    if legend:
        # place the number of participants behind each category
        counts = df.groupby(category, observed=False).count()

        for tt in legend.get_texts():
            label = tt.get_text()
            # get number of participants...
            try:
                # ...for string keys
                group_n = counts.loc[label]["data"]
            except KeyError:
                # ...for integer keys
                group_n = counts.loc[int(label)]["data"]
            # also replace the label if it's in the replacement dictionary
            replacement = legend_replace.get(label, label)

            new_label = "\n".join(wrap(f"{replacement} ({group_n})", 25))
            tt.set_text(new_label)
        if legend_title is not None:
            legend.set_title(legend_title)
    else:
        # place the number of participants in the top right corner
        ax.text(
            0.99,
            0.99,
            f"N = {len(df)}",
            ha="right",
            va="top",
            transform=ax.transAxes,
        )

    return figure, ax
