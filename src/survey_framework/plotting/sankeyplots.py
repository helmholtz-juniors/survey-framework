from textwrap import wrap

import ausankey as sky  # type: ignore
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from . import helmholtzcolors as hc


def plot_sankey(
    data_df: pd.DataFrame,
    titles: list[str] | None = None,
    title: str = "Two staged sanke diagram",
    width: int = 16,
    height: int = 30,
    fontsize: int = 15,
) -> Figure:
    """Plots a two staged sankey diagram

    Args:
        data_df (pd.DataFrame): Data containing rows like
            (label_left, count, label_right, same_count)
        titles (str, optional): Titles of both stages. Defaults to "".
        width (int, optional): Total plot width. Defaults to 12.
        height (int, optional): Total plot height. Defaults to 10.

    Returns:
        tuple[plt.figure, plt.axes]: New Figure and Axes
    """

    hc.set_plotstyle()

    # Colors
    color_dict = {}
    # colors = hc.get_blues(len(xxx["E9"].unique()))
    colors = sns.color_palette("Paired").as_hex()

    # Take one color for each label on the left side
    for i, row in enumerate(data_df[0].unique()):
        color_dict[row] = colors[i]

    # Plot
    figure = plt.figure(dpi=300, figsize=(width, height), layout="constrained")

    sky.sankey(
        data_df,
        sort="top",
        titles=titles,
        valign="center",
        color_dict=color_dict,
        # value_loc=["right", "left"],
        node_gap=0.04,
        fontsize=fontsize,
    )

    plt.title(
        "\n".join(wrap(title, 60)),
        fontsize=fontsize + 3,
    )

    return figure
