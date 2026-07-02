from sqlalchemy import Column, ForeignKey, Integer, Table

from ecommerce_api.infrastructure.database import table_registry

product_categories = Table(
    'product_categories',
    table_registry.metadata,
    Column(
        'product_id',
        Integer,
        ForeignKey('products.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column(
        'category_id',
        Integer,
        ForeignKey('categories.id', ondelete='CASCADE'),
        primary_key=True,
    ),
)
