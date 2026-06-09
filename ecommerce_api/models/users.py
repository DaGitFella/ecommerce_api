import enum
from datetime import datetime

from sqlalchemy import Boolean, String, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.infrastructure.database import table_registry


class UserRole(enum.Enum):
    CUSTOMER = 'customer'
    EMPLOYEE = 'employee'
    ADMIN = 'admin'
    GUEST = 'guest'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False, name='password_hash'
    )
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), nullable=False)
    profile_picture_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, name='created_at', init=False, server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


@table_registry.mapped_as_dataclass
class EmployeeProfile:
    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    hire_date: Mapped[datetime] = mapped_column(nullable=False)
    emergency_contact: Mapped[str] = mapped_column(String(255), nullable=True)
    hourly_rate: Mapped[float] = mapped_column(nullable=True)
