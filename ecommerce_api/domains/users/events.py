from dataclasses import dataclass

from ecommerce_api.core.events.base import DomainEvent


@dataclass(frozen=True, kw_only=True)
class UserRegistered(DomainEvent):
    user_id: int
    email: str
