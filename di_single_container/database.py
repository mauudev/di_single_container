import os
from contextlib import AbstractContextManager, contextmanager
from functools import cache
from typing import Callable, ContextManager

from sqlalchemy import QueuePool
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

DB_URI = os.getenv(
    "DATABASE_URI", "postgresql://admin:admin@localhost:7001/silver_bullet"
)
DATABASE_POOL_SIZE = os.getenv("DATABASE_POOL_SIZE", 10)


def build_engine() -> Engine:
    return create_engine(
        DB_URI,
        poolclass=QueuePool,
        pool_size=int(DATABASE_POOL_SIZE),
    )


@cache
def db_pool_connexion_session() -> Callable[[], Session]:
    print("Creating database session ..")
    session_factory = sessionmaker(
        bind=build_engine(), autocommit=False, autoflush=True
    )
    return scoped_session(session_factory)


@contextmanager
def db_session() -> ContextManager[Session]:
    session: Session = db_pool_connexion_session()
    try:
        yield session

    except Exception as e:
        print("Database error: making rollback", exc_info=True)
        session.rollback()
        raise e

    finally:
        session.close()


class Database:
    def __init__(self, db_url: str = DB_URI) -> None:
        self._engine = create_engine(
            db_url, poolclass=QueuePool, pool_size=int(DATABASE_POOL_SIZE), echo=True
        )
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=True,
                bind=self._engine,
            ),
        )

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session

        except Exception:
            print("Session rollback because of exception ..")
            session.rollback()
            raise

        finally:
            session.close()
