from di_single_container.container import Container
from di_single_container.tasks import (
    TaskBus,
    db_op_with_database,
    db_op_with_transaction,
)

if __name__ == "__main__":
    container = Container()
    container.wire(modules=["di_single_container.tasks"])

    bus = TaskBus()
    bus.register_task("db_transaction", db_op_with_transaction)
    bus.register_task("db_session", db_op_with_database)

    bus.execute("db_session")
