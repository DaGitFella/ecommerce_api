from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ecommerce_api.core.bootstrap import register_event_handlers
from ecommerce_api.core.events import event_bus
from ecommerce_api.core.exceptions import AppError
from ecommerce_api.domains.shopping_carts.handlers import CartEventHandlers
from ecommerce_api.domains.shopping_carts.repository import ShoppingCartRepository
from ecommerce_api.domains.shopping_carts.service import ShoppingCartService
from ecommerce_api.domains.users import routes
from ecommerce_api.infrastructure.database import get_db_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    cart_handlers = CartEventHandlers(
        cart_service=ShoppingCartService(ShoppingCartRepository(get_db_session))
    )
    register_event_handlers(event_bus, cart_handlers)
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
