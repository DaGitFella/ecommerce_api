from typing import List

from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


class CategoryPublic(BaseModel):
    id: int
    name: str
    slug: str


class CategoryUpdate(BaseModel):
    name: str
    slug: str


class CategoryList(BaseModel):
    categories: List[CategoryPublic]
