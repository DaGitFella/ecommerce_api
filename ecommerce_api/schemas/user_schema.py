from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr

from ecommerce_api.models.users import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    profile_picture_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    profile_picture_url: str | None = None
    is_active: bool


class UserList(BaseModel):
    users: List[UserPublic]
