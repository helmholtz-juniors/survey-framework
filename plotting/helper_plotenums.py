from enum import Enum, StrEnum


class Orientation(StrEnum):
    VERTICAL = "v"
    HORIZONTAL = "h"


class PercentCount(StrEnum):
    PERCENT = "Percentage"
    COUNT = "Counts"


class ShowAxesLabel(Enum):
    NONE = 1
    COUNT = 2
    PERCENT = 3
