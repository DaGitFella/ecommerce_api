from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.infrastructure.database import table_registry


@table_registry.mapped_as_dataclass
class Discount:
    __tablename__ = 'discounts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    value: Mapped[float] = mapped_column(nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)
