from typing import TypeAlias, TypedDict


class ResponseData(TypedDict):
    """Dictionary with metadata about response options."""

    name: str
    format: str | None
    length: str | None
    label: str | None
    choices: dict[str, str] | None


ResponseTypeAlias: TypeAlias = "tuple[ResponseData, dict[str, str] | None]"
QuestionTypeAlias: TypeAlias = "dict[str, str | dict[str, str] | None]"
