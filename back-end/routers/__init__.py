from fastapi import APIRouter


from .leetcode.description import router as description_router
from .leetcode.code import router as code_router

api_router = APIRouter()
api_router.include_router(description_router, prefix="/api", tags=["leetcode"])
api_router.include_router(code_router, prefix="/api", tags=["leetcode"])

__all__ = ["api_router"]
