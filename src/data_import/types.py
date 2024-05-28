from typing import Optional, TypeAlias, TypedDict, Union


class ResponseData(TypedDict):
    name: str
    format: Optional[str]
    length: Optional[str]
    label: Optional[str]
    choices: Optional[dict[str, str]]


ResponseTypeAlias: TypeAlias = "tuple[ResponseData, Optional[dict[str, str]]]"
QuestionTypeAlias: TypeAlias = "dict[str, Union[str, dict[str, str], None]]"
