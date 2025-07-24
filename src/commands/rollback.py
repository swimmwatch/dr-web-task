from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from utils.commands import BaseCommand
from utils.db import BaseDatabase
from utils.types import ArgumentContext


class RollbackCommand(BaseCommand):
    class Meta:
        name = "ROLLBACK"
        args = None

    @inject
    def callback(
        self,
        _: ArgumentContext,
        db: BaseDatabase = Provide["db"],
    ) -> None:
        db.rollback()
