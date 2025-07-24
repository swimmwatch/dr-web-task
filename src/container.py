import sys

from dependency_injector import containers
from dependency_injector import providers

from commands.begin import BeginCommand
from commands.commit import CommitCommand
from commands.counts import CountsCommand
from commands.end import EndCommand
from commands.find import FindCommand
from commands.get import GetCommand
from commands.rollback import RollbackCommand
from commands.set import SetCommand
from commands.unset import UnsetCommand
from utils.commands import CommandChainOfResponsibilityHandler
from utils.commands import CommandHandlerProcessor
from utils.db import InMemoryDatabase
from utils.repl import Repl


class Container(containers.DeclarativeContainer):
    db = providers.Singleton(InMemoryDatabase)
    command_processor = providers.Factory(
        CommandHandlerProcessor,
        commands=[
            CommandChainOfResponsibilityHandler(command())  # type: ignore[abstract]
            for command in [
                GetCommand,
                EndCommand,
                SetCommand,
                UnsetCommand,
                CountsCommand,
                FindCommand,
                CommitCommand,
                BeginCommand,
                RollbackCommand,
            ]
        ],
    )
    repl = providers.Singleton(
        Repl,
        input_stream=sys.stdin,
        output_stream=sys.stdout,
        command_processor=command_processor,
    )
