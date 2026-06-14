from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, registry

from ecommerce_api.core.settings import Settings

engine = create_engine(Settings().DATABASE_URL, echo=True)

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}

metadata_with_convention = MetaData(naming_convention=convention)
table_registry = registry(metadata=metadata_with_convention)


def get_db_session():
    """Dependency that provides a database session."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
