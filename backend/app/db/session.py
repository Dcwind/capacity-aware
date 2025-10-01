from collections.abc import Generator
from sqlmodel import SQLModel, Session, create_engine
import os

DB_PATH = os.environ.get("LP_DB_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "leave.sqlite3"))
DB_URI = f"sqlite:///{os.path.abspath(DB_PATH)}"
engine = create_engine(DB_URI, echo=False, connect_args={"check_same_thread": False})

def init_db() -> None:
    from . import models  # noqa: F401
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
