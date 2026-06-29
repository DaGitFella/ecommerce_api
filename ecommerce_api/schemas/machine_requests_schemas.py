from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from ecommerce_api.models.machine_requests import MachineRequestStatus


class MachineRequestsCreate(BaseModel):
    estimated_shipping_price: Optional[float] = float | None
    estimated_delivery_date: Optional[datetime] = datetime | None
    status: MachineRequestStatus
    hourly_rate: Optional[float] = float | None


class MachineRequestsPublic(BaseModel):
    id: int
    user_id: int
    estimated_shipping_price: Optional[float] = float | None
    estimated_delivery_date: Optional[datetime] = datetime | None
    status: MachineRequestStatus
    hourly_rate: Optional[float] = float | None


class MachineRequestsList(BaseModel):
    machine_requests: List[MachineRequestsPublic]
