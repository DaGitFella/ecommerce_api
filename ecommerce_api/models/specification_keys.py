from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.infrastructure.database import table_registry


@table_registry.mapped_as_dataclass
class SpecificationKey:
    __tablename__ = 'specification_keys'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
