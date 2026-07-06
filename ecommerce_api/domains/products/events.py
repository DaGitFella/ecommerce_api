from dataclasses import dataclass

from ecommerce_api.core.events.base import DomainEvent
from ecommerce_api.domains.categories.schema import CategoryList


@dataclass(frozen=True, kw_only=True)
class ProductCreated(DomainEvent):
    categories: CategoryList
