from typing import Optional

from pydantic import BaseModel


class CartItemCreate(BaseModel):
    cart_id: int
    product_id: int
    quantity: int


class CartItemPublic(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int


class CartItemUpdate(BaseModel):
    cart_id: Optional[int] = int | None
    product_id: Optional[int] = int | None
    quantity: Optional[int] = int | None
