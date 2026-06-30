from typing import List, Optional

from pydantic import BaseModel


class ShoppingCartCreate(BaseModel):
    shipping_type: str
    shipping_cost: Optional[float] = None


class ShoppingCartPublic(BaseModel):
    id: int
    user_id: int
    shipping_type: str
    shipping_cost: Optional[float] = None


class ShoppingCartUpdate(BaseModel):
    id: int
    shipping_type: str
    shipping_cost: Optional[float] = None


class ShoppingCartList(BaseModel):
    shoppingcarts: List[ShoppingCartPublic]
