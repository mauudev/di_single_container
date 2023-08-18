from dataclasses import dataclass
from typing import Callable, ContextManager

from dependency_injector.wiring import Provide, inject
from sqlalchemy import text
from sqlalchemy.orm import Session

from .container import Container


class Service:
    def hello(self):
        return "hello!"


@dataclass
class DBCommand:
    query: str


@inject
def db_op_with_transaction(
    command: DBCommand,
    db_transaction: ContextManager[Session] = Provide[Container.db_transaction],
) -> None:
    with db_transaction as session:
        result = session.execute(text(command.query))
        print(result.scalar())


@inject
def db_op_with_database(
    command: DBCommand,
    database: ContextManager[Session] = Provide[Container.database],
) -> None:
    with database.session() as session:
        result = session.execute(text(command.query))
        print(result.scalar())


class TaskBus:
    def __init__(self):
        self.tasks = dict()

    def register_task(self, command: DBCommand, task: Callable):
        self.tasks[command.__class__.__name__] = task

    def execute(self, command: DBCommand):
        self.tasks[command.__class__.__name__](command)
