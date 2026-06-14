from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ecommerce_api.core.constants import UserRole
from ecommerce_api.infrastructure.database import table_registry

if TYPE_CHECKING:
    from .shopping_cart import ShoppingCart


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False, name='password_hash'
    )
    shopping_carts: Mapped['ShoppingCart'] = relationship(back_populates='user')
    profile_picture_url: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=''
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, name='created_at', init=False, server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole), nullable=False, default=UserRole.CUSTOMER
    )


@table_registry.mapped_as_dataclass
class EmployeeProfile:
    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    hire_date: Mapped[datetime] = mapped_column(nullable=False)
    emergency_contact: Mapped[str] = mapped_column(String(255), nullable=True)
    hourly_rate: Mapped[float] = mapped_column(nullable=True)
