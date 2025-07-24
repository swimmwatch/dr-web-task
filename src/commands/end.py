from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from utils.commands import BaseCommand
from utils.repl import Repl
from utils.types import ArgumentContext


class EndCommand(BaseCommand):
    class Meta:
        name = "END"
        args = None

    @inject
    def callback(self, _: ArgumentContext, repl: Repl = Provide["repl"]) -> None:
        """Callback to end the REPL session."""
        repl.output("Ending REPL session.\n")
        repl.finish()
