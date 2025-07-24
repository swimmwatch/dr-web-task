from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from utils.commands import BaseCommand
from utils.db import BaseDatabase
from utils.repl import Repl
from utils.types import ArgumentContext


class CountsCommand(BaseCommand):
    class Meta:
        name = "COUNTS"
        args = [
            "<str:value>",
        ]

    @inject
    def callback(
        self,
        args: ArgumentContext,
        repl: Repl = Provide["repl"],
        db: BaseDatabase = Provide["db"],
    ) -> None:
        count = db.counts(args["value"])
        repl.output(str(count) + "\n")
