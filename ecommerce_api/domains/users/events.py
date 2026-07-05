from dataclasses import dataclass

from ecommerce_api.core.events.base import DomainEvent

from .models import User


@dataclass(frozen=True, kw_only=True)
class UserRegistered(DomainEvent):
    user: User
    email: str
