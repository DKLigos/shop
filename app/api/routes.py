from fastapi import APIRouter
from app.api import article
from app.api import auth

api_router = APIRouter()
api_router.include_router(article.router)
api_router.include_router(auth.router)
