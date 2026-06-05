from fastapi import FastAPI

app = FastAPI()
app.title = 'E-commerce API'
app.version = '0.1.0'


@app.get('/')
async def root():
    return {'message': 'Welcome to the E-commerce API!'}
