from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ecommerce_api.infrastructure.db.session import table_registry

if TYPE_CHECKING:
    from ecommerce_api.domains.products.models import Product


@table_registry.mapped_as_dataclass
class Discount:
    __tablename__ = 'discounts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    value: Mapped[float] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(nullable=False, unique=True)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)

    products: Mapped[list[Product]] = relationship(
        'Product',
        secondary='product_discounts',
        back_populates='discounts',
        default_factory=list,
    )
