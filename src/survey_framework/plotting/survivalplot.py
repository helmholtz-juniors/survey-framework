from collections.abc import Callable, Iterable
from textwrap import wrap

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from . import helmholtzcolors as hc


def plot_survival_plot(
    df: pd.DataFrame,
    category: str | None = None,
    ticks: Iterable[int] | None = None,
    tick_map: Callable[[int], str] = str,
    legend_replace: dict[str, str] | None = None,
    legend_title: str | None = None,
    fig_size_x: int = 6,
    fig_size_y: int = 4,
) -> tuple[Figure, Axes]:
    """
    Plots the given DataFrame as a survival plot, approaching zero.

    Args:
        df: DataFrame with a column of numerical data called "data".
        category (optional): Column in `df` to categorize the data. Defaults to None.
        ticks (optional): Iterable of x axis ticks. Defaults to None.
        tick_map (optional): Function to generate strings from ticks. Defaults to str.
        legend_replace (optional): Replacements for legend entries. Defaults to None.
        legend_title (optional): Heading for the legend. Defaults to None.
        fig_size_x (optional): Horizontal figure size. Defaults to 6.
        fig_size_y (optional): Vertical figure size. Defaults to 4.

    Returns:
        tuple[Figure, Axes]: The matplotlib figure and axes.
    """
    if legend_replace is None:
        legend_replace = dict()
    hc.set_plotstyle()

    figure, axs = plt.subplots(
        dpi=300, figsize=(fig_size_x, fig_size_y), layout="constrained"
    )
    ax: Axes = axs

    if category:
        n_colors = len(pd.unique(df[category]))
        colors = hc.get_blues(n_colors)
    else:
        colors = None

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
                group_n = counts.iloc[int(label)]["data"]
            # also replace the label if it's in the replacement dictionary
            replacement = legend_replace.get(label, label)

            new_label = "\n".join(wrap(f"{replacement} ({group_n})", 25))
            tt.set_text(new_label)
        if legend_title:
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
