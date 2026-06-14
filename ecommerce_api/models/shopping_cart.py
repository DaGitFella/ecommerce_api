from typing import TYPE_CHECKING

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ecommerce_api.core.constants import ShippingTypes
from ecommerce_api.infrastructure.database import table_registry

if TYPE_CHECKING:
    from .users import User


@table_registry.mapped_as_dataclass
class ShoppingCart:
    __tablename__ = 'shopping_carts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False, init=False
    )
    user: Mapped['User'] = relationship(back_populates='shopping_carts')
    shipping_cost: Mapped[float] = mapped_column(nullable=True, default=0)
    shipping_type: Mapped[ShippingTypes] = mapped_column(
        SqlEnum(ShippingTypes),
        String(50),
        nullable=False,
        default=ShippingTypes.DELIVERY,
    )

    __table_args_ = (UniqueConstraint('user_id'),)
