from enum import Enum, StrEnum, auto


class Orientation(StrEnum):
    """
    Whether to plot horizontal or vertical bars.

    The string value can be used directly with seaborn functions.
    """

    VERTICAL = "v"
    HORIZONTAL = "h"


class PlotStat(StrEnum):
    """
    Which stat to use in a plot: absolute (COUNT) or relative (PERCENT) numbers.
    PROPORTION indicates that values a normalized to [0..1].

    The string value can be used directly with seaborn functions.
    """

    PERCENT = "percent"
    COUNT = "count"
    PROPORTION = "proportion"


class BarLabels(Enum):
    """
    How each bar in a plot should be labeled. Can be different from PlotStat.
    """

    NONE = auto()
    COUNT = auto()
    PERCENT = auto()


class PlotType(Enum):
    SINGLE_Q = auto()  # use blue
    MULTI_Q = auto()  # use shades of blue
    SINGLE_Q_COMPARISON = auto()  # use blue and green
    MULTI_Q_COMPARISON = auto()  # use shades of blue and green
