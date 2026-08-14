from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ecommerce_api.core.bootstrap import EventRegistry
from ecommerce_api.core.events import event_bus
from ecommerce_api.core.exceptions import AppError
from ecommerce_api.domains.categories.handlers import CategoryEventHandlers
from ecommerce_api.domains.categories.repository import CategoryRepository
from ecommerce_api.domains.categories.service import CategoryService
from ecommerce_api.domains.shopping_carts.handlers import CartEventHandlers
from ecommerce_api.domains.shopping_carts.repository import ShoppingCartRepository
from ecommerce_api.domains.shopping_carts.service import ShoppingCartService
from ecommerce_api.domains.specifications.handlers import SpecificationsEventHandlers
from ecommerce_api.domains.specifications.repository import SpecificationKeyRepository
from ecommerce_api.domains.specifications.service import SpecificationsService
from ecommerce_api.domains.users import routes
from ecommerce_api.infrastructure.db import models  # noqa: F401
from ecommerce_api.infrastructure.db.session import get_db_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    cart_handlers = CartEventHandlers(
        cart_service=ShoppingCartService(ShoppingCartRepository(get_db_session))
    )

    category_handlers = CategoryEventHandlers(
        category_service=CategoryService(CategoryRepository(get_db_session))
    )

    specifications_handlers = SpecificationsEventHandlers(
        specification_service=SpecificationsService(
            SpecificationKeyRepository(get_db_session)
        )
    )

    event_register = EventRegistry(event_bus)

    event_register.register_all(
        cart_handlers=cart_handlers,
        category_handlers=category_handlers,
        specifications_handlers=specifications_handlers,
    )

    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'error': exc.message,
                'detail': exc.detail,
            },
        )

    # config
    app.title = 'ecommerce api'
    app.version = '0.1'
    app.description = 'trying to build an ecommerce api from scratch'

    # routes
    app.include_router(routes.router)

    return app


app = create_app()


@app.get('/', status_code=200)
def root():
    return {'message': 'Welcome to the E-commerce API!'}
