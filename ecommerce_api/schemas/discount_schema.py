from datetime import datetime
from typing import List

from pydantic import BaseModel


class DiscountCreate(BaseModel):
    value: float
    start_date: datetime
    end_date: datetime


class DiscountPublic(BaseModel):
    id: int
    value: float
    start_date: datetime
    end_date: datetime


class DiscountUpdate(BaseModel):
    value: float
    start_date: datetime
    end_date: datetime


class DiscountList(BaseModel):
    discounts: List[DiscountPublic]
