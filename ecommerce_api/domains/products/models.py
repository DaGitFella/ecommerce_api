from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ecommerce_api.infrastructure.database import table_registry

if TYPE_CHECKING:
    from ecommerce_api.domains.categories.models import Category
    from ecommerce_api.domains.discount.models import Discount
    from ecommerce_api.domains.specifications.models import SpecificationKey


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    price: Mapped[float] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)
    discount_id: Mapped[int] = mapped_column(nullable=True, default=None)
    description: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    image_url: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=''
    )

    categories: Mapped[list['Category']] = relationship(
        'Category',
        secondary='product_categories',
        back_populates='products',
        default_factory=list,
    )

    specification_keys: Mapped[list['SpecificationKey']] = relationship(
        'SpecificationKey',
        secondary='product_specifications',
        back_populates='products',
        default_factory=list,
    )

    discounts: Mapped[list['Discount']] = relationship(
        'Discount',
        secondary='product_discounts',
        back_populates='products',
        default_factory=list,
        nullable=True,
    )


product_specifications = Table(
    'product_specifications',
    table_registry.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column(
        'specification_id',
        Integer,
        ForeignKey('specification_keys.id'),
        primary_key=True,
    ),
    Column('value', String(255), nullable=False),
)

product_discounts = Table(
    'product_discounts',
    table_registry.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('discount_id', Integer, ForeignKey('discounts.id'), primary_key=True),
)
