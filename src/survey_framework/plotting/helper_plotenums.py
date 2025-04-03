from enum import Enum, StrEnum, auto


class Orientation(StrEnum):
    VERTICAL = "v"
    HORIZONTAL = "h"


class PercentCount(StrEnum):
    PERCENT = "Percent"
    COUNT = "Count"


class BarLabels(Enum):
    NONE = auto()
    COUNT = auto()
    PERCENT = auto()


class PlotType(Enum):
    SINGLE_Q = auto()  # use blue
    MULTI_Q = auto()  # use shades of blue
    SINGLE_Q_COMPARISON = auto()  # use blue and green
    MULTI_Q_COMPARISON = auto()  # use shades of blue and green
