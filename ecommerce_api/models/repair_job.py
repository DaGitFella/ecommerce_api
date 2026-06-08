import enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.infrastructure.database import table_registry


class RepairJobStatus(enum.Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    WAITING_PARTS = 'waiting_parts'
    WAITING_PAYMENT = 'waiting_payment'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


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
