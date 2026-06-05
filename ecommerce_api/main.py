from fastapi import FastAPI

from ecommerce_api.api.routers import users

app = FastAPI()
app.title = 'E-commerce API'
app.version = '0.1.0'

app.include_router(users.router)


@app.get('/')
async def root():
    return {'message': 'Welcome to the E-commerce API!'}
