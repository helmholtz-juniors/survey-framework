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


def validateOrientation(orientation: Orientation) -> None:
    if orientation == Orientation.VERTICAL or orientation == Orientation.HORIZONTAL:
        return
    raise ValueError(
        f"Invalid value for Orientation: {orientation}. Expected 'Orientation.VERTICAL = \"v\"' or 'Orientation.HORIZONTAL = \"h\"'"
    )


def validatePercentCount(percentcount: PercentCount) -> None:
    if percentcount == PercentCount.PERCENT or percentcount == PercentCount.COUNT:
        return
    raise ValueError(
        f"Invalid value for PercentCount: {percentcount}. Expected 'PercentCount.PERCENT = \"Percentages\"' or 'PercentCount.COUNT = \"Count\"'"
    )
