from fastapi import APIRouter
# from .home import router as home_router
# from .user import router as user_router
# from .booking import router as booking_router
# from .orders import router as orders_router

api_router = APIRouter()
# api_router.include_router(home_router, prefix="/api", tags=["home"])
# api_router.include_router(user_router, prefix="/api", tags=["user"])
# api_router.include_router(booking_router, prefix="/api", tags=["booking"])
# api_router.include_router(orders_router, prefix="/api", tags=["orders"])

__all__ = ["api_router"]
