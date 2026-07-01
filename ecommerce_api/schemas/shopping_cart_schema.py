from typing import List, Optional

from pydantic import BaseModel

from ecommerce_api.core.constants import ShippingTypes


class ShoppingCartCreate(BaseModel):
    shipping_type: ShippingTypes
    shipping_cost: Optional[float] = None


class ShoppingCartPublic(BaseModel):
    id: int
    user_id: int
    shipping_type: ShippingTypes
    shipping_cost: Optional[float] = None


class ShoppingCartUpdate(BaseModel):
    shipping_type: ShippingTypes
    shipping_cost: Optional[float] = None


class ShoppingCartList(BaseModel):
    shoppingcarts: List[ShoppingCartPublic]
