from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.core.constants import RepairJobStatus
from ecommerce_api.infrastructure.db.session import table_registry


@table_registry.mapped_as_dataclass
class RepairJob:
    __tablename__ = 'repair_jobs'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    customer_id: Mapped[int] = mapped_column(nullable=False)
    employee_id: Mapped[int] = mapped_column(nullable=False)
    issue_description: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[RepairJobStatus] = mapped_column(
        SqlEnum(RepairJobStatus), nullable=False
    )
    cost_estimate: Mapped[float] = mapped_column(nullable=True)
    machine_model: Mapped[str] = mapped_column(String(100), nullable=True)
