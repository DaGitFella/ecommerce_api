from typing import List

from pydantic import BaseModel


class SpecificationSchema(BaseModel):
    name: str
    slug: str


class SpecificationPublic(BaseModel):
    id: int
    name: str
    slug: str


class SpecificationList(BaseModel):
    specifications: List[SpecificationPublic]
