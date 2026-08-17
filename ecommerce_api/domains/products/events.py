from dataclasses import dataclass
from typing import Optional

from ecommerce_api.core.events.base import DomainEvent
from ecommerce_api.domains.categories.schema import CategoryList
from ecommerce_api.domains.discount.schema import DiscountList
from ecommerce_api.domains.specifications.schema import SpecificationList

from .models import Product


@dataclass(frozen=True, kw_only=True)
class ProductCreated(DomainEvent):
    categories: Optional[CategoryList] = None
    specifications: Optional[SpecificationList] = None
    discounts: Optional[DiscountList] = None
    product: Product
