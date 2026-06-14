from ecommerce_api.core.exceptions import ConflictError
from ecommerce_api.repositories.product_repo import ProductRepository
from ecommerce_api.schemas.product_schema import CreateProduct, UpdateProduct


class ProductService:
    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo

    def register_product(self, data: CreateProduct):
        # We need to associate an product specification table
        # We need to check for discount before creating a product
        if self.repo.name_exists(data.name):
            raise ConflictError(f'Product with name {data.name} already registered.')
        return self.repo.create(**data.model_dump())

    def update_product(self, data: UpdateProduct, id: int):
        if self.repo.name_exists(data.name):
            raise ConflictError(f'Product with name {data.name} already registered.')
        return self.repo.update(**data.model_dump(), id=id)

    def delete_product(self, id: int) -> None:
        product = self.repo.get_or_raise(id)

        return self.repo.delete(product.id)
