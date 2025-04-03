import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame, Series

import survey_framework.plotting.helmholtzcolors as hc
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.plotting.helper_barplots import add_tick_labels
from survey_framework.plotting.helper_plotenums import Orientation


def simple_histplot(
    survey: LimeSurveyData,
    data_df: DataFrame,
    question_code: str,
    hue_series: "Series[str] | None",
    order_dict: dict[str, list[str]],
    hue_order: list[str] | None,
    width: int = 10,
    height: int = 6,
) -> tuple[Figure, Axes]:
    """Very simple histplot. Currently in experimental state, to be expanded
        for stacked barplots and KDE plots.

    Args:
        survey (LimeSurveyData): _description_
        data_df (DataFrame): _description_
        question_code (str): _description_
        hue_series (Series | None): _description_
        order_dict (dict[str, list[str]]): _description_
        hue_order (list[str] | None): _description_
        width (int, optional): _description_. Defaults to 10.
        height (int, optional): _description_. Defaults to 6.

    Returns:
        tuple[Figure, Axes]: _description_
    """

    orderlist = order_dict.get(question_code)
    if orderlist:
        data_df[question_code] = pd.Categorical(
            data_df[question_code], categories=orderlist, ordered=True
        )
    # todo: descending data ordering?!

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
        )
    else:
        ax = sns.histplot(
            data=data_df,
            ax=ax,
            x=question_code,
            stat="percent",
            color=hc.helmholtzblue,
            shrink=0.8,
        )

    add_tick_labels(survey, ax, question_code, Orientation.VERTICAL, 10, 30)

    return figure, ax
