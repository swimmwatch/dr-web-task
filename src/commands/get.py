import typing

from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from utils.commands import BaseCommand
from utils.db import BaseDatabase
from utils.repl import Repl
from utils.types import ArgumentContext


class GetCommand(BaseCommand):
    class Meta:
        name = "GET"
        args = [
            "<str:key>",
        ]

    @inject
    def callback(
        self,
        args: ArgumentContext,
        repl: Repl = Provide["repl"],
        db: BaseDatabase = Provide["db"],
    ) -> None:
        key = typing.cast(str, args.get("key"))
        val = db.get(key)
        result = str(val) if val is not None else "NULL"
        repl.output(f"{result}\n")
