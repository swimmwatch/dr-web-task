from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from utils.commands import BaseCommand
from utils.db import BaseDatabase
from utils.types import ArgumentContext


class SetCommand(BaseCommand):
    class Meta:
        name = "SET"
        args = [
            "<str:key>",
            "<str:value>",
        ]

    @inject
    def callback(
        self,
        args: ArgumentContext,
        db: BaseDatabase = Provide["db"],
    ) -> None:
        db.set(args["key"], args["value"])
