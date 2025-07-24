from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from utils.commands import BaseCommand
from utils.db import BaseDatabase
from utils.repl import Repl
from utils.types import ArgumentContext


class FindCommand(BaseCommand):
    class Meta:
        name = "FIND"
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
        keys = db.find(args["value"])
        content = "\n".join(keys) + "\n"
        repl.output(content)
