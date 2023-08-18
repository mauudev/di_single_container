from di_single_container.container import Container
from di_single_container.tasks import (
    DBCommand,
    TaskBus,
    db_op_with_database,
    db_op_with_transaction,
)

if __name__ == "__main__":
    container = Container()
    container.wire(modules=["di_single_container.tasks"])

    command_1 = DBCommand(query="SELECT 1")
    command_2 = DBCommand(query="SELECT 2")
    bus = TaskBus()
    bus.register_task(command_1, db_op_with_transaction)
    bus.register_task(command_2, db_op_with_database)

    bus.execute(command_1)
    bus.execute(command_2)
