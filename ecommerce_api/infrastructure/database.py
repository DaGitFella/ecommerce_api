from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from ecommerce_api.core.settings import Settings

table_registry = registry()
engine = create_engine(
    Settings().DATABASE_URL, echo=True
)


def get_db_session():
    """Dependency that provides a database session."""
    with Session(engine) as session:
        yield session
