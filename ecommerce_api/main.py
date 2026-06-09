from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ecommerce_api.api.routers import users
from ecommerce_api.core.exceptions import AppError


def create_app() -> FastAPI:
    app = FastAPI()

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'error': exc.message,
                'detail': exc.detail,
            },
        )

    return app


app = create_app()

app.title = 'ecommerce api'
app.version = '0.1'
app.description = 'trying to build an ecommerce api from scratch'

app.include_router(users.router)


@app.get('/', status_code=200)
def root():
    return {'message': 'Welcome to the E-commerce API!'}
