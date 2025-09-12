from fastapi import FastAPI
from app.api import api_router
from app.middleware import add_middlewares

app = FastAPI(
    title="{{name}}",
    version="0.0.1",
    docs_url="/api",
)
add_middlewares(app)

app.include_router(api_router, prefix='/api')

@app.get('/')
def root():
    return {'message': 'Enhanced FastAPI App'}
