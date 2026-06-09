from typing import List

from models.users import UserRole
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole
    profile_picture_url: str | None = None


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    profile_picture_url: str | None = None
    is_active: bool


class UserList(BaseModel):
    users: List[UserPublic]
