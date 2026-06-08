from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.infrastructure.database import table_registry


@table_registry.mapped_as_dataclass
class ProductSpecification:
    __tablename__ = 'product_specifications'

    product_id: Mapped[int] = mapped_column(nullable=False)
    specification_id: Mapped[int] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(String(100), nullable=False)
