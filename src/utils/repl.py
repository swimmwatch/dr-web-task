import io

from utils.commands import CommandHandlerProcessor
from utils.commands import CommandRequest


class Repl:
    def __init__(
        self, input_stream: io.TextIOBase, output_stream: io.TextIOBase, command_processor: CommandHandlerProcessor,
    ):
        self.input_stream = input_stream
        self.output_stream = output_stream
        self._command_processor = command_processor
        self._finished = False

    def finish(self):
        self._finished = True
        self.input_stream.close()
        self.output_stream.close()

    def _prompt(self) -> None:
        self.output_stream.write(">> ")
        self.output_stream.flush()

    def input(self) -> str:
        return self.input_stream.readline().strip()

    def output(self, content: str) -> None:
        self.output_stream.write(content)
        self.output_stream.flush()

    def _handle_command(self, text: str) -> None:
        command_request = CommandRequest(text=text)
        self._command_processor.handle(command_request)

    def execute(self):
        while True:
            try:
                self._prompt()

                text = self.input()
                if not text:
                    self.finish()
                    break

                self._handle_command(text)

                if self._finished:
                    break
            except KeyboardInterrupt:
                self.output("\nExiting REPL session.\n")
                self.finish()
                break
            except Exception as e:
                self.output(f"Error: {e}\n")
