from collections.abc import Sequence

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame, Series

import survey_framework.plotting.helmholtzcolors as hc


def simple_histplot(
    data_df: DataFrame,
    question_code: str,
    order_dict: dict[str, list[str]],
    hue_series: "Series[str] | None" = None,
    hue_order: Sequence[str] | None = None,
    kde: bool = False,
    log_scale: bool = False,
    binwidth: int | None = None,
    width: int = 10,
    height: int = 6,
) -> tuple[Figure, Axes]:
    """Very simple histplot. Currently in experimental state, to be expanded
        for stacked barplots and KDE plots.

    Args:
        data_df: DataFrame to be plotted
        question_code: Column in `data_df` to be plotted
        order_dict: answer ordering, can be empty (ORDER from order/order2024.py)
        hue_series (Optional): Separator for data_df (needs same index).
        hue_order (Optional): How to sort hues in the legend and plot
        kde (Optional): Whether to plot a density curve. Defaults to False.
        binwidth (Optional): Width of bins; automatically inferred if not given.
        width (Optional): Plot width. Defaults to 10.
        height (Optional): Plot height. Defaults to 6.

    Returns:
        tuple: new Figure and Axes of the histogram
    """

    orderlist = order_dict.get(question_code)
    if orderlist:
        data_df[question_code] = pd.Categorical(
            data_df[question_code], categories=orderlist, ordered=True
        )

    hc.set_plotstyle()
    figure, ax = plt.subplots(dpi=300, figsize=(width, height), layout="constrained")

    if hue_series is not None:
        df = data_df.join(hue_series, on="id")
        hue = hue_series.name
        assert isinstance(hue, str)

        ax = sns.histplot(
            data=df,
            ax=ax,
            x=question_code,
            hue=hue,
            hue_order=hue_order,
            palette=[hc.helmholtzblue, hc.helmholtzgreen],
            stat="percent",
            common_norm=False,
            multiple="dodge",
            shrink=0.8,
            binwidth=binwidth,
            kde=kde,
            log_scale=log_scale,
        )
    else:
        ax = sns.histplot(
            data=data_df,
            ax=ax,
            x=question_code,
            stat="percent",
            color=hc.helmholtzblue,
            shrink=0.8,
            binwidth=binwidth,
            kde=kde,
            log_scale=log_scale,
        )

    return figure, ax
