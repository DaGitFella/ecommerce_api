from ecommerce_api.categories.service import CategoryService
from ecommerce_api.core.exceptions import ConflictError
from ecommerce_api.products.repository import ProductRepository
from ecommerce_api.products.schema import ProductCreate, ProductList, ProductUpdate


class ProductService:
    def __init__(
        self, repo: ProductRepository, category_service: CategoryService
    ) -> None:
        self.repo = repo
        self.category_service = category_service

    def register_product(self, data: ProductCreate):
        # We need to associate an product specification table
        # We need to check for discount before creating a product
        if self.repo.name_exists(data.name):
            raise ConflictError(f'Product with name {data.name} already registered.')

        categories = [
            self.category_service.get_or_create_category(cat)
            for cat in data.categories or []
        ]

        product = self.repo.create_product(data)

        product.categories.extend(categories)

        return product

    def update_product(self, data: ProductUpdate, id: int):
        if self.repo.name_exists(data.name):
            raise ConflictError(f'Product with name {data.name} already registered.')
        return self.repo.update(**data.model_dump(), id=id)

    def delete_product(self, id: int) -> None:
        product = self.repo.get_or_raise(id)

        return self.repo.delete(product.id)

    def list_products(
        self, limit: int = 20, offset: int = 0, *filters: any
    ) -> ProductList:
        products = self.repo.list(limit=limit, offset=offset, *filters)

        return {'products': products}
