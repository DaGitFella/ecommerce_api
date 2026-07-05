from typing import List, Optional

from pydantic import BaseModel

from ecommerce_api.domains.categories.schema import CategoryCreate


class ProductCreate(BaseModel):
    discount_id: Optional[int] = None
    name: str
    description: str
    price: float
    stock: int
    categories: Optional[List[CategoryCreate]] = None
    image_url: Optional[str] = None


class ProductPublic(BaseModel):
    id: int
    discount_id: Optional[int] = int | None
    name: str
    description: str
    price: float
    stock: int
    image_url: Optional[str] = str | None


class ProductUpdate(BaseModel):
    discount_id: Optional[int] = int | None
    name: str
    description: str
    price: float
    stock: int
    image_url: Optional[str] = str | None


class ProductList(BaseModel):
    products: List[ProductPublic]
