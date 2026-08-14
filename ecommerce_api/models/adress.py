from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.infrastructure.db.session import table_registry


@table_registry.mapped_as_dataclass
class Adress:
    __tablename__ = 'adresses'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False, init=False
    )
    cep: Mapped[str] = mapped_column(String(11), nullable=True)
    street: Mapped[str] = mapped_column(String(260), nullable=True)
    number: Mapped[str] = mapped_column(String(10), nullable=True)
    complement: Mapped[str] = mapped_column(String(150), nullable=True)
    neighborhood: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
