import os
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

# SQLite persistence to prevent rework when scaling to PostgreSQL
sqlite_file_name = "astrosdk.db"
sqlite_url = os.environ.get("SQLITE_URL", f"sqlite:///{sqlite_file_name}")

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)


def create_db_and_tables() -> None:
    """Initialize the persistence layer and create all SQLModel tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency for providing a transactional database session."""
    with Session(engine) as session:
        yield session
