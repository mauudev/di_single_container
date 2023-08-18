from typing import Callable, ContextManager

from dependency_injector.wiring import Provide, inject
from sqlalchemy import text
from sqlalchemy.orm import Session

from .container import Container


class Service:
    def hello(self):
        return "hello!"


@inject
def db_op_with_transaction(
    db_transaction: ContextManager[Session] = Provide[Container.db_transaction],
) -> None:
    with db_transaction as session:
        result = session.execute(text("SELECT 1"))
        print(result.scalar())


@inject
def db_op_with_database(
    database: ContextManager[Session] = Provide[Container.database],
) -> None:
    with database.session() as session:
        result = session.execute(text("SELECT 2"))
        print(result.scalar())


class TaskBus:
    def __init__(self):
        self.tasks = dict()

    def register_task(self, command: str, task: Callable):
        self.tasks[command] = task

    def execute(self, command: str):
        self.tasks[command]()
