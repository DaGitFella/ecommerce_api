from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.infrastructure.database import table_registry


@table_registry.mapped_as_dataclass
class ProductCategory:
    __tablename__ = 'product_categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    product_id: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(nullable=False)
