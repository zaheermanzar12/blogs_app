from fastapi import APIRouter

from blogs.api.endpoints import blogs, auth

api_router = APIRouter()
api_router.include_router(blogs.router, tags=["blogs"])
api_router.include_router(auth.router, tags=["auth"])
