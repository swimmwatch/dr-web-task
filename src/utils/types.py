import enum
import typing

ArgumentContext = dict[str, typing.Any]
ParameterType = tuple[type, str]
ArgumentMetadata = tuple["ArgumentTypeEnum", ParameterType | None]


class ArgumentTypeEnum(str, enum.Enum):
    STRING = "string"
    PARAMETER = "parameter"
