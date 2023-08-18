from dependency_injector import containers, providers

from .database import Database, db_session


class Container(containers.DeclarativeContainer):
    db_transaction = providers.Singleton(db_session)
    database = providers.Singleton(Database)
