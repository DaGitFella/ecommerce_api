from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.infrastructure.database import table_registry


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    discount_id: Mapped[int] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
