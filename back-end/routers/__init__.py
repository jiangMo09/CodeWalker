from fastapi import APIRouter

from .user.login import router as login_router
from .user.register import router as register_router

from .leetcode.description import router as description_router
from .leetcode.code import router as code_router
from .leetcode.data_input import router as data_input_router

from .vercel.pure_js import router as pure_js_router

api_router = APIRouter()
api_router.include_router(description_router, tags=["leetcode"])
api_router.include_router(code_router, tags=["leetcode"])
api_router.include_router(data_input_router, tags=["leetcode"])
api_router.include_router(pure_js_router, tags=["vercel"])
api_router.include_router(login_router, tags=["login"])
api_router.include_router(register_router, tags=["register"])

__all__ = ["api_router"]
