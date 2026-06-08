import enum
from datetime import datetime

from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce_api.infrastructure.database import table_registry


class MachineRequestStatus(enum.Enum):
    PENDING = 'pending'
    WAITING_DEPOSIT = 'waiting_deposit'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    SHIPPED_FROM_ABROAD = 'shipped_from_abroad'
    READY_FOR_PICKUP = 'ready_for_pickup'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


@table_registry.mapped_as_dataclass
class MachineRequest:
    __tablename__ = 'machine_requests'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    estimated_shipping_price: Mapped[float | None] = mapped_column(nullable=True)
    estimated_delivery_date: Mapped[datetime | None] = mapped_column(nullable=True)
    status: Mapped[MachineRequestStatus] = mapped_column(
        SqlEnum(MachineRequestStatus), nullable=False
    )
    hourly_rate: Mapped[float | None] = mapped_column(nullable=True)
