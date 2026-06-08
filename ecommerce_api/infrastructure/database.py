from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from ecommerce_api.core.settings import settings

table_registry = registry()
engine = create_engine(
    settings.DATABASE_URL, echo=True, autocommit=False, autoflush=False
)


def get_db_session():
    """Dependency that provides a database session."""
    with Session(engine) as session:
        yield session
