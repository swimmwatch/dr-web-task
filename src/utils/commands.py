import abc
import dataclasses
import enum
import typing

from utils.types import ArgumentContext
from utils.types import ArgumentMetadata
from utils.types import ParameterType


@dataclasses.dataclass
class CommandRequest:
    text: str


class ArgumentTypeEnum(str, enum.Enum):
    STRING = "string"
    PARAMETER = "parameter"


class ArgumentParser(abc.ABC):
    _PARAMETER_SEPARATOR = ":"
    _PARAMETER_BEGIN = "<"
    _PARAMETER_END = ">"

    # TODO: add support for more types
    _MAP_PARAMETER_CLS = {
        "int": int,
        "str": str,
    }

    def __init__(self, args: typing.Sequence[str] | None = None) -> None:
        self._args = args
        self._metadata = self._parse_args(args)

    @staticmethod
    def _list_args(text: str | typing.Sequence[str]) -> typing.Sequence[str]:
        args: typing.Sequence[str]

        if isinstance(text, str):
            args = text.split()
        elif isinstance(text, typing.Sequence):
            args = text
        else:
            raise ValueError(f"Unexpected text type: {type(text)}")

        return args

    def parse(self, text: str | typing.Sequence[str]) -> ArgumentContext | None:
        """Returns arguments context. Extracts and parses parameters from text."""
        context: ArgumentContext = {}
        words = self._list_args(text)

        if self._args is None:
            return context

        if len(words) != len(self._args):
            return None

        for arg, word in zip(self._args, words):
            arg_type, metadata = self._metadata[arg]

            if arg_type is ArgumentTypeEnum.STRING:
                continue

            if metadata is None:
                raise ValueError(f"For parameter {arg} must be set metadata.")

            cls, arg_name = metadata
            context[arg_name] = cls(word)

        return context

    def _parse_parameter(self, parameter: str) -> ParameterType:
        type_, arg_name = parameter[1:-1].split(self._PARAMETER_SEPARATOR)
        cls = self._MAP_PARAMETER_CLS.get(type_)
        if cls is None:
            expected_types = ", ".join(self._MAP_PARAMETER_CLS.keys())
            raise ValueError(f"Unexpected type {type_}. Expected one of {expected_types}.")

        return cls, arg_name

    def _parse_args(self, args: typing.Sequence[str] | None = None) -> dict[str, ArgumentMetadata]:
        metadata: dict[str, ArgumentMetadata] = {}

        if args is None:
            return metadata

        for arg in args:
            arg_type = self._get_arg_type(arg)

            match arg_type:
                case ArgumentTypeEnum.STRING:
                    metadata[arg] = (arg_type, None)  # type: ignore[assignment]
                case ArgumentTypeEnum.PARAMETER:
                    cls, arg_name = self._parse_parameter(arg)
                    metadata[arg] = (arg_type, (cls, arg_name))  # type: ignore[assignment]
                case _:
                    typing.assert_never(arg)

        return metadata

    def _validate_parameter(self, parameter: str) -> bool:
        if not parameter:
            return False

        return (
            parameter[0] == self._PARAMETER_BEGIN
            and parameter[-1] == self._PARAMETER_END
            and self._PARAMETER_SEPARATOR in parameter
        )

    def _get_arg_type(self, arg: str) -> ArgumentTypeEnum:
        if not arg:
            raise ValueError(f"Unexpected argument value: {arg}")

        if self._validate_parameter(arg):
            return ArgumentTypeEnum.PARAMETER

        return ArgumentTypeEnum.STRING

    def validate(self, text: str | typing.Sequence[str]) -> bool:
        words = self._list_args(text)

        if self._args is None:
            return True

        if len(words) != len(self._args):
            return False

        for arg, word in zip(self._args, words):
            arg_type, metadata = self._metadata[arg]

            match arg_type:
                case ArgumentTypeEnum.PARAMETER:
                    if metadata is None:
                        raise ValueError(f"For parameter {arg} must be set metadata.")

                    cls, _ = metadata

                    try:
                        cls(word)
                    except Exception:
                        return False
                case ArgumentTypeEnum.STRING:
                    if arg != word:
                        return False
                case _:
                    typing.assert_never(arg_type)  # type: ignore[arg-type]

        return True


class BaseCommand(abc.ABC):
    class Meta:
        name: str
        args: typing.Sequence[str] | None = None

    def __init__(self) -> None:
        self._argument_parser = ArgumentParser(self.Meta.args)

    def parse(self, text: str) -> tuple[bool, ArgumentContext | None]:
        """Parses the command text and returns a tuple of success status and arguments context."""
        if not text.startswith(self.Meta.name):
            return False, None

        text = text[len(self.Meta.name) :].strip()
        args = self._argument_parser.parse(text)
        if args is None:
            return False, None

        return True, args

    @abc.abstractmethod
    def callback(self, args: ArgumentContext) -> None:
        """Callback to be implemented by subclasses.

        This method will be called when the command is successfully parsed.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def emit(self, args: ArgumentContext) -> None:
        self.callback(args)


class ChainOfResponsibilityHandler(abc.ABC):
    @abc.abstractmethod
    def process_request(self, request: CommandRequest) -> bool:
        pass


class CommandChainOfResponsibilityHandler(ChainOfResponsibilityHandler):
    def __init__(
        self,
        command: BaseCommand,
    ):
        self._command = command

    def process_request(self, request: CommandRequest) -> bool:
        if request.text is None:
            return False

        success, args = self._command.parse(request.text)
        if not success:
            return False

        args = typing.cast(ArgumentContext, args)
        self._command.emit(args)

        return True


class CommandHandlerProcessor:
    def __init__(self, commands: typing.Sequence[ChainOfResponsibilityHandler]) -> None:
        self._commands = commands

    def handle(self, request: CommandRequest) -> None:
        for command in self._commands:
            handled = command.process_request(request)
            if handled:
                break
