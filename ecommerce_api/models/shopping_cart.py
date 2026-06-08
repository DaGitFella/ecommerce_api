from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.infrastructure.database import table_registry


@table_registry.mapped_as_dataclass
class ShoppingCart:
    __tablename__ = 'shopping_carts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    shipping_type: Mapped[str] = mapped_column(String(50), nullable=False)
    shipping_cost: Mapped[float | None] = mapped_column(nullable=True)
