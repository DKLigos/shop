from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import api_router


async def startup_tasks():
    app.router.include_router(api_router, prefix='/api')


app = FastAPI(
    title='API СУВД. Service-to-service communication',
    version="1.0.0",
    docs_url=f"/openapi",
    redoc_url=f"/docs",
    openapi_url=f"/openapi.json",
    on_startup=[startup_tasks]
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)