
from fastapi import APIRouter

from .endpoints import (
    algorithms
)

api_router = APIRouter()

# api_router.include_router(setting.router, prefix="/setting", tags=["setting"])
api_router.include_router(algorithms.router, prefix="/algorithms", tags=["algorithms"])
