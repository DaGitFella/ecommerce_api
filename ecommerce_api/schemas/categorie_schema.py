from typing import List

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    slug: str


class CategoryPublic(BaseModel):
    id: int
    name: str
    slug: str


class CategoryUpdate(BaseModel):
    name: str
    slug: str


class CategoryList(BaseModel):
    categories: List[CategoryPublic]
