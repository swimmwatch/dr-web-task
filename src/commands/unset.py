from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from utils.commands import BaseCommand
from utils.db import BaseDatabase
from utils.types import ArgumentContext


class UnsetCommand(BaseCommand):
    class Meta:
        name = "UNSET"
        args = [
            "<str:key>",
        ]

    @inject
    def callback(
        self,
        args: ArgumentContext,
        db: BaseDatabase = Provide["db"],
    ) -> None:
        db.unset(args["key"])
