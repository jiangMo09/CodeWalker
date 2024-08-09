from fastapi import APIRouter


from .leetcode.description import router as description_router

api_router = APIRouter()
api_router.include_router(description_router, prefix="/api", tags=["leetcode"])

__all__ = ["api_router"]
