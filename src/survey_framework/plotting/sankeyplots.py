import ausankey as sky  # type: ignore[import-untyped]
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from .helmholtzcolors import set_plotstyle


def plot_sankey(
    data_df: pd.DataFrame,
    titles: list[str] | None = None,
    title: str = "",
    width: float = 6,
    height: float = 8,
    fontsize: int | None = None,
    plot_fractions: bool = True,
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
    set_plotstyle()

    # Colors
    color_dict = {}
    colors = sns.color_palette("Paired").as_hex()

    # Take one color for each label on the left side
    for i, row in enumerate(data_df[0].unique()):
        color_dict[row] = colors[i]

    # Plot
    fig, ax = plt.subplots(dpi=300, figsize=(width, height), layout="constrained")

    sky.sankey(
        data_df,
        ax=ax,
        sort="none",  # keep dataframe ordering
        titles=titles,
        valign="center",
        color_dict=color_dict,
        node_gap=0.02,
        frame_gap=0,  # remove whitespace above/below
        value_loc="both" if plot_fractions else "none",
        value_thresh_ofmax=0.01,  # prevent label clashes
        fontsize=fontsize,
    )

    return fig
