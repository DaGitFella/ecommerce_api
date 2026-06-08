from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.infrastructure.database import table_registry


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False, max_length=100)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, max_length=100)
    password_hash: Mapped[str] = mapped_column(nullable=False, name='password_hash')
    role: Mapped[str] = mapped_column(nullable=False, max_length=50)
    profile_picture_url: Mapped[str] = mapped_column(nullable=True, max_length=255)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, name='created_at', init=False, server_default=func.now()
    )
