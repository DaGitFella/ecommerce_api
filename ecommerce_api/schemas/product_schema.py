from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    stock: int
    price: float


class UpdateProduct(BaseModel):
    name: str
    description: str
    stock: int
    price: float

class PublicProduct(BaseModel):
    id: int
    name: str
    description: str
    stock: int
    price: float
    image_url: str
