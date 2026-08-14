from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ecommerce_api.infrastructure.db.session import table_registry

if TYPE_CHECKING:
    from ecommerce_api.domains.products.models import Product


@table_registry.mapped_as_dataclass
class SpecificationKey:
    __tablename__ = 'specification_keys'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    products: Mapped[List[Product]] = relationship(
        secondary='product_specifications',
        back_populates='specification_keys',
        default_factory=list,
    )
